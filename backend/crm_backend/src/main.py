import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

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
    
    # Documentação interativa com Swagger UI
    @app.route('/apidocs/')
    def api_docs():
        """Documentação interativa da API com Swagger UI"""
        swagger_ui_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CRM JT Telecom API - Documentação Interativa</title>
            <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
            <style>
                html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
                *, *:before, *:after { box-sizing: inherit; }
                body { margin:0; background: #fafafa; }
                .swagger-ui .topbar { display: none; }
                .swagger-ui .info { margin: 20px 0; }
                .swagger-ui .info .title { color: #3b4151; font-size: 36px; }
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
            <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
            <script>
                window.onload = function() {
                    const ui = SwaggerUIBundle({
                        url: '/apispec.json',
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        plugins: [
                            SwaggerUIBundle.plugins.DownloadUrl
                        ],
                        layout: "StandaloneLayout",
                        tryItOutEnabled: true,
                        supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                        onComplete: function() {
                            console.log("Swagger UI carregado com sucesso!");
                        },
                        onFailure: function(data) {
                            console.error("Erro ao carregar Swagger UI:", data);
                        }
                    });
                };
            </script>
        </body>
        </html>
        """
        return swagger_ui_html
    
    # Endpoint para especificação JSON completa do Swagger
    @app.route('/apispec.json')
    def api_spec():
        """Especificação completa da API em formato OpenAPI 3.0"""
        from src.swagger_spec import get_swagger_spec
        return jsonify(get_swagger_spec())
    
    print("✅ Documentação interativa Swagger UI configurada")
    
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

