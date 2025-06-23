from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
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
    'security': [{
        'BearerAuth': []
    }],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'description': 'ID do usuário para filtrar dados (apenas para admins/managers)'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de início do período (YYYY-MM-DD)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de fim do período (YYYY-MM-DD)'
        }
    ],
    'responses': {
        '200': {'description': 'Visão geral do dashboard com KPIs principais'},
        '400': {'description': 'Formato de data inválido'},
        '403': {'description': 'Sem permissão'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_dashboard_overview():
    """Obtém visão geral do dashboard com KPIs principais"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros opcionais
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if user_id and user_id != current_user_id:
        if current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Sem permissão para ver dados de outros usuários'}), 403
    
    # Preparar período
    date_range = None
    if start_date and end_date:
        try:
            # Validar formato das datas
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            date_range = {'start': start_date, 'end': end_date}
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    try:
        # Obter dados do dashboard
        dashboard_data = analytics_service.get_dashboard_overview(
            user_id=user_id or current_user_id,
            date_range=date_range
        )
        
        if 'error' in dashboard_data:
            return jsonify({'error': dashboard_data['error']}), 500
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter dashboard: {e}")
        return jsonify({'error': f'Erro ao obter dashboard: {str(e)}'}), 500

@dashboard_bp.route('/sales-funnel', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{
        'BearerAuth': []
    }],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'description': 'ID do usuário para filtrar dados (apenas para admins/managers)'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de início do período (YYYY-MM-DD)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de fim do período (YYYY-MM-DD)'
        }
    ],
    'responses': {
        '200': {'description': 'Análise detalhada do funil de vendas'},
        '400': {'description': 'Formato de data inválido'},
        '403': {'description': 'Sem permissão'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_sales_funnel():
    """Obtém análise detalhada do funil de vendas"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros opcionais
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if user_id and user_id != current_user_id:
        if current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Sem permissão para ver dados de outros usuários'}), 403
    
    # Preparar período
    date_range = None
    if start_date and end_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            date_range = {'start': start_date, 'end': end_date}
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    try:
        # Obter análise do funil
        funnel_data = analytics_service.get_sales_funnel_analysis(
            user_id=user_id or current_user_id,
            date_range=date_range
        )
        
        if 'error' in funnel_data:
            return jsonify({'error': funnel_data['error']}), 500
        
        return jsonify(funnel_data), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter funil de vendas: {e}")
        return jsonify({'error': f'Erro ao obter funil de vendas: {str(e)}'}), 500

@dashboard_bp.route('/team-performance', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{
        'BearerAuth': []
    }],
    'parameters': [
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de início do período (YYYY-MM-DD)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de fim do período (YYYY-MM-DD)'
        }
    ],
    'responses': {
        '200': {'description': 'Performance da equipe'},
        '400': {'description': 'Formato de data inválido'},
        '403': {'description': 'Sem permissão'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_team_performance():
    """Obtém performance da equipe (apenas para admins/managers)"""
    current_user_id = get_jwt_identity()
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if current_user.role not in ['admin', 'manager']:
        return jsonify({'error': 'Sem permissão para ver performance da equipe'}), 403
    
    # Parâmetros opcionais
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Preparar período
    date_range = None
    if start_date and end_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            date_range = {'start': start_date, 'end': end_date}
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    try:
        # Obter performance da equipe (user_id=None para todos)
        team_data = analytics_service.get_dashboard_overview(
            user_id=None,
            date_range=date_range
        )
        
        if 'error' in team_data:
            return jsonify({'error': team_data['error']}), 500
        
        return jsonify(team_data), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter performance da equipe: {e}")
        return jsonify({'error': f'Erro ao obter performance da equipe: {str(e)}'}), 500

@dashboard_bp.route('/kpis', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{
        'BearerAuth': []
    }],
    'parameters': [
        {
            'name': 'type',
            'in': 'query',
            'type': 'string',
            'enum': ['all', 'leads', 'opportunities', 'revenue', 'conversion', 'activities'],
            'description': 'Tipo de KPI para filtrar (leads, opportunities, revenue, conversion, activities)'
        },
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'description': 'ID do usuário para filtrar dados (apenas para admins/managers)'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de início do período (YYYY-MM-DD)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de fim do período (YYYY-MM-DD)'
        }
    ],
    'responses': {
        '200': {'description': 'KPIs específicos'},
        '400': {'description': 'Formato de data ou tipo de KPI inválido'},
        '403': {'description': 'Sem permissão'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_kpis():
    """Obtém KPIs específicos"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros
    kpi_type = request.args.get('type', 'all')  # leads, opportunities, revenue, conversion, activities
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if user_id and user_id != current_user_id:
        if current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Sem permissão para ver dados de outros usuários'}), 403
    
    # Preparar período
    date_range = None
    if start_date and end_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            date_range = {'start': start_date, 'end': end_date}
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    try:
        # Obter dados completos
        dashboard_data = analytics_service.get_dashboard_overview(
            user_id=user_id or current_user_id,
            date_range=date_range
        )
        
        if 'error' in dashboard_data:
            return jsonify({'error': dashboard_data['error']}), 500
        
        # Filtrar por tipo de KPI se especificado
        if kpi_type != 'all':
            if kpi_type in dashboard_data:
                return jsonify({
                    'type': kpi_type,
                    'data': dashboard_data[kpi_type],
                    'period': dashboard_data.get('period')
                }), 200
            else:
                return jsonify({'error': f'Tipo de KPI inválido: {kpi_type}'}), 400
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter KPIs: {e}")
        return jsonify({'error': f'Erro ao obter KPIs: {str(e)}'}), 500

@dashboard_bp.route('/quick-stats', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{
        'BearerAuth': []
    }],
    'responses': {
        '200': {'description': 'Estatísticas rápidas para widgets'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_quick_stats():
    """Obtém estatísticas rápidas para widgets"""
    current_user_id = get_jwt_identity()
    
    try:
        # Período padrão: hoje
        today = date.today()
        
        # Obter dados do dia
        today_data = analytics_service.get_dashboard_overview(
            user_id=current_user_id,
            date_range={'start': today.isoformat(), 'end': today.isoformat()}
        )
        
        # Obter dados do mês
        month_start = today.replace(day=1)
        month_data = analytics_service.get_dashboard_overview(
            user_id=current_user_id,
            date_range={'start': month_start.isoformat(), 'end': today.isoformat()}
        )
        
        if 'error' in today_data or 'error' in month_data:
            return jsonify({'error': 'Erro ao obter estatísticas'}), 500
        
        # Extrair estatísticas rápidas
        quick_stats = {
            'today': {
                'leads_created': today_data.get('leads', {}).get('total', 0),
                'tasks_completed': today_data.get('activities', {}).get('tasks', {}).get('completed', 0),
                'calls_made': today_data.get('activities', {}).get('calls', {}).get('total', 0),
                'revenue': today_data.get('revenue', {}).get('realized', 0)
            },
            'month': {
                'leads_created': month_data.get('leads', {}).get('total', 0),
                'opportunities_won': month_data.get('opportunities', {}).get('won', 0),
                'contracts_signed': len([c for c in month_data.get('conversion', {}).get('funnel', {}).get('contracts', 0)]),
                'revenue': month_data.get('revenue', {}).get('realized', 0),
                'conversion_rate': month_data.get('conversion', {}).get('rates', {}).get('overall', 0)
            }
        }
        
        return jsonify(quick_stats), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas rápidas: {e}")
        return jsonify({'error': f'Erro ao obter estatísticas rápidas: {str(e)}'}), 500

@dashboard_bp.route('/charts/revenue-evolution', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{
        'BearerAuth': []
    }],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'description': 'ID do usuário para filtrar dados (apenas para admins/managers)'
        },
        {
            'name': 'period',
            'in': 'query',
            'type': 'string',
            'enum': ['daily', 'weekly', 'monthly'],
            'description': 'Período da evolução (daily, weekly, monthly)',
            'default': 'monthly'
        },
        {
            'name': 'months',
            'in': 'query',
            'type': 'integer',
            'description': 'Número de meses para incluir na evolução',
            'default': 12
        }
    ],
    'responses': {
        '200': {'description': 'Evolução da receita para gráficos'},
        '403': {'description': 'Sem permissão'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_revenue_evolution():
    """Obtém evolução da receita para gráficos"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros
    user_id = request.args.get('user_id')
    period = request.args.get('period', 'monthly')  # daily, weekly, monthly
    months = request.args.get('months', 12, type=int)  # últimos X meses
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if user_id and user_id != current_user_id:
        if current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Sem permissão para ver dados de outros usuários'}), 403
    
    try:
        # Calcular período
        end_date = date.today()
        start_date = end_date - timedelta(days=months * 30)  # Aproximação
        
        dashboard_data = analytics_service.get_dashboard_overview(
            user_id=user_id or current_user_id,
            date_range={'start': start_date.isoformat(), 'end': end_date.isoformat()}
        )
        
        if 'error' in dashboard_data:
            return jsonify({'error': dashboard_data['error']}), 500
        
        # Extrair evolução da receita
        revenue_evolution = dashboard_data.get('revenue', {}).get('monthly_evolution', [])
        
        return jsonify({
            'period': period,
            'months': months,
            'evolution': revenue_evolution
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter evolução da receita: {e}")
        return jsonify({'error': f'Erro ao obter evolução da receita: {str(e)}'}), 500

@dashboard_bp.route('/charts/conversion-funnel', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{
        'BearerAuth': []
    }],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'description': 'ID do usuário para filtrar dados (apenas para admins/managers)'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de início do período (YYYY-MM-DD)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de fim do período (YYYY-MM-DD)'
        }
    ],
    'responses': {
        '200': {'description': 'Dados do funil de conversão para gráficos'},
        '400': {'description': 'Formato de data inválido'},
        '403': {'description': 'Sem permissão'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_conversion_funnel_chart():
    """Obtém dados do funil de conversão para gráficos"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if user_id and user_id != current_user_id:
        if current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Sem permissão para ver dados de outros usuários'}), 403
    
    # Preparar período
    date_range = None
    if start_date and end_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            date_range = {'start': start_date, 'end': end_date}
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    try:
        dashboard_data = analytics_service.get_dashboard_overview(
            user_id=user_id or current_user_id,
            date_range=date_range
        )
        
        if 'error' in dashboard_data:
            return jsonify({'error': dashboard_data['error']}), 500
        
        # Extrair dados do funil
        conversion_data = dashboard_data.get('conversion', {})
        funnel_data = conversion_data.get('funnel', {})
        rates_data = conversion_data.get('rates', {})
        
        # Formatar para gráfico de funil
        funnel_chart = [
            {'stage': 'Leads', 'count': funnel_data.get('leads', 0), 'rate': 100},
            {'stage': 'Oportunidades', 'count': funnel_data.get('opportunities', 0), 'rate': rates_data.get('lead_to_opportunity', 0)},
            {'stage': 'Propostas', 'count': funnel_data.get('proposals', 0), 'rate': rates_data.get('opportunity_to_proposal', 0)},
            {'stage': 'Contratos', 'count': funnel_data.get('contracts', 0), 'rate': rates_data.get('proposal_to_contract', 0)}
        ]
        
        return jsonify({
            'funnel': funnel_chart,
            'overall_conversion_rate': rates_data.get('overall', 0),
            'avg_conversion_time_days': conversion_data.get('avg_conversion_time_days', 0)
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter funil de conversão: {e}")
        return jsonify({'error': f'Erro ao obter funil de conversão: {str(e)}'}), 500

@dashboard_bp.route('/charts/activities-breakdown', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dashboard'],
    'security': [{
        'BearerAuth': []
    }],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'string',
            'description': 'ID do usuário para filtrar dados (apenas para admins/managers)'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de início do período (YYYY-MM-DD)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'description': 'Data de fim do período (YYYY-MM-DD)'
        }
    ],
    'responses': {
        '200': {'description': 'Breakdown de atividades para gráficos'},
        '400': {'description': 'Formato de data inválido'},
        '403': {'description': 'Sem permissão'},
        '500': {'description': 'Erro interno do servidor'}
    }
})
def get_activities_breakdown():
    """Obtém breakdown de atividades para gráficos"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if user_id and user_id != current_user_id:
        if current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Sem permissão para ver dados de outros usuários'}), 403
    
    # Preparar período
    date_range = None
    if start_date and end_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            date_range = {'start': start_date, 'end': end_date}
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    try:
        dashboard_data = analytics_service.get_dashboard_overview(
            user_id=user_id or current_user_id,
            date_range=date_range
        )
        
        if 'error' in dashboard_data:
            return jsonify({'error': dashboard_data['error']}), 500
        
        # Extrair dados de atividades
        activities_data = dashboard_data.get('activities', {})
        task_breakdown = activities_data.get('tasks', {}).get('breakdown', {})
        
        # Formatar para gráfico
        activities_chart = [
            {'type': activity_type.replace('_', ' ').title(), 'count': count}
            for activity_type, count in task_breakdown.items()
        ]
        
        # Adicionar outras atividades
        activities_chart.extend([
            {'type': 'Chamadas', 'count': activities_data.get('calls', {}).get('total', 0)},
            {'type': 'Emails', 'count': activities_data.get('emails_sent', 0)},
            {'type': 'Reuniões', 'count': activities_data.get('meetings_held', 0)}
        ])
        
        return jsonify({
            'activities': activities_chart,
            'completion_rate': activities_data.get('tasks', {}).get('completion_rate', 0),
            'total_call_duration': activities_data.get('calls', {}).get('total_duration_minutes', 0)
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter breakdown de atividades: {e}")
        return jsonify({'error': f'Erro ao obter breakdown de atividades: {str(e)}'}), 500


