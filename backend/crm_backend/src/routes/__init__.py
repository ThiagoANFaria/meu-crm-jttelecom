# src/routes/__init__.py
"""
Módulo de rotas do CRM
Sistema de importação e registro de blueprints com tratamento robusto de erros
"""

import traceback
from typing import Dict, List, Tuple, Any, Optional
from flask import Flask

# Controle de importação de rotas
routes_registry = {}
import_errors = []
registered_blueprints = []

def safe_route_import(module_name: str, blueprint_name: str) -> Optional[Any]:
    """Importa blueprints de forma segura com tratamento de erros"""
    try:
        # Tentar importar o módulo
        module = __import__(f".{module_name}", fromlist=[blueprint_name], level=1)
        
        # Tentar obter o blueprint
        blueprint = getattr(module, blueprint_name)
        
        if blueprint is not None:
            routes_registry[blueprint_name] = blueprint
            print(f"✅ Blueprint {blueprint_name} de {module_name} importado com sucesso")
            return blueprint
        else:
            error_msg = f"Blueprint {blueprint_name} é None em {module_name}"
            import_errors.append(error_msg)
            print(f"⚠️  {error_msg}")
            return None
    
    except ImportError as e:
        error_msg = f"Erro ao importar {module_name}: {str(e)}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return None
    
    except AttributeError as e:
        error_msg = f"Blueprint {blueprint_name} não encontrado em {module_name}: {str(e)}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return None
    
    except Exception as e:
        error_msg = f"Erro inesperado ao importar {blueprint_name} de {module_name}: {str(e)}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        print("📋 Traceback completo:")
        traceback.print_exc()
        return None

# ==================== IMPORTAÇÃO SEGURA DE BLUEPRINTS ====================

print("🛣️  Iniciando importação segura de rotas...")

# Lista de blueprints para importar (module_name, blueprint_name)
blueprints_to_import = [
    ('leads', 'leads_bp'),
    ('dashboard', 'dashboard_bp'),
    ('opportunities', 'opportunities_bp'),
    ('tasks', 'tasks_bp'),
    ('proposals', 'proposals_bp'),
    ('contracts', 'contracts_bp'),
    ('users', 'users_bp'),
    ('auth', 'auth_bp'),
    ('automation', 'automation_bp'),
    ('telephony', 'telephony_bp')
]

# Importar cada blueprint
for module_name, blueprint_name in blueprints_to_import:
    blueprint = safe_route_import(module_name, blueprint_name)
    # O blueprint é automaticamente adicionado ao registry se bem-sucedido

# Tentar importar funções utilitárias específicas (se existirem)
utility_functions = {}

# Importar funções utilitárias de cada módulo
for module_name, _ in blueprints_to_import:
    try:
        module = __import__(f".{module_name}", fromlist=[''], level=1)
        
        # Procurar por funções úteis comuns
        common_functions = ['get_stats', 'validate_data', 'export_data']
        for func_name in common_functions:
            if hasattr(module, func_name):
                utility_functions[f"{module_name}_{func_name}"] = getattr(module, func_name)
    except:
        pass  # Funções utilitárias são opcionais

# ==================== FUNÇÕES DE REGISTRO ====================

def register_all_blueprints(app: Flask) -> int:
    """Registra todos os blueprints disponíveis na aplicação"""
    registered_count = 0
    registration_errors = []
    
    print("📝 Registrando blueprints na aplicação...")
    
    for blueprint_name, blueprint in routes_registry.items():
        try:
            if blueprint is not None:
                app.register_blueprint(blueprint)
                registered_blueprints.append(blueprint_name)
                print(f"✅ Blueprint '{blueprint_name}' registrado com sucesso")
                registered_count += 1
            else:
                error_msg = f"Blueprint '{blueprint_name}' é None - não pode ser registrado"
                registration_errors.append(error_msg)
                print(f"⚠️  {error_msg}")
        
        except Exception as e:
            error_msg = f"Erro ao registrar blueprint '{blueprint_name}': {str(e)}"
            registration_errors.append(error_msg)
            import_errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    # Adicionar erros de registro aos erros de importação
    import_errors.extend(registration_errors)
    
    print(f"📊 Blueprints registrados: {registered_count}/{len(routes_registry)}")
    
    if registration_errors:
        print(f"⚠️  Erros de registro: {len(registration_errors)}")
        for error in registration_errors:
            print(f"   • {error}")
    
    return registered_count

