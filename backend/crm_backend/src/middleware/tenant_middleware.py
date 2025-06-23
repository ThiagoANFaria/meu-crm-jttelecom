from flask import request, g, jsonify, current_app
from functools import wraps
import re
from typing import Optional
from src.models.tenant import Tenant, TenantStatus
from src.models.user import User
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware:
    """Middleware para detecção e isolamento de tenant"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa o middleware com a aplicação Flask"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Executa antes de cada request para detectar o tenant"""
        try:
            # Detectar tenant
            tenant = self.detect_tenant()
            
            # Armazenar no contexto da request
            g.current_tenant = tenant
            g.tenant_id = tenant.id if tenant else None
            
            # Verificar se o tenant está ativo (exceto para rotas de sistema)
            if tenant and not self.is_system_route():
                if not self.is_tenant_accessible(tenant):
                    return jsonify({
                        'error': 'Tenant não está acessível',
                        'status': tenant.status.value if tenant.status else 'unknown'
                    }), 403
            
            # Log da request
            if tenant:
                logger.info(f"Request para tenant {tenant.slug} ({tenant.name})")
            
        except Exception as e:
            logger.error(f"Erro no middleware de tenant: {e}")
            # Em caso de erro, continuar sem tenant (para rotas de sistema)
            g.current_tenant = None
            g.tenant_id = None
    
    def after_request(self, response):
        """Executa após cada request"""
        # Adicionar headers de tenant se disponível
        if hasattr(g, 'current_tenant') and g.current_tenant:
            response.headers['X-Tenant-ID'] = g.current_tenant.id
            response.headers['X-Tenant-Slug'] = g.current_tenant.slug
        
        return response
    
    def detect_tenant(self) -> Optional[Tenant]:
        """Detecta o tenant atual baseado na request"""
        tenant = None
        
        # 1. Tentar por subdomínio
        tenant = self.detect_by_subdomain()
        if tenant:
            return tenant
        
        # 2. Tentar por header personalizado
        tenant = self.detect_by_header()
        if tenant:
            return tenant
        
        # 3. Tentar por domínio customizado
        tenant = self.detect_by_custom_domain()
        if tenant:
            return tenant
        
        # 4. Para rotas de API, tentar por API key
        tenant = self.detect_by_api_key()
        if tenant:
            return tenant
        
        return None
    
    def detect_by_subdomain(self) -> Optional[Tenant]:
        """Detecta tenant por subdomínio (empresa1.jtcrm.com.br)"""
        try:
            host = request.headers.get('Host', '')
            
            # Regex para extrair subdomínio
            # Suporta: empresa1.jtcrm.com.br, empresa1.localhost:5000
            pattern = r'^([a-zA-Z0-9-]+)\.(jtcrm\.com\.br|localhost)'
            match = re.match(pattern, host)
            
            if match:
                subdomain = match.group(1)
                
                # Ignorar subdomínios de sistema
                if subdomain in ['www', 'api', 'admin', 'app', 'dashboard']:
                    return None
                
                # Buscar tenant pelo slug
                tenant = Tenant.query.filter_by(slug=subdomain).first()
                return tenant
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao detectar tenant por subdomínio: {e}")
            return None
    
    def detect_by_header(self) -> Optional[Tenant]:
        """Detecta tenant por header X-Tenant-ID ou X-Tenant-Slug"""
        try:
            # Por ID
            tenant_id = request.headers.get('X-Tenant-ID')
            if tenant_id:
                tenant = Tenant.query.get(tenant_id)
                if tenant:
                    return tenant
            
            # Por slug
            tenant_slug = request.headers.get('X-Tenant-Slug')
            if tenant_slug:
                tenant = Tenant.query.filter_by(slug=tenant_slug).first()
                if tenant:
                    return tenant
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao detectar tenant por header: {e}")
            return None
    
    def detect_by_custom_domain(self) -> Optional[Tenant]:
        """Detecta tenant por domínio customizado"""
        try:
            host = request.headers.get('Host', '').split(':')[0]  # Remove porta
            
            # Buscar tenant com domínio customizado
            tenant = Tenant.query.filter_by(custom_domain=host).first()
            return tenant
            
        except Exception as e:
            logger.error(f"Erro ao detectar tenant por domínio customizado: {e}")
            return None
    
    def detect_by_api_key(self) -> Optional[Tenant]:
        """Detecta tenant por API key (para APIs externas)"""
        try:
            # Verificar se é uma rota de API
            if not request.path.startswith('/api/'):
                return None
            
            # Buscar API key no header Authorization
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                api_key = auth_header[7:]  # Remove "Bearer "
                
                # Buscar tenant pela API key
                tenant = Tenant.query.filter_by(api_key=api_key).first()
                return tenant
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao detectar tenant por API key: {e}")
            return None
    
    def is_system_route(self) -> bool:
        """Verifica se é uma rota de sistema que não precisa de tenant"""
        system_routes = [
            '/health',
            '/status',
            '/metrics',
            '/admin',
            '/super-admin',
            '/auth/register-tenant',
            '/auth/login-super-admin',
            '/static',
            '/favicon.ico'
        ]
        
        path = request.path
        return any(path.startswith(route) for route in system_routes)
    
    def is_tenant_accessible(self, tenant: Tenant) -> bool:
        """Verifica se o tenant está acessível"""
        if not tenant:
            return False
        
        # Verificar status
        if tenant.status == TenantStatus.CANCELLED:
            return False
        
        if tenant.status == TenantStatus.SUSPENDED:
            # Permitir apenas para super admins
            return self.is_super_admin_request()
        
        # Verificar se trial expirou
        if tenant.is_trial and tenant.trial_days_remaining <= 0:
            return False
        
        # Verificar se assinatura expirou
        if not tenant.is_trial and tenant.subscription_days_remaining <= 0:
            return False
        
        return True
    
    def is_super_admin_request(self) -> bool:
        """Verifica se a request é de um super admin"""
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            
            # Verificar se há JWT válido
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            
            if user_id:
                user = User.query.get(user_id)
                return user and user.role == 'super_admin'
            
            return False
            
        except:
            return False

