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
    
    # Documentação básica sem Swagger (temporário)
    @app.route('/apidocs/')
    def api_docs():
        """Documentação básica da API"""
        docs_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CRM JT Telecom API - Documentação</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .method { color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
                .get { background: #61affe; }
                .post { background: #49cc90; }
                .put { background: #fca130; }
                .delete { background: #f93e3e; }
            </style>
        </head>
        <body>
            <h1>🚀 CRM JT Telecom API</h1>
            <p><strong>Versão:</strong> 1.0.0</p>
            <p><strong>Base URL:</strong> https://api.app.jttecnologia.com.br</p>
            
            <h2>📋 Módulos Disponíveis</h2>
            
            <div class="endpoint">
                <h3>🔐 Autenticação (/auth)</h3>
                <p><span class="method post">POST</span> /auth/login - Login de usuário</p>
                <p><span class="method post">POST</span> /auth/register - Registro de usuário</p>
                <p><span class="method post">POST</span> /auth/logout - Logout de usuário</p>
            </div>
            
            <div class="endpoint">
                <h3>👥 Leads (/leads)</h3>
                <p><span class="method get">GET</span> /leads - Listar leads</p>
                <p><span class="method post">POST</span> /leads - Criar lead</p>
                <p><span class="method get">GET</span> /leads/{id} - Obter lead específico</p>
                <p><span class="method put">PUT</span> /leads/{id} - Atualizar lead</p>
                <p><span class="method delete">DELETE</span> /leads/{id} - Deletar lead</p>
            </div>
            
            <div class="endpoint">
                <h3>🔄 Pipelines (/pipelines)</h3>
                <p><span class="method get">GET</span> /pipelines - Listar pipelines</p>
                <p><span class="method post">POST</span> /pipelines - Criar pipeline</p>
                <p><span class="method get">GET</span> /pipelines/{id} - Obter pipeline específico</p>
                <p><span class="method put">PUT</span> /pipelines/{id} - Atualizar pipeline</p>
            </div>
            
            <div class="endpoint">
                <h3>✅ Tarefas (/tasks)</h3>
                <p><span class="method get">GET</span> /tasks - Listar tarefas</p>
                <p><span class="method post">POST</span> /tasks - Criar tarefa</p>
                <p><span class="method get">GET</span> /tasks/{id} - Obter tarefa específica</p>
                <p><span class="method put">PUT</span> /tasks/{id} - Atualizar tarefa</p>
            </div>
            
            <div class="endpoint">
                <h3>🤖 Automação (/automation)</h3>
                <p><span class="method get">GET</span> /automation/workflows - Listar workflows</p>
                <p><span class="method post">POST</span> /automation/workflows - Criar workflow</p>
                <p><span class="method post">POST</span> /automation/trigger - Disparar automação</p>
            </div>
            
            <div class="endpoint">
                <h3>📞 Telefonia (/telephony)</h3>
                <p><span class="method post">POST</span> /telephony/call - Fazer chamada</p>
                <p><span class="method get">GET</span> /telephony/calls - Listar chamadas</p>
                <p><span class="method get">GET</span> /telephony/recordings - Listar gravações</p>
            </div>
            
            <div class="endpoint">
                <h3>💬 Chatbot (/chatbot)</h3>
                <p><span class="method post">POST</span> /chatbot/message - Enviar mensagem</p>
                <p><span class="method get">GET</span> /chatbot/conversations - Listar conversas</p>
            </div>
            
            <div class="endpoint">
                <h3>📊 Dashboard (/dashboard)</h3>
                <p><span class="method get">GET</span> /dashboard/stats - Estatísticas gerais</p>
                <p><span class="method get">GET</span> /dashboard/charts - Dados para gráficos</p>
            </div>
            
            <div class="endpoint">
                <h3>📄 Contratos (/contracts)</h3>
                <p><span class="method get">GET</span> /contracts - Listar contratos</p>
                <p><span class="method post">POST</span> /contracts - Criar contrato</p>
                <p><span class="method get">GET</span> /contracts/{id} - Obter contrato específico</p>
            </div>
            
            <h2>🔧 Endpoints de Sistema</h2>
            <div class="endpoint">
                <p><span class="method get">GET</span> / - Informações da API</p>
                <p><span class="method get">GET</span> /health - Status de saúde</p>
                <p><span class="method get">GET</span> /apidocs/ - Esta documentação</p>
            </div>
            
            <hr>
            <p><em>Documentação gerada automaticamente - CRM JT Telecom v1.0.0</em></p>
        </body>
        </html>
        """
        return docs_html
    
    # Endpoint para especificação JSON básica
    @app.route('/apispec.json')
    def api_spec():
        """Especificação básica da API em JSON"""
        return jsonify({
            "openapi": "3.0.0",
            "info": {
                "title": "CRM JT Telecom API",
                "description": "API do Sistema de CRM da JT Telecom",
                "version": "1.0.0"
            },
            "servers": [
                {"url": "https://api.app.jttecnologia.com.br", "description": "Servidor de Produção"}
            ],
            "paths": {
                "/": {"get": {"summary": "Informações da API"}},
                "/health": {"get": {"summary": "Status de saúde"}},
                "/auth/login": {"post": {"summary": "Login de usuário"}},
                "/auth/register": {"post": {"summary": "Registro de usuário"}},
                "/leads": {"get": {"summary": "Listar leads"}, "post": {"summary": "Criar lead"}},
                "/pipelines": {"get": {"summary": "Listar pipelines"}, "post": {"summary": "Criar pipeline"}},
                "/tasks": {"get": {"summary": "Listar tarefas"}, "post": {"summary": "Criar tarefa"}},
                "/automation/workflows": {"get": {"summary": "Listar workflows"}, "post": {"summary": "Criar workflow"}},
                "/telephony/call": {"post": {"summary": "Fazer chamada"}},
                "/chatbot/message": {"post": {"summary": "Enviar mensagem"}},
                "/dashboard/stats": {"get": {"summary": "Estatísticas gerais"}},
                "/contracts": {"get": {"summary": "Listar contratos"}, "post": {"summary": "Criar contrato"}}
            }
        })
    
    print("✅ Documentação básica configurada (sem Swagger)")
    
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