def register_single_blueprint(app: Flask, blueprint_name: str) -> bool:
    """Registra um blueprint específico"""
    if blueprint_name not in routes_registry:
        print(f"❌ Blueprint '{blueprint_name}' não encontrado no registry")
        return False
    
    try:
        blueprint = routes_registry[blueprint_name]
        if blueprint is not None:
            app.register_blueprint(blueprint)
            if blueprint_name not in registered_blueprints:
                registered_blueprints.append(blueprint_name)
            print(f"✅ Blueprint '{blueprint_name}' registrado individualmente")
            return True
        else:
            print(f"❌ Blueprint '{blueprint_name}' é None")
            return False
    
    except Exception as e:
        error_msg = f"Erro ao registrar blueprint '{blueprint_name}': {str(e)}"
        import_errors.append(error_msg)
        print(f"❌ {error_msg}")
        return False

def unregister_blueprint(app: Flask, blueprint_name: str) -> bool:
    """Remove um blueprint da aplicação (se possível)"""
    try:
        if blueprint_name in registered_blueprints:
            # Flask não tem método nativo para remover blueprints
            # Esta é uma limitação do Flask
            print(f"⚠️  Flask não suporta remoção de blueprints em runtime")
            print(f"   Blueprint '{blueprint_name}' permanecerá registrado")
            return False
        else:
            print(f"⚠️  Blueprint '{blueprint_name}' não está registrado")
            return False
    
    except Exception as e:
        print(f"❌ Erro ao tentar remover blueprint '{blueprint_name}': {str(e)}")
        return False

# ==================== FUNÇÕES UTILITÁRIAS ====================

def get_available_routes() -> List[Dict[str, Any]]:
    """Retorna lista de rotas disponíveis"""
    routes = []
    
    for blueprint_name, blueprint in routes_registry.items():
        if blueprint is not None:
            try:
                route_info = {
                    'name': blueprint_name,
                    'prefix': getattr(blueprint, 'url_prefix', '/'),
                    'status': 'registered' if blueprint_name in registered_blueprints else 'loaded',
                    'module': getattr(blueprint, 'import_name', 'unknown')
                }
                routes.append(route_info)
            except Exception as e:
                routes.append({
                    'name': blueprint_name,
                    'status': f'error: {str(e)}',
                    'prefix': 'unknown'
                })
    
    return routes

def get_route_status() -> Dict[str, Any]:
    """Retorna status detalhado das rotas"""
    total_attempted = len(blueprints_to_import)
    loaded_successfully = len(routes_registry)
    registered_successfully = len(registered_blueprints)
    
    return {
        'total_attempted': total_attempted,
        'loaded_successfully': loaded_successfully,
        'registered_successfully': registered_successfully,
        'failed_to_load': total_attempted - loaded_successfully,
        'load_success_rate': round((loaded_successfully / total_attempted * 100), 2) if total_attempted > 0 else 0,
        'register_success_rate': round((registered_successfully / loaded_successfully * 100), 2) if loaded_successfully > 0 else 0,
        'import_errors': len(import_errors),
        'routes_registry': list(routes_registry.keys()),
        'registered_blueprints': registered_blueprints,
        'available_routes': get_available_routes(),
        'utility_functions': list(utility_functions.keys())
    }