# Decorador para garantir isolamento de tenant
def require_tenant(f):
    """Decorador que garante que há um tenant válido na request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_tenant') or not g.current_tenant:
            return jsonify({'error': 'Tenant não identificado'}), 400
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_active_tenant(f):
    """Decorador que garante que o tenant está ativo"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_tenant') or not g.current_tenant:
            return jsonify({'error': 'Tenant não identificado'}), 400
        
        if not g.current_tenant.is_active:
            return jsonify({
                'error': 'Tenant não está ativo',
                'status': g.current_tenant.status.value
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_tenant_feature(feature_name: str):
    """Decorador que verifica se o tenant tem um recurso habilitado"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'current_tenant') or not g.current_tenant:
                return jsonify({'error': 'Tenant não identificado'}), 400
            
            if not g.current_tenant.get_feature_enabled(feature_name):
                return jsonify({
                    'error': f'Recurso {feature_name} não está habilitado para este plano'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def check_tenant_limits(resource_type: str, increment: int = 1):
    """Decorador que verifica limites de uso do tenant"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'current_tenant') or not g.current_tenant:
                return jsonify({'error': 'Tenant não identificado'}), 400
            
            tenant = g.current_tenant
            
            # Verificar limite específico
            if resource_type == 'users' and tenant.current_users + increment > tenant.max_users:
                return jsonify({
                    'error': 'Limite de usuários excedido',
                    'current': tenant.current_users,
                    'limit': tenant.max_users
                }), 403
            
            elif resource_type == 'leads' and tenant.current_leads + increment > tenant.max_leads:
                return jsonify({
                    'error': 'Limite de leads excedido',
                    'current': tenant.current_leads,
                    'limit': tenant.max_leads
                }), 403
            
            elif resource_type == 'email_sends' and tenant.current_email_sends_month + increment > tenant.max_email_sends_month:
                return jsonify({
                    'error': 'Limite de envios de email excedido',
                    'current': tenant.current_email_sends_month,
                    'limit': tenant.max_email_sends_month
                }), 403
            
            elif resource_type == 'api_calls' and tenant.current_api_calls_month + increment > tenant.max_api_calls_month:
                return jsonify({
                    'error': 'Limite de chamadas de API excedido',
                    'current': tenant.current_api_calls_month,
                    'limit': tenant.max_api_calls_month
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

# Função para obter tenant atual
def get_current_tenant() -> Optional[Tenant]:
    """Obtém o tenant atual do contexto da request"""
    return getattr(g, 'current_tenant', None)

def get_current_tenant_id() -> Optional[str]:
    """Obtém o ID do tenant atual"""
    return getattr(g, 'tenant_id', None)

# Função para filtrar queries por tenant
def filter_by_tenant(query, model_class, tenant_field='tenant_id'):
    """Adiciona filtro de tenant a uma query"""
    tenant_id = get_current_tenant_id()
    if tenant_id:
        return query.filter(getattr(model_class, tenant_field) == tenant_id)
    return query

# Classe base para modelos com tenant
class TenantMixin:
    """Mixin para adicionar tenant_id aos modelos"""
    
    @classmethod
    def query_for_tenant(cls, tenant_id=None):
        """Query filtrada por tenant"""
        if tenant_id is None:
            tenant_id = get_current_tenant_id()
        
        if tenant_id:
            return cls.query.filter(cls.tenant_id == tenant_id)
        return cls.query
    
    def set_tenant(self, tenant_id=None):
        """Define o tenant do objeto"""
        if tenant_id is None:
            tenant_id = get_current_tenant_id()
        
        if tenant_id:
            self.tenant_id = tenant_id

