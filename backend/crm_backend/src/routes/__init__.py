# src/routes/__init__.py
"""
Módulo de rotas do CRM
Sistema de importação compatível com arquivos existentes profissionais
"""

import traceback
from typing import Dict, List, Any, Optional
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
        return None

# ==================== IMPORTAÇÃO SEGURA DE BLUEPRINTS ====================

print("🛣️  Iniciando importação segura de rotas...")

# Lista de blueprints para importar - seus arquivos existentes
blueprints_to_import = [
    # Seus arquivos já existentes e profissionais
    ('leads', 'leads_bp'),           # ✅ Seu arquivo completo
    ('dashboard', 'dashboard_bp'),   # ✅ Seu arquivo completo
    
    # Outros blueprints que podem existir ou serem criados no futuro
    ('users', 'users_bp'),
    ('auth', 'auth_bp'),
    ('opportunities', 'opportunities_bp'),
    ('tasks', 'tasks_bp'),
    ('proposals', 'proposals_bp'),
    ('contracts', 'contracts_bp'),
    ('automation', 'automation_bp'),
    ('telephony', 'telephony_bp'),
    ('pipeline', 'pipeline_bp'),
    ('chatbot', 'chatbot_bp')
]

# Importar cada blueprint
successful_imports = 0
for module_name, blueprint_name in blueprints_to_import:
    blueprint = safe_route_import(module_name, blueprint_name)
    if blueprint is not None:
        successful_imports += 1

print(f"📊 Importação concluída: {successful_imports}/{len(blueprints_to_import)} blueprints carregados")

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
    
    print(f"📊 Blueprints registrados: {registered_count}/{len(routes_registry)}")
    
    if registration_errors:
        print(f"⚠️  Erros de registro: {len(registration_errors)}")
        for error in registration_errors[:3]:  # Mostrar apenas os primeiros 3
            print(f"   • {error}")
        if len(registration_errors) > 3:
            print(f"   ... e mais {len(registration_errors) - 3} erros")
    
    return registered_count

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
                    'module': getattr(blueprint, 'import_name', 'unknown'),
                    'endpoints': len(getattr(blueprint, 'deferred_functions', []))
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
        'available_routes': get_available_routes()
    }

def print_routes_summary():
    """Imprime resumo detalhado das rotas"""
    print("\n" + "="*60)
    print("🛣️  RESUMO DAS ROTAS")
    print("="*60)
    
    status = get_route_status()
    
    print(f"📊 Estatísticas:")
    print(f"   • Total blueprints: {status['total_attempted']}")
    print(f"   • Carregados: {status['loaded_successfully']}")
    print(f"   • Registrados: {status['registered_successfully']}")
    print(f"   • Taxa de sucesso: {status['load_success_rate']}%")
    
    if status['loaded_successfully'] > 0:
        print(f"\n✅ ROTAS CARREGADAS ({status['loaded_successfully']}):")
        for route_name in status['routes_registry']:
            status_icon = "🟢" if route_name in status['registered_blueprints'] else "🟡"
            status_text = "registrada" if route_name in status['registered_blueprints'] else "carregada"
            print(f"   {status_icon} {route_name} ({status_text})")
    
    # Mostrar detalhes das rotas principais
    main_routes = ['leads_bp', 'dashboard_bp']
    available_main = [r for r in main_routes if r in status['routes_registry']]
    
    if available_main:
        print(f"\n🎯 ROTAS PRINCIPAIS DISPONÍVEIS:")
        for route in available_main:
            route_info = next((r for r in status['available_routes'] if r['name'] == route), {})
            prefix = route_info.get('prefix', 'N/A')
            print(f"   🚀 {route}: {prefix}")
    
    if import_errors:
        print(f"\n❌ ERROS DE IMPORTAÇÃO ({len(import_errors)}):")
        for error in import_errors[:3]:  # Mostrar apenas os primeiros 3
            print(f"   • {error}")
        if len(import_errors) > 3:
            print(f"   ... e mais {len(import_errors) - 3} erros")
    
    print("="*60 + "\n")

def get_endpoints_summary():
    """Retorna resumo dos endpoints disponíveis"""
    endpoints = {}
    
    for blueprint_name, blueprint in routes_registry.items():
        if blueprint and blueprint_name in registered_blueprints:
            prefix = getattr(blueprint, 'url_prefix', '/')
            
            # Mapeamento dos endpoints conhecidos
            endpoint_map = {
                'leads_bp': [
                    f"{prefix}/leads - GET/POST (Listar/Criar leads)",
                    f"{prefix}/leads/<id> - GET/PUT/DELETE (Gerenciar lead)",
                    f"{prefix}/tags - GET/POST (Gerenciar tags)",
                    f"{prefix}/lead-field-templates - GET/POST (Templates)"
                ],
                'dashboard_bp': [
                    f"{prefix}/overview - GET (Visão geral)",
                    f"{prefix}/sales-funnel - GET (Funil de vendas)",
                    f"{prefix}/team-performance - GET (Performance)",
                    f"{prefix}/kpis - GET (KPIs)",
                    f"{prefix}/charts/* - GET (Gráficos)"
                ]
            }
            
            if blueprint_name in endpoint_map:
                endpoints[blueprint_name] = endpoint_map[blueprint_name]
            else:
                endpoints[blueprint_name] = [f"{prefix}/* - Endpoints disponíveis"]
    
    return endpoints

# ==================== EXPORTAÇÕES ====================

# Exportar blueprints carregados
__all__ = list(routes_registry.keys()) + [
    'register_all_blueprints',
    'get_available_routes',
    'get_route_status',
    'get_endpoints_summary',
    'print_routes_summary',
    'routes_registry',
    'import_errors',
    'registered_blueprints'
]

# Executar resumo se chamado diretamente
if __name__ == "__main__":
    print_routes_summary()
else:
    # Mostrar resumo rápido quando importado
    status = get_route_status()
    main_routes_loaded = sum(1 for r in ['leads_bp', 'dashboard_bp'] if r in routes_registry)
    
    if main_routes_loaded == 2:
        print(f"🎉 Rotas principais carregadas: {main_routes_loaded}/2 - Sistema pronto!")
    elif main_routes_loaded > 0:
        print(f"✅ Rotas carregadas: {status['loaded_successfully']}/{status['total_attempted']} - {main_routes_loaded}/2 principais")
    else:
        print(f"⚠️  Rotas: {status['loaded_successfully']}/{status['total_attempted']} - Verificar dependências")
