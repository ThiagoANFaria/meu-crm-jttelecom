from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.analytics_service import AnalyticsService
from datetime import datetime, date, timedelta
import logging
from flasgger import swag_from

dashboard_bp = Blueprint('dashboard', __name__)
logger = logging.getLogger(__name__)

# Inicializar serviço
analytics_service = AnalyticsService()

@dashboard_bp.route('/overview', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{'BearerAuth': []}],
    'summary': 'Obter visão geral do dashboard',
    'description': 'Retorna métricas principais do CRM',
    'responses': {
        200: {
            'description': 'Visão geral obtida com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'leads': {'type': 'object'},
                    'opportunities': {'type': 'object'},
                    'tasks': {'type': 'object'},
                    'revenue': {'type': 'object'}
                }
            }
        }
    }
})
def get_overview():
    """Obter visão geral do dashboard"""
    try:
        user_id = get_jwt_identity()
        tenant_id = request.headers.get('X-Tenant-ID', 'default')
        
        overview = analytics_service.get_dashboard_overview(tenant_id, user_id)
        
        return jsonify({
            'success': True,
            'data': overview
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter overview: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/analytics/leads', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{'BearerAuth': []}],
    'summary': 'Obter analytics de leads',
    'parameters': [
        {
            'name': 'period',
            'in': 'query',
            'type': 'string',
            'default': '30d',
            'description': 'Período para análise (7d, 30d, 90d)'
        }
    ],
    'responses': {
        200: {
            'description': 'Analytics de leads obtidas com sucesso'
        }
    }
})
def get_leads_analytics():
    """Obter analytics de leads"""
    try:
        user_id = get_jwt_identity()
        tenant_id = request.headers.get('X-Tenant-ID', 'default')
        period = request.args.get('period', '30d')
        
        analytics = analytics_service.get_leads_analytics(tenant_id, period)
        
        return jsonify({
            'success': True,
            'data': analytics
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter analytics de leads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/analytics/sales', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{'BearerAuth': []}],
    'summary': 'Obter analytics de vendas',
    'responses': {
        200: {
            'description': 'Analytics de vendas obtidas com sucesso'
        }
    }
})
def get_sales_analytics():
    """Obter analytics de vendas"""
    try:
        user_id = get_jwt_identity()
        tenant_id = request.headers.get('X-Tenant-ID', 'default')
        period = request.args.get('period', '30d')
        
        analytics = analytics_service.get_sales_analytics(tenant_id, period)
        
        return jsonify({
            'success': True,
            'data': analytics
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter analytics de vendas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/analytics/team', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{'BearerAuth': []}],
    'summary': 'Obter performance da equipe',
    'responses': {
        200: {
            'description': 'Performance da equipe obtida com sucesso'
        }
    }
})
def get_team_performance():
    """Obter performance da equipe"""
    try:
        user_id = get_jwt_identity()
        tenant_id = request.headers.get('X-Tenant-ID', 'default')
        period = request.args.get('period', '30d')
        
        performance = analytics_service.get_team_performance(tenant_id, period)
        
        return jsonify({
            'success': True,
            'data': performance
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter performance da equipe: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

