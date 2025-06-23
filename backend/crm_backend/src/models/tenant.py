from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from src.models.user import db
from datetime import datetime, date
import uuid
import enum

class SubscriptionPlan(enum.Enum):
    """Planos de assinatura"""
    TRIAL = "trial"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

class TenantStatus(enum.Enum):
    """Status do tenant"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    TRIAL = "trial"
    PENDING = "pending"

class BillingCycle(enum.Enum):
    """Ciclo de cobrança"""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class Tenant(db.Model):
    """Modelo de Tenant/Organização para SaaS Multi-Tenant"""
    __tablename__ = 'tenants'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Informações básicas da empresa
    name = db.Column(db.String(200), nullable=False)  # Nome da empresa
    slug = db.Column(db.String(100), unique=True, nullable=False)  # Subdomínio (empresa1.jtcrm.com.br)
    display_name = db.Column(db.String(200))  # Nome de exibição
    description = db.Column(db.Text)
    
    # Dados da empresa
    cnpj = db.Column(db.String(18))
    company_email = db.Column(db.String(200))
    company_phone = db.Column(db.String(20))
    website = db.Column(db.String(500))
    
    # Endereço
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    country = db.Column(db.String(50), default='Brasil')
    
    # Status e assinatura
    status = db.Column(db.Enum(TenantStatus), default=TenantStatus.TRIAL)
    subscription_plan = db.Column(db.Enum(SubscriptionPlan), default=SubscriptionPlan.TRIAL)
    billing_cycle = db.Column(db.Enum(BillingCycle), default=BillingCycle.MONTHLY)
    
    # Datas importantes
    trial_start_date = db.Column(db.Date)
    trial_end_date = db.Column(db.Date)
    subscription_start_date = db.Column(db.Date)
    subscription_end_date = db.Column(db.Date)
    last_payment_date = db.Column(db.Date)
    next_payment_date = db.Column(db.Date)
    
    # Valores
    monthly_value = db.Column(db.Numeric(10, 2), default=0)
    setup_fee = db.Column(db.Numeric(10, 2), default=0)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)
    
    # Limites do plano
    max_users = db.Column(db.Integer, default=5)
    max_leads = db.Column(db.Integer, default=1000)
    max_storage_gb = db.Column(db.Integer, default=1)
    max_email_sends_month = db.Column(db.Integer, default=1000)
    max_api_calls_month = db.Column(db.Integer, default=10000)
    
    # Uso atual
    current_users = db.Column(db.Integer, default=0)
    current_leads = db.Column(db.Integer, default=0)
    current_storage_gb = db.Column(db.Numeric(8, 3), default=0)
    current_email_sends_month = db.Column(db.Integer, default=0)
    current_api_calls_month = db.Column(db.Integer, default=0)
    
    # Recursos habilitados
    features_enabled = db.Column(db.JSON, default=dict)  # {"telephony": true, "automation": false, etc}
    
    # Customização
    custom_domain = db.Column(db.String(200))  # Domínio personalizado
    logo_url = db.Column(db.String(500))
    primary_color = db.Column(db.String(7), default='#1e40af')  # Cor primária (hex)
    secondary_color = db.Column(db.String(7), default='#64748b')  # Cor secundária
    custom_css = db.Column(db.Text)  # CSS personalizado
    
    # Configurações
    timezone = db.Column(db.String(50), default='America/Sao_Paulo')
    language = db.Column(db.String(5), default='pt-BR')
    currency = db.Column(db.String(3), default='BRL')
    date_format = db.Column(db.String(20), default='DD/MM/YYYY')
    
    # Configurações de segurança
    require_2fa = db.Column(db.Boolean, default=False)
    password_policy = db.Column(db.JSON, default=dict)
    session_timeout_minutes = db.Column(db.Integer, default=480)  # 8 horas
    allowed_ip_ranges = db.Column(db.JSON, default=list)
    
    # Configurações de integração
    api_key = db.Column(db.String(64))  # API key do tenant
    webhook_url = db.Column(db.String(500))  # URL para webhooks
    webhook_secret = db.Column(db.String(64))  # Secret para validar webhooks
    
    # Dados de cobrança
    billing_email = db.Column(db.String(200))
    billing_contact_name = db.Column(db.String(200))
    billing_phone = db.Column(db.String(20))
    payment_method = db.Column(db.String(50))  # credit_card, boleto, pix, etc
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))  # Super admin que criou
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    users = db.relationship('User', backref='tenant', cascade='all, delete-orphan')
    subscriptions = db.relationship('TenantSubscription', backref='tenant', cascade='all, delete-orphan')
    usage_logs = db.relationship('TenantUsageLog', backref='tenant', cascade='all, delete-orphan')
    
    @property
    def is_trial(self):
        """Verifica se está em período de trial"""
        return self.status == TenantStatus.TRIAL
    
    @property
    def is_active(self):
        """Verifica se o tenant está ativo"""
        return self.status == TenantStatus.ACTIVE
    
    @property
    def is_suspended(self):
        """Verifica se o tenant está suspenso"""
        return self.status == TenantStatus.SUSPENDED
    
    @property
    def trial_days_remaining(self):
        """Dias restantes do trial"""
        if not self.trial_end_date:
            return 0
        
        today = date.today()
        if today > self.trial_end_date:
            return 0
        
        return (self.trial_end_date - today).days
    
    @property
    def subscription_days_remaining(self):
        """Dias restantes da assinatura"""
        if not self.subscription_end_date:
            return 0
        
        today = date.today()
        if today > self.subscription_end_date:
            return 0
        
        return (self.subscription_end_date - today).days
    
    @property
    def is_over_limits(self):
        """Verifica se está excedendo limites"""
        return (
            self.current_users > self.max_users or
            self.current_leads > self.max_leads or
            self.current_storage_gb > self.max_storage_gb or
            self.current_email_sends_month > self.max_email_sends_month or
            self.current_api_calls_month > self.max_api_calls_month
        )
    
    def get_feature_enabled(self, feature_name: str) -> bool:
        """Verifica se um recurso está habilitado"""
        return self.features_enabled.get(feature_name, False)
    
    def set_feature_enabled(self, feature_name: str, enabled: bool):
        """Habilita/desabilita um recurso"""
        if not self.features_enabled:
            self.features_enabled = {}
        
        self.features_enabled[feature_name] = enabled
        db.session.add(self)
    
    def check_usage_limits(self) -> Dict[str, Any]:
        """Verifica limites de uso"""
        return {
            'users': {
                'current': self.current_users,
                'limit': self.max_users,
                'percentage': round((self.current_users / self.max_users * 100) if self.max_users > 0 else 0, 2),
                'over_limit': self.current_users > self.max_users
            },
            'leads': {
                'current': self.current_leads,
                'limit': self.max_leads,
                'percentage': round((self.current_leads / self.max_leads * 100) if self.max_leads > 0 else 0, 2),
                'over_limit': self.current_leads > self.max_leads
            },
            'storage': {
                'current': float(self.current_storage_gb),
                'limit': self.max_storage_gb,
                'percentage': round((float(self.current_storage_gb) / self.max_storage_gb * 100) if self.max_storage_gb > 0 else 0, 2),
                'over_limit': self.current_storage_gb > self.max_storage_gb
            },
            'email_sends': {
                'current': self.current_email_sends_month,
                'limit': self.max_email_sends_month,
                'percentage': round((self.current_email_sends_month / self.max_email_sends_month * 100) if self.max_email_sends_month > 0 else 0, 2),
                'over_limit': self.current_email_sends_month > self.max_email_sends_month
            },
            'api_calls': {
                'current': self.current_api_calls_month,
                'limit': self.max_api_calls_month,
                'percentage': round((self.current_api_calls_month / self.max_api_calls_month * 100) if self.max_api_calls_month > 0 else 0, 2),
                'over_limit': self.current_api_calls_month > self.max_api_calls_month
            }
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'display_name': self.display_name,
            'description': self.description,
            'cnpj': self.cnpj,
            'company_email': self.company_email,
            'company_phone': self.company_phone,
            'website': self.website,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'status': self.status.value if self.status else None,
            'subscription_plan': self.subscription_plan.value if self.subscription_plan else None,
            'billing_cycle': self.billing_cycle.value if self.billing_cycle else None,
            'trial_start_date': self.trial_start_date.isoformat() if self.trial_start_date else None,
            'trial_end_date': self.trial_end_date.isoformat() if self.trial_end_date else None,
            'subscription_start_date': self.subscription_start_date.isoformat() if self.subscription_start_date else None,
            'subscription_end_date': self.subscription_end_date.isoformat() if self.subscription_end_date else None,
            'monthly_value': float(self.monthly_value) if self.monthly_value else 0,
            'max_users': self.max_users,
            'max_leads': self.max_leads,
            'max_storage_gb': self.max_storage_gb,
            'current_users': self.current_users,
            'current_leads': self.current_leads,
            'current_storage_gb': float(self.current_storage_gb) if self.current_storage_gb else 0,
            'features_enabled': self.features_enabled,
            'custom_domain': self.custom_domain,
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'timezone': self.timezone,
            'language': self.language,
            'currency': self.currency,
            'is_trial': self.is_trial,
            'is_active': self.is_active,
            'trial_days_remaining': self.trial_days_remaining,
            'subscription_days_remaining': self.subscription_days_remaining,
            'is_over_limits': self.is_over_limits,
            'usage_limits': self.check_usage_limits(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TenantSubscription(db.Model):
    """Histórico de assinaturas do tenant"""
    __tablename__ = 'tenant_subscriptions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    
    # Dados da assinatura
    plan = db.Column(db.Enum(SubscriptionPlan), nullable=False)
    billing_cycle = db.Column(db.Enum(BillingCycle), nullable=False)
    
    # Valores
    monthly_value = db.Column(db.Numeric(10, 2), nullable=False)
    setup_fee = db.Column(db.Numeric(10, 2), default=0)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)
    total_paid = db.Column(db.Numeric(10, 2), default=0)
    
    # Período
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    cancelled_date = db.Column(db.Date)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    cancellation_reason = db.Column(db.Text)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'plan': self.plan.value if self.plan else None,
            'billing_cycle': self.billing_cycle.value if self.billing_cycle else None,
            'monthly_value': float(self.monthly_value) if self.monthly_value else 0,
            'setup_fee': float(self.setup_fee) if self.setup_fee else 0,
            'discount_percent': float(self.discount_percent) if self.discount_percent else 0,
            'total_paid': float(self.total_paid) if self.total_paid else 0,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'cancelled_date': self.cancelled_date.isoformat() if self.cancelled_date else None,
            'is_active': self.is_active,
            'cancellation_reason': self.cancellation_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TenantUsageLog(db.Model):
    """Log de uso do tenant"""
    __tablename__ = 'tenant_usage_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    
    # Data do log
    log_date = db.Column(db.Date, nullable=False, default=date.today)
    
    # Métricas de uso
    users_count = db.Column(db.Integer, default=0)
    leads_count = db.Column(db.Integer, default=0)
    storage_gb = db.Column(db.Numeric(8, 3), default=0)
    email_sends = db.Column(db.Integer, default=0)
    api_calls = db.Column(db.Integer, default=0)
    
    # Atividades
    logins_count = db.Column(db.Integer, default=0)
    tasks_created = db.Column(db.Integer, default=0)
    calls_made = db.Column(db.Integer, default=0)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'log_date': self.log_date.isoformat() if self.log_date else None,
            'users_count': self.users_count,
            'leads_count': self.leads_count,
            'storage_gb': float(self.storage_gb) if self.storage_gb else 0,
            'email_sends': self.email_sends,
            'api_calls': self.api_calls,
            'logins_count': self.logins_count,
            'tasks_created': self.tasks_created,
            'calls_made': self.calls_made,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TenantInvitation(db.Model):
    """Convites para usuários se juntarem a um tenant"""
    __tablename__ = 'tenant_invitations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    
    # Dados do convite
    email = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, manager, user
    token = db.Column(db.String(64), unique=True, nullable=False)
    
    # Status
    is_accepted = db.Column(db.Boolean, default=False)
    accepted_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Metadados
    invited_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    tenant = db.relationship('Tenant', backref='invitations')
    inviter = db.relationship('User', backref='sent_invitations')
    
    @property
    def is_expired(self):
        """Verifica se o convite expirou"""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'email': self.email,
            'role': self.role,
            'is_accepted': self.is_accepted,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_expired': self.is_expired,
            'invited_by': self.invited_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'tenant': {
                'id': self.tenant.id,
                'name': self.tenant.name
            } if self.tenant else None
        }

