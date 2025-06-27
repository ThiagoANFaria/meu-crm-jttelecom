# src/models/__init__.py
"""
Módulo central de modelos do CRM
Sistema de importação com tratamento robusto de erros
"""

import sys
import traceback
from typing import Dict, Any, Optional

# Variáveis globais para controle de importação
db = None
models_registry = {}
import_errors = []

def safe_model_import(module_name: str, model_names: list) -> Dict[str, Any]:
    """Importa modelos de forma segura com tratamento de erros"""
    imported = {}
    
    try:
        # Tentar importar o módulo
        module = __import__(f".{module_name}", fromlist=model_names, level=1)
        
        # Verificar cada modelo individualmente
        for model_name in model_names:
            try:
                model = getattr(module, model_name)
                imported[model_name] = model
                print(f"✅ {module_name}.{model_name} importado com sucesso")
            except AttributeError:
                error_msg = f"Modelo {model_name} não encontrado em {module_name}"
                import_errors.append(error_msg)
                print(f"⚠️  {error_msg}")
                imported[model_name] = None
            except Exception as e:
                error_msg = f"Erro ao importar {model_name} de {module_name}: {str(e)}"
                import_errors.append(error_msg)
                print(f"❌ {error_msg}")
                imported[model_name] = None
    
    except ImportError as e:
        error_msg = f"Erro ao importar módulo {module_name}: {str(e)}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        
        # Criar entradas None para todos os modelos
        for model_name in model_names:
            imported[model_name] = None
    
    except Exception as e:
        error_msg = f"Erro inesperado ao importar {module_name}: {str(e)}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        print("📋 Traceback completo:")
        traceback.print_exc()
        
        # Criar entradas None para todos os modelos
        for model_name in model_names:
            imported[model_name] = None
    
    return imported

# ==================== IMPORTAÇÃO SEGURA DOS MODELOS ====================

print("🔧 Iniciando importação segura de modelos...")

# 1. Importar modelos de usuário (base - obrigatório)
user_models = safe_model_import('user', ['db', 'User', 'Role', 'Permission'])
db = user_models.get('db')
User = user_models.get('User')
Role = user_models.get('Role')
Permission = user_models.get('Permission')

# Verificar se o db foi carregado (crítico)
if db is None:
    print("❌ CRÍTICO: Database (db) não foi carregado!")
    print("   O sistema não funcionará sem a instância do banco")
else:
    print("✅ Database (db) carregado com sucesso")

# 2. Importar modelos de lead
lead_models = safe_model_import('lead', ['Lead', 'Tag', 'LeadFieldTemplate'])
Lead = lead_models.get('Lead')
Tag = lead_models.get('Tag')
LeadFieldTemplate = lead_models.get('LeadFieldTemplate')

# 3. Importar modelos de pipeline
pipeline_models = safe_model_import('pipeline', ['Pipeline', 'PipelineStage', 'Product', 'Opportunity'])
Pipeline = pipeline_models.get('Pipeline')
PipelineStage = pipeline_models.get('PipelineStage')
Product = pipeline_models.get('Product')
Opportunity = pipeline_models.get('Opportunity')

# 4. Importar modelos de task
task_models = safe_model_import('task', ['Task', 'TaskComment', 'TaskTimeLog', 'TaskTemplate', 'ActivitySummary'])
Task = task_models.get('Task')
TaskComment = task_models.get('TaskComment')
TaskTimeLog = task_models.get('TaskTimeLog')
TaskTemplate = task_models.get('TaskTemplate')
ActivitySummary = task_models.get('ActivitySummary')

# 5. Importar modelos de proposal
proposal_models = safe_model_import('proposal', ['ProposalTemplate', 'Proposal', 'ProposalItem'])
ProposalTemplate = proposal_models.get('ProposalTemplate')
Proposal = proposal_models.get('Proposal')
ProposalItem = proposal_models.get('ProposalItem')

# 6. Importar modelos de contract
contract_models = safe_model_import('contract', ['ContractTemplate', 'Contract', 'ContractAmendment'])
ContractTemplate = contract_models.get('ContractTemplate')
Contract = contract_models.get('Contract')
ContractAmendment = contract_models.get('ContractAmendment')

# 7. Importar modelos de chatbot
chatbot_models = safe_model_import('chatbot', ['ChatFlow', 'ChatConversation', 'ChatMessage', 'ChatIntegration', 'ChatAIConfig'])
ChatFlow = chatbot_models.get('ChatFlow')
ChatConversation = chatbot_models.get('ChatConversation')
ChatMessage = chatbot_models.get('ChatMessage')
ChatIntegration = chatbot_models.get('ChatIntegration')
ChatAIConfig = chatbot_models.get('ChatAIConfig')

