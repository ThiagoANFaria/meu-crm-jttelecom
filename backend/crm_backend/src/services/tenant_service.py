from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
import secrets
import string
import re
from decimal import Decimal

from src.models.tenant import (
    Tenant, TenantSubscription, TenantUsageLog, TenantInvitation,
    SubscriptionPlan, TenantStatus, BillingCycle, db
)
from src.models.user import User
import logging

logger = logging.getLogger(__name__)

class TenantService:
    """Serviço para gestão de tenants"""
    
    def create_tenant(self, data: Dict[str, Any], created_by: str = None) -> Dict[str, Any]:
        """
        Cria um novo tenant
        
        Args:
            data: Dados do tenant
            created_by: ID do usuário que está criando (super admin)
            
        Returns:
            Resultado da operação
        """
        try:
            # Validações
            validation_result = self._validate_tenant_data(data)
            if not validation_result['valid']:
                return {'success': False, 'errors': validation_result['errors']}
            
            # Gerar slug único
            slug = self._generate_unique_slug(data['name'])
            
            # Criar tenant
            tenant = Tenant(
                name=data['name'],
                slug=slug,
                display_name=data.get('display_name', data['name']),
                description=data.get('description'),
                cnpj=data.get('cnpj'),
                company_email=data.get('company_email'),
                company_phone=data.get('company_phone'),
                website=data.get('website'),
                address=data.get('address'),
                city=data.get('city'),
                state=data.get('state'),
                zip_code=data.get('zip_code'),
                country=data.get('country', 'Brasil'),
                subscription_plan=SubscriptionPlan(data.get('subscription_plan', 'trial')),
                billing_cycle=BillingCycle(data.get('billing_cycle', 'monthly')),
                status=TenantStatus.TRIAL,
                trial_start_date=date.today(),
                trial_end_date=date.today() + timedelta(days=14),  # 14 dias de trial
                created_by=created_by
            )
            
            # Configurar limites baseado no plano
            self._set_plan_limits(tenant, tenant.subscription_plan)
            
            # Gerar API key
            tenant.api_key = self._generate_api_key()
            
            # Configurações padrão
            tenant.features_enabled = self._get_default_features(tenant.subscription_plan)
            
            db.session.add(tenant)
            db.session.flush()  # Para obter o ID
            
            # Criar primeira assinatura (trial)
            subscription = TenantSubscription(
                tenant_id=tenant.id,
                plan=tenant.subscription_plan,
                billing_cycle=tenant.billing_cycle,
                monthly_value=Decimal('0'),  # Trial gratuito
                start_date=tenant.trial_start_date,
                end_date=tenant.trial_end_date,
                created_by=created_by
            )
            
            db.session.add(subscription)
            
            # Criar usuário admin do tenant se fornecido
            if data.get('admin_user'):
                admin_data = data['admin_user']
                admin_user = self._create_tenant_admin(tenant.id, admin_data, created_by)
                if not admin_user:
                    db.session.rollback()
                    return {'success': False, 'error': 'Erro ao criar usuário admin'}
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tenant criado com sucesso',
                'tenant': tenant.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar tenant: {e}")
            return {'success': False, 'error': f'Erro ao criar tenant: {str(e)}'}
    
    def update_tenant(self, tenant_id: str, data: Dict[str, Any], updated_by: str = None) -> Dict[str, Any]:
        """Atualiza dados do tenant"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'success': False, 'error': 'Tenant não encontrado'}
            
            # Campos que podem ser atualizados
            updatable_fields = [
                'name', 'display_name', 'description', 'cnpj', 'company_email',
                'company_phone', 'website', 'address', 'city', 'state', 'zip_code',
                'country', 'billing_email', 'billing_contact_name', 'billing_phone',
                'custom_domain', 'logo_url', 'primary_color', 'secondary_color',
                'timezone', 'language', 'currency', 'require_2fa'
            ]
            
            for field in updatable_fields:
                if field in data:
                    setattr(tenant, field, data[field])
            
            # Atualizar configurações se fornecidas
            if 'features_enabled' in data:
                tenant.features_enabled = data['features_enabled']
            
            if 'password_policy' in data:
                tenant.password_policy = data['password_policy']
            
            tenant.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tenant atualizado com sucesso',
                'tenant': tenant.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar tenant: {e}")
            return {'success': False, 'error': f'Erro ao atualizar tenant: {str(e)}'}
    
    def change_subscription_plan(self, tenant_id: str, new_plan: str, billing_cycle: str = None, changed_by: str = None) -> Dict[str, Any]:
        """Altera o plano de assinatura do tenant"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'success': False, 'error': 'Tenant não encontrado'}
            
            old_plan = tenant.subscription_plan
            new_plan_enum = SubscriptionPlan(new_plan)
            
            # Finalizar assinatura atual
            current_subscription = TenantSubscription.query.filter_by(
                tenant_id=tenant_id,
                is_active=True
            ).first()
            
            if current_subscription:
                current_subscription.is_active = False
                current_subscription.end_date = date.today()
            
            # Atualizar tenant
            tenant.subscription_plan = new_plan_enum
            if billing_cycle:
                tenant.billing_cycle = BillingCycle(billing_cycle)
            
            # Configurar novos limites
            self._set_plan_limits(tenant, new_plan_enum)
            
            # Atualizar recursos habilitados
            tenant.features_enabled = self._get_default_features(new_plan_enum)
            
            # Se não for trial, definir datas de assinatura
            if new_plan_enum != SubscriptionPlan.TRIAL:
                tenant.status = TenantStatus.ACTIVE
                tenant.subscription_start_date = date.today()
                tenant.subscription_end_date = self._calculate_subscription_end_date(
                    date.today(), tenant.billing_cycle
                )
            
            # Criar nova assinatura
            monthly_value = self._get_plan_price(new_plan_enum, tenant.billing_cycle)
            
            new_subscription = TenantSubscription(
                tenant_id=tenant_id,
                plan=new_plan_enum,
                billing_cycle=tenant.billing_cycle,
                monthly_value=monthly_value,
                start_date=date.today(),
                created_by=changed_by
            )
            
            db.session.add(new_subscription)
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Plano alterado de {old_plan.value} para {new_plan}',
                'tenant': tenant.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao alterar plano: {e}")
            return {'success': False, 'error': f'Erro ao alterar plano: {str(e)}'}
    
    def suspend_tenant(self, tenant_id: str, reason: str = None, suspended_by: str = None) -> Dict[str, Any]:
        """Suspende um tenant"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'success': False, 'error': 'Tenant não encontrado'}
            
            tenant.status = TenantStatus.SUSPENDED
            tenant.updated_at = datetime.utcnow()
            
            # Log da suspensão
            logger.warning(f"Tenant {tenant.slug} suspenso. Motivo: {reason}")
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tenant suspenso com sucesso'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao suspender tenant: {e}")
            return {'success': False, 'error': f'Erro ao suspender tenant: {str(e)}'}
    
    def reactivate_tenant(self, tenant_id: str, reactivated_by: str = None) -> Dict[str, Any]:
        """Reativa um tenant suspenso"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'success': False, 'error': 'Tenant não encontrado'}
            
            if tenant.status != TenantStatus.SUSPENDED:
                return {'success': False, 'error': 'Tenant não está suspenso'}
            
            tenant.status = TenantStatus.ACTIVE
            tenant.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tenant reativado com sucesso'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao reativar tenant: {e}")
            return {'success': False, 'error': f'Erro ao reativar tenant: {str(e)}'}
    
    def cancel_tenant(self, tenant_id: str, reason: str = None, cancelled_by: str = None) -> Dict[str, Any]:
        """Cancela um tenant"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'success': False, 'error': 'Tenant não encontrado'}
            
            tenant.status = TenantStatus.CANCELLED
            tenant.updated_at = datetime.utcnow()
            
            # Finalizar assinatura atual
            current_subscription = TenantSubscription.query.filter_by(
                tenant_id=tenant_id,
                is_active=True
            ).first()
            
            if current_subscription:
                current_subscription.is_active = False
                current_subscription.cancelled_date = date.today()
                current_subscription.cancellation_reason = reason
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tenant cancelado com sucesso'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao cancelar tenant: {e}")
            return {'success': False, 'error': f'Erro ao cancelar tenant: {str(e)}'}
    
    def update_usage_metrics(self, tenant_id: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza métricas de uso do tenant"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'success': False, 'error': 'Tenant não encontrado'}
            
            # Atualizar métricas atuais
            if 'users_count' in metrics:
                tenant.current_users = metrics['users_count']
            
            if 'leads_count' in metrics:
                tenant.current_leads = metrics['leads_count']
            
            if 'storage_gb' in metrics:
                tenant.current_storage_gb = Decimal(str(metrics['storage_gb']))
            
            if 'email_sends_month' in metrics:
                tenant.current_email_sends_month = metrics['email_sends_month']
            
            if 'api_calls_month' in metrics:
                tenant.current_api_calls_month = metrics['api_calls_month']
            
            tenant.updated_at = datetime.utcnow()
            
            # Criar log de uso
            usage_log = TenantUsageLog(
                tenant_id=tenant_id,
                log_date=date.today(),
                users_count=tenant.current_users,
                leads_count=tenant.current_leads,
                storage_gb=tenant.current_storage_gb,
                email_sends=tenant.current_email_sends_month,
                api_calls=tenant.current_api_calls_month,
                logins_count=metrics.get('logins_count', 0),
                tasks_created=metrics.get('tasks_created', 0),
                calls_made=metrics.get('calls_made', 0)
            )
            
            db.session.add(usage_log)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Métricas atualizadas com sucesso',
                'usage_limits': tenant.check_usage_limits()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar métricas: {e}")
            return {'success': False, 'error': f'Erro ao atualizar métricas: {str(e)}'}
    
    def create_invitation(self, tenant_id: str, email: str, role: str, invited_by: str) -> Dict[str, Any]:
        """Cria convite para usuário se juntar ao tenant"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'success': False, 'error': 'Tenant não encontrado'}
            
            # Verificar se já existe convite pendente
            existing_invitation = TenantInvitation.query.filter_by(
                tenant_id=tenant_id,
                email=email,
                is_accepted=False
            ).first()
            
            if existing_invitation and not existing_invitation.is_expired:
                return {'success': False, 'error': 'Já existe convite pendente para este email'}
            
            # Verificar se usuário já existe no tenant
            existing_user = User.query.filter_by(
                email=email,
                tenant_id=tenant_id
            ).first()
            
            if existing_user:
                return {'success': False, 'error': 'Usuário já faz parte deste tenant'}
            
            # Gerar token único
            token = self._generate_invitation_token()
            
            # Criar convite
            invitation = TenantInvitation(
                tenant_id=tenant_id,
                email=email,
                role=role,
                token=token,
                expires_at=datetime.utcnow() + timedelta(days=7),  # Expira em 7 dias
                invited_by=invited_by
            )
            
            db.session.add(invitation)
            db.session.commit()
            
            # TODO: Enviar email de convite
            
            return {
                'success': True,
                'message': 'Convite criado com sucesso',
                'invitation': invitation.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar convite: {e}")
            return {'success': False, 'error': f'Erro ao criar convite: {str(e)}'}
    
    def accept_invitation(self, token: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aceita convite e cria usuário no tenant"""
        try:
            invitation = TenantInvitation.query.filter_by(token=token).first()
            
            if not invitation:
                return {'success': False, 'error': 'Convite não encontrado'}
            
            if invitation.is_accepted:
                return {'success': False, 'error': 'Convite já foi aceito'}
            
            if invitation.is_expired:
                return {'success': False, 'error': 'Convite expirado'}
            
            # Verificar se tenant está ativo
            if not invitation.tenant.is_active:
                return {'success': False, 'error': 'Tenant não está ativo'}
            
            # Criar usuário
            user = User(
                email=invitation.email,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=invitation.role,
                tenant_id=invitation.tenant_id,
                is_active=True
            )
            
            # Definir senha
            user.set_password(user_data['password'])
            
            # Marcar convite como aceito
            invitation.is_accepted = True
            invitation.accepted_at = datetime.utcnow()
            
            db.session.add(user)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Convite aceito e usuário criado com sucesso',
                'user': user.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao aceitar convite: {e}")
            return {'success': False, 'error': f'Erro ao aceitar convite: {str(e)}'}
    
    def get_tenant_analytics(self, tenant_id: str, days: int = 30) -> Dict[str, Any]:
        """Obtém analytics do tenant"""
        try:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'error': 'Tenant não encontrado'}
            
            # Período de análise
            end_date = date.today()
            start_date = end_date - timedelta(days=days)
            
            # Buscar logs de uso
            usage_logs = TenantUsageLog.query.filter(
                TenantUsageLog.tenant_id == tenant_id,
                TenantUsageLog.log_date >= start_date,
                TenantUsageLog.log_date <= end_date
            ).order_by(TenantUsageLog.log_date.asc()).all()
            
            # Calcular métricas
            analytics = {
                'tenant': tenant.to_dict(),
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                },
                'usage_evolution': [log.to_dict() for log in usage_logs],
                'current_usage': tenant.check_usage_limits(),
                'subscription_info': {
                    'plan': tenant.subscription_plan.value,
                    'status': tenant.status.value,
                    'trial_days_remaining': tenant.trial_days_remaining,
                    'subscription_days_remaining': tenant.subscription_days_remaining
                }
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Erro ao obter analytics do tenant: {e}")
            return {'error': f'Erro ao obter analytics: {str(e)}'}
    
    def list_tenants(self, filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Lista tenants com filtros"""
        try:
            query = Tenant.query
            
            # Aplicar filtros
            if filters:
                if 'status' in filters:
                    query = query.filter(Tenant.status == TenantStatus(filters['status']))
                
                if 'plan' in filters:
                    query = query.filter(Tenant.subscription_plan == SubscriptionPlan(filters['plan']))
                
                if 'search' in filters:
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        db.or_(
                            Tenant.name.ilike(search_term),
                            Tenant.slug.ilike(search_term),
                            Tenant.company_email.ilike(search_term)
                        )
                    )
            
            # Paginação
            total = query.count()
            tenants = query.offset((page - 1) * per_page).limit(per_page).all()
            
            return {
                'tenants': [tenant.to_dict() for tenant in tenants],
                'total': total,
                'pages': (total + per_page - 1) // per_page,
                'current_page': page,
                'per_page': per_page
            }
            
        except Exception as e:
            logger.error(f"Erro ao listar tenants: {e}")
            return {'error': f'Erro ao listar tenants: {str(e)}'}
    
    # Métodos privados
    
    def _validate_tenant_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados do tenant"""
        errors = []
        
        # Campos obrigatórios
        required_fields = ['name']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f'Campo {field} é obrigatório')
        
        # Validar email se fornecido
        if 'company_email' in data and data['company_email']:
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['company_email']):
                errors.append('Email da empresa inválido')
        
        # Validar CNPJ se fornecido
        if 'cnpj' in data and data['cnpj']:
            cnpj = re.sub(r'[^0-9]', '', data['cnpj'])
            if len(cnpj) != 14:
                errors.append('CNPJ deve ter 14 dígitos')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _generate_unique_slug(self, name: str) -> str:
        """Gera slug único baseado no nome"""
        # Converter para slug
        slug = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
        slug = slug[:20]  # Limitar tamanho
        
        # Verificar se já existe
        counter = 1
        original_slug = slug
        
        while Tenant.query.filter_by(slug=slug).first():
            slug = f"{original_slug}{counter}"
            counter += 1
        
        return slug
    
    def _generate_api_key(self) -> str:
        """Gera API key única"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
    
    def _generate_invitation_token(self) -> str:
        """Gera token de convite único"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    def _set_plan_limits(self, tenant: Tenant, plan: SubscriptionPlan):
        """Define limites baseado no plano"""
        limits = {
            SubscriptionPlan.TRIAL: {
                'max_users': 2,
                'max_leads': 100,
                'max_storage_gb': 1,
                'max_email_sends_month': 100,
                'max_api_calls_month': 1000
            },
            SubscriptionPlan.BASIC: {
                'max_users': 5,
                'max_leads': 1000,
                'max_storage_gb': 5,
                'max_email_sends_month': 1000,
                'max_api_calls_month': 10000
            },
            SubscriptionPlan.PRO: {
                'max_users': 15,
                'max_leads': 5000,
                'max_storage_gb': 20,
                'max_email_sends_month': 5000,
                'max_api_calls_month': 50000
            },
            SubscriptionPlan.ENTERPRISE: {
                'max_users': 50,
                'max_leads': 20000,
                'max_storage_gb': 100,
                'max_email_sends_month': 20000,
                'max_api_calls_month': 200000
            }
        }
        
        plan_limits = limits.get(plan, limits[SubscriptionPlan.TRIAL])
        
        for key, value in plan_limits.items():
            setattr(tenant, key, value)
    
    def _get_default_features(self, plan: SubscriptionPlan) -> Dict[str, bool]:
        """Retorna recursos padrão por plano"""
        features = {
            SubscriptionPlan.TRIAL: {
                'telephony': False,
                'automation': False,
                'advanced_reports': False,
                'api_access': False,
                'custom_branding': False,
                'integrations': False
            },
            SubscriptionPlan.BASIC: {
                'telephony': True,
                'automation': False,
                'advanced_reports': False,
                'api_access': True,
                'custom_branding': False,
                'integrations': False
            },
            SubscriptionPlan.PRO: {
                'telephony': True,
                'automation': True,
                'advanced_reports': True,
                'api_access': True,
                'custom_branding': True,
                'integrations': True
            },
            SubscriptionPlan.ENTERPRISE: {
                'telephony': True,
                'automation': True,
                'advanced_reports': True,
                'api_access': True,
                'custom_branding': True,
                'integrations': True
            }
        }
        
        return features.get(plan, features[SubscriptionPlan.TRIAL])
    
    def _get_plan_price(self, plan: SubscriptionPlan, billing_cycle: BillingCycle) -> Decimal:
        """Retorna preço do plano"""
        monthly_prices = {
            SubscriptionPlan.TRIAL: Decimal('0'),
            SubscriptionPlan.BASIC: Decimal('97'),
            SubscriptionPlan.PRO: Decimal('197'),
            SubscriptionPlan.ENTERPRISE: Decimal('497')
        }
        
        monthly_price = monthly_prices.get(plan, Decimal('0'))
        
        # Aplicar desconto para ciclos maiores
        if billing_cycle == BillingCycle.QUARTERLY:
            return monthly_price * Decimal('0.95')  # 5% desconto
        elif billing_cycle == BillingCycle.YEARLY:
            return monthly_price * Decimal('0.85')  # 15% desconto
        
        return monthly_price
    
    def _calculate_subscription_end_date(self, start_date: date, billing_cycle: BillingCycle) -> date:
        """Calcula data de fim da assinatura"""
        if billing_cycle == BillingCycle.MONTHLY:
            return start_date + timedelta(days=30)
        elif billing_cycle == BillingCycle.QUARTERLY:
            return start_date + timedelta(days=90)
        elif billing_cycle == BillingCycle.YEARLY:
            return start_date + timedelta(days=365)
        
        return start_date + timedelta(days=30)
    
    def _create_tenant_admin(self, tenant_id: str, admin_data: Dict[str, Any], created_by: str = None) -> Optional[User]:
        """Cria usuário admin do tenant"""
        try:
            admin_user = User(
                email=admin_data['email'],
                first_name=admin_data['first_name'],
                last_name=admin_data['last_name'],
                role='admin',
                tenant_id=tenant_id,
                is_active=True,
                created_by=created_by
            )
            
            admin_user.set_password(admin_data['password'])
            
            db.session.add(admin_user)
            return admin_user
            
        except Exception as e:
            logger.error(f"Erro ao criar admin do tenant: {e}")
            return None

