from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from flasgger import Swagger # Importar Swagger

# Importar modelos
from src.models.user import db
from src.models.lead import Lead, Tag
from src.models.pipeline import Pipeline, PipelineStage, Opportunity
from src.models.proposal import ProposalTemplate, Proposal
from src.models.contract import ContractTemplate, Contract, ContractAmendment
from src.models.chatbot import ChatFlow, ChatConversation, ChatMessage, ChatIntegration, ChatAIConfig
from src.models.telephony import Call, CallLog
from src.models.tenant import Tenant, TenantSubscription, TenantUsageLog, TenantInvitation
from src.models.automation import AutomationRule, AutomationAction, AutomationExecution, EmailCampaign, CadenceSequence, CadenceStep, CadenceEnrollment
from src.models.task import Task, TaskComment, TaskTimeLog, TaskTemplate, ActivitySummary

# Importar rotas
from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.routes.leads import leads_bp
from src.routes.pipelines import pipelines_bp
from src.routes.dashboard import dashboard_bp
from src.routes.proposals import proposals_bp
from src.routes.contracts import contracts_bp
from src.routes.chatbot import chatbot_bp
from src.routes.telephony import telephony_bp
from src.routes.automation import automation_bp
from src.routes.tasks import task_bp
from src.routes.tenant_admin import super_admin_bp, tenant_admin_bp

# Importar middleware
from src.middleware.tenant_middleware import TenantMiddleware

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://crm_user:crm_password@localhost/crm_jttelcom"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "jwt-secret-string-change-in-production"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    
    # Configuração do Swagger
    app.config["SWAGGER"] = {
        "title": "JT Telecom CRM API",
        "uiversion": 3,
        "specs_route": "/apidocs/",
        "host": "www.api.app.jttecnologia.com.br"
    }
    Swagger(app) # Inicializar Swagger
    
    # Inicializar extensões
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Inicializar middleware de tenant
    TenantMiddleware(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(leads_bp, url_prefix="/api/leads")
    app.register_blueprint(pipelines_bp, url_prefix="/api/pipelines")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(proposals_bp, url_prefix="/api/proposals")
    app.register_blueprint(contracts_bp, url_prefix="/api/contracts")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    app.register_blueprint(telephony_bp, url_prefix="/api/telephony")
    app.register_blueprint(automation_bp, url_prefix="/api/automations")
    app.register_blueprint(task_bp, url_prefix="/api/tasks")
    app.register_blueprint(super_admin_bp, url_prefix="/api/super-admin")
    app.register_blueprint(tenant_admin_bp, url_prefix="/api/tenant-admin")
    
    # Rota de health check
    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "CRM JT Telecom API is running",
            "modules": [
                "Authentication",
                "Users",
                "Leads",
                "Pipelines",
                "Dashboard",
                "Proposals",
                "Contracts",
                "Chatbot",
                "Telephony",
                "Automations",
                "Tasks",
                "Tenant Management"
            ]
        })
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


