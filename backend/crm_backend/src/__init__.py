# src/__init__.py
"""
Módulo principal do CRM JT Tecnologia
Sistema de importação com tratamento robusto de erros
"""

import sys
import traceback
from typing import Dict, List, Tuple, Any

__version__ = "1.0.0"
__author__ = "JT Tecnologia"
__description__ = "Sistema CRM completo com automações, chatbot e telefonia"

# Status global de importação
IMPORT_STATUS = {
    'models': {'success': False, 'errors': [], 'loaded': []},
    'routes': {'success': False, 'errors': [], 'loaded': []},
    'services': {'success': False, 'errors': [], 'loaded': []}
}

def log_import_status(module_type: str, module_name: str, success: bool, error: str = None):
    """Log do status de importação de módulos"""
    if success:
        IMPORT_STATUS[module_type]['loaded'].append(module_name)
        print(f"✅ {module_type.capitalize()}: {module_name} importado com sucesso")
    else:
        IMPORT_STATUS[module_type]['errors'].append(f"{module_name}: {error}")
        print(f"❌ {module_type.capitalize()}: Erro ao importar {module_name} - {error}")

def safe_import(module_path: str, module_type: str = 'general'):
    """Importação segura com tratamento de erros"""
    try:
        if module_path.startswith('.'):
            # Importação relativa
            module = __import__(module_path, fromlist=[''], level=1)
        else:
            # Importação absoluta
            module = __import__(module_path)
        
        log_import_status(module_type, module_path, True)
        return module
    except ImportError as e:
        log_import_status(module_type, module_path, False, str(e))
        return None
    except Exception as e:
        log_import_status(module_type, module_path, False, f"Erro inesperado: {str(e)}")
        return None

# ==================== IMPORTAÇÃO DE MODELOS ====================
print("🔧 Iniciando importação de modelos...")

# Tentar importar modelos principais
db = None
models_loaded = {}

