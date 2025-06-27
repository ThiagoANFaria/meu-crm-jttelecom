from flask import Flask, jsonify
import os

def create_app():
    app = Flask(__name__)
    
    # Rota principal
    @app.route("/")
    database_url = os.getenv('DATABASE_URL', 'postgresql://crm_user:SENHA@crm_jttelecom_crm-db:5432/crm_jttelecom')
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
    def test():
        return jsonify({
            "test": "OK",
            "message": "Teste realizado com sucesso!"
        })
@app.route("/db-test")
def db_test():
    try:
        with app.app_context():
            result = db.engine.execute("SELECT version();")
            version = str(result.fetchone()[0])
            return jsonify({"status": "✅ CONECTADO!", "db_version": version})
    except Exception as e:
        return jsonify({"status": "❌ ERRO", "message": str(e)})    
    return app

if __name__ == "__main__":
    print("🚀 Iniciando CRM JT Telecom - Versão Simplificada...")
    app = create_app()
  # Em vez de:
app.run(host="0.0.0.0", port=5000, debug=True)

# Use:
app.run(host="0.0.0.0", port=5000, debug=False)
