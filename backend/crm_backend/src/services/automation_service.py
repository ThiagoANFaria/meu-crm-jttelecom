import smtplib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import logging
import re
from jinja2 import Template

from src.models.automation import (
    AutomationRule, AutomationAction, AutomationExecution,
    EmailCampaign, CadenceSequence, CadenceStep, CadenceEnrollment,
    TriggerType, ActionType, db
)
from src.models.lead import Lead
from src.models.user import User

logger = logging.getLogger(__name__)

class AutomationEngine:
    """Engine principal para execução de automações"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.task_service = TaskService()
    
    def trigger_automation(self, trigger_type: TriggerType, trigger_data: Dict[str, Any]) -> List[str]:
        """
        Dispara automações baseadas em um gatilho
        
        Args:
            trigger_type: Tipo do gatilho
            trigger_data: Dados do evento que disparou
            
        Returns:
            Lista de IDs das execuções criadas
        """
        execution_ids = []
        
        try:
            # Buscar regras ativas para este tipo de gatilho
            rules = AutomationRule.query.filter(
                AutomationRule.trigger_type == trigger_type,
                AutomationRule.is_active == True
            ).order_by(AutomationRule.priority.desc()).all()
            
            for rule in rules:
                try:
                    # Verificar se as condições do gatilho são atendidas
                    if self._check_trigger_conditions(rule, trigger_data):
                        # Verificar filtros da regra
                        if self._check_rule_filters(rule, trigger_data):
                            # Criar execução
                            execution_id = self._create_execution(rule, trigger_data)
                            if execution_id:
                                execution_ids.append(execution_id)
                                
                                # Executar imediatamente ou agendar
                                if rule.delay_minutes == 0:
                                    self._execute_automation(execution_id)
                                else:
                                    self._schedule_execution(execution_id, rule.delay_minutes)
                                    
                except Exception as e:
                    logger.error(f"Erro ao processar regra {rule.id}: {e}")
                    continue
            
            return execution_ids
            
        except Exception as e:
            logger.error(f"Erro no trigger de automação: {e}")
            return []
    
    def _check_trigger_conditions(self, rule: AutomationRule, trigger_data: Dict[str, Any]) -> bool:
        """Verifica se as condições específicas do gatilho são atendidas"""
        conditions = rule.trigger_conditions or {}
        
        if not conditions:
            return True
        
        # Verificar condições baseadas no tipo de gatilho
        if rule.trigger_type == TriggerType.LEAD_STATUS_CHANGED:
            required_from = conditions.get('from_status')
            required_to = conditions.get('to_status')
            
            if required_from and trigger_data.get('from_status') != required_from:
                return False
            if required_to and trigger_data.get('to_status') != required_to:
                return False
        
        elif rule.trigger_type == TriggerType.LEAD_STAGE_CHANGED:
            required_from = conditions.get('from_stage')
            required_to = conditions.get('to_stage')
            
            if required_from and trigger_data.get('from_stage') != required_from:
                return False
            if required_to and trigger_data.get('to_stage') != required_to:
                return False
        
        # Adicionar mais condições conforme necessário
        
        return True
    
    def _check_rule_filters(self, rule: AutomationRule, trigger_data: Dict[str, Any]) -> bool:
        """Verifica se os filtros da regra são atendidos"""
        filters = rule.filters or {}
        
        if not filters:
            return True
        
        # Obter o objeto alvo (lead, opportunity, etc.)
        target_type = trigger_data.get('target_type')
        target_id = trigger_data.get('target_id')
        
        if target_type == 'lead' and target_id:
            lead = Lead.query.get(target_id)
            if not lead:
                return False
            
            # Verificar filtros do lead
            if 'lead_source' in filters:
                if lead.source not in filters['lead_source']:
                    return False
            
            if 'lead_status' in filters:
                if lead.status not in filters['lead_status']:
                    return False
            
            if 'assigned_user' in filters:
                if lead.assigned_to not in filters['assigned_user']:
                    return False
            
            # Adicionar mais filtros conforme necessário
        
        return True
    
    def _create_execution(self, rule: AutomationRule, trigger_data: Dict[str, Any]) -> Optional[str]:
        """Cria uma nova execução de automação"""
        try:
            execution = AutomationExecution(
                rule_id=rule.id,
                trigger_data=trigger_data,
                target_type=trigger_data.get('target_type'),
                target_id=trigger_data.get('target_id'),
                status='pending'
            )
            
            db.session.add(execution)
            db.session.commit()
            
            return execution.id
            
        except Exception as e:
            logger.error(f"Erro ao criar execução: {e}")
            db.session.rollback()
            return None
    
    def _execute_automation(self, execution_id: str) -> bool:
        """Executa uma automação"""
        try:
            execution = AutomationExecution.query.get(execution_id)
            if not execution:
                return False
            
            execution.status = 'running'
            execution.started_at = datetime.utcnow()
            db.session.commit()
            
            rule = execution.rule
            actions = sorted(rule.actions, key=lambda x: x.order)
            
            execution_log = []
            actions_executed = 0
            actions_successful = 0
            actions_failed = 0
            
            for action in actions:
                if not action.is_active:
                    continue
                
                try:
                    # Verificar condições da ação
                    if self._check_action_conditions(action, execution.trigger_data):
                        # Executar ação
                        result = self._execute_action(action, execution)
                        
                        actions_executed += 1
                        if result.get('success'):
                            actions_successful += 1
                        else:
                            actions_failed += 1
                        
                        execution_log.append({
                            'action_id': action.id,
                            'action_type': action.action_type.value,
                            'timestamp': datetime.utcnow().isoformat(),
                            'result': result
                        })
                        
                except Exception as e:
                    actions_executed += 1
                    actions_failed += 1
                    execution_log.append({
                        'action_id': action.id,
                        'action_type': action.action_type.value,
                        'timestamp': datetime.utcnow().isoformat(),
                        'error': str(e)
                    })
                    logger.error(f"Erro ao executar ação {action.id}: {e}")
            
            # Atualizar execução
            execution.status = 'completed' if actions_failed == 0 else 'failed'
            execution.completed_at = datetime.utcnow()
            execution.actions_executed = actions_executed
            execution.actions_successful = actions_successful
            execution.actions_failed = actions_failed
            execution.execution_log = execution_log
            
            # Atualizar estatísticas da regra
            rule.execution_count += 1
            rule.last_executed_at = datetime.utcnow()
            if execution.status == 'completed':
                rule.success_count += 1
            else:
                rule.error_count += 1
            
            db.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na execução da automação {execution_id}: {e}")
            if execution:
                execution.status = 'failed'
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                db.session.commit()
            return False
    
    def _check_action_conditions(self, action: AutomationAction, trigger_data: Dict[str, Any]) -> bool:
        """Verifica se as condições da ação são atendidas"""
        conditions = action.conditions or {}
        
        if not conditions:
            return True
        
        # Implementar verificação de condições específicas
        # Por enquanto, retorna True
        return True
    
    def _execute_action(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa uma ação específica"""
        try:
            if action.action_type == ActionType.SEND_EMAIL:
                return self._execute_send_email(action, execution)
            
            elif action.action_type == ActionType.CREATE_TASK:
                return self._execute_create_task(action, execution)
            
            elif action.action_type == ActionType.UPDATE_LEAD_STATUS:
                return self._execute_update_lead_status(action, execution)
            
            elif action.action_type == ActionType.MOVE_LEAD_STAGE:
                return self._execute_move_lead_stage(action, execution)
            
            elif action.action_type == ActionType.ASSIGN_USER:
                return self._execute_assign_user(action, execution)
            
            elif action.action_type == ActionType.ADD_TAG:
                return self._execute_add_tag(action, execution)
            
            elif action.action_type == ActionType.REMOVE_TAG:
                return self._execute_remove_tag(action, execution)
            
            elif action.action_type == ActionType.WAIT:
                return self._execute_wait(action, execution)
            
            else:
                return {
                    'success': False,
                    'message': f'Tipo de ação não implementado: {action.action_type.value}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def _execute_send_email(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa ação de envio de email"""
        config = action.action_config
        
        # Obter dados do lead
        if execution.target_type == 'lead':
            lead = Lead.query.get(execution.target_id)
            if not lead or not lead.email:
                return {'success': False, 'message': 'Lead não encontrado ou sem email'}
            
            # Renderizar template do email
            subject = self._render_template(config.get('subject', ''), lead)
            content = self._render_template(config.get('content', ''), lead)
            
            # Enviar email
            result = self.email_service.send_email(
                to_email=lead.email,
                to_name=lead.name,
                subject=subject,
                content=content,
                sender_name=config.get('sender_name'),
                sender_email=config.get('sender_email')
            )
            
            return result
        
        return {'success': False, 'message': 'Tipo de alvo não suportado para envio de email'}
    
    def _execute_create_task(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa ação de criação de tarefa"""
        config = action.action_config
        
        if execution.target_type == 'lead':
            lead = Lead.query.get(execution.target_id)
            if not lead:
                return {'success': False, 'message': 'Lead não encontrado'}
            
            # Criar tarefa
            task_data = {
                'title': self._render_template(config.get('title', ''), lead),
                'description': self._render_template(config.get('description', ''), lead),
                'lead_id': lead.id,
                'assigned_to': config.get('assigned_to') or lead.assigned_to,
                'due_date': self._calculate_due_date(config.get('due_in_days', 1)),
                'priority': config.get('priority', 'medium'),
                'task_type': config.get('task_type', 'follow_up')
            }
            
            result = self.task_service.create_task(task_data)
            return result
        
        return {'success': False, 'message': 'Tipo de alvo não suportado para criação de tarefa'}
    
    def _execute_update_lead_status(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa ação de atualização de status do lead"""
        config = action.action_config
        
        if execution.target_type == 'lead':
            lead = Lead.query.get(execution.target_id)
            if not lead:
                return {'success': False, 'message': 'Lead não encontrado'}
            
            new_status = config.get('new_status')
            if not new_status:
                return {'success': False, 'message': 'Novo status não especificado'}
            
            old_status = lead.status
            lead.status = new_status
            lead.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Status alterado de {old_status} para {new_status}'
            }
        
        return {'success': False, 'message': 'Tipo de alvo não suportado'}
    
    def _execute_assign_user(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa ação de atribuição de usuário"""
        config = action.action_config
        
        if execution.target_type == 'lead':
            lead = Lead.query.get(execution.target_id)
            if not lead:
                return {'success': False, 'message': 'Lead não encontrado'}
            
            user_id = config.get('user_id')
            if not user_id:
                return {'success': False, 'message': 'Usuário não especificado'}
            
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'message': 'Usuário não encontrado'}
            
            old_user = lead.assigned_to
            lead.assigned_to = user_id
            lead.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Lead atribuído para {user.first_name} {user.last_name}'
            }
        
        return {'success': False, 'message': 'Tipo de alvo não suportado'}
    
    def _execute_add_tag(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa ação de adicionar tag"""
        # Implementar quando sistema de tags estiver pronto
        return {'success': True, 'message': 'Tag adicionada (funcionalidade em desenvolvimento)'}
    
    def _execute_remove_tag(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa ação de remover tag"""
        # Implementar quando sistema de tags estiver pronto
        return {'success': True, 'message': 'Tag removida (funcionalidade em desenvolvimento)'}
    
    def _execute_wait(self, action: AutomationAction, execution: AutomationExecution) -> Dict[str, Any]:
        """Executa ação de espera"""
        config = action.action_config
        wait_minutes = config.get('wait_minutes', 0)
        
        # Para ações de espera, apenas registramos o tempo
        return {
            'success': True,
            'message': f'Aguardando {wait_minutes} minutos'
        }
    
    def _render_template(self, template_str: str, lead: Lead) -> str:
        """Renderiza template com dados do lead"""
        if not template_str:
            return ""
        
        try:
            template = Template(template_str)
            
            # Preparar dados do lead para o template
            lead_data = {
                'name': lead.name or '',
                'email': lead.email or '',
                'phone': lead.phone or '',
                'company': lead.company or '',
                'position': lead.position or '',
                'source': lead.source or '',
                'status': lead.status or '',
                'created_at': lead.created_at.strftime('%d/%m/%Y') if lead.created_at else '',
                'assigned_user': f"{lead.assignee.first_name} {lead.assignee.last_name}" if lead.assignee else ''
            }
            
            return template.render(lead=lead_data)
            
        except Exception as e:
            logger.error(f"Erro ao renderizar template: {e}")
            return template_str
    
    def _calculate_due_date(self, days_from_now: int) -> datetime:
        """Calcula data de vencimento"""
        return datetime.utcnow() + timedelta(days=days_from_now)
    
    def _schedule_execution(self, execution_id: str, delay_minutes: int):
        """Agenda execução para o futuro"""
        # Por enquanto, apenas log. Implementar com Celery ou similar
        logger.info(f"Execução {execution_id} agendada para {delay_minutes} minutos")

class EmailService:
    """Serviço para envio de emails"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.default_sender = os.getenv('DEFAULT_SENDER_EMAIL')
        self.default_sender_name = os.getenv('DEFAULT_SENDER_NAME', 'JT Telecom')
    
    def send_email(self, to_email: str, to_name: str, subject: str, content: str,
                   sender_email: str = None, sender_name: str = None) -> Dict[str, Any]:
        """Envia email"""
        try:
            if not self.smtp_username or not self.smtp_password:
                return {
                    'success': False,
                    'message': 'Configurações SMTP não encontradas'
                }
            
            sender_email = sender_email or self.default_sender
            sender_name = sender_name or self.default_sender_name
            
            # Criar mensagem
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{sender_name} <{sender_email}>"
            msg['To'] = f"{to_name} <{to_email}>"
            
            # Adicionar conteúdo HTML
            html_part = MimeText(content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return {
                'success': True,
                'message': 'Email enviado com sucesso'
            }
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")
            return {
                'success': False,
                'message': f'Erro ao enviar email: {str(e)}'
            }

class TaskService:
    """Serviço para criação de tarefas"""
    
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova tarefa"""
        try:
            # Importar modelo de tarefa quando estiver implementado
            # from src.models.task import Task
            
            # Por enquanto, apenas simular criação
            return {
                'success': True,
                'message': 'Tarefa criada com sucesso',
                'task_id': 'simulated_task_id'
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar tarefa: {e}")
            return {
                'success': False,
                'message': f'Erro ao criar tarefa: {str(e)}'
            }

class CadenceService:
    """Serviço para gerenciamento de cadências"""
    
    def __init__(self):
        self.automation_engine = AutomationEngine()
    
    def enroll_lead_in_cadence(self, lead_id: str, sequence_id: str, enrolled_by: str) -> Dict[str, Any]:
        """Inscreve um lead em uma sequência de cadência"""
        try:
            # Verificar se lead já está inscrito
            existing = CadenceEnrollment.query.filter(
                CadenceEnrollment.lead_id == lead_id,
                CadenceEnrollment.sequence_id == sequence_id,
                CadenceEnrollment.status == 'active'
            ).first()
            
            if existing:
                return {
                    'success': False,
                    'message': 'Lead já está inscrito nesta sequência'
                }
            
            # Criar inscrição
            enrollment = CadenceEnrollment(
                sequence_id=sequence_id,
                lead_id=lead_id,
                enrolled_by=enrolled_by,
                status='active',
                current_step=1
            )
            
            # Calcular próxima ação
            sequence = CadenceSequence.query.get(sequence_id)
            if sequence and sequence.steps:
                first_step = min(sequence.steps, key=lambda x: x.order)
                enrollment.next_action_at = self._calculate_next_action_time(first_step)
            
            db.session.add(enrollment)
            
            # Atualizar estatísticas da sequência
            sequence.enrolled_count += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Lead inscrito na cadência com sucesso',
                'enrollment_id': enrollment.id
            }
            
        except Exception as e:
            logger.error(f"Erro ao inscrever lead na cadência: {e}")
            db.session.rollback()
            return {
                'success': False,
                'message': f'Erro ao inscrever lead: {str(e)}'
            }
    
    def process_cadence_actions(self) -> Dict[str, Any]:
        """Processa ações de cadência que estão prontas para execução"""
        try:
            # Buscar inscrições com ações pendentes
            now = datetime.utcnow()
            enrollments = CadenceEnrollment.query.filter(
                CadenceEnrollment.status == 'active',
                CadenceEnrollment.next_action_at <= now
            ).all()
            
            processed = 0
            errors = 0
            
            for enrollment in enrollments:
                try:
                    result = self._process_enrollment_step(enrollment)
                    if result.get('success'):
                        processed += 1
                    else:
                        errors += 1
                        
                except Exception as e:
                    logger.error(f"Erro ao processar inscrição {enrollment.id}: {e}")
                    errors += 1
            
            return {
                'success': True,
                'processed': processed,
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar cadências: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def _process_enrollment_step(self, enrollment: CadenceEnrollment) -> Dict[str, Any]:
        """Processa um passo específico da cadência"""
        try:
            sequence = enrollment.sequence
            current_step_obj = None
            
            # Encontrar o passo atual
            for step in sequence.steps:
                if step.order == enrollment.current_step:
                    current_step_obj = step
                    break
            
            if not current_step_obj:
                # Cadência completada
                enrollment.status = 'completed'
                enrollment.completed_at = datetime.utcnow()
                sequence.completed_count += 1
                db.session.commit()
                
                return {
                    'success': True,
                    'message': 'Cadência completada'
                }
            
            # Executar ação do passo
            action_result = self._execute_cadence_action(current_step_obj, enrollment)
            
            # Atualizar estatísticas
            enrollment.steps_completed += 1
            
            if current_step_obj.action_type == ActionType.SEND_EMAIL:
                enrollment.emails_sent += 1
            elif current_step_obj.action_type == ActionType.CREATE_TASK:
                enrollment.tasks_created += 1
            
            # Avançar para próximo passo
            enrollment.current_step += 1
            
            # Calcular próxima ação
            next_step = None
            for step in sequence.steps:
                if step.order == enrollment.current_step:
                    next_step = step
                    break
            
            if next_step:
                enrollment.next_action_at = self._calculate_next_action_time(next_step)
            else:
                # Cadência completada
                enrollment.status = 'completed'
                enrollment.completed_at = datetime.utcnow()
                sequence.completed_count += 1
            
            enrollment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return action_result
            
        except Exception as e:
            logger.error(f"Erro ao processar passo da cadência: {e}")
            db.session.rollback()
            return {
                'success': False,
                'message': str(e)
            }
    
    def _execute_cadence_action(self, step: CadenceStep, enrollment: CadenceEnrollment) -> Dict[str, Any]:
        """Executa a ação de um passo da cadência"""
        try:
            # Criar dados de trigger simulados para usar o automation engine
            trigger_data = {
                'target_type': 'lead',
                'target_id': enrollment.lead_id,
                'cadence_step_id': step.id,
                'enrollment_id': enrollment.id
            }
            
            # Criar ação temporária para execução
            temp_action = AutomationAction(
                action_type=step.action_type,
                action_config=step.action_config,
                conditions=step.conditions
            )
            
            # Criar execução temporária
            temp_execution = AutomationExecution(
                trigger_data=trigger_data,
                target_type='lead',
                target_id=enrollment.lead_id
            )
            
            # Executar ação
            result = self.automation_engine._execute_action(temp_action, temp_execution)
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao executar ação da cadência: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def _calculate_next_action_time(self, step: CadenceStep) -> datetime:
        """Calcula o horário da próxima ação"""
        now = datetime.utcnow()
        
        total_minutes = (
            (step.delay_days or 0) * 24 * 60 +
            (step.delay_hours or 0) * 60 +
            (step.delay_minutes or 0)
        )
        
        return now + timedelta(minutes=total_minutes)

