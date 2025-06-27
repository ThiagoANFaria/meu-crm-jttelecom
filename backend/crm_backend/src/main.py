from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os

# Inicializar o banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações básicas
    database_url = os.getenv('DATABASE_URL', 'postgresql://crm_user:crm_password@localhost/crm_jttelcom')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string-change-in-production')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    
    # Inicializar extensões
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Rota de health check simples
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "CRM JT Telecom API está funcionando!",
            "version": "1.0.0"
        })
    
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
                "Dashboard"
            ]
        })
    
    # Criar tabelas (sem modelos complexos por enquanto)
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados iniciado com sucesso!")
        except Exception as e:
            print(f"⚠️ Aviso: Problema com banco de dados: {e}")
    
    return app

if __name__ == "__main__":
    app = create_app()
    print("🚀 Iniciando CRM JT Telecom...")
    app.run(host="0.0.0.0", port=5000, debug=False)
