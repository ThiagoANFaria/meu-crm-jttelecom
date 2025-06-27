# main.py - Sistema CRM JT Tecnologia com tratamento robusto de erros
import sys
import os
import traceback
from datetime import datetime

# Adicionar o diretório atual ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2

# Carregar variáveis de ambiente
load_dotenv()

# Controle global de inicialização
SYSTEM_STATUS = {
    'app_created': False,
    'db_initialized': False,
    'routes_registered': False,
    'startup_time': None,
    'errors': [],
    'warnings': []
}

def log_system_event(event_type: str, message: str, is_error: bool = False):
    """Log de eventos do sistema"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if is_error:
        SYSTEM_STATUS['errors'].append(f"[{timestamp}] {message}")
        print(f"❌ [{timestamp}] {message}")
    else:
        print(f"✅ [{timestamp}] {message}")

def create_app():
    """Factory function para criar a aplicação Flask com tratamento de erros"""
    startup_time = datetime.now()
    
    print("="*60)
    print("🚀 INICIANDO CRM JT TECNOLOGIA")
    print("="*60)
    print(f"⏰ Horário de início: {startup_time.strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Criar aplicação Flask
        app = Flask(__name__)
        log_system_event("Flask", "Aplicação Flask criada")
        
        # Configurações básicas
        configure_app(app)
        
        # Inicializar extensões
        initialize_extensions(app)
        
        # Inicializar banco de dados
        db_success = initialize_database(app)
        
        # Registrar blueprints (rotas)
        routes_count = register_application_routes(app)
        
        # Rotas básicas do sistema
        register_system_routes(app)
        
        # Handlers de erro globais
        register_error_handlers(app)
        
        # Finalizar inicialização
        finalize_initialization(app, startup_time, db_success, routes_count)
        
        SYSTEM_STATUS['app_created'] = True
        return app
        
    except Exception as e:
        error_msg = f"Erro crítico ao criar aplicação: {str(e)}"
        log_system_event("CRITICAL", error_msg, True)
        print("📋 Traceback completo:")
        traceback.print_exc()
        
        # Tentar criar uma aplicação mínima para mostrar o erro
        return create_emergency_app(error_msg)

def configure_app(app: Flask):
    """Configura a aplicação Flask"""
    try:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
        
        # Verificar se DATABASE_URL está configurada
        if not app.config['SQLALCHEMY_DATABASE_URI']:
            warning_msg = "DATABASE_URL não configurada - usando SQLite como fallback"
            SYSTEM_STATUS['warnings'].append(warning_msg)
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm_fallback.db'
            print(f"⚠️  {warning_msg}")
        
        log_system_event("Config", "Configurações da aplicação carregadas")
        
    except Exception as e:
        error_msg = f"Erro ao configurar aplicação: {str(e)}"
        log_system_event("Config", error_msg, True)
        raise

def initialize_extensions(app: Flask):
    """Inicializa extensões do Flask"""
    try:
        # CORS
        CORS(app)
        log_system_event("CORS", "CORS inicializado")
        
        # Outras extensões futuras podem ser adicionadas aqui
        
    except Exception as e:
        error_msg = f"Erro ao inicializar extensões: {str(e)}"
        log_system_event("Extensions", error_msg, True)
        raise

def initialize_database(app: Flask) -> bool:
    """Inicializa o banco de dados"""
    try:
        log_system_event("Database", "Iniciando inicialização do banco...")
        
        # Tentar importar sistema de modelos
        try:
            from src import initialize_system
            success = initialize_system(app)
            
            if success:
                SYSTEM_STATUS['db_initialized'] = True
                log_system_event("Database", "Banco de dados inicializado com sucesso")
                return True
            else:
                warning_msg = "Banco inicializado com avisos"
                SYSTEM_STATUS['warnings'].append(warning_msg)
                log_system_event("Database", warning_msg)
                return False
                
        except ImportError as e:
            # Fallback: tentar importar diretamente dos modelos
            try:
                from src.models import init_database
                success = init_database(app)
                SYSTEM_STATUS['db_initialized'] = success
                
                if success:
                    log_system_event("Database", "Banco inicializado (método fallback)")
                else:
                    log_system_event("Database", "Falha na inicialização (método fallback)", True)
                
                return success
                
            except Exception as e2:
                error_msg = f"Erro crítico de banco: {str(e2)}"
                log_system_event("Database", error_msg, True)
                return False
        
    except Exception as e:
        error_msg = f"Erro inesperado na inicialização do banco: {str(e)}"
        log_system_event("Database", error_msg, True)
        return False

def register_application_routes(app: Flask) -> int:
    """Registra todas as rotas da aplicação"""
    try:
        log_system_event("Routes", "Iniciando registro de rotas...")
        
        # Tentar usar sistema de rotas integrado
        try:
            from src.routes import register_all_blueprints
            routes_count = register_all_blueprints(app)
            
            SYSTEM_STATUS['routes_registered'] = routes_count > 0
            log_system_event("Routes", f"{routes_count} blueprints registrados")
            return routes_count
            
        except ImportError as e:
            warning_msg = f"Sistema de rotas não disponível: {str(e)}"
            SYSTEM_STATUS['warnings'].append(warning_msg)
            log_system_event("Routes", warning_msg)
            
            # Tentar importar rotas individuais
            return register_individual_routes(app)
        
    except Exception as e:
        error_msg = f"Erro ao registrar rotas: {str(e)}"
        log_system_event("Routes", error_msg, True)
        return 0

def register_individual_routes(app: Flask) -> int:
    """Registra rotas individualmente como fallback"""
    registered = 0
    
    # Lista de rotas para tentar registrar
    route_attempts = [
        ('src.routes.leads', 'leads_bp'),
        ('src.routes.dashboard', 'dashboard_bp'),
        ('src.routes.opportunities', 'opportunities_bp')
    ]
    
    for module_path, blueprint_name in route_attempts:
        try:
            module = __import__(module_path, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            
            if blueprint:
                app.register_blueprint(blueprint)
                registered += 1
                log_system_event("Routes", f"Blueprint {blueprint_name} registrado individualmente")
        except Exception as e:
            log_system_event("Routes", f"Falha ao registrar {blueprint_name}: {str(e)}")
    
    return registered

def register_system_routes(app: Flask):
    """Registra rotas básicas do sistema"""
    
    @app.route('/')
    def home():
        """Página inicial com status do sistema"""
        try:
            # Tentar obter informações detalhadas
            system_info = get_system_info()
            
            return jsonify({
                "message": "🚀 CRM JT Tecnologia API está funcionando!",
                "version": "1.0.0",
                "status": "online",
                "system_status": SYSTEM_STATUS,
                "startup_time": SYSTEM_STATUS.get('startup_time'),
                "features": [
                    "Gestão de Leads",
                    "Pipeline de Vendas", 
                    "Propostas Automáticas",
                    "Contratos Digitais",
                    "Chatbot Inteligente",
                    "Automações de Marketing",
                    "Telefonia Integrada"
                ],
                "endpoints": {
                    "health": "/health",
                    "status": "/system-status",
                    "db_test": "/db-test",
                    "models": "/api/models",
                    "leads": "/api/leads",
                    "dashboard": "/api/dashboard"
                },
                "system_info": system_info
            })
        except Exception as e:
            return jsonify({
                "message": "🚀 CRM JT Tecnologia API",
                "version": "1.0.0",
                "status": "online_with_errors",
                "error": str(e),
                "basic_endpoints": ["/health", "/system-status", "/db-test"]
            })
    
    @app.route('/health')
    def health_check():
        """Health check detalhado"""
        try:
            # Testar conexão com banco
            db_status = test_database_connection()
            
            # Verificar status dos componentes
            components_status = {
                'database': db_status,
                'models': SYSTEM_STATUS['db_initialized'],
                'routes': SYSTEM_STATUS['routes_registered'],
                'flask_app': SYSTEM_STATUS['app_created']
            }
            
            # Determinar status geral
            all_ok = all(components_status.values())
            
            return jsonify({
                "status": "healthy" if all_ok else "degraded",
                "timestamp": datetime.now().isoformat(),
                "components": components_status,
                "uptime": get_uptime(),
                "errors_count": len(SYSTEM_STATUS['errors']),
                "warnings_count": len(SYSTEM_STATUS['warnings'])
            })
            
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500
    
    @app.route('/system-status')
    def system_status():
        """Status detalhado do sistema"""
        try:
            # Obter informações dos modelos
            models_info = get_models_info()
            
            # Obter informações das rotas
            routes_info = get_routes_info()
            
            return jsonify({
                "system_status": SYSTEM_STATUS,
                "models_info": models_info,
                "routes_info": routes_info,
                "environment": {
                    "python_version": sys.version,
                    "flask_env": os.getenv('FLASK_ENV', 'production'),
                    "debug_mode": os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
                }
            })
            
        except Exception as e:
            return jsonify({
                "error": str(e),
                "basic_status": SYSTEM_STATUS
            }), 500
    
    @app.route('/api/models')
    def list_models():
        """Lista modelos disponíveis"""
        try:
            from src.models import validate_models
            return jsonify(validate_models())
        except ImportError:
            return jsonify({
                "error": "Módulo de modelos não disponível",
                "models_loaded": False
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/db-test')
    def db_test():
        """Teste detalhado de conexão com banco"""
        try:
            DATABASE_URL = os.getenv('DATABASE_URL')
            
            if not DATABASE_URL:
                return jsonify({
                    "status": "error",
                    "message": "❌ DATABASE_URL não configurada",
                    "using_fallback": True
                }), 500
            
            # Conectar ao banco
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            # Executar queries de teste
            cursor.execute('SELECT version();')
            version = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            table_count = cursor.fetchone()[0]
            
            # Testar performance básica
            start_time = datetime.now()
            cursor.execute('SELECT 1;')
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "status": "success",
                "message": "✅ Conexão com PostgreSQL OK!",
                "database_version": version,
                "tables_count": table_count,
                "response_time_ms": round(response_time, 2),
                "test_timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"❌ Erro ao conectar: {str(e)}",
                "test_timestamp": datetime.now().isoformat()
            }), 500

def register_error_handlers(app: Flask):
    """Registra handlers de erro globais"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint não encontrado",
            "message": "Verifique a URL e tente novamente",
            "available_endpoints": [
                "/", "/health", "/system-status", "/api/models", 
                "/db-test", "/api/leads", "/api/dashboard"
            ],
            "timestamp": datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        error_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "error_id": error_id,
            "message": "Entre em contato com o suporte informando o error_id",
            "timestamp": datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handler para todas as exceções não tratadas"""
        error_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        error_msg = f"Exceção não tratada: {str(e)}"
        
        # Log do erro
        log_system_event("Exception", f"{error_msg} (ID: {error_id})", True)
        
        return jsonify({
            "success": False,
            "error": "Erro inesperado no servidor",
            "error_id": error_id,
            "message": "Um erro inesperado ocorreu. Entre em contato com o suporte.",
            "timestamp": datetime.now().isoformat()
        }), 500

def create_emergency_app(error_message: str) -> Flask:
    """Cria uma aplicação mínima em caso de erro crítico"""
    app = Flask(__name__)
    
    @app.route('/')
    def emergency_home():
        return jsonify({
            "status": "emergency_mode",
            "message": "Sistema em modo de emergência",
            "error": error_message,
            "available_endpoints": ["/", "/emergency-status"],
            "contact": "Entre em contato com o suporte técnico"
        })
    
    @app.route('/emergency-status')
    def emergency_status():
        return jsonify({
            "mode": "emergency",
            "initialization_error": error_message,
            "system_errors": SYSTEM_STATUS['errors'],
            "timestamp": datetime.now().isoformat()
        })
    
    return app

def finalize_initialization(app: Flask, startup_time: datetime, db_success: bool, routes_count: int):
    """Finaliza a inicialização e exibe resumo"""
    end_time = datetime.now()
    startup_duration = (end_time - startup_time).total_seconds()
    
    SYSTEM_STATUS['startup_time'] = startup_time.isoformat()
    
    print("\n" + "="*60)
    print("📊 RESUMO DA INICIALIZAÇÃO")
    print("="*60)
    print(f"⏱️  Tempo de startup: {startup_duration:.2f}s")
    print(f"🗄️  Banco de dados: {'✅ OK' if db_success else '❌ Erro'}")
    print(f"🛣️  Rotas registradas: {routes_count}")
    print(f"⚠️  Avisos: {len(SYSTEM_STATUS['warnings'])}")
    print(f"❌ Erros: {len(SYSTEM_STATUS['errors'])}")
    
    if SYSTEM_STATUS['warnings']:
        print(f"\n⚠️  AVISOS:")
        for warning in SYSTEM_STATUS['warnings']:
            print(f"   • {warning}")
    
    if SYSTEM_STATUS['errors']:
        print(f"\n❌ ERROS:")
        for error in SYSTEM_STATUS['errors'][:5]:  # Mostrar apenas os primeiros 5
            print(f"   • {error}")
        if len(SYSTEM_STATUS['errors']) > 5:
            print(f"   ... e mais {len(SYSTEM_STATUS['errors']) - 5} erros")
    
    # Status final
    if db_success and routes_count > 0 and len(SYSTEM_STATUS['errors']) == 0:
        print(f"\n🎉 SISTEMA INICIALIZADO COM SUCESSO!")
        status = "success"
    elif db_success and routes_count > 0:
        print(f"\n✅ SISTEMA FUNCIONAL COM AVISOS")
        status = "functional_with_warnings"
    else:
        print(f"\n⚠️  SISTEMA INICIALIZADO COM PROBLEMAS")
        status = "degraded"
    
    print("="*60 + "\n")
    
    return status

# ==================== FUNÇÕES UTILITÁRIAS ====================

def get_system_info() -> dict:
    """Retorna informações gerais do sistema"""
    try:
        return {
            "database_initialized": SYSTEM_STATUS['db_initialized'],
            "routes_registered": SYSTEM_STATUS['routes_registered'],
            "startup_time": SYSTEM_STATUS.get('startup_time'),
            "errors_count": len(SYSTEM_STATUS['errors']),
            "warnings_count": len(SYSTEM_STATUS['warnings'])
        }
    except:
        return {"error": "Unable to get system info"}

def get_models_info() -> dict:
    """Retorna informações dos modelos"""
    try:
        from src.models import validate_models
        return validate_models()
    except ImportError:
        return {"error": "Models module not available"}
    except Exception as e:
        return {"error": str(e)}

def get_routes_info() -> dict:
    """Retorna informações das rotas"""
    try:
        from src.routes import get_route_status
        return get_route_status()
    except ImportError:
        return {"error": "Routes module not available"}
    except Exception as e:
        return {"error": str(e)}

def test_database_connection() -> bool:
    """Testa conexão com banco de dados"""
    try:
        from src.models import db
        if db:
            db.session.execute('SELECT 1')
            return True
        return False
    except:
        return False

def get_uptime() -> str:
    """Retorna tempo de atividade do sistema"""
    try:
        if SYSTEM_STATUS.get('startup_time'):
            startup = datetime.fromisoformat(SYSTEM_STATUS['startup_time'])
            uptime = datetime.now() - startup
            return str(uptime).split('.')[0]  # Remove microsegundos
        return "Unknown"
    except:
        return "Error calculating uptime"

def print_startup_banner():
    """Exibe banner de inicialização"""
    print("""
    ██████╗ ██████╗ ███╗   ███╗         ██╗████████╗
   ██╔════╝ ██╔══██╗████╗ ████║         ██║╚══██╔══╝
   ██║      ██████╔╝██╔████╔██║         ██║   ██║   
   ██║      ██╔══██╗██║╚██╔╝██║    ██   ██║   ██║   
   ╚██████╗ ██║  ██║██║ ╚═╝ ██║    ╚█████╔╝   ██║   
    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝     ╚════╝    ╚═╝   
    
              🚀 JT TECNOLOGIA CRM 🚀
         Sistema Completo de Gestão de Vendas
    """)

if __name__ == '__main__':
    # Exibir banner
    print_startup_banner()
    
    # Criar aplicação
    app = create_app()
    
    # Configurações de execução
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Informações de execução
    print("🌐 INFORMAÇÕES DE EXECUÇÃO")
    print("-" * 30)
    print(f"🏠 Host: {host}")
    print(f"🔌 Porta: {port}")
    print(f"🐛 Debug: {debug_mode}")
    print(f"🔗 URL: http://{host}:{port}")
    print("-" * 30)
    
    try:
        # Executar aplicação
        app.run(
            debug=debug_mode,
            host=host,
            port=port,
            use_reloader=debug_mode,  # Usar reloader apenas em debug
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar aplicação: {e}")
        sys.exit(1)
