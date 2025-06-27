from flask import Flask, jsonify
import os

def create_app():
    app = Flask(__name__)
    
    # Rota principal
    @app.route("/")
    def home():
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
    
    return app

if __name__ == "__main__":
    print("🚀 Iniciando CRM JT Telecom - Versão Simplificada...")
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
