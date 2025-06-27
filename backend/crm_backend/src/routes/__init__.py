"""
Módulo de rotas do CRM JT Telecom
"""
import logging

logger = logging.getLogger(__name__)

def register_blueprints(app):
    """Registra todos os blueprints da aplicação"""
    registered_count = 0
    
    try:
        # Importar e registrar blueprint de autenticação
        from .auth import auth_bp
        app.register_blueprint(auth_bp)
        logger.info("✅ Blueprint auth registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar auth: {e}")
    
    try:
        # Importar e registrar blueprint de usuários
        from .user import user_bp
        app.register_blueprint(user_bp)
        logger.info("✅ Blueprint user registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar user: {e}")
    
    try:
        # Importar e registrar blueprint de leads
        from .leads import leads_bp
        app.register_blueprint(leads_bp)
        logger.info("✅ Blueprint leads registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar leads: {e}")
    
    try:
        # Importar e registrar blueprint de pipelines
        from .pipelines import pipelines_bp
        app.register_blueprint(pipelines_bp)
        logger.info("✅ Blueprint pipelines registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar pipelines: {e}")
    
    try:
        # Importar e registrar blueprint de dashboard
        from .dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp)
        logger.info("✅ Blueprint dashboard registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar dashboard: {e}")
    
    try:
        # Importar e registrar blueprint de propostas
        from .proposals import proposals_bp
        app.register_blueprint(proposals_bp)
        logger.info("✅ Blueprint proposals registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar proposals: {e}")
    
    try:
        # Importar e registrar blueprint de contratos
        from .contracts import contracts_bp
        app.register_blueprint(contracts_bp)
        logger.info("✅ Blueprint contracts registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar contracts: {e}")
    
    try:
        # Importar e registrar blueprint de chatbot
        from .chatbot import chatbot_bp
        app.register_blueprint(chatbot_bp)
        logger.info("✅ Blueprint chatbot registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar chatbot: {e}")
    
    try:
        # Importar e registrar blueprint de telefonia
        from .telephony import telephony_bp
        app.register_blueprint(telephony_bp)
        logger.info("✅ Blueprint telephony registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar telephony: {e}")
    
    try:
        # Importar e registrar blueprint de automação
        from .automation import automation_bp
        app.register_blueprint(automation_bp)
        logger.info("✅ Blueprint automation registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar automation: {e}")
    
    try:
        # Importar e registrar blueprint de tarefas
        from .tasks import tasks_bp
        app.register_blueprint(tasks_bp)
        logger.info("✅ Blueprint tasks registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar tasks: {e}")
    
    try:
        # Importar e registrar blueprint de admin tenant
        from .tenant_admin import tenant_admin_bp
        app.register_blueprint(tenant_admin_bp)
        logger.info("✅ Blueprint tenant_admin registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar tenant_admin: {e}")
    
    logger.info(f"🎉 Total de blueprints registrados: {registered_count}")
    return registered_count

# Alias para compatibilidade
register_all_blueprints = register_blueprints


def get_available_routes():
    """Retorna lista de rotas disponíveis"""
    routes = [
        {'path': '/auth', 'methods': ['GET', 'POST'], 'description': 'Autenticação'},
        {'path': '/leads', 'methods': ['GET', 'POST'], 'description': 'Gestão de leads'},
        {'path': '/pipelines', 'methods': ['GET', 'POST'], 'description': 'Funis de vendas'},
        {'path': '/dashboard', 'methods': ['GET'], 'description': 'Dashboard'},
        {'path': '/contracts', 'methods': ['GET', 'POST'], 'description': 'Contratos'},
        {'path': '/chatbot', 'methods': ['GET', 'POST'], 'description': 'Chatbot'},
        {'path': '/telephony', 'methods': ['GET', 'POST'], 'description': 'Telefonia'},
        {'path': '/automation', 'methods': ['GET', 'POST'], 'description': 'Automação'},
        {'path': '/tasks', 'methods': ['GET', 'POST'], 'description': 'Tarefas'},
        {'path': '/users', 'methods': ['GET', 'POST'], 'description': 'Usuários'},
        {'path': '/admin', 'methods': ['GET', 'POST'], 'description': 'Administração'},
        {'path': '/proposals', 'methods': ['GET', 'POST'], 'description': 'Propostas'}
    ]
    return routes

