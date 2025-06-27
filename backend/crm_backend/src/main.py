from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

# Depois adicione:
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
 db_user = "crm_user"
db_pass = "Ve4gKJT7Ltv&AmnL7C&QKg"
db_host = "crm_jttelecom_crm-db"
database_url = os.getenv('DATABASE_URL', f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}')
        return jsonify({
            "status": "success",
            "message": "🎉 CRM JT Telecom API está funcionando!",
            "version": "1.0.0",
            "endpoints": ["/", "/health", "/test"]
        })
    
    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "CRM JT Telecom API is running perfectly!",
            "modules": ["Authentication", "Users", "Leads", "Pipelines"]
        })
    
    @app.route("/test")
   @app.route("/db-test")
def db_test():
    try:
        from sqlalchemy import text
        result = db.session.execute(text("SELECT version();"))
        version = str(result.fetchone()[0])
        return jsonify({"status": "✅ CONECTADO!", "db_version": version})
    except Exception as e:
        return jsonify({"status": "❌ ERRO", "message": str(e)})
if __name__ == "__main__":
    print("🚀 Iniciando CRM JT Telecom - Versão Simplificada...")
    app = create_app()
  # Em vez de:
app.run(host="0.0.0.0", port=5000, debug=True)

# Use:
app.run(host="0.0.0.0", port=5000, debug=False)