# 8. Importar modelos de automation
automation_models = safe_model_import('automation', [
    'AutomationRule', 'AutomationAction', 'AutomationExecution', 
    'EmailCampaign', 'CadenceSequence', 'CadenceStep', 'CadenceEnrollment'
])
AutomationRule = automation_models.get('AutomationRule')
AutomationAction = automation_models.get('AutomationAction')
AutomationExecution = automation_models.get('AutomationExecution')
EmailCampaign = automation_models.get('EmailCampaign')
CadenceSequence = automation_models.get('CadenceSequence')
CadenceStep = automation_models.get('CadenceStep')
CadenceEnrollment = automation_models.get('CadenceEnrollment')

# 9. Importar modelos de telephony
telephony_models = safe_model_import('telephony', ['Call', 'CallLog'])
Call = telephony_models.get('Call')
CallLog = telephony_models.get('CallLog')

# 10. Importar modelos de tenant
tenant_models = safe_model_import('tenant', ['Tenant', 'TenantSubscription', 'TenantUsageLog', 'TenantInvitation'])
Tenant = tenant_models.get('Tenant')
TenantSubscription = tenant_models.get('TenantSubscription')
TenantUsageLog = tenant_models.get('TenantUsageLog')
TenantInvitation = tenant_models.get('TenantInvitation')

# ==================== REGISTRO DE MODELOS ====================

# Registrar todos os modelos carregados
all_models = {
    **user_models,
    **lead_models,
    **pipeline_models,
    **task_models,
    **proposal_models,
    **contract_models,
    **chatbot_models,
    **automation_models,
    **telephony_models,
    **tenant_models
}

# Filtrar apenas modelos que foram carregados com sucesso
models_registry = {name: model for name, model in all_models.items() if model is not None}

# ==================== FUNÇÕES UTILITÁRIAS ====================

def create_default_roles():
    """Cria roles e permissões padrão do sistema com tratamento de erros"""
    if not db or not Role or not Permission:
        error_msg = "Modelos Role/Permission não carregados, pulando criação de roles"
        import_errors.append(error_msg)
        print(f"⚠️  {error_msg}")
        return False
        
    try:
        # Verificar se já existem roles
        if Role.query.count() > 0:
            print("✅ Roles já existem no banco")
            return True
        
        print("🔧 Criando roles e permissões padrão...")
        
        # Definir permissões padrão
        permissions_data = [
            {'name': 'leads_read', 'description': 'Visualizar leads'},
            {'name': 'leads_write', 'description': 'Criar/editar leads'},
            {'name': 'leads_delete', 'description': 'Excluir leads'},
            {'name': 'opportunities_read', 'description': 'Visualizar oportunidades'},
            {'name': 'opportunities_write', 'description': 'Criar/editar oportunidades'},
            {'name': 'tasks_read', 'description': 'Visualizar tarefas'},
            {'name': 'tasks_write', 'description': 'Criar/editar tarefas'},
            {'name': 'proposals_read', 'description': 'Visualizar propostas'},
            {'name': 'proposals_write', 'description': 'Criar/editar propostas'},
            {'name': 'admin_access', 'description': 'Acesso administrativo'},
            {'name': 'users_manage', 'description': 'Gerenciar usuários'},
            {'name': 'reports_access', 'description': 'Acessar relatórios'}
        ]
        
        # Criar permissões
        permissions = {}
        for perm_data in permissions_data:
            try:
                permission = Permission(
                    name=perm_data['name'],
                    description=perm_data['description']
                )
                db.session.add(permission)
                permissions[perm_data['name']] = permission
            except Exception as e:
                print(f"❌ Erro ao criar permissão {perm_data['name']}: {e}")
        
        # Definir roles padrão
        roles_data = [
            {
                'name': 'admin',
                'description': 'Administrador com acesso total',
                'permissions': list(permissions.keys())
            },
            {
                'name': 'manager',
                'description': 'Gerente de vendas',
                'permissions': [
                    'leads_read', 'leads_write',
                    'opportunities_read', 'opportunities_write',
                    'tasks_read', 'tasks_write',
                    'proposals_read', 'proposals_write',
                    'reports_access'
                ]
            },
            {
                'name': 'sales',
                'description': 'Vendedor',
                'permissions': [
                    'leads_read', 'leads_write',
                    'opportunities_read', 'opportunities_write',
                    'tasks_read', 'tasks_write',
                    'proposals_read'
                ]
            },
            {
                'name': 'user',
                'description': 'Usuário básico',
                'permissions': [
                    'leads_read',
                    'opportunities_read',
                    'tasks_read', 'tasks_write'
                ]
            }
        ]
        
        # Criar roles
        for role_data in roles_data:
            try:
                role = Role(
                    name=role_data['name'],
                    description=role_data['description']
                )
                
                # Adicionar permissões ao role
                for perm_name in role_data['permissions']:
                    if perm_name in permissions:
                        role.permissions.append(permissions[perm_name])
                
                db.session.add(role)
            except Exception as e:
                print(f"❌ Erro ao criar role {role_data['name']}: {e}")
        
        db.session.commit()
        print("✅ Roles e permissões criados com sucesso!")
        return True
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"Erro ao criar roles: {e}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return False

