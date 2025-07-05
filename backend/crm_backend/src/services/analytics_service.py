"""
Serviço de Analytics e Relatórios
"""
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Serviço para análises e métricas do CRM"""
    
    def __init__(self):
        self.logger = logger
    
    def get_dashboard_overview(self, tenant_id, user_id=None):
        """Retorna visão geral do dashboard"""
        try:
            # Simulação de dados para demonstração
            return {
                'leads': {
                    'total': 150,
                    'new_this_month': 45,
                    'conversion_rate': 12.5,
                    'growth': 8.2
                },
                'opportunities': {
                    'total': 32,
                    'total_value': 450000.00,
                    'won_this_month': 8,
                    'average_deal_size': 14062.50
                },
                'tasks': {
                    'pending': 23,
                    'completed_today': 12,
                    'overdue': 5,
                    'completion_rate': 85.7
                },
                'revenue': {
                    'this_month': 125000.00,
                    'last_month': 98000.00,
                    'growth': 27.6,
                    'target': 150000.00
                }
            }
        except Exception as e:
            self.logger.error(f"Erro ao obter overview do dashboard: {e}")
            return {}
    
    def get_leads_analytics(self, tenant_id, period='30d'):
        """Retorna analytics de leads"""
        try:
            return {
                'total_leads': 150,
                'new_leads': 45,
                'qualified_leads': 28,
                'conversion_rate': 18.7,
                'sources': {
                    'website': 35,
                    'social_media': 28,
                    'referral': 22,
                    'cold_call': 15,
                    'email': 12,
                    'other': 8
                },
                'status_distribution': {
                    'novo': 45,
                    'qualificado': 28,
                    'proposta': 15,
                    'negociacao': 12,
                    'fechado': 8,
                    'perdido': 42
                }
            }
        except Exception as e:
            self.logger.error(f"Erro ao obter analytics de leads: {e}")
            return {}
    
    def get_sales_analytics(self, tenant_id, period='30d'):
        """Retorna analytics de vendas"""
        try:
            return {
                'total_revenue': 125000.00,
                'deals_won': 8,
                'deals_lost': 5,
                'win_rate': 61.5,
                'average_deal_size': 15625.00,
                'sales_cycle': 45,  # dias
                'pipeline_value': 450000.00,
                'monthly_trend': [
                    {'month': 'Jan', 'revenue': 98000},
                    {'month': 'Feb', 'revenue': 112000},
                    {'month': 'Mar', 'revenue': 125000}
                ]
            }
        except Exception as e:
            self.logger.error(f"Erro ao obter analytics de vendas: {e}")
            return {}
    
    def get_team_performance(self, tenant_id, period='30d'):
        """Retorna performance da equipe"""
        try:
            return {
                'total_users': 12,
                'active_users': 10,
                'top_performers': [
                    {'name': 'João Silva', 'deals': 5, 'revenue': 75000},
                    {'name': 'Maria Santos', 'deals': 3, 'revenue': 50000},
                    {'name': 'Pedro Costa', 'deals': 2, 'revenue': 35000}
                ],
                'activities': {
                    'calls': 156,
                    'emails': 89,
                    'meetings': 34,
                    'tasks_completed': 78
                }
            }
        except Exception as e:
            self.logger.error(f"Erro ao obter performance da equipe: {e}")
            return {}
    
    def generate_report(self, tenant_id, report_type, filters=None):
        """Gera relatório específico"""
        try:
            if report_type == 'leads':
                return self.get_leads_analytics(tenant_id)
            elif report_type == 'sales':
                return self.get_sales_analytics(tenant_id)
            elif report_type == 'team':
                return self.get_team_performance(tenant_id)
            else:
                return {'error': 'Tipo de relatório não suportado'}
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            return {'error': str(e)}