try:
    from .models import (
        db, User, Role, Permission, Lead, Tag, Pipeline, 
        PipelineStage, Product, Opportunity, Task, Proposal, 
        Contract, ChatFlow, AutomationRule, Call, Tenant,
        validate_models, init_database
    )
    
    # Verificar quais modelos foram carregados com sucesso
    model_checks = [
        ('db', db),
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
    
    for name, model in model_checks:
        if model is not None:
            models_loaded[name] = model
            log_import_status('models', name, True)
        else:
            log_import_status('models', name, False, "Modelo não disponível")
    
    IMPORT_STATUS['models']['success'] = len(models_loaded) > 0
    
except ImportError as e:
    log_import_status('models', 'all_models', False, f"Erro de importação: {str(e)}")
    print("📋 Detalhes do erro de importação de modelos:")
    traceback.print_exc()
except Exception as e:
    log_import_status('models', 'all_models', False, f"Erro inesperado: {str(e)}")
    print("📋 Detalhes do erro inesperado:")
    traceback.print_exc()

# ==================== IMPORTAÇÃO DE ROTAS ====================
print("🛣️  Iniciando importação de rotas...")

routes_loaded = {}

try:
    from .routes import (
        register_all_blueprints, get_available_routes,
        leads_bp, dashboard_bp
    )
    
    # Verificar quais rotas foram carregadas
    route_checks = [
        ('register_all_blueprints', register_all_blueprints),
        ('get_available_routes', get_available_routes),
        ('leads_bp', leads_bp),
        ('dashboard_bp', dashboard_bp)
    ]
    
    for name, route in route_checks:
        if route is not None:
            routes_loaded[name] = route
            log_import_status('routes', name, True)
        else:
            log_import_status('routes', name, False, "Rota não disponível")
    
    IMPORT_STATUS['routes']['success'] = len(routes_loaded) > 0
    
except ImportError as e:
    log_import_status('routes', 'all_routes', False, f"Erro de importação: {str(e)}")
    print("📋 Detalhes do erro de importação de rotas:")
    traceback.print_exc()
except Exception as e:
    log_import_status('routes', 'all_routes', False, f"Erro inesperado: {str(e)}")

# ==================== IMPORTAÇÃO DE SERVIÇOS ====================
print("⚙️  Iniciando importação de serviços...")

services_loaded = {}

try:
    # Tentar importar serviços se existirem
    service_modules = [
        'auth_service',
        'email_service', 
        'automation_service'
    ]
    
    for service_name in service_modules:
        try:
            service = safe_import(f'.services.{service_name}', 'services')
            if service:
                services_loaded[service_name] = service
        except:
            pass  # Serviços são opcionais
    
    IMPORT_STATUS['services']['success'] = True  # Serviços são opcionais
    
except Exception as e:
    log_import_status('services', 'all_services', False, f"Erro inesperado: {str(e)}")

# ==================== FUNÇÕES UTILITÁRIAS ====================

def get_import_status() -> Dict[str, Any]:
    """Retorna status completo de importação"""
    return {
        **IMPORT_STATUS,
        'summary': {
            'models_loaded': len(models_loaded),
            'routes_loaded': len(routes_loaded),
            'services_loaded': len(services_loaded),
            'total_errors': sum(len(module['errors']) for module in IMPORT_STATUS.values())
        }
    }

def print_import_summary():
    """Imprime resumo das importações"""
    print("\n" + "="*60)
    print("📊 RESUMO DAS IMPORTAÇÕES")
    print("="*60)
    
    print(f"📦 Modelos: {len(models_loaded)} carregados")
    for name in models_loaded.keys():
        print(f"   ✅ {name}")
    
    print(f"🛣️  Rotas: {len(routes_loaded)} carregadas")
    for name in routes_loaded.keys():
        print(f"   ✅ {name}")
    
    print(f"⚙️  Serviços: {len(services_loaded)} carregados")
    for name in services_loaded.keys():
        print(f"   ✅ {name}")
    
    # Mostrar erros se houver
    total_errors = sum(len(module['errors']) for module in IMPORT_STATUS.values())
    if total_errors > 0:
        print(f"\n⚠️  Erros encontrados: {total_errors}")
        for module_type, status in IMPORT_STATUS.items():
            if status['errors']:
                print(f"   {module_type.upper()}:")
                for error in status['errors']:
                    print(f"     ❌ {error}")
    
    print("="*60 + "\n")

def validate_system():
    """Valida se o sistema pode funcionar com os módulos carregados"""
    critical_models = ['db', 'User', 'Lead']
    missing_critical = [model for model in critical_models if model not in models_loaded]
    
    if missing_critical:
        print(f"⚠️  AVISO: Modelos críticos não carregados: {missing_critical}")
        return False
    
    print("✅ Sistema validado - módulos críticos carregados")
    return True

def initialize_system(app=None):
    """Inicializa o sistema com os módulos carregados"""
    print("🚀 Inicializando sistema...")
    
    # Validar sistema
    if not validate_system():
        print("❌ Sistema não pode ser inicializado - módulos críticos ausentes")
        return False
    
    # Inicializar banco se disponível
    if 'init_database' in models_loaded and app:
        try:
            success = models_loaded['init_database'](app)
            if success:
                print("✅ Banco de dados inicializado")
            else:
                print("⚠️  Banco inicializado com avisos")
        except Exception as e:
            print(f"❌ Erro ao inicializar banco: {e}")
            return False
    
    # Registrar rotas se disponível
    if 'register_all_blueprints' in routes_loaded and app:
        try:
            count = routes_loaded['register_all_blueprints'](app)
            print(f"✅ {count} rotas registradas")
        except Exception as e:
            print(f"❌ Erro ao registrar rotas: {e}")
            return False
    
    print("🎉 Sistema inicializado com sucesso!")
    return True

# ==================== EXPORTAÇÕES ====================

# Exportar tudo que foi carregado com sucesso
__all__ = list(models_loaded.keys()) + list(routes_loaded.keys()) + list(services_loaded.keys()) + [
    'get_import_status',
    'print_import_summary', 
    'validate_system',
    'initialize_system',
    'IMPORT_STATUS'
]

# Executar resumo se chamado diretamente
if __name__ == "__main__":
    print_import_summary()
else:
    # Mostrar resumo rápido quando importado
    total_loaded = len(models_loaded) + len(routes_loaded) + len(services_loaded)
    total_errors = sum(len(module['errors']) for module in IMPORT_STATUS.values())
    
    if total_errors == 0:
        print(f"✅ Sistema carregado: {total_loaded} módulos importados com sucesso")
    else:
        print(f"⚠️  Sistema carregado: {total_loaded} módulos, {total_errors} erros")
        print("   Use src.print_import_summary() para detalhes")
