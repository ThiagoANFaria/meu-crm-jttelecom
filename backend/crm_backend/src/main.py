# main.py - Arquivo principal do CRM JT Tecnologia
import sys
import os

# Adicionar o diretório atual ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    print("🚀 Iniciando CRM JT Tecnologia...")
    
    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Inicializar extensões
    CORS(app)
    print("✅ CORS inicializado")
    
    # Inicializar banco de dados
    db_success = init_database(app)
    
    # Registrar blueprints (rotas)
    routes_count = register_blueprints(app)
    
    # Rotas básicas
    register_basic_routes(app)
    
    # Handlers de erro
    register_error_handlers(app)
    
    print(f"📊 Status: DB={db_success}, Rotas={routes_count}")
    print("✅ Aplicação configurada com sucesso!")
    
    return app

def init_database(app):
    """Inicializa o banco de dados"""
    try:
        print("🔧 Inicializando banco de dados...")
        
        # Tentar importar modelos
        from src.models import init_database
        
        success = init_database(app)
        
        if success:
            print("✅ Banco de dados inicializado com sucesso!")
        else:
            print("⚠️  Banco inicializado com avisos")
            
        return success
        
    except ImportError as e:
        print(f"❌ Erro ao importar modelos: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

def register_blueprints(app):
    """Registra todos os blueprints da aplicação"""
    try:
        print("🛣️  Registrando rotas...")
        
        # Tentar importar e registrar blueprints
        from src.routes import register_all_blueprints
        
        routes_count = register_all_blueprints(app)
        return routes_count
        
    except ImportError as e:
        print(f"⚠️  Erro ao importar rotas: {e}")
        return 0
    except Exception as e:
        print(f"❌ Erro ao registrar blueprints: {e}")
        return 0

def register_basic_routes(app):
    """Registra rotas básicas do sistema"""
    
    @app.route('/')
    def home():
        # Tentar obter informações das rotas
        try:
            from src.routes import get_available_routes
            available_routes = get_available_routes()
        except:
            available_routes = []
        
        return jsonify({
            "message": "🚀 CRM JT Tecnologia API está funcionando!",
            "version": "1.0.0",
            "status": "online",
            "features": [
                "Gestão de Leads",
                "Pipeline de Vendas", 
                "Propostas Automáticas",
                "Contratos Digitais",
                "Chatbot Inteligente",
                "Automações de Marketing",
                "Telefonia Integrada"
            ],
            "available_routes": available_routes,
            "endpoints": {
                "health": "/health",
                "db_test": "/db-test",
                "models": "/api/models",
                "leads": "/api/leads",
                "dashboard": "/api/dashboard"
            },
            "database": "PostgreSQL conectado ✅"
        })
    
    @app.route('/health')
    def health_check():
        """Health check da API"""
        try:
            # Testar conexão com banco se disponível
            try:
                from src.models import db
                if db:
                    db.session.execute('SELECT 1')
                    db_status = "connected"
                else:
                    db_status = "not_initialized"
            except Exception as e:
                db_status = f"error: {str(e)}"
        except ImportError:
            db_status = "models_not_available"
        
        return jsonify({
            "status": "healthy" if "connected" in db_status else "partial",
            "database": db_status,
            "timestamp": "2024-12-20T15:30:00Z"
        })
    
    @app.route('/api/info')
    def api_info():
        """Informações da API"""
        return jsonify({
            "api_name": "CRM JT Tecnologia",
            "version": "1.0.0",
            "description": "Sistema CRM completo com automações, chatbot e telefonia",
            "technologies": {
                "backend": "Flask + SQLAlchemy",
                "database": "PostgreSQL",
                "deployment": "EasyPanel + GitHub Actions"
            },
            "developer": "JT Tecnologia",
            "contact": "contato@jttecnologia.com.br"
        })
    
    @app.route('/api/models')
    def list_models():
        """Lista todos os modelos disponíveis"""
        try:
            from src.models import validate_models
            
            validation = validate_models()
            return jsonify(validation)
            
        except ImportError as e:
            return jsonify({
                "error": f"Erro ao importar modelos: {str(e)}",
                "total_models": 0,
                "loaded_models": 0
            })
    
    @app.route('/db-test')
    def db_test():
        """Teste de conexão com PostgreSQL"""
        try:
            DATABASE_URL = os.getenv('DATABASE_URL')
            
            if not DATABASE_URL:
                return jsonify({
                    "status": "error",
                    "message": "❌ DATABASE_URL não configurada"
                }), 500
            
            # Conectar ao banco
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            # Executar query simples
            cursor.execute('SELECT version();')
            version = cursor.fetchone()[0]
            
            # Contar tabelas existentes
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            table_count = cursor.fetchone()[0]
            
            # Fechar conexão
            cursor.close()
            conn.close()
            
            return jsonify({
                "status": "success",
                "message": "✅ Conexão com PostgreSQL realizada com sucesso!",
                "database_version": version,
                "tables_count": table_count,
                "connection_info": "Connected successfully"
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"❌ Erro ao conectar ao banco: {str(e)}"
            }), 500

def register_error_handlers(app):
    """Registra handlers de erro globais"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint não encontrado",
            "message": "Verifique a URL e tente novamente",
            "available_endpoints": [
                "/",
                "/health", 
                "/api/info",
                "/api/models",
                "/api/leads",
                "/api/dashboard",
                "/db-test"
            ]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "message": "Entre em contato com o suporte"
        }), 500

if __name__ == '__main__':
    app = create_app()
    
    # Configurações de desenvolvimento
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    print("="*50)
    print("🚀 CRM JT TECNOLOGIA")
    print("="*50)
    print(f"🌐 Porta: {port}")
    print(f"📊 Debug: {debug_mode}")
    print(f"🔗 URL: http://localhost:{port}")
    print("="*50)
    
    app.run(
        debug=debug_mode, 
        host='0.0.0.0', 
        port=port
    )
