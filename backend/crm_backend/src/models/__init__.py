# src/models/__init__.py
"""
Módulo central de modelos do CRM
Importa e organiza todos os modelos do sistema
"""

# Importar o db do arquivo de usuário (base)
try:
    from .user import db, User, Role, Permission
    print("✅ Modelos de usuário importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar user: {e}")
    db = User = Role = Permission = None

# Importar modelos de leads e pipeline
try:
    from .lead import Lead, Tag, LeadFieldTemplate
    print("✅ Modelos de lead importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar lead: {e}")
    Lead = Tag = LeadFieldTemplate = None

try:
    from .pipeline import Pipeline, PipelineStage, Product, Opportunity
    print("✅ Modelos de pipeline importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar pipeline: {e}")
    Pipeline = PipelineStage = Product = Opportunity = None

# Importar modelos de tarefas e atividades  
try:
    from .task import Task, TaskComment, TaskTimeLog, TaskTemplate, ActivitySummary
    print("✅ Modelos de task importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar task: {e}")
    Task = TaskComment = TaskTimeLog = TaskTemplate = ActivitySummary = None

# Importar modelos de propostas e contratos
try:
    from .proposal import ProposalTemplate, Proposal, ProposalItem
    print("✅ Modelos de proposal importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar proposal: {e}")
    ProposalTemplate = Proposal = ProposalItem = None

try:
    from .contract import ContractTemplate, Contract, ContractAmendment
    print("✅ Modelos de contract importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar contract: {e}")
    ContractTemplate = Contract = ContractAmendment = None

# Importar modelos de chatbot e automação
try:
    from .chatbot import ChatFlow, ChatConversation, ChatMessage, ChatIntegration, ChatAIConfig
    print("✅ Modelos de chatbot importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar chatbot: {e}")
    ChatFlow = ChatConversation = ChatMessage = ChatIntegration = ChatAIConfig = None

try:
    from .automation import (
        AutomationRule, AutomationAction, AutomationExecution, 
        EmailCampaign, CadenceSequence, CadenceStep, CadenceEnrollment
    )
    print("✅ Modelos de automation importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar automation: {e}")
    AutomationRule = AutomationAction = AutomationExecution = None
    EmailCampaign = CadenceSequence = CadenceStep = CadenceEnrollment = None

# Importar modelos de telefonia
try:
    from .telephony import Call, CallLog
    print("✅ Modelos de telephony importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar telephony: {e}")
    Call = CallLog = None

# Importar modelos de tenant (multi-tenancy)
try:
    from .tenant import Tenant, TenantSubscription, TenantUsageLog, TenantInvitation
    print("✅ Modelos de tenant importados com sucesso")
except ImportError as e:
    print(f"⚠️  Erro ao importar tenant: {e}")
    Tenant = TenantSubscription = TenantUsageLog = TenantInvitation = None

# Exportar todos os modelos
__all__ = [
    # Database
    'db',
    
    # User & Auth
    'User', 'Role', 'Permission',
    
    # Leads & Pipeline
    'Lead', 'Tag', 'LeadFieldTemplate',
    'Pipeline', 'PipelineStage', 'Product', 'Opportunity',
    
    # Tasks & Activities
    'Task', 'TaskComment', 'TaskTimeLog', 'TaskTemplate', 'ActivitySummary',
    
    # Proposals & Contracts
    'ProposalTemplate', 'Proposal', 'ProposalItem',
    'ContractTemplate', 'Contract', 'ContractAmendment',
    
    # Chatbot & AI
    'ChatFlow', 'ChatConversation', 'ChatMessage', 'ChatIntegration', 'ChatAIConfig',
    
    # Automation & Marketing
    'AutomationRule', 'AutomationAction', 'AutomationExecution', 
    'EmailCampaign', 'CadenceSequence', 'CadenceStep', 'CadenceEnrollment',
    
    # Telephony
    'Call', 'CallLog',
    
    # Multi-tenancy
    'Tenant', 'TenantSubscription', 'TenantUsageLog', 'TenantInvitation'
]

