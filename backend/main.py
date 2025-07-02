import os
import sys
# DON'T CHANGE: Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

# Importar modelos
from models import db, User, Tenant

# Importar blueprints
from routes.auth import auth_bp
from routes.system import system_bp
from routes.leads import leads_bp
from routes.pipelines import pipelines_bp
from routes.dashboard import dashboard_bp
from routes.tasks import tasks_bp
from routes.proposals import proposals_bp
from routes.clients import clients_bp
from routes.contracts import contracts_bp
from routes.chatbot import chatbot_bp
from routes.telephony import telephony_bp
from routes.automation import automation_bp
from routes.master import master_bp
from routes.tenant_admin import tenant_admin_bp

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['JWT_ALGORITHM'] = 'HS256'
    
    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///crm_multitenant.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    CORS(app, origins="*")
    jwt = JWTManager(app)
    
    # Configurar handlers JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expirado'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Token inválido'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Token de autorização necessário'}), 401
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(system_bp, url_prefix='/system')
    app.register_blueprint(leads_bp, url_prefix='/leads')
    app.register_blueprint(pipelines_bp, url_prefix='/pipelines')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(proposals_bp, url_prefix='/proposals')
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(contracts_bp, url_prefix='/contracts')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(telephony_bp, url_prefix='/telephony')
    app.register_blueprint(automation_bp, url_prefix='/automation')
    app.register_blueprint(master_bp, url_prefix='/master')
    app.register_blueprint(tenant_admin_bp, url_prefix='/tenant-admin')
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
        
        # Verificar se Admin Master existe, se não, criar
        existing_master = User.query.filter_by(user_level='master').first()
        if not existing_master:
            master_user = User(
                name='Admin Master JT Telecom',
                email='master@jttecnologia.com.br',
                user_level='master',
                status='active'
            )
            master_user.set_password('MasterJT2024!')
            db.session.add(master_user)
            db.session.commit()
            print("✅ Admin Master criado: master@jttecnologia.com.br / MasterJT2024!")
    
    # Rota raiz
    @app.route('/')
    def home():
        return jsonify({
            "message": "CRM JT Telecom Multi-Tenant API",
            "version": "2.0.0",
            "status": "running",
            "architecture": "multi-tenant",
            "endpoints": {
                "auth": "/auth/*",
                "master": "/master/*",
                "tenant_admin": "/tenant-admin/*",
                "system": "/system/*",
                "leads": "/leads/*",
                "clients": "/clients/*",
                "dashboard": "/dashboard/*",
                "documentation": "/apidocs/"
            }
        })
    
    # Rota de health check
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "multi_tenant": "enabled"
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

