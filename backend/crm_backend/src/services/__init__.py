"""
Módulo de serviços do CRM JT Telecom
Centraliza todos os serviços e utilitários
"""

# Importar serviços básicos
try:
    from .auth_service import AuthService
    from .email_service import EmailService  
    from .automation_service import AutomationService, AutomationEngine
    print("✅ Módulo de serviços carregado")
except ImportError as e:
    print(f"⚠️ Erro ao carregar serviços: {e}")

def init_services():
    """Inicializa todos os serviços"""
    print("✅ Serviços inicializados")
    return True

# Exportar serviços
__all__ = [
    'AuthService',
    'EmailService', 
    'AutomationService',
    'AutomationEngine',
    'init_services'
]

