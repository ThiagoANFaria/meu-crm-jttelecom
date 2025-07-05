from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def dashboard_data():
    """Dados do dashboard"""
    return jsonify({
        "total_leads": 150,
        "total_clients": 45,
        "total_proposals": 23,
        "revenue": 125000.50
    }), 200

@dashboard_bp.route('/charts', methods=['GET'])
@jwt_required()
def dashboard_charts():
    """Dados para gráficos"""
    return jsonify({
        "sales_chart": [100, 150, 200, 180, 220],
        "leads_chart": [10, 15, 12, 18, 25]
    }), 200

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def dashboard_stats():
    """Estatísticas gerais"""
    return jsonify({
        "conversion_rate": 15.5,
        "avg_deal_size": 2500.00,
        "monthly_growth": 8.2
    }), 200

