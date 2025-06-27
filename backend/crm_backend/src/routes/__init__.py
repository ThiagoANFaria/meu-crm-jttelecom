"""
Módulo de rotas do CRM JT Telecom
Centraliza todas as importações e configurações das rotas
"""

from flask import Blueprint

# Importar todos os blueprints
try:
    from .auth import auth_bp
    print("✅ Blueprint auth importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar auth blueprint: {e}")
    auth_bp = None

try:
    from .user import user_bp
    print("✅ Blueprint user importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar user blueprint: {e}")
    user_bp = None

try:
    from .leads import leads_bp
    print("✅ Blueprint leads importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar leads blueprint: {e}")
    leads_bp = None

try:
    from .pipelines import pipelines_bp
    print("✅ Blueprint pipelines importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar pipelines blueprint: {e}")
    pipelines_bp = None

try:
    from .dashboard import dashboard_bp
    print("✅ Blueprint dashboard importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar dashboard blueprint: {e}")
    dashboard_bp = None

try:
    from .proposals import proposals_bp
    print("✅ Blueprint proposals importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar proposals blueprint: {e}")
    proposals_bp = None

try:
    from .contracts import contracts_bp
    print("✅ Blueprint contracts importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar contracts blueprint: {e}")
    contracts_bp = None

try:
    from .chatbot import chatbot_bp
    print("✅ Blueprint chatbot importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar chatbot blueprint: {e}")
    chatbot_bp = None

try:
    from .telephony import telephony_bp
    print("✅ Blueprint telephony importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar telephony blueprint: {e}")
    telephony_bp = None

try:
    from .automation import automation_bp
    print("✅ Blueprint automation importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar automation blueprint: {e}")
    automation_bp = None

try:
    from .tasks import task_bp
    print("✅ Blueprint tasks importado")
except ImportError as e:
    print(f"⚠️ Erro ao importar tasks blueprint: {e}")
    task_bp = None

try:
    from .tenant_admin import super_admin_bp, tenant_admin_bp
    print("✅ Blueprints tenant_admin importados")
except ImportError as e:
    print(f"⚠️ Erro ao importar tenant_admin blueprints: {e}")
    super_admin_bp = None
    tenant_admin_bp = None

def register_blueprints(app):
    """Registra todos os blueprints na aplicação Flask"""
    blueprints = [
        (auth_bp, "/api/auth"),
        (user_bp, "/api/users"),
        (leads_bp, "/api/leads"),
        (pipelines_bp, "/api/pipelines"),
        (dashboard_bp, "/api/dashboard"),
        (proposals_bp, "/api/proposals"),
        (contracts_bp, "/api/contracts"),
        (chatbot_bp, "/api/chatbot"),
        (telephony_bp, "/api/telephony"),
        (automation_bp, "/api/automations"),
        (task_bp, "/api/tasks"),
        (super_admin_bp, "/api/super-admin"),
        (tenant_admin_bp, "/api/tenant-admin")
    ]
    
    registered_count = 0
    for blueprint, url_prefix in blueprints:
        if blueprint is not None:
            try:
                app.register_blueprint(blueprint, url_prefix=url_prefix)
                print(f"✅ Blueprint registrado: {blueprint.name} em {url_prefix}")
                registered_count += 1
            except Exception as e:
                print(f"⚠️ Erro ao registrar blueprint {blueprint.name}: {e}")
        else:
            print(f"⚠️ Blueprint não disponível para {url_prefix}")
    
    print(f"✅ Total de blueprints registrados: {registered_count}")
    return registered_count