def init_database(app):
    """Inicializa o banco de dados com tratamento de erros"""
    if not db:
        error_msg = "Database não inicializado - modelos não carregados"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return False
        
    try:
        print("🔧 Inicializando banco de dados...")
        db.init_app(app)
        
        with app.app_context():
            # Criar todas as tabelas
            print("📊 Criando tabelas...")
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Criar roles padrão
            roles_success = create_default_roles()
            
            return True
        
    except Exception as e:
        error_msg = f"Erro ao inicializar banco: {e}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        print("📋 Traceback completo:")
        traceback.print_exc()
        return False

def validate_models() -> Dict[str, Any]:
    """Valida quais modelos foram carregados com sucesso"""
    try:
        loaded_models = [name for name, model in models_registry.items() if model is not None]
        failed_models = [name for name, model in all_models.items() if model is None]
        
        return {
            'total_models': len(all_models),
            'loaded_models': len(loaded_models),
            'failed_models': len(failed_models),
            'models_list': loaded_models,
            'failed_list': failed_models,
            'database_available': db is not None,
            'critical_models_ok': all(models_registry.get(model) is not None for model in ['db', 'User']),
            'import_errors': import_errors,
            'error_count': len(import_errors)
        }
        
    except Exception as e:
        return {'error': str(e), 'import_errors': import_errors}

def get_model_status():
    """Retorna status detalhado de cada modelo"""
    status = {}
    
    for name, model in all_models.items():
        if model is not None:
            try:
                # Tentar acessar o nome da tabela para verificar se está válido
                table_name = getattr(model, '__tablename__', 'N/A')
                status[name] = {
                    'loaded': True,
                    'table_name': table_name,
                    'status': 'OK'
                }
            except Exception as e:
                status[name] = {
                    'loaded': True,
                    'status': f'Erro: {str(e)}'
                }
        else:
            status[name] = {
                'loaded': False,
                'status': 'Não carregado'
            }
    
    return status

def print_model_summary():
    """Imprime resumo detalhado dos modelos"""
    print("\n" + "="*60)
    print("📊 RESUMO DOS MODELOS")
    print("="*60)
    
    validation = validate_models()
    
    print(f"📦 Total de modelos: {validation['total_models']}")
    print(f"✅ Modelos carregados: {validation['loaded_models']}")
    print(f"❌ Modelos falharam: {validation['failed_models']}")
    print(f"🗄️  Database disponível: {'Sim' if validation['database_available'] else 'Não'}")
    print(f"🔑 Modelos críticos OK: {'Sim' if validation['critical_models_ok'] else 'Não'}")
    
    if validation['loaded_models'] > 0:
        print(f"\n✅ MODELOS CARREGADOS ({validation['loaded_models']}):")
        for model in validation['models_list']:
            print(f"   {model}")
    
    if validation['failed_models'] > 0:
        print(f"\n❌ MODELOS FALHARAM ({validation['failed_models']}):")
        for model in validation['failed_list']:
            print(f"   {model}")
    
    if validation['error_count'] > 0:
        print(f"\n⚠️  ERROS DE IMPORTAÇÃO ({validation['error_count']}):")
        for error in validation['import_errors']:
            print(f"   • {error}")
    
    print("="*60 + "\n")

# ==================== EXPORTAÇÕES ====================

# Exportar todos os modelos (incluindo None para os que falharam)
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
    'Tenant', 'TenantSubscription', 'TenantUsageLog', 'TenantInvitation',
    
    # Funções utilitárias
    'create_default_roles',
    'init_database',
    'validate_models',
    'get_model_status',
    'print_model_summary',
    'models_registry',
    'import_errors'
]

# Executar resumo se chamado diretamente
if __name__ == "__main__":
    print_model_summary()
else:
    # Mostrar resumo rápido quando importado
    validation = validate_models()
    if validation.get('error_count', 0) == 0:
        print(f"✅ Modelos carregados: {validation.get('loaded_models', 0)}/{validation.get('total_models', 0)}")
    else:
        print(f"⚠️
