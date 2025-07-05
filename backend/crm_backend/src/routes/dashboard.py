from flask import Blueprint, jsonify
from flask import Blueprint, request, jsonify
from datetime import datetime, date, timedelta
import logging

dashboard_bp = Blueprint('dashboard', __name__)
logger = logging.getLogger(__name__)

@dashboard_bp.route('/', methods=['GET'])
def dashboard_info():
    """Informações do dashboard"""
    return jsonify({
        "module": "dashboard",
        "description": "Dashboard com estatísticas do CRM",
        "endpoints": [
            {"path": "/overview", "method": "GET", "description": "Visão geral"},
            {"path": "/stats", "method": "GET", "description": "Estatísticas"}
        ]
    })

@dashboard_bp.route('/overview', methods=['GET'])
def get_overview():
    """Visão geral do dashboard"""
    return jsonify({
        "leads_total": 150,
        "leads_novos": 25,
        "pipelines_ativas": 5,
        "contratos_mes": 12,
        "receita_mes": 45000.00,
        "ultima_atualizacao": datetime.now().isoformat()
    })

@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    """Estatísticas detalhadas"""
    return jsonify({
        "vendas": {
            "mes_atual": 12,
            "mes_anterior": 8,
            "crescimento": "50%"
        },
        "leads": {
            "total": 150,
            "qualificados": 45,
            "convertidos": 12
        },
        "performance": {
            "taxa_conversao": "8%",
            "ticket_medio": 3750.00,
            "tempo_medio_fechamento": "15 dias"
        }
    })

