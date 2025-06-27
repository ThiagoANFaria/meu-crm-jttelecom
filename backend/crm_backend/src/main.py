from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

# Inicializar o banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações do banco
    db_user = "crm_user"
    db_pass = "Ve4gKJT7Ltv&AmnL7C&QKg"
    db_host = "crm_jttelecom_crm-db"
    db_name = "crm_jttelecom"
    database_url = os.getenv('DATABASE_URL', f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}')
    
    # Configuração do app
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Inicializar extensões
    db.init_app(app)
    
    # Rota principal
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "🎉 CRM JT Telecom API está funcionando!",
            "version": "1.0.0",
            "endpoints": ["/", "/health", "/test", "/db-test"]
        })
    
    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "CRM JT Telecom API is running perfectly!",
            "modules": ["Authentication", "Users", "Leads", "Pipelines"]
        })
    
    @app.route("/test")
    def test():
        return jsonify({
            "test": "OK",
            "message": "Teste realizado com sucesso!"
        })
    
    @app.route("/db-test")
    def db_test():
        try:
            from sqlalchemy import text
            result = db.session.execute(text("SELECT version();"))
            version = str(result.fetchone()[0])
            return jsonify({"status": "✅ CONECTADO!", "db_version": version})
        except Exception as e:
            return jsonify({"status": "❌ ERRO", "message": str(e)})
    
    return app

if __name__ == "__main__":
    print("🚀 Iniciando CRM JT Telecom - Versão Simplificada...")
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
