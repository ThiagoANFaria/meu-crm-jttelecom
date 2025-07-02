from flask import Blueprint, jsonify
from datetime import datetime

system_bp = Blueprint('system', __name__)

@system_bp.route('/', methods=['GET'])
def api_info():
    """Informações da API"""
    return jsonify({
        "message": "Bem-vindo à API do CRM JT Telecom",
        "version": "1.0.0",
        "documentation": "/apidocs/",
        "health": "/health"
    }), 200

@system_bp.route('/health', methods=['GET'])
def health_check():
    """Status de saúde da API"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "crm-jt-telecom",
        "version": "1.0.0"
    }), 200

