# src/routes/__init__.py
"""
Módulo de rotas do CRM
Centraliza a importação de todos os blueprints
"""

# Tentar importar todas as rotas disponíveis
try:
    from .leads import leads_bp
    print("✅ Blueprint de leads importado")
except ImportError as e:
    print(f"⚠️  Erro ao importar leads blueprint: {e}")
    leads_bp = None

try:
    from .dashboard import dashboard_bp
    print("✅ Blueprint de dashboard importado")
except ImportError as e:
    print(f"⚠️  Erro ao importar dashboard blueprint: {e}")
    dashboard_bp = None

try:
    from .opportunities import opportunities_bp
    print("✅ Blueprint de opportunities importado")
except ImportError as e:
    print(f"⚠️  Erro ao importar opportunities blueprint: {e}")
    opportunities_bp = None

try:
    from .tasks import tasks_bp
    print("✅ Blueprint de tasks importado")
except ImportError as e:
    print(f"⚠️  Erro ao importar tasks blueprint: {e}")
    tasks_bp = None

try:
    from .proposals import proposals_bp
    print("✅ Blueprint de proposals importado")
except ImportError as e:
    print(f"⚠️  Erro ao importar proposals blueprint: {e}")
    proposals_bp = None

try:
    from .contracts import contracts_bp
    print("✅ Blueprint de contracts importado")
except ImportError as e:
    print(f"⚠️  Erro ao importar contracts blueprint: {e}")
    contracts_bp = None

# Lista de blueprints disponíveis
available_blueprints = [
    ('leads', leads_bp),
    ('dashboard', dashboard_bp),
    ('opportunities', opportunities_bp),
    ('tasks', tasks_bp),
    ('proposals', proposals_bp),
    ('contracts', contracts_bp)
]

# Filtrar apenas blueprints que foram importados com sucesso
active_blueprints = [(name, bp) for name, bp in available_blueprints if bp is not None]

def register_all_blueprints(app):
    """Registra todos os blueprints disponíveis na aplicação"""
    registered_count = 0
    
    for name, blueprint in active_blueprints:
        try:
            app.register_blueprint(blueprint)
            print(f"✅ Blueprint '{name}' registrado com sucesso")
            registered_count += 1
        except Exception as e:
            print(f"❌ Erro ao registrar blueprint '{name}': {e}")
    
    print(f"📊 Total de blueprints registrados: {registered_count}/{len(available_blueprints)}")
    return registered_count

def get_available_routes():
    """Retorna lista de rotas disponíveis"""
    routes = []
    
    for name, blueprint in active_blueprints:
        if blueprint:
            routes.append({
                'name': name,
                'prefix': getattr(blueprint, 'url_prefix', '/'),
                'status': 'active'
            })
    
    return routes

# Exportar blueprints para facilitar importação
__all__ = [
    'leads_bp',
    'dashboard_bp', 
    'opportunities_bp',
    'tasks_bp',
    'proposals_bp',
    'contracts_bp',
    'register_all_blueprints',
    'get_available_routes',
    'active_blueprints'
]
