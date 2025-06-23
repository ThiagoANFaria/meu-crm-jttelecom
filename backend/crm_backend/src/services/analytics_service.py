from sqlalchemy import func, and_, or_, case, extract, text
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
from decimal import Decimal

from src.models.user import db, User
from src.models.lead import Lead
from src.models.pipeline import Pipeline, PipelineStage, Opportunity
from src.models.proposal import Proposal
from src.models.contract import Contract
from src.models.task import Task, TaskStatus, TaskType
from src.models.telephony import Call

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Serviço para análise de dados e KPIs do CRM"""
    
    def get_dashboard_overview(self, user_id: str = None, date_range: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Obtém visão geral do dashboard com KPIs principais
        
        Args:
            user_id: ID do usuário (None para todos)
            date_range: Período de análise {'start': 'YYYY-MM-DD', 'end': 'YYYY-MM-DD'}
            
        Returns:
            Dados do dashboard
        """
        try:
            # Definir período padrão (últimos 30 dias)
            if not date_range:
                end_date = date.today()
                start_date = end_date - timedelta(days=30)
            else:
                start_date = datetime.strptime(date_range['start'], '%Y-%m-%d').date()
                end_date = datetime.strptime(date_range['end'], '%Y-%m-%d').date()
            
            # KPIs principais
            leads_metrics = self._get_leads_metrics(user_id, start_date, end_date)
            opportunities_metrics = self._get_opportunities_metrics(user_id, start_date, end_date)
            revenue_metrics = self._get_revenue_metrics(user_id, start_date, end_date)
            conversion_metrics = self._get_conversion_metrics(user_id, start_date, end_date)
            activity_metrics = self._get_activity_metrics(user_id, start_date, end_date)
            performance_metrics = self._get_performance_metrics(user_id, start_date, end_date)
            
            return {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': (end_date - start_date).days + 1
                },
                'leads': leads_metrics,
                'opportunities': opportunities_metrics,
                'revenue': revenue_metrics,
                'conversion': conversion_metrics,
                'activities': activity_metrics,
                'performance': performance_metrics,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter dashboard: {e}")
            return {'error': str(e)}
    
    def _get_leads_metrics(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Métricas de leads"""
        try:
            base_query = Lead.query
            
            if user_id:
                base_query = base_query.filter(Lead.assigned_to == user_id)
            
            # Total de leads no período
            total_leads = base_query.filter(
                Lead.created_at >= start_date,
                Lead.created_at <= end_date
            ).count()
            
            # Leads por status
            status_query = base_query.filter(
                Lead.created_at >= start_date,
                Lead.created_at <= end_date
            ).with_entities(
                Lead.status,
                func.count(Lead.id).label('count')
            ).group_by(Lead.status).all()
            
            status_breakdown = {status: count for status, count in status_query}
            
            # Leads por origem
            source_query = base_query.filter(
                Lead.created_at >= start_date,
                Lead.created_at <= end_date
            ).with_entities(
                Lead.source,
                func.count(Lead.id).label('count')
            ).group_by(Lead.source).all()
            
            source_breakdown = {source or 'Não informado': count for source, count in source_query}
            
            # Leads qualificados (com score > 70)
            qualified_leads = base_query.filter(
                Lead.created_at >= start_date,
                Lead.created_at <= end_date,
                Lead.score >= 70
            ).count()
            
            # Evolução diária
            daily_evolution = self._get_daily_evolution(
                base_query, start_date, end_date, Lead.created_at
            )
            
            # Período anterior para comparação
            previous_period_days = (end_date - start_date).days + 1
            previous_start = start_date - timedelta(days=previous_period_days)
            previous_end = start_date - timedelta(days=1)
            
            previous_total = base_query.filter(
                Lead.created_at >= previous_start,
                Lead.created_at <= previous_end
            ).count()
            
            growth_rate = self._calculate_growth_rate(total_leads, previous_total)
            
            return {
                'total': total_leads,
                'qualified': qualified_leads,
                'qualification_rate': round((qualified_leads / total_leads * 100) if total_leads > 0 else 0, 2),
                'status_breakdown': status_breakdown,
                'source_breakdown': source_breakdown,
                'daily_evolution': daily_evolution,
                'growth_rate': growth_rate,
                'previous_period_total': previous_total
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas de leads: {e}")
            return {}
    
    def _get_opportunities_metrics(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Métricas de oportunidades"""
        try:
            base_query = Opportunity.query
            
            if user_id:
                base_query = base_query.filter(Opportunity.assigned_to == user_id)
            
            # Total de oportunidades
            total_opportunities = base_query.filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date
            ).count()
            
            # Oportunidades por estágio
            stage_query = base_query.join(PipelineStage).filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date
            ).with_entities(
                PipelineStage.name,
                func.count(Opportunity.id).label('count'),
                func.sum(Opportunity.value).label('total_value')
            ).group_by(PipelineStage.name).all()
            
            stage_breakdown = [
                {
                    'stage': stage,
                    'count': count,
                    'total_value': float(total_value or 0)
                }
                for stage, count, total_value in stage_query
            ]
            
            # Oportunidades ganhas
            won_opportunities = base_query.filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date,
                Opportunity.status == 'won'
            ).count()
            
            # Oportunidades perdidas
            lost_opportunities = base_query.filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date,
                Opportunity.status == 'lost'
            ).count()
            
            # Taxa de conversão
            closed_opportunities = won_opportunities + lost_opportunities
            win_rate = round((won_opportunities / closed_opportunities * 100) if closed_opportunities > 0 else 0, 2)
            
            # Valor total em pipeline
            pipeline_value = base_query.filter(
                Opportunity.status == 'open'
            ).with_entities(
                func.sum(Opportunity.value)
            ).scalar() or 0
            
            # Valor médio das oportunidades
            avg_opportunity_value = base_query.filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date
            ).with_entities(
                func.avg(Opportunity.value)
            ).scalar() or 0
            
            return {
                'total': total_opportunities,
                'won': won_opportunities,
                'lost': lost_opportunities,
                'win_rate': win_rate,
                'pipeline_value': float(pipeline_value),
                'avg_value': float(avg_opportunity_value),
                'stage_breakdown': stage_breakdown
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas de oportunidades: {e}")
            return {}
    
    def _get_revenue_metrics(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Métricas de receita"""
        try:
            # Receita de contratos assinados
            contract_query = Contract.query
            
            if user_id:
                contract_query = contract_query.filter(Contract.created_by == user_id)
            
            # Receita realizada (contratos assinados)
            realized_revenue = contract_query.filter(
                Contract.signed_at >= start_date,
                Contract.signed_at <= end_date,
                Contract.status == 'signed'
            ).with_entities(
                func.sum(Contract.contract_value)
            ).scalar() or 0
            
            # Receita prevista (oportunidades em pipeline)
            opportunity_query = Opportunity.query
            
            if user_id:
                opportunity_query = opportunity_query.filter(Opportunity.assigned_to == user_id)
            
            predicted_revenue = opportunity_query.filter(
                Opportunity.status == 'open'
            ).with_entities(
                func.sum(Opportunity.value * Opportunity.probability / 100)
            ).scalar() or 0
            
            # Receita por mês (últimos 12 meses)
            monthly_revenue = self._get_monthly_revenue(user_id)
            
            # Meta de receita (simulada - pode vir de configuração)
            revenue_target = 100000  # R$ 100.000 por mês
            target_achievement = round((float(realized_revenue) / revenue_target * 100) if revenue_target > 0 else 0, 2)
            
            # Receita média por contrato
            avg_contract_value = contract_query.filter(
                Contract.signed_at >= start_date,
                Contract.signed_at <= end_date,
                Contract.status == 'signed'
            ).with_entities(
                func.avg(Contract.contract_value)
            ).scalar() or 0
            
            return {
                'realized': float(realized_revenue),
                'predicted': float(predicted_revenue),
                'target': revenue_target,
                'target_achievement': target_achievement,
                'avg_contract_value': float(avg_contract_value),
                'monthly_evolution': monthly_revenue
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas de receita: {e}")
            return {}
    
    def _get_conversion_metrics(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Métricas de conversão"""
        try:
            # Funil de conversão
            lead_query = Lead.query
            opportunity_query = Opportunity.query
            proposal_query = Proposal.query
            contract_query = Contract.query
            
            if user_id:
                lead_query = lead_query.filter(Lead.assigned_to == user_id)
                opportunity_query = opportunity_query.filter(Opportunity.assigned_to == user_id)
                proposal_query = proposal_query.filter(Proposal.created_by == user_id)
                contract_query = contract_query.filter(Contract.created_by == user_id)
            
            # Leads criados
            total_leads = lead_query.filter(
                Lead.created_at >= start_date,
                Lead.created_at <= end_date
            ).count()
            
            # Leads que viraram oportunidades
            leads_to_opportunities = lead_query.join(Opportunity).filter(
                Lead.created_at >= start_date,
                Lead.created_at <= end_date
            ).count()
            
            # Oportunidades que viraram propostas
            opportunities_to_proposals = opportunity_query.join(Proposal).filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date
            ).count()
            
            # Propostas que viraram contratos
            proposals_to_contracts = proposal_query.join(Contract).filter(
                Proposal.created_at >= start_date,
                Proposal.created_at <= end_date
            ).count()
            
            # Calcular taxas de conversão
            lead_to_opportunity_rate = round((leads_to_opportunities / total_leads * 100) if total_leads > 0 else 0, 2)
            opportunity_to_proposal_rate = round((opportunities_to_proposals / leads_to_opportunities * 100) if leads_to_opportunities > 0 else 0, 2)
            proposal_to_contract_rate = round((proposals_to_contracts / opportunities_to_proposals * 100) if opportunities_to_proposals > 0 else 0, 2)
            
            # Taxa de conversão geral (lead para contrato)
            overall_conversion_rate = round((proposals_to_contracts / total_leads * 100) if total_leads > 0 else 0, 2)
            
            # Tempo médio de conversão
            avg_conversion_time = self._get_average_conversion_time(user_id, start_date, end_date)
            
            return {
                'funnel': {
                    'leads': total_leads,
                    'opportunities': leads_to_opportunities,
                    'proposals': opportunities_to_proposals,
                    'contracts': proposals_to_contracts
                },
                'rates': {
                    'lead_to_opportunity': lead_to_opportunity_rate,
                    'opportunity_to_proposal': opportunity_to_proposal_rate,
                    'proposal_to_contract': proposal_to_contract_rate,
                    'overall': overall_conversion_rate
                },
                'avg_conversion_time_days': avg_conversion_time
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas de conversão: {e}")
            return {}
    
    def _get_activity_metrics(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Métricas de atividades"""
        try:
            task_query = Task.query
            call_query = Call.query
            
            if user_id:
                task_query = task_query.filter(Task.assigned_to == user_id)
                call_query = call_query.filter(Call.user_id == user_id)
            
            # Tarefas por tipo
            task_type_query = task_query.filter(
                Task.created_at >= start_date,
                Task.created_at <= end_date
            ).with_entities(
                Task.task_type,
                func.count(Task.id).label('count')
            ).group_by(Task.task_type).all()
            
            task_breakdown = {
                task_type.value if task_type else 'unknown': count 
                for task_type, count in task_type_query
            }
            
            # Tarefas completadas
            completed_tasks = task_query.filter(
                Task.completed_at >= start_date,
                Task.completed_at <= end_date,
                Task.status == TaskStatus.COMPLETED
            ).count()
            
            # Total de tarefas criadas
            total_tasks = task_query.filter(
                Task.created_at >= start_date,
                Task.created_at <= end_date
            ).count()
            
            # Taxa de conclusão
            completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
            
            # Chamadas realizadas
            total_calls = call_query.filter(
                Call.start_time >= start_date,
                Call.start_time <= end_date
            ).count()
            
            # Duração total de chamadas (em minutos)
            total_call_duration = call_query.filter(
                Call.start_time >= start_date,
                Call.start_time <= end_date
            ).with_entities(
                func.sum(Call.duration)
            ).scalar() or 0
            
            # Emails enviados (tarefas de email completadas)
            emails_sent = task_query.filter(
                Task.completed_at >= start_date,
                Task.completed_at <= end_date,
                Task.task_type == TaskType.EMAIL,
                Task.status == TaskStatus.COMPLETED
            ).count()
            
            # Reuniões realizadas
            meetings_held = task_query.filter(
                Task.completed_at >= start_date,
                Task.completed_at <= end_date,
                Task.task_type == TaskType.MEETING,
                Task.status == TaskStatus.COMPLETED
            ).count()
            
            return {
                'tasks': {
                    'total_created': total_tasks,
                    'completed': completed_tasks,
                    'completion_rate': completion_rate,
                    'breakdown': task_breakdown
                },
                'calls': {
                    'total': total_calls,
                    'total_duration_minutes': int(total_call_duration)
                },
                'emails_sent': emails_sent,
                'meetings_held': meetings_held
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas de atividades: {e}")
            return {}
    
    def _get_performance_metrics(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Métricas de performance por usuário"""
        try:
            if user_id:
                # Performance individual
                user = User.query.get(user_id)
                if not user:
                    return {}
                
                return {
                    'user': {
                        'id': user.id,
                        'name': f"{user.first_name} {user.last_name}",
                        'role': user.role
                    },
                    'individual_metrics': self._get_individual_performance(user_id, start_date, end_date)
                }
            else:
                # Performance da equipe
                team_performance = self._get_team_performance(start_date, end_date)
                return {
                    'team_metrics': team_performance
                }
                
        except Exception as e:
            logger.error(f"Erro ao calcular métricas de performance: {e}")
            return {}
    
    def _get_individual_performance(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Performance individual do usuário"""
        try:
            # Leads criados
            leads_created = Lead.query.filter(
                Lead.assigned_to == user_id,
                Lead.created_at >= start_date,
                Lead.created_at <= end_date
            ).count()
            
            # Oportunidades ganhas
            opportunities_won = Opportunity.query.filter(
                Opportunity.assigned_to == user_id,
                Opportunity.updated_at >= start_date,
                Opportunity.updated_at <= end_date,
                Opportunity.status == 'won'
            ).count()
            
            # Contratos fechados
            contracts_signed = Contract.query.filter(
                Contract.created_by == user_id,
                Contract.signed_at >= start_date,
                Contract.signed_at <= end_date,
                Contract.status == 'signed'
            ).count()
            
            # Receita gerada
            revenue_generated = Contract.query.filter(
                Contract.created_by == user_id,
                Contract.signed_at >= start_date,
                Contract.signed_at <= end_date,
                Contract.status == 'signed'
            ).with_entities(
                func.sum(Contract.contract_value)
            ).scalar() or 0
            
            # Tarefas completadas
            tasks_completed = Task.query.filter(
                Task.assigned_to == user_id,
                Task.completed_at >= start_date,
                Task.completed_at <= end_date,
                Task.status == TaskStatus.COMPLETED
            ).count()
            
            # Chamadas realizadas
            calls_made = Call.query.filter(
                Call.user_id == user_id,
                Call.start_time >= start_date,
                Call.start_time <= end_date
            ).count()
            
            return {
                'leads_created': leads_created,
                'opportunities_won': opportunities_won,
                'contracts_signed': contracts_signed,
                'revenue_generated': float(revenue_generated),
                'tasks_completed': tasks_completed,
                'calls_made': calls_made
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular performance individual: {e}")
            return {}
    
    def _get_team_performance(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Performance da equipe"""
        try:
            # Buscar todos os usuários ativos
            users = User.query.filter(User.is_active == True).all()
            
            team_metrics = []
            
            for user in users:
                individual_metrics = self._get_individual_performance(user.id, start_date, end_date)
                
                team_metrics.append({
                    'user': {
                        'id': user.id,
                        'name': f"{user.first_name} {user.last_name}",
                        'role': user.role
                    },
                    'metrics': individual_metrics
                })
            
            # Ordenar por receita gerada
            team_metrics.sort(key=lambda x: x['metrics'].get('revenue_generated', 0), reverse=True)
            
            return team_metrics
            
        except Exception as e:
            logger.error(f"Erro ao calcular performance da equipe: {e}")
            return []
    
    def _get_daily_evolution(self, base_query, start_date: date, end_date: date, date_field) -> List[Dict[str, Any]]:
        """Evolução diária de uma métrica"""
        try:
            daily_data = base_query.filter(
                date_field >= start_date,
                date_field <= end_date
            ).with_entities(
                func.date(date_field).label('date'),
                func.count().label('count')
            ).group_by(func.date(date_field)).all()
            
            # Criar lista completa de dias
            current_date = start_date
            evolution = []
            
            # Converter dados para dict para lookup rápido
            data_dict = {data_date: count for data_date, count in daily_data}
            
            while current_date <= end_date:
                evolution.append({
                    'date': current_date.isoformat(),
                    'count': data_dict.get(current_date, 0)
                })
                current_date += timedelta(days=1)
            
            return evolution
            
        except Exception as e:
            logger.error(f"Erro ao calcular evolução diária: {e}")
            return []
    
    def _get_monthly_revenue(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Receita dos últimos 12 meses"""
        try:
            # Últimos 12 meses
            end_date = date.today()
            start_date = end_date.replace(day=1) - timedelta(days=365)
            
            contract_query = Contract.query.filter(
                Contract.signed_at >= start_date,
                Contract.signed_at <= end_date,
                Contract.status == 'signed'
            )
            
            if user_id:
                contract_query = contract_query.filter(Contract.created_by == user_id)
            
            monthly_data = contract_query.with_entities(
                extract('year', Contract.signed_at).label('year'),
                extract('month', Contract.signed_at).label('month'),
                func.sum(Contract.contract_value).label('revenue')
            ).group_by(
                extract('year', Contract.signed_at),
                extract('month', Contract.signed_at)
            ).all()
            
            # Organizar dados por mês
            monthly_revenue = []
            for year, month, revenue in monthly_data:
                month_date = date(int(year), int(month), 1)
                monthly_revenue.append({
                    'month': month_date.strftime('%Y-%m'),
                    'revenue': float(revenue or 0)
                })
            
            return monthly_revenue
            
        except Exception as e:
            logger.error(f"Erro ao calcular receita mensal: {e}")
            return []
    
    def _get_average_conversion_time(self, user_id: str, start_date: date, end_date: date) -> float:
        """Tempo médio de conversão de lead para contrato"""
        try:
            # Buscar contratos com leads associados
            query = db.session.query(
                Contract.signed_at,
                Lead.created_at
            ).join(
                Lead, Contract.lead_id == Lead.id
            ).filter(
                Contract.signed_at >= start_date,
                Contract.signed_at <= end_date,
                Contract.status == 'signed'
            )
            
            if user_id:
                query = query.filter(Contract.created_by == user_id)
            
            conversions = query.all()
            
            if not conversions:
                return 0
            
            total_days = 0
            for contract_date, lead_date in conversions:
                if contract_date and lead_date:
                    delta = contract_date.date() - lead_date.date()
                    total_days += delta.days
            
            return round(total_days / len(conversions), 1) if conversions else 0
            
        except Exception as e:
            logger.error(f"Erro ao calcular tempo médio de conversão: {e}")
            return 0
    
    def _calculate_growth_rate(self, current: int, previous: int) -> float:
        """Calcula taxa de crescimento"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        
        return round(((current - previous) / previous * 100), 2)
    
    def get_sales_funnel_analysis(self, user_id: str = None, date_range: Dict[str, str] = None) -> Dict[str, Any]:
        """Análise detalhada do funil de vendas"""
        try:
            if not date_range:
                end_date = date.today()
                start_date = end_date - timedelta(days=30)
            else:
                start_date = datetime.strptime(date_range['start'], '%Y-%m-%d').date()
                end_date = datetime.strptime(date_range['end'], '%Y-%m-%d').date()
            
            # Análise por estágio do pipeline
            pipeline_analysis = self._get_pipeline_stage_analysis(user_id, start_date, end_date)
            
            # Análise de tempo por estágio
            stage_duration_analysis = self._get_stage_duration_analysis(user_id, start_date, end_date)
            
            # Análise de perda por estágio
            loss_analysis = self._get_loss_analysis(user_id, start_date, end_date)
            
            return {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'pipeline_stages': pipeline_analysis,
                'stage_durations': stage_duration_analysis,
                'loss_analysis': loss_analysis
            }
            
        except Exception as e:
            logger.error(f"Erro na análise do funil: {e}")
            return {'error': str(e)}
    
    def _get_pipeline_stage_analysis(self, user_id: str, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Análise por estágio do pipeline"""
        try:
            query = db.session.query(
                PipelineStage.name,
                PipelineStage.order,
                func.count(Opportunity.id).label('count'),
                func.sum(Opportunity.value).label('total_value'),
                func.avg(Opportunity.value).label('avg_value'),
                func.avg(Opportunity.probability).label('avg_probability')
            ).join(
                Opportunity, PipelineStage.id == Opportunity.stage_id
            ).filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date
            )
            
            if user_id:
                query = query.filter(Opportunity.assigned_to == user_id)
            
            results = query.group_by(
                PipelineStage.name,
                PipelineStage.order
            ).order_by(PipelineStage.order).all()
            
            stage_analysis = []
            for stage_name, order, count, total_value, avg_value, avg_probability in results:
                stage_analysis.append({
                    'stage_name': stage_name,
                    'order': order,
                    'opportunities_count': count,
                    'total_value': float(total_value or 0),
                    'avg_value': float(avg_value or 0),
                    'avg_probability': float(avg_probability or 0),
                    'weighted_value': float((total_value or 0) * (avg_probability or 0) / 100)
                })
            
            return stage_analysis
            
        except Exception as e:
            logger.error(f"Erro na análise por estágio: {e}")
            return []
    
    def _get_stage_duration_analysis(self, user_id: str, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Análise de duração por estágio"""
        # Por enquanto retorna dados simulados
        # Implementar quando houver histórico de mudanças de estágio
        return [
            {'stage_name': 'Qualificação', 'avg_days': 3.5},
            {'stage_name': 'Proposta', 'avg_days': 7.2},
            {'stage_name': 'Negociação', 'avg_days': 12.8},
            {'stage_name': 'Fechamento', 'avg_days': 5.1}
        ]
    
    def _get_loss_analysis(self, user_id: str, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Análise de perdas por estágio"""
        try:
            query = db.session.query(
                PipelineStage.name,
                func.count(case([(Opportunity.status == 'lost', 1)])).label('lost_count'),
                func.count(Opportunity.id).label('total_count')
            ).join(
                Opportunity, PipelineStage.id == Opportunity.stage_id
            ).filter(
                Opportunity.created_at >= start_date,
                Opportunity.created_at <= end_date
            )
            
            if user_id:
                query = query.filter(Opportunity.assigned_to == user_id)
            
            results = query.group_by(PipelineStage.name).all()
            
            loss_analysis = []
            for stage_name, lost_count, total_count in results:
                loss_rate = round((lost_count / total_count * 100) if total_count > 0 else 0, 2)
                loss_analysis.append({
                    'stage_name': stage_name,
                    'lost_count': lost_count,
                    'total_count': total_count,
                    'loss_rate': loss_rate
                })
            
            return loss_analysis
            
        except Exception as e:
            logger.error(f"Erro na análise de perdas: {e}")
            return []

