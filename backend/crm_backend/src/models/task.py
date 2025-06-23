from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, Enum, Date, Time
from sqlalchemy.orm import relationship
from src.models.user import db
from datetime import datetime, date, time
import uuid
import enum

class TaskType(enum.Enum):
    """Tipos de tarefas"""
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    VISIT = "visit"
    WHATSAPP = "whatsapp"
    SMS = "sms"
    FOLLOW_UP = "follow_up"
    DEMO = "demo"
    PROPOSAL = "proposal"
    CONTRACT = "contract"
    NEGOTIATION = "negotiation"
    ONBOARDING = "onboarding"
    SUPPORT = "support"
    OTHER = "other"

class TaskStatus(enum.Enum):
    """Status das tarefas"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"

class TaskPriority(enum.Enum):
    """Prioridades das tarefas"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class RecurrenceType(enum.Enum):
    """Tipos de recorrência"""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class Task(db.Model):
    """Tarefa/Atividade do CRM"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    
    # Tipo e categoria
    task_type = db.Column(db.Enum(TaskType), nullable=False, default=TaskType.FOLLOW_UP)
    category = db.Column(db.String(100))  # Categoria personalizada
    
    # Status e prioridade
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.MEDIUM)
    
    # Datas e horários
    due_date = db.Column(db.Date)  # Data de vencimento
    due_time = db.Column(db.Time)  # Horário de vencimento
    start_date = db.Column(db.Date)  # Data de início
    start_time = db.Column(db.Time)  # Horário de início
    duration_minutes = db.Column(db.Integer)  # Duração estimada em minutos
    
    # Datas de execução
    completed_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    
    # Relacionamentos principais
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'))
    opportunity_id = db.Column(db.String(36), db.ForeignKey('opportunities.id'))
    proposal_id = db.Column(db.String(36), db.ForeignKey('proposals.id'))
    contract_id = db.Column(db.String(36), db.ForeignKey('contracts.id'))
    
    # Atribuição
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Recorrência
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_type = db.Column(db.Enum(RecurrenceType), default=RecurrenceType.NONE)
    recurrence_interval = db.Column(db.Integer, default=1)  # A cada X dias/semanas/meses
    recurrence_end_date = db.Column(db.Date)
    parent_task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'))  # Para tarefas recorrentes
    
    # Notificações
    reminder_minutes = db.Column(db.Integer)  # Lembrete X minutos antes
    email_reminder = db.Column(db.Boolean, default=True)
    sms_reminder = db.Column(db.Boolean, default=False)
    
    # Localização (para visitas)
    location = db.Column(db.String(500))
    address = db.Column(db.Text)
    
    # Contatos relacionados
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(200))
    
    # Resultados e acompanhamento
    result = db.Column(db.Text)  # Resultado da atividade
    next_action = db.Column(db.Text)  # Próxima ação sugerida
    outcome = db.Column(db.String(100))  # success, failed, rescheduled, no_answer, etc.
    
    # Anexos e links
    attachments = db.Column(db.JSON, default=list)
    external_links = db.Column(db.JSON, default=list)
    
    # Integração com calendários
    calendar_event_id = db.Column(db.String(255))  # ID do evento no calendário externo
    calendar_provider = db.Column(db.String(50))  # google, outlook, etc.
    
    # Metadados
    tags = db.Column(db.JSON, default=list)
    custom_fields = db.Column(db.JSON, default=dict)
    
    # Controle
    is_active = db.Column(db.Boolean, default=True)
    is_template = db.Column(db.Boolean, default=False)  # Para templates de tarefas
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    lead = db.relationship('Lead', backref='tasks')
    opportunity = db.relationship('Opportunity', backref='tasks')
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_tasks')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_tasks')
    parent_task = db.relationship('Task', remote_side=[id], backref='recurring_tasks')
    comments = db.relationship('TaskComment', backref='task', cascade='all, delete-orphan')
    time_logs = db.relationship('TaskTimeLog', backref='task', cascade='all, delete-orphan')
    
    @property
    def is_overdue(self):
        """Verifica se a tarefa está atrasada"""
        if self.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return False
        
        if not self.due_date:
            return False
        
        now = datetime.now()
        due_datetime = datetime.combine(self.due_date, self.due_time or time(23, 59))
        
        return now > due_datetime
    
    @property
    def time_until_due(self):
        """Retorna tempo até o vencimento em minutos"""
        if not self.due_date:
            return None
        
        now = datetime.now()
        due_datetime = datetime.combine(self.due_date, self.due_time or time(23, 59))
        
        if now > due_datetime:
            return 0  # Já venceu
        
        delta = due_datetime - now
        return int(delta.total_seconds() / 60)
    
    @property
    def total_time_logged(self):
        """Retorna tempo total logado em minutos"""
        return sum(log.duration_minutes for log in self.time_logs)
    
    def mark_completed(self, result: str = None, outcome: str = None, next_action: str = None):
        """Marca tarefa como completada"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        
        if result:
            self.result = result
        if outcome:
            self.outcome = outcome
        if next_action:
            self.next_action = next_action
        
        self.updated_at = datetime.utcnow()
    
    def reschedule(self, new_due_date: date, new_due_time: time = None):
        """Reagenda a tarefa"""
        self.due_date = new_due_date
        if new_due_time:
            self.due_time = new_due_time
        
        self.status = TaskStatus.PENDING
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'task_type': self.task_type.value if self.task_type else None,
            'category': self.category,
            'status': self.status.value if self.status else None,
            'priority': self.priority.value if self.priority else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'due_time': self.due_time.isoformat() if self.due_time else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'duration_minutes': self.duration_minutes,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'lead_id': self.lead_id,
            'opportunity_id': self.opportunity_id,
            'proposal_id': self.proposal_id,
            'contract_id': self.contract_id,
            'assigned_to': self.assigned_to,
            'created_by': self.created_by,
            'is_recurring': self.is_recurring,
            'recurrence_type': self.recurrence_type.value if self.recurrence_type else None,
            'recurrence_interval': self.recurrence_interval,
            'recurrence_end_date': self.recurrence_end_date.isoformat() if self.recurrence_end_date else None,
            'parent_task_id': self.parent_task_id,
            'reminder_minutes': self.reminder_minutes,
            'email_reminder': self.email_reminder,
            'sms_reminder': self.sms_reminder,
            'location': self.location,
            'address': self.address,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'result': self.result,
            'next_action': self.next_action,
            'outcome': self.outcome,
            'attachments': self.attachments,
            'external_links': self.external_links,
            'calendar_event_id': self.calendar_event_id,
            'calendar_provider': self.calendar_provider,
            'tags': self.tags,
            'custom_fields': self.custom_fields,
            'is_active': self.is_active,
            'is_template': self.is_template,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_overdue': self.is_overdue,
            'time_until_due': self.time_until_due,
            'total_time_logged': self.total_time_logged,
            'assignee': {
                'id': self.assignee.id,
                'name': f"{self.assignee.first_name} {self.assignee.last_name}",
                'email': self.assignee.email
            } if self.assignee else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None,
            'lead': {
                'id': self.lead.id,
                'name': self.lead.name,
                'company': self.lead.company
            } if self.lead else None,
            'opportunity': {
                'id': self.opportunity.id,
                'title': self.opportunity.title
            } if self.opportunity else None
        }

