"""
Módulo de modelos do CRM JT Telecom
Centraliza todas as importações e configurações dos modelos de dados
"""

from flask_sqlalchemy import SQLAlchemy

# Instância global do SQLAlchemy
db = SQLAlchemy()

# Importar todos os modelos
try:
    from .user import User, Role, UserRole, UserPermission, UserSession, UserPreference
    from .lead import Lead, Tag, LeadTag, LeadHistory, LeadNote, LeadAttachment
    from .pipeline import Pipeline, PipelineStage, Opportunity, OpportunityHistory
    from .proposal import ProposalTemplate, Proposal, ProposalItem, ProposalHistory
    from .contract import ContractTemplate, Contract, ContractAmendment, ContractHistory
    from .chatbot import ChatFlow, ChatConversation, ChatMessage, ChatIntegration, ChatAIConfig
    from .telephony import Call, CallLog, CallRecording, PhoneNumber
    from .tenant import Tenant, TenantSubscription, TenantUsageLog, TenantInvitation
    from .automation import (
        AutomationRule, AutomationAction, AutomationExecution,
        EmailCampaign, CadenceSequence, CadenceStep, CadenceEnrollment
    )
    from .task import Task, TaskComment, TaskTimeLog, TaskTemplate, ActivitySummary
    
    print("✅ Todos os modelos foram importados com sucesso")
    
except ImportError as e:
    print(f"⚠️ Erro ao importar modelos: {e}")

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    db.init_app(app)
    
def create_tables(app):
    """Cria todas as tabelas no banco de dados"""
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso")

def validate_models():
    """Valida se todos os modelos foram carregados corretamente"""
    models = [
        'User', 'Role', 'UserRole', 'UserPermission', 'UserSession', 'UserPreference',
        'Lead', 'Tag', 'LeadTag', 'LeadHistory', 'LeadNote', 'LeadAttachment',
        'Pipeline', 'PipelineStage', 'Opportunity', 'OpportunityHistory',
        'ProposalTemplate', 'Proposal', 'ProposalItem', 'ProposalHistory',
        'ContractTemplate', 'Contract', 'ContractAmendment', 'ContractHistory',
        'ChatFlow', 'ChatConversation', 'ChatMessage', 'ChatIntegration', 'ChatAIConfig',
        'Call', 'CallLog', 'CallRecording', 'PhoneNumber',
        'Tenant', 'TenantSubscription', 'TenantUsageLog', 'TenantInvitation',
        'AutomationRule', 'AutomationAction', 'AutomationExecution',
        'EmailCampaign', 'CadenceSequence', 'CadenceStep', 'CadenceEnrollment',
        'Task', 'TaskComment', 'TaskTimeLog', 'TaskTemplate', 'ActivitySummary'
    ]
    
    loaded_models = 0
    error_count = 0
    
    for model_name in models:
        try:
            globals()[model_name]
            loaded_models += 1
        except KeyError:
            error_count += 1
            print(f"⚠️ Modelo não encontrado: {model_name}")
    
    return {
        'total_models': len(models),
        'loaded_models': loaded_models,
        'error_count': error_count
    }

def print_model_summary():
    """Imprime um resumo dos modelos carregados"""
    validation = validate_models()
    print("\n" + "="*50)
    print("RESUMO DOS MODELOS DO CRM JT TELECOM")
    print("="*50)
    print(f"Total de modelos: {validation['total_models']}")
    print(f"Modelos carregados: {validation['loaded_models']}")
    print(f"Erros encontrados: {validation['error_count']}")
    
    if validation['error_count'] == 0:
        print("✅ Todos os modelos foram carregados com sucesso!")
    else:
        print(f"⚠️ {validation['error_count']} modelo(s) com problemas")
    
    print("="*50)

# Executar validação quando o módulo for importado
if __name__ == "__main__":
    print_model_summary()
else:
    # Mostrar resumo rápido quando importado
    validation = validate_models()
    if validation.get('error_count', 0) == 0:
        print(f"✅ Modelos carregados: {validation.get('loaded_models', 0)}/{validation.get('total_models', 0)}")
    else:
        print(f"⚠️ {validation.get('error_count', 0)} modelo(s) com problemas")

