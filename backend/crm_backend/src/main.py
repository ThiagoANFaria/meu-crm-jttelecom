from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import os

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/crm')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    CORS(app)
    jwt = JWTManager(app)
    
    # Rota de health check
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'CRM JT Telecom API está funcionando',
            'version': '1.0.0'
        }), 200
    
    # Rota raiz
    @app.route('/', methods=['GET'])
    def root():
        """Rota raiz da API"""
        return jsonify({
            'message': 'Bem-vindo à API do CRM JT Telecom',
            'version': '1.0.0',
            'documentation': '/apidocs/',
            'health': '/health'
        }), 200
    
    # Inicializar banco de dados
    try:
        from src.models import init_db
        init_db(app)
        print("✅ Banco de dados inicializado")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar banco: {e}")
    
    # Registrar blueprints PRIMEIRO
    try:
        from src.routes import register_blueprints
        registered = register_blueprints(app)
        print(f"✅ {registered} blueprints registrados")
    except Exception as e:
        print(f"⚠️ Erro ao registrar rotas: {e}")
    
    # Configurar Swagger DEPOIS dos blueprints - VERSÃO SIMPLIFICADA
    try:
        # Configuração mínima do Swagger
        swagger_config = {
            "swagger_ui": True,
            "specs_route": "/apidocs/"
        }
        
        # Template básico
        swagger_template = {
            "swagger": "2.0",
            "info": {
                "title": "CRM JT Telecom API",
                "description": "API do Sistema de CRM da JT Telecom",
                "version": "1.0.0"
            },
            "host": os.getenv('SWAGGER_HOST', 'api.app.jttecnologia.com.br'),
            "basePath": "/",
            "schemes": ["https", "http"]
        }
        
        swagger = Swagger(app, config=swagger_config, template=swagger_template)
        print("✅ Swagger básico inicializado com sucesso")
        
    except Exception as e:
        print(f"⚠️ Erro ao inicializar Swagger: {e}")
        # Sem Swagger como último recurso
        print("⚠️ Continuando sem Swagger")
    
    # Inicializar serviços
    try:
        from src.services import init_services
        init_services()
        print("✅ Serviços inicializados")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar serviços: {e}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Configurações do servidor
    host = '0.0.0.0'
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🚀 Iniciando CRM JT Telecom API")
    print(f"📍 Host: {host}:{port}")
    print(f"🔧 Debug: {debug}")
    print(f"📚 Documentação: http://{host}:{port}/apidocs/")
    
    app.run(host=host, port=port, debug=debug)

