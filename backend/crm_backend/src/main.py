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
    
    # Configurar Swagger DEPOIS dos blueprints
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "uiversion": 3
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "CRM JT Telecom API",
            "description": "API do Sistema de CRM da JT Telecom",
            "version": "1.0.0",
            "contact": {
                "email": "suporte@jttelecom.com.br"
            }
        },
        "host": os.getenv('SWAGGER_HOST', 'api.app.jttecnologia.com.br'),
        "basePath": "/",
        "schemes": ["https", "http"],
        "definitions": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "is_active": {"type": "boolean"}
                }
            },
            "UserCreate": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"}
                },
                "required": ["email", "password", "first_name", "last_name"]
            },
            "UserLogin": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["email", "password"]
            },
            "Lead": {
                "type": "object", 
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "status": {"type": "string"},
                    "source": {"type": "string"},
                    "score": {"type": "integer"}
                }
            },
            "LeadCreate": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "source": {"type": "string"}
                },
                "required": ["name", "email"]
            },
            "Pipeline": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "stages": {"type": "array", "items": {"$ref": "#/definitions/PipelineStage"}}
                }
            },
            "PipelineStage": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "order": {"type": "integer"},
                    "color": {"type": "string"}
                }
            },
            "Task": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {"type": "string"},
                    "priority": {"type": "string"},
                    "due_date": {"type": "string", "format": "date-time"}
                }
            },
            "Automation": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "trigger": {"type": "string"},
                    "actions": {"type": "array"}
                }
            },
            "Call": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "phone": {"type": "string"},
                    "duration": {"type": "integer"},
                    "status": {"type": "string"},
                    "recording_url": {"type": "string"}
                }
            },
            "Contract": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "value": {"type": "number"},
                    "status": {"type": "string"},
                    "start_date": {"type": "string", "format": "date"}
                }
            },
            "Proposal": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "value": {"type": "number"},
                    "status": {"type": "string"},
                    "valid_until": {"type": "string", "format": "date"}
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "message": {"type": "string"}
                }
            },
            "Success": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "data": {"type": "object"}
                }
            }
        }
    }
    
    # Inicializar Swagger DEPOIS dos blueprints
    try:
        swagger = Swagger(app, config=swagger_config, template=swagger_template)
        print("✅ Swagger inicializado com sucesso")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar Swagger: {e}")
        # Swagger básico como fallback
        try:
            basic_config = {"swagger_ui": True, "specs_route": "/apidocs/"}
            swagger = Swagger(app, config=basic_config)
            print("✅ Swagger básico inicializado como fallback")
        except Exception as e2:
            print(f"❌ Erro crítico no Swagger: {e2}")
    
    # Adicionar rota de teste para apispec
    @app.route('/apispec.json', methods=['GET'])
    def get_apispec():
        """Endpoint para obter especificação da API"""
        try:
            return jsonify({
                "swagger": "2.0",
                "info": {
                    "title": "CRM JT Telecom API",
                    "version": "1.0.0"
                },
                "host": os.getenv('SWAGGER_HOST', 'api.app.jttecnologia.com.br'),
                "basePath": "/",
                "schemes": ["https", "http"],
                "paths": {},
                "definitions": {}
            })
        except Exception as e:
            return jsonify({"error": "Erro ao gerar especificação", "message": str(e)}), 500
    
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