def validate_routes() -> Dict[str, Any]:
    """Valida se as rotas estão funcionando corretamente"""
    try:
        status = get_route_status()
        
        # Verificar se pelo menos algumas rotas críticas foram carregadas
        critical_routes = ['leads_bp', 'dashboard_bp']
        critical_loaded = [route for route in critical_routes if route in routes_registry]
        
        validation = {
            **status,
            'critical_routes_loaded': len(critical_loaded),
            'critical_routes_total': len(critical_routes),
            'critical_routes_ok': len(critical_loaded) >= 1,  # Pelo menos uma rota crítica
            'system_functional': status['loaded_successfully'] > 0 and len(import_errors) == 0,
            'warnings': []
        }
        
        # Adicionar avisos se necessário
        if validation['load_success_rate'] < 50:
            validation['warnings'].append("Baixa taxa de sucesso no carregamento de rotas")
        
        if validation['critical_routes_loaded'] == 0:
            validation['warnings'].append("Nenhuma rota crítica foi carregada")
        
        if len(import_errors) > 0:
            validation['warnings'].append(f"{len(import_errors)} erros de importação encontrados")
        
        return validation
        
    except Exception as e:
        return {'error': str(e), 'import_errors': import_errors}

def print_routes_summary():
    """Imprime resumo detalhado das rotas"""
    print("\n" + "="*60)
    print("🛣️  RESUMO DAS ROTAS")
    print("="*60)
    
    status = get_route_status()
    validation = validate_routes()
    
    print(f"📊 Estatísticas:")
    print(f"   • Total tentativas: {status['total_attempted']}")
    print(f"   • Carregadas: {status['loaded_successfully']}")
    print(f"   • Registradas: {status['registered_successfully']}")
    print(f"   • Taxa de sucesso (carga): {status['load_success_rate']}%")
    print(f"   • Taxa de sucesso (registro): {status['register_success_rate']}%")
    
    if status['loaded_successfully'] > 0:
        print(f"\n✅ ROTAS CARREGADAS ({status['loaded_successfully']}):")
        for route_name in status['routes_registry']:
            status_text = "registrada" if route_name in status['registered_blueprints'] else "carregada"
            print(f"   • {route_name} ({status_text})")
    
    if status['utility_functions']:
        print(f"\n🔧 FUNÇÕES UTILITÁRIAS ({len(status['utility_functions'])}):")
        for func_name in status['utility_functions']:
            print(f"   • {func_name}")
    
    if validation.get('warnings'):
        print(f"\n⚠️  AVISOS ({len(validation['warnings'])}):")
        for warning in validation['warnings']:
            print(f"   • {warning}")
    
    if import_errors:
        print(f"\n❌ ERROS DE IMPORTAÇÃO ({len(import_errors)}):")
        for error in import_errors[:10]:  # Mostrar apenas os primeiros 10
            print(f"   • {error}")
        if len(import_errors) > 10:
            print(f"   ... e mais {len(import_errors) - 10} erros")
    
    print("="*60 + "\n")

def reset_routes():
    """Reseta o estado das rotas (útil para testes)"""
    global routes_registry, import_errors, registered_blueprints
    
    routes_registry.clear()
    import_errors.clear()
    registered_blueprints.clear()
    
    print("🔄 Estado das rotas resetado")

# ==================== EXPORTAÇÕES ====================

# Exportar blueprints carregados
__all__ = list(routes_registry.keys()) + [
    'register_all_blueprints',
    'register_single_blueprint',
    'unregister_blueprint',
    'get_available_routes',
    'get_route_status',
    'validate_routes',
    'print_routes_summary',
    'reset_routes',
    'routes_registry',
    'import_errors',
    'registered_blueprints',
    'utility_functions'
]

# Executar resumo se chamado diretamente
if __name__ == "__main__":
    print_routes_summary()
else:
    # Mostrar resumo rápido quando importado
    status = get_route_status()
    if status['import_errors'] == 0:
        print(f"✅ Rotas carregadas: {status['loaded_successfully']}/{status['total_attempted']}")
    else:
        print(f"⚠️  Rotas: {status['loaded_successfully']}/{status['total_attempted']} - {status['import_errors']} erros")
        print("   Use src.routes.print_routes_summary() para detalhes")
