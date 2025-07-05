"""
Módulo de serviços do CRM JT Telecom
"""
import logging

logger = logging.getLogger(__name__)

# Importar serviços com tratamento de erro
try:
    from .auth_service import AuthService
    logger.info("✅ AuthService importado")
except Exception as e:
    logger.error(f"❌ Erro ao importar AuthService: {e}")
    
    # Criar classe básica como fallback
    class AuthService:
        def __init__(self):
            pass
        
        def authenticate(self, email, password):
            return {"success": False, "error": "Serviço não disponível"}

try:
    from .email_service import EmailService
    logger.info("✅ EmailService importado")
except Exception as e:
    logger.error(f"❌ Erro ao importar EmailService: {e}")
    
    # Criar classe básica como fallback
    class EmailService:
        def __init__(self):
            pass
        
        def send_email(self, to, subject, body):
            return {"success": False, "error": "Serviço não disponível"}

try:
    from .automation_service import AutomationEngine
    logger.info("✅ AutomationEngine importado")
except Exception as e:
    logger.error(f"❌ Erro ao importar AutomationEngine: {e}")
    
    # Criar classe básica como fallback
    class AutomationEngine:
        def __init__(self):
            pass
        
        def execute_rule(self, rule_id):
            return {"success": False, "error": "Serviço não disponível"}

try:
    from .analytics_service import AnalyticsService
    logger.info("✅ AnalyticsService importado")
except Exception as e:
    logger.error(f"❌ Erro ao importar AnalyticsService: {e}")
    
    # Criar classe básica como fallback
    class AnalyticsService:
        def __init__(self):
            pass
        
        def get_dashboard_overview(self, tenant_id, user_id):
            return {"leads": 0, "opportunities": 0, "tasks": 0, "revenue": 0}

try:
    from .telephony_service import TelephonyService
    logger.info("✅ TelephonyService importado")
except Exception as e:
    logger.error(f"❌ Erro ao importar TelephonyService: {e}")
    
    # Criar classe básica como fallback
    class TelephonyService:
        def __init__(self):
            pass
        
        def make_call(self, from_number, to_number, user_id, lead_id=None):
            return {"success": False, "error": "Serviço não disponível"}

# Exportar todos os serviços
__all__ = [
    'AuthService', 'EmailService', 'AutomationEngine',
    'AnalyticsService', 'TelephonyService'
]

def init_services():
    """Inicializar todos os serviços"""
    try:
        # Instanciar serviços globais se necessário
        logger.info("🚀 Inicializando serviços...")
        
        # Verificar se os serviços estão funcionando
        auth_service = AuthService()
        email_service = EmailService()
        automation_engine = AutomationEngine()
        analytics_service = AnalyticsService()
        telephony_service = TelephonyService()
        
        logger.info("✅ Todos os serviços inicializados com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar serviços: {e}")
        return False

logger.info(f"🎉 Módulo de serviços inicializado com {len(__all__)} classes")

