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
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        logger.info("✅ Blueprint auth registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar auth: {e}")
    
    try:
        # Importar e registrar blueprint de usuários
        from .user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/users')
        logger.info("✅ Blueprint user registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar user: {e}")
    
    try:
        # Importar e registrar blueprint de leads
        from .leads import leads_bp
        app.register_blueprint(leads_bp, url_prefix='/api/leads')
        logger.info("✅ Blueprint leads registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar leads: {e}")
    
    try:
        # Importar e registrar blueprint de pipelines
        from .pipelines import pipelines_bp
        app.register_blueprint(pipelines_bp, url_prefix='/api/pipelines')
        logger.info("✅ Blueprint pipelines registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar pipelines: {e}")
    
    try:
        # Importar e registrar blueprint de dashboard
        from .dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
        logger.info("✅ Blueprint dashboard registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar dashboard: {e}")
    
    try:
        # Importar e registrar blueprint de propostas
        from .proposals import proposals_bp
        app.register_blueprint(proposals_bp, url_prefix='/api/proposals')
        logger.info("✅ Blueprint proposals registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar proposals: {e}")
    
    try:
        # Importar e registrar blueprint de contratos
        from .contracts import contracts_bp
        app.register_blueprint(contracts_bp, url_prefix='/api/contracts')
        logger.info("✅ Blueprint contracts registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar contracts: {e}")
    
    try:
        # Importar e registrar blueprint de chatbot
        from .chatbot import chatbot_bp
        app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
        logger.info("✅ Blueprint chatbot registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar chatbot: {e}")
    
    try:
        # Importar e registrar blueprint de telefonia
        from .telephony import telephony_bp
        app.register_blueprint(telephony_bp, url_prefix='/api/telephony')
        logger.info("✅ Blueprint telephony registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar telephony: {e}")
    
    try:
        # Importar e registrar blueprint de automação
        from .automation import automation_bp
        app.register_blueprint(automation_bp, url_prefix='/api/automation')
        logger.info("✅ Blueprint automation registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar automation: {e}")
    
    try:
        # Importar e registrar blueprint de tarefas
        from .tasks import tasks_bp
        app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
        logger.info("✅ Blueprint tasks registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar tasks: {e}")
    
    try:
        # Importar e registrar blueprint de admin tenant
        from .tenant_admin import tenant_admin_bp
        app.register_blueprint(tenant_admin_bp, url_prefix='/api/admin')
        logger.info("✅ Blueprint tenant_admin registrado")
        registered_count += 1
    except Exception as e:
        logger.error(f"❌ Erro ao registrar tenant_admin: {e}")
    
    logger.info(f"🎉 Total de blueprints registrados: {registered_count}")
    return registered_count

# Alias para compatibilidade
register_all_blueprints = register_blueprints