class TaskComment(db.Model):
    """Comentário em uma tarefa"""
    __tablename__ = 'task_comments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'), nullable=False)
    
    # Conteúdo
    content = db.Column(db.Text, nullable=False)
    
    # Tipo de comentário
    comment_type = db.Column(db.String(50), default='comment')  # comment, status_change, reminder, etc.
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    author = db.relationship('User', backref='task_comments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'content': self.content,
            'comment_type': self.comment_type,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': {
                'id': self.author.id,
                'name': f"{self.author.first_name} {self.author.last_name}",
                'email': self.author.email
            } if self.author else None
        }

class TaskTimeLog(db.Model):
    """Log de tempo gasto em uma tarefa"""
    __tablename__ = 'task_time_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'), nullable=False)
    
    # Tempo
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)  # Calculado automaticamente
    
    # Descrição
    description = db.Column(db.Text)
    
    # Metadados
    logged_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    logger = db.relationship('User', backref='time_logs')
    
    def calculate_duration(self):
        """Calcula duração em minutos"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration_minutes = int(delta.total_seconds() / 60)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_minutes': self.duration_minutes,
            'description': self.description,
            'logged_by': self.logged_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'logger': {
                'id': self.logger.id,
                'name': f"{self.logger.first_name} {self.logger.last_name}"
            } if self.logger else None
        }

class TaskTemplate(db.Model):
    """Template de tarefa para reutilização"""
    __tablename__ = 'task_templates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Configuração do template
    title_template = db.Column(db.String(500), nullable=False)
    description_template = db.Column(db.Text)
    task_type = db.Column(db.Enum(TaskType), nullable=False)
    category = db.Column(db.String(100))
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.MEDIUM)
    
    # Configurações padrão
    default_duration_minutes = db.Column(db.Integer)
    default_reminder_minutes = db.Column(db.Integer)
    
    # Recorrência padrão
    default_recurrence_type = db.Column(db.Enum(RecurrenceType), default=RecurrenceType.NONE)
    default_recurrence_interval = db.Column(db.Integer, default=1)
    
    # Configurações de notificação
    default_email_reminder = db.Column(db.Boolean, default=True)
    default_sms_reminder = db.Column(db.Boolean, default=False)
    
    # Campos personalizados
    custom_fields_config = db.Column(db.JSON, default=dict)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=False)  # Disponível para todos os usuários
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='task_templates')
    
    def create_task_from_template(self, assigned_to: str, created_by: str, 
                                 lead_id: str = None, opportunity_id: str = None,
                                 due_date: date = None, custom_data: dict = None) -> 'Task':
        """Cria uma tarefa a partir do template"""
        custom_data = custom_data or {}
        
        # Renderizar templates com dados personalizados
        title = self._render_template(self.title_template, custom_data)
        description = self._render_template(self.description_template, custom_data) if self.description_template else None
        
        task = Task(
            title=title,
            description=description,
            task_type=self.task_type,
            category=self.category,
            priority=self.priority,
            assigned_to=assigned_to,
            created_by=created_by,
            lead_id=lead_id,
            opportunity_id=opportunity_id,
            due_date=due_date,
            duration_minutes=self.default_duration_minutes,
            reminder_minutes=self.default_reminder_minutes,
            email_reminder=self.default_email_reminder,
            sms_reminder=self.default_sms_reminder,
            is_recurring=self.default_recurrence_type != RecurrenceType.NONE,
            recurrence_type=self.default_recurrence_type,
            recurrence_interval=self.default_recurrence_interval,
            custom_fields=custom_data
        )
        
        return task
    
    def _render_template(self, template_str: str, data: dict) -> str:
        """Renderiza template com dados fornecidos"""
        if not template_str:
            return ""
        
        try:
            from jinja2 import Template
            template = Template(template_str)
            return template.render(**data)
        except Exception:
            return template_str
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'title_template': self.title_template,
            'description_template': self.description_template,
            'task_type': self.task_type.value if self.task_type else None,
            'category': self.category,
            'priority': self.priority.value if self.priority else None,
            'default_duration_minutes': self.default_duration_minutes,
            'default_reminder_minutes': self.default_reminder_minutes,
            'default_recurrence_type': self.default_recurrence_type.value if self.default_recurrence_type else None,
            'default_recurrence_interval': self.default_recurrence_interval,
            'default_email_reminder': self.default_email_reminder,
            'default_sms_reminder': self.default_sms_reminder,
            'custom_fields_config': self.custom_fields_config,
            'is_active': self.is_active,
            'is_public': self.is_public,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

class ActivitySummary(db.Model):
    """Resumo de atividades por usuário/período"""
    __tablename__ = 'activity_summaries'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Período
    summary_date = db.Column(db.Date, nullable=False)
    summary_type = db.Column(db.String(20), default='daily')  # daily, weekly, monthly
    
    # Estatísticas de tarefas
    tasks_created = db.Column(db.Integer, default=0)
    tasks_completed = db.Column(db.Integer, default=0)
    tasks_overdue = db.Column(db.Integer, default=0)
    
    # Estatísticas por tipo
    calls_made = db.Column(db.Integer, default=0)
    emails_sent = db.Column(db.Integer, default=0)
    meetings_held = db.Column(db.Integer, default=0)
    visits_made = db.Column(db.Integer, default=0)
    
    # Tempo total
    total_time_logged = db.Column(db.Integer, default=0)  # em minutos
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='activity_summaries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'summary_date': self.summary_date.isoformat() if self.summary_date else None,
            'summary_type': self.summary_type,
            'tasks_created': self.tasks_created,
            'tasks_completed': self.tasks_completed,
            'tasks_overdue': self.tasks_overdue,
            'calls_made': self.calls_made,
            'emails_sent': self.emails_sent,
            'meetings_held': self.meetings_held,
            'visits_made': self.visits_made,
            'total_time_logged': self.total_time_logged,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': {
                'id': self.user.id,
                'name': f"{self.user.first_name} {self.user.last_name}"
            } if self.user else None
        }