def create_default_roles():
    """Cria roles e permissões padrão do sistema"""
    if not db or not Role or not Permission:
        print("⚠️  Modelos não carregados, pulando criação de roles")
        return
        
    try:
        # Verificar se já existem roles
        if Role.query.count() > 0:
            print("✅ Roles já existem no banco")
            return
        
        print("🔧 Criando roles e permissões padrão...")
        
        # Definir permissões padrão
        permissions_data = [
            {'name': 'leads_read', 'description': 'Visualizar leads'},
            {'name': 'leads_write', 'description': 'Criar/editar leads'},
            {'name': 'leads_delete', 'description': 'Excluir leads'},
            {'name': 'opportunities_read', 'description': 'Visualizar oportunidades'},
            {'name': 'opportunities_write', 'description': 'Criar/editar oportunidades'},
            {'name': 'opportunities_delete', 'description': 'Excluir oportunidades'},
            {'name': 'tasks_read', 'description': 'Visualizar tarefas'},
            {'name': 'tasks_write', 'description': 'Criar/editar tarefas'},
            {'name': 'tasks_delete', 'description': 'Excluir tarefas'},
            {'name': 'proposals_read', 'description': 'Visualizar propostas'},
            {'name': 'proposals_write', 'description': 'Criar/editar propostas'},
            {'name': 'contracts_read', 'description': 'Visualizar contratos'},
            {'name': 'contracts_write', 'description': 'Criar/editar contratos'},
            {'name': 'admin_access', 'description': 'Acesso administrativo'},
            {'name': 'users_manage', 'description': 'Gerenciar usuários'},
            {'name': 'settings_manage', 'description': 'Gerenciar configurações'},
            {'name': 'reports_access', 'description': 'Acessar relatórios'},
            {'name': 'automation_manage', 'description': 'Gerenciar automações'},
            {'name': 'telephony_access', 'description': 'Acessar telefonia'},
            {'name': 'chatbot_manage', 'description': 'Gerenciar chatbot'}
        ]
        
        # Criar permissões
        permissions = {}
        for perm_data in permissions_data:
            permission = Permission(
                name=perm_data['name'],
                description=perm_data['description']
            )
            db.session.add(permission)
            permissions[perm_data['name']] = permission
        
        # Definir roles padrão
        roles_data = [
            {
                'name': 'super_admin',
                'description': 'Super Administrador com acesso total',
                'permissions': list(permissions.keys())
            },
            {
                'name': 'admin',
                'description': 'Administrador da empresa',
                'permissions': [
                    'leads_read', 'leads_write', 'leads_delete',
                    'opportunities_read', 'opportunities_write', 'opportunities_delete',
                    'tasks_read', 'tasks_write', 'tasks_delete',
                    'proposals_read', 'proposals_write',
                    'contracts_read', 'contracts_write',
                    'users_manage', 'settings_manage', 'reports_access',
                    'automation_manage', 'telephony_access', 'chatbot_manage'
                ]
            },
            {
                'name': 'manager',
                'description': 'Gerente de vendas',
                'permissions': [
                    'leads_read', 'leads_write',
                    'opportunities_read', 'opportunities_write',
                    'tasks_read', 'tasks_write',
                    'proposals_read', 'proposals_write',
                    'contracts_read',
                    'reports_access', 'telephony_access'
                ]
            },
            {
                'name': 'sales',
                'description': 'Vendedor',
                'permissions': [
                    'leads_read', 'leads_write',
                    'opportunities_read', 'opportunities_write',
                    'tasks_read', 'tasks_write',
                    'proposals_read', 'proposals_write',
                    'telephony_access'
                ]
            },
            {
                'name': 'user',
                'description': 'Usuário básico',
                'permissions': [
                    'leads_read',
                    'opportunities_read',
                    'tasks_read', 'tasks_write',
                    'proposals_read'
                ]
            }
        ]
        
        # Criar roles
        for role_data in roles_data:
            role = Role(
                name=role_data['name'],
                description=role_data['description']
            )
            
            # Adicionar permissões ao role
            for perm_name in role_data['permissions']:
                if perm_name in permissions:
                    role.permissions.append(permissions[perm_name])
            
            db.session.add(role)
        
        db.session.commit()
        print("✅ Roles e permissões criados com sucesso!")
        print(f"   - {len(permissions_data)} permissões criadas")
        print(f"   - {len(roles_data)} roles criados")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao criar roles: {e}")

def init_database(app):
    """Inicializa o banco de dados"""
    if not db:
        print("❌ Database não inicializado")
        return False
        
    print("🔧 Inicializando banco de dados...")
    db.init_app(app)
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            print("📊 Criando tabelas...")
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Criar roles padrão
            create_default_roles()
            
            return True
        except Exception as e:
            print(f"❌ Erro ao inicializar banco: {e}")
            return False

def get_available_models():
    """Retorna lista de modelos disponíveis"""
    available = []
    models_to_check = [
        ('User', User),
        ('Role', Role), 
        ('Permission', Permission),
        ('Lead', Lead),
        ('Tag', Tag),
        ('Pipeline', Pipeline),
        ('PipelineStage', PipelineStage),
        ('Product', Product),
        ('Opportunity', Opportunity),
        ('Task', Task),
        ('Proposal', Proposal),
        ('Contract', Contract),
        ('ChatFlow', ChatFlow),
        ('AutomationRule', AutomationRule),
        ('Call', Call),
        ('Tenant', Tenant)
    ]
    
    for name, model in models_to_check:
        if model is not None:
            available.append(name)
    
    return available

def validate_models():
    """Valida se os modelos estão funcionando corretamente"""
    try:
        available_models = get_available_models()
        
        result = {
            'total_models': len(__all__) - 1,  # -1 para excluir 'db'
            'available_models': len(available_models),
            'models_list': available_models,
            'database_available': db is not None
        }
        
        return result
        
    except Exception as e:
        return {'error': str(e)}

# Função de debug para desenvolvimento
def debug_info():
    """Informações de debug dos modelos"""
    print("\n" + "="*50)
    print("🔍 DEBUG - INFORMAÇÕES DOS MODELOS")
    print("="*50)
    
    print(f"📦 Database (db): {'✅ Disponível' if db else '❌ Não disponível'}")
    
    models_status = [
        ('User', User),
        ('Lead', Lead),
        ('Pipeline', Pipeline),
        ('Task', Task),
        ('Proposal', Proposal),
        ('Contract', Contract),
        ('ChatFlow', ChatFlow),
        ('AutomationRule', AutomationRule),
        ('Call', Call),
        ('Tenant', Tenant)
    ]
    
    for name, model in models_status:
        status = "✅ Carregado" if model else "❌ Não carregado"
        print(f"📋 {name}: {status}")
    
    validation = validate_models()
    print(f"\n📊 Total de modelos: {validation.get('total_models', 0)}")
    print(f"✅ Modelos disponíveis: {validation.get('available_models', 0)}")
    print("="*50 + "\n")

# Executar debug se chamado diretamente
if __name__ == "__main__":
    debug_info()
