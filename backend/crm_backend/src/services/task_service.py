import smtplib
import os
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Any, Optional
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import logging
from sqlalchemy import and_, or_, func

from src.models.task import (
    Task, TaskComment, TaskTimeLog, TaskTemplate, ActivitySummary,
    TaskType, TaskStatus, TaskPriority, RecurrenceType, db
)
from src.models.user import User
from src.models.lead import Lead

logger = logging.getLogger(__name__)

class TaskService:
    """Serviço para gerenciamento de tarefas e atividades"""
    
    def __init__(self):
        self.notification_service = NotificationService()
        self.calendar_service = CalendarService()
    
    def create_task(self, task_data: Dict[str, Any], created_by: str) -> Dict[str, Any]:
        """
        Cria uma nova tarefa
        
        Args:
            task_data: Dados da tarefa
            created_by: ID do usuário que está criando
            
        Returns:
            Resultado da criação
        """
        try:
            # Validações básicas
            if not task_data.get('title'):
                return {'success': False, 'message': 'Título é obrigatório'}
            
            if not task_data.get('assigned_to'):
                return {'success': False, 'message': 'Responsável é obrigatório'}
            
            # Verificar se usuário responsável existe
            assignee = User.query.get(task_data['assigned_to'])
            if not assignee:
                return {'success': False, 'message': 'Usuário responsável não encontrado'}
            
            # Processar datas
            due_date = None
            due_time = None
            if task_data.get('due_date'):
                due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d').date()
            if task_data.get('due_time'):
                due_time = datetime.strptime(task_data['due_time'], '%H:%M').time()
            
            start_date = None
            start_time = None
            if task_data.get('start_date'):
                start_date = datetime.strptime(task_data['start_date'], '%Y-%m-%d').date()
            if task_data.get('start_time'):
                start_time = datetime.strptime(task_data['start_time'], '%H:%M').time()
            
            # Criar tarefa
            task = Task(
                title=task_data['title'],
                description=task_data.get('description'),
                task_type=TaskType(task_data.get('task_type', 'follow_up')),
                category=task_data.get('category'),
                priority=TaskPriority(task_data.get('priority', 'medium')),
                due_date=due_date,
                due_time=due_time,
                start_date=start_date,
                start_time=start_time,
                duration_minutes=task_data.get('duration_minutes'),
                lead_id=task_data.get('lead_id'),
                opportunity_id=task_data.get('opportunity_id'),
                proposal_id=task_data.get('proposal_id'),
                contract_id=task_data.get('contract_id'),
                assigned_to=task_data['assigned_to'],
                created_by=created_by,
                reminder_minutes=task_data.get('reminder_minutes'),
                email_reminder=task_data.get('email_reminder', True),
                sms_reminder=task_data.get('sms_reminder', False),
                location=task_data.get('location'),
                address=task_data.get('address'),
                contact_phone=task_data.get('contact_phone'),
                contact_email=task_data.get('contact_email'),
                tags=task_data.get('tags', []),
                custom_fields=task_data.get('custom_fields', {}),
                is_recurring=task_data.get('is_recurring', False),
                recurrence_type=RecurrenceType(task_data.get('recurrence_type', 'none')),
                recurrence_interval=task_data.get('recurrence_interval', 1),
                recurrence_end_date=datetime.strptime(task_data['recurrence_end_date'], '%Y-%m-%d').date() if task_data.get('recurrence_end_date') else None
            )
            
            db.session.add(task)
            db.session.flush()  # Para obter o ID
            
            # Criar evento no calendário se configurado
            if task_data.get('create_calendar_event', False):
                calendar_result = self.calendar_service.create_event(task)
                if calendar_result.get('success'):
                    task.calendar_event_id = calendar_result.get('event_id')
                    task.calendar_provider = calendar_result.get('provider')
            
            # Agendar notificações
            if task.reminder_minutes and task.due_date:
                self.notification_service.schedule_reminder(task)
            
            # Criar tarefas recorrentes se necessário
            if task.is_recurring and task.recurrence_type != RecurrenceType.NONE:
                self._create_recurring_tasks(task)
            
            db.session.commit()
            
            # Enviar notificação de atribuição
            if task.assigned_to != created_by:
                self.notification_service.send_task_assignment_notification(task)
            
            return {
                'success': True,
                'message': 'Tarefa criada com sucesso',
                'task_id': task.id,
                'task': task.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar tarefa: {e}")
            return {
                'success': False,
                'message': f'Erro ao criar tarefa: {str(e)}'
            }
    
    def update_task(self, task_id: str, task_data: Dict[str, Any], updated_by: str) -> Dict[str, Any]:
        """Atualiza uma tarefa existente"""
        try:
            task = Task.query.get(task_id)
            if not task:
                return {'success': False, 'message': 'Tarefa não encontrada'}
            
            # Verificar permissões (responsável ou criador)
            if task.assigned_to != updated_by and task.created_by != updated_by:
                # Verificar se é admin/manager
                user = User.query.get(updated_by)
                if not user or user.role not in ['admin', 'manager']:
                    return {'success': False, 'message': 'Sem permissão para editar esta tarefa'}
            
            # Atualizar campos
            if 'title' in task_data:
                task.title = task_data['title']
            if 'description' in task_data:
                task.description = task_data['description']
            if 'task_type' in task_data:
                task.task_type = TaskType(task_data['task_type'])
            if 'category' in task_data:
                task.category = task_data['category']
            if 'priority' in task_data:
                old_priority = task.priority
                task.priority = TaskPriority(task_data['priority'])
                
                # Notificar se prioridade mudou para alta/urgente
                if old_priority != task.priority and task.priority in [TaskPriority.HIGH, TaskPriority.URGENT]:
                    self.notification_service.send_priority_change_notification(task)
            
            # Atualizar datas
            if 'due_date' in task_data:
                task.due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d').date() if task_data['due_date'] else None
            if 'due_time' in task_data:
                task.due_time = datetime.strptime(task_data['due_time'], '%H:%M').time() if task_data['due_time'] else None
            
            # Atualizar responsável
            if 'assigned_to' in task_data and task_data['assigned_to'] != task.assigned_to:
                old_assignee = task.assigned_to
                task.assigned_to = task_data['assigned_to']
                
                # Notificar novo responsável
                self.notification_service.send_task_assignment_notification(task)
                
                # Notificar antigo responsável sobre a remoção
                if old_assignee:
                    self.notification_service.send_task_unassignment_notification(task, old_assignee)
            
            # Outros campos
            for field in ['location', 'address', 'contact_phone', 'contact_email', 'tags', 'custom_fields']:
                if field in task_data:
                    setattr(task, field, task_data[field])
            
            task.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tarefa atualizada com sucesso',
                'task': task.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar tarefa: {e}")
            return {
                'success': False,
                'message': f'Erro ao atualizar tarefa: {str(e)}'
            }
    
    def complete_task(self, task_id: str, completion_data: Dict[str, Any], completed_by: str) -> Dict[str, Any]:
        """Marca tarefa como completada"""
        try:
            task = Task.query.get(task_id)
            if not task:
                return {'success': False, 'message': 'Tarefa não encontrada'}
            
            if task.status == TaskStatus.COMPLETED:
                return {'success': False, 'message': 'Tarefa já está completada'}
            
            # Marcar como completada
            task.mark_completed(
                result=completion_data.get('result'),
                outcome=completion_data.get('outcome'),
                next_action=completion_data.get('next_action')
            )
            
            # Adicionar comentário se fornecido
            if completion_data.get('comment'):
                comment = TaskComment(
                    task_id=task.id,
                    content=completion_data['comment'],
                    comment_type='completion',
                    created_by=completed_by
                )
                db.session.add(comment)
            
            # Criar próxima tarefa se sugerida
            if completion_data.get('create_next_task') and completion_data.get('next_task_data'):
                next_task_data = completion_data['next_task_data']
                next_task_data['lead_id'] = task.lead_id
                next_task_data['opportunity_id'] = task.opportunity_id
                next_task_data['assigned_to'] = next_task_data.get('assigned_to', task.assigned_to)
                
                self.create_task(next_task_data, completed_by)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tarefa completada com sucesso',
                'task': task.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao completar tarefa: {e}")
            return {
                'success': False,
                'message': f'Erro ao completar tarefa: {str(e)}'
            }
    
    def reschedule_task(self, task_id: str, new_due_date: str, new_due_time: str = None, reason: str = None, rescheduled_by: str = None) -> Dict[str, Any]:
        """Reagenda uma tarefa"""
        try:
            task = Task.query.get(task_id)
            if not task:
                return {'success': False, 'message': 'Tarefa não encontrada'}
            
            # Converter datas
            due_date = datetime.strptime(new_due_date, '%Y-%m-%d').date()
            due_time = datetime.strptime(new_due_time, '%H:%M').time() if new_due_time else None
            
            # Reagendar
            task.reschedule(due_date, due_time)
            
            # Adicionar comentário sobre reagendamento
            if reason and rescheduled_by:
                comment = TaskComment(
                    task_id=task.id,
                    content=f"Tarefa reagendada para {due_date.strftime('%d/%m/%Y')}. Motivo: {reason}",
                    comment_type='reschedule',
                    created_by=rescheduled_by
                )
                db.session.add(comment)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tarefa reagendada com sucesso',
                'task': task.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao reagendar tarefa: {e}")
            return {
                'success': False,
                'message': f'Erro ao reagendar tarefa: {str(e)}'
            }
    
    def add_time_log(self, task_id: str, time_data: Dict[str, Any], logged_by: str) -> Dict[str, Any]:
        """Adiciona log de tempo a uma tarefa"""
        try:
            task = Task.query.get(task_id)
            if not task:
                return {'success': False, 'message': 'Tarefa não encontrada'}
            
            # Processar horários
            start_time = datetime.fromisoformat(time_data['start_time'])
            end_time = datetime.fromisoformat(time_data['end_time']) if time_data.get('end_time') else None
            
            # Criar log
            time_log = TaskTimeLog(
                task_id=task.id,
                start_time=start_time,
                end_time=end_time,
                description=time_data.get('description'),
                logged_by=logged_by
            )
            
            # Calcular duração
            time_log.calculate_duration()
            
            db.session.add(time_log)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Tempo registrado com sucesso',
                'time_log': time_log.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao registrar tempo: {e}")
            return {
                'success': False,
                'message': f'Erro ao registrar tempo: {str(e)}'
            }
    
    def get_user_tasks(self, user_id: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Obtém tarefas de um usuário com filtros"""
        try:
            query = Task.query.filter(Task.assigned_to == user_id, Task.is_active == True)
            
            if filters:
                # Filtro por status
                if 'status' in filters:
                    if isinstance(filters['status'], list):
                        query = query.filter(Task.status.in_([TaskStatus(s) for s in filters['status']]))
                    else:
                        query = query.filter(Task.status == TaskStatus(filters['status']))
                
                # Filtro por tipo
                if 'task_type' in filters:
                    if isinstance(filters['task_type'], list):
                        query = query.filter(Task.task_type.in_([TaskType(t) for t in filters['task_type']]))
                    else:
                        query = query.filter(Task.task_type == TaskType(filters['task_type']))
                
                # Filtro por prioridade
                if 'priority' in filters:
                    if isinstance(filters['priority'], list):
                        query = query.filter(Task.priority.in_([TaskPriority(p) for p in filters['priority']]))
                    else:
                        query = query.filter(Task.priority == TaskPriority(filters['priority']))
                
                # Filtro por data de vencimento
                if 'due_date_from' in filters:
                    due_date_from = datetime.strptime(filters['due_date_from'], '%Y-%m-%d').date()
                    query = query.filter(Task.due_date >= due_date_from)
                
                if 'due_date_to' in filters:
                    due_date_to = datetime.strptime(filters['due_date_to'], '%Y-%m-%d').date()
                    query = query.filter(Task.due_date <= due_date_to)
                
                # Filtro por lead
                if 'lead_id' in filters:
                    query = query.filter(Task.lead_id == filters['lead_id'])
                
                # Filtro por oportunidade
                if 'opportunity_id' in filters:
                    query = query.filter(Task.opportunity_id == filters['opportunity_id'])
                
                # Filtro por tags
                if 'tags' in filters:
                    for tag in filters['tags']:
                        query = query.filter(Task.tags.contains([tag]))
                
                # Filtro por vencimento
                if 'overdue_only' in filters and filters['overdue_only']:
                    today = date.today()
                    query = query.filter(
                        and_(
                            Task.due_date < today,
                            Task.status.in_([TaskStatus.PENDING, TaskStatus.IN_PROGRESS])
                        )
                    )
                
                # Filtro por hoje
                if 'today_only' in filters and filters['today_only']:
                    today = date.today()
                    query = query.filter(Task.due_date == today)
            
            # Ordenação
            sort_by = filters.get('sort_by', 'due_date') if filters else 'due_date'
            sort_order = filters.get('sort_order', 'asc') if filters else 'asc'
            
            if sort_by == 'due_date':
                if sort_order == 'desc':
                    query = query.order_by(Task.due_date.desc().nullslast())
                else:
                    query = query.order_by(Task.due_date.asc().nullsfirst())
            elif sort_by == 'priority':
                # Ordenar por prioridade (urgent > high > medium > low)
                priority_order = {
                    TaskPriority.URGENT: 4,
                    TaskPriority.HIGH: 3,
                    TaskPriority.MEDIUM: 2,
                    TaskPriority.LOW: 1
                }
                if sort_order == 'desc':
                    query = query.order_by(Task.priority.desc())
                else:
                    query = query.order_by(Task.priority.asc())
            elif sort_by == 'created_at':
                if sort_order == 'desc':
                    query = query.order_by(Task.created_at.desc())
                else:
                    query = query.order_by(Task.created_at.asc())
            
            tasks = query.all()
            return [task.to_dict() for task in tasks]
            
        except Exception as e:
            logger.error(f"Erro ao buscar tarefas do usuário: {e}")
            return []
    
    def get_overdue_tasks(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Obtém tarefas em atraso"""
        try:
            today = date.today()
            query = Task.query.filter(
                and_(
                    Task.due_date < today,
                    Task.status.in_([TaskStatus.PENDING, TaskStatus.IN_PROGRESS]),
                    Task.is_active == True
                )
            )
            
            if user_id:
                query = query.filter(Task.assigned_to == user_id)
            
            query = query.order_by(Task.due_date.asc())
            
            tasks = query.all()
            return [task.to_dict() for task in tasks]
            
        except Exception as e:
            logger.error(f"Erro ao buscar tarefas em atraso: {e}")
            return []
    
    def get_upcoming_tasks(self, user_id: str, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Obtém tarefas dos próximos dias"""
        try:
            today = date.today()
            end_date = today + timedelta(days=days_ahead)
            
            query = Task.query.filter(
                and_(
                    Task.due_date >= today,
                    Task.due_date <= end_date,
                    Task.assigned_to == user_id,
                    Task.status.in_([TaskStatus.PENDING, TaskStatus.IN_PROGRESS]),
                    Task.is_active == True
                )
            ).order_by(Task.due_date.asc(), Task.due_time.asc().nullsfirst())
            
            tasks = query.all()
            return [task.to_dict() for task in tasks]
            
        except Exception as e:
            logger.error(f"Erro ao buscar próximas tarefas: {e}")
            return []
    
    def _create_recurring_tasks(self, parent_task: Task):
        """Cria tarefas recorrentes"""
        if not parent_task.is_recurring or parent_task.recurrence_type == RecurrenceType.NONE:
            return
        
        try:
            current_date = parent_task.due_date
            end_date = parent_task.recurrence_end_date or (current_date + timedelta(days=365))  # Máximo 1 ano
            interval = parent_task.recurrence_interval or 1
            
            created_count = 0
            max_tasks = 50  # Limite de segurança
            
            while current_date <= end_date and created_count < max_tasks:
                # Calcular próxima data
                if parent_task.recurrence_type == RecurrenceType.DAILY:
                    current_date += timedelta(days=interval)
                elif parent_task.recurrence_type == RecurrenceType.WEEKLY:
                    current_date += timedelta(weeks=interval)
                elif parent_task.recurrence_type == RecurrenceType.MONTHLY:
                    # Aproximação para meses
                    current_date += timedelta(days=30 * interval)
                elif parent_task.recurrence_type == RecurrenceType.YEARLY:
                    current_date += timedelta(days=365 * interval)
                
                if current_date > end_date:
                    break
                
                # Criar tarefa recorrente
                recurring_task = Task(
                    title=parent_task.title,
                    description=parent_task.description,
                    task_type=parent_task.task_type,
                    category=parent_task.category,
                    priority=parent_task.priority,
                    due_date=current_date,
                    due_time=parent_task.due_time,
                    duration_minutes=parent_task.duration_minutes,
                    lead_id=parent_task.lead_id,
                    opportunity_id=parent_task.opportunity_id,
                    assigned_to=parent_task.assigned_to,
                    created_by=parent_task.created_by,
                    parent_task_id=parent_task.id,
                    reminder_minutes=parent_task.reminder_minutes,
                    email_reminder=parent_task.email_reminder,
                    sms_reminder=parent_task.sms_reminder,
                    location=parent_task.location,
                    address=parent_task.address,
                    contact_phone=parent_task.contact_phone,
                    contact_email=parent_task.contact_email,
                    tags=parent_task.tags.copy() if parent_task.tags else [],
                    custom_fields=parent_task.custom_fields.copy() if parent_task.custom_fields else {}
                )
                
                db.session.add(recurring_task)
                created_count += 1
            
            logger.info(f"Criadas {created_count} tarefas recorrentes para a tarefa {parent_task.id}")
            
        except Exception as e:
            logger.error(f"Erro ao criar tarefas recorrentes: {e}")

class NotificationService:
    """Serviço para notificações de tarefas"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
    
    def send_task_assignment_notification(self, task: Task):
        """Envia notificação de atribuição de tarefa"""
        if not task.assignee or not task.assignee.email:
            return
        
        try:
            subject = f"Nova tarefa atribuída: {task.title}"
            
            content = f"""
            <h2>Nova Tarefa Atribuída</h2>
            <p><strong>Título:</strong> {task.title}</p>
            <p><strong>Descrição:</strong> {task.description or 'Sem descrição'}</p>
            <p><strong>Tipo:</strong> {task.task_type.value if task.task_type else 'N/A'}</p>
            <p><strong>Prioridade:</strong> {task.priority.value if task.priority else 'N/A'}</p>
            <p><strong>Vencimento:</strong> {task.due_date.strftime('%d/%m/%Y') if task.due_date else 'Sem data'}</p>
            
            {f'<p><strong>Lead:</strong> {task.lead.name}</p>' if task.lead else ''}
            {f'<p><strong>Localização:</strong> {task.location}</p>' if task.location else ''}
            
            <p>Acesse o CRM para mais detalhes.</p>
            """
            
            self._send_email(task.assignee.email, subject, content)
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de atribuição: {e}")
    
    def send_task_unassignment_notification(self, task: Task, old_assignee_id: str):
        """Envia notificação de remoção de atribuição"""
        try:
            old_assignee = User.query.get(old_assignee_id)
            if not old_assignee or not old_assignee.email:
                return
            
            subject = f"Tarefa removida: {task.title}"
            
            content = f"""
            <h2>Tarefa Removida</h2>
            <p>A tarefa "<strong>{task.title}</strong>" foi removida de você e atribuída a outro usuário.</p>
            <p>Se você tinha trabalho em andamento nesta tarefa, entre em contato com seu supervisor.</p>
            """
            
            self._send_email(old_assignee.email, subject, content)
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de remoção: {e}")
    
    def send_priority_change_notification(self, task: Task):
        """Envia notificação de mudança de prioridade"""
        if not task.assignee or not task.assignee.email:
            return
        
        try:
            subject = f"Prioridade alterada: {task.title}"
            
            priority_text = "ALTA" if task.priority == TaskPriority.HIGH else "URGENTE"
            
            content = f"""
            <h2>Prioridade da Tarefa Alterada</h2>
            <p>A tarefa "<strong>{task.title}</strong>" teve sua prioridade alterada para <strong>{priority_text}</strong>.</p>
            <p><strong>Vencimento:</strong> {task.due_date.strftime('%d/%m/%Y') if task.due_date else 'Sem data'}</p>
            <p>Por favor, priorize esta tarefa em sua agenda.</p>
            """
            
            self._send_email(task.assignee.email, subject, content)
            
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de prioridade: {e}")
    
    def schedule_reminder(self, task: Task):
        """Agenda lembrete para uma tarefa"""
        # Por enquanto apenas log. Implementar com Celery ou similar
        logger.info(f"Lembrete agendado para tarefa {task.id} em {task.reminder_minutes} minutos antes do vencimento")
    
    def _send_email(self, to_email: str, subject: str, content: str):
        """Envia email"""
        if not self.smtp_username or not self.smtp_password:
            logger.warning("Configurações SMTP não encontradas")
            return
        
        try:
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            
            html_part = MimeText(content, 'html', 'utf-8')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email enviado para {to_email}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")

class CalendarService:
    """Serviço para integração com calendários"""
    
    def create_event(self, task: Task) -> Dict[str, Any]:
        """Cria evento no calendário"""
        # Por enquanto apenas simulação
        # Implementar integração com Google Calendar, Outlook, etc.
        
        return {
            'success': True,
            'event_id': f"cal_event_{task.id}",
            'provider': 'google',
            'message': 'Evento criado no calendário (simulado)'
        }
    
    def update_event(self, task: Task) -> Dict[str, Any]:
        """Atualiza evento no calendário"""
        return {
            'success': True,
            'message': 'Evento atualizado no calendário (simulado)'
        }
    
    def delete_event(self, task: Task) -> Dict[str, Any]:
        """Remove evento do calendário"""
        return {
            'success': True,
            'message': 'Evento removido do calendário (simulado)'
        }

