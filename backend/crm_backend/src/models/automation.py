from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.models.user import db
from datetime import datetime
import uuid
import enum

class TriggerType(enum.Enum):
    """Tipos de gatilhos para automações"""
    LEAD_CREATED = "lead_created"
    LEAD_STATUS_CHANGED = "lead_status_changed"
    LEAD_STAGE_CHANGED = "lead_stage_changed"
    OPPORTUNITY_CREATED = "opportunity_created"
    OPPORTUNITY_STAGE_CHANGED = "opportunity_stage_changed"
    PROPOSAL_SENT = "proposal_sent"
    PROPOSAL_VIEWED = "proposal_viewed"
    CONTRACT_SIGNED = "contract_signed"
    CALL_COMPLETED = "call_completed"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    TASK_COMPLETED = "task_completed"
    TIME_BASED = "time_based"
    INACTIVITY = "inactivity"

class ActionType(enum.Enum):
    """Tipos de ações para automações"""
    SEND_EMAIL = "send_email"
    CREATE_TASK = "create_task"
    UPDATE_LEAD_STATUS = "update_lead_status"
    MOVE_LEAD_STAGE = "move_lead_stage"
    ASSIGN_USER = "assign_user"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    CREATE_OPPORTUNITY = "create_opportunity"
    SEND_SMS = "send_sms"
    SEND_WHATSAPP = "send_whatsapp"
    WEBHOOK = "webhook"
    WAIT = "wait"

class AutomationRule(db.Model):
    """Regra de automação"""
    __tablename__ = 'automation_rules'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Configuração do gatilho
    trigger_type = db.Column(db.Enum(TriggerType), nullable=False)
    trigger_conditions = db.Column(db.JSON, default=dict)  # Condições específicas do gatilho
    
    # Configuração de filtros
    filters = db.Column(db.JSON, default=dict)  # Filtros para aplicar a regra
    
    # Configuração de timing
    delay_minutes = db.Column(db.Integer, default=0)  # Atraso antes de executar
    
    # Status e controle
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=1)  # Prioridade de execução
    
    # Estatísticas
    execution_count = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    last_executed_at = db.Column(db.DateTime)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='automation_rules')
    actions = db.relationship('AutomationAction', backref='rule', cascade='all, delete-orphan')
    executions = db.relationship('AutomationExecution', backref='rule', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'trigger_type': self.trigger_type.value if self.trigger_type else None,
            'trigger_conditions': self.trigger_conditions,
            'filters': self.filters,
            'delay_minutes': self.delay_minutes,
            'is_active': self.is_active,
            'priority': self.priority,
            'execution_count': self.execution_count,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'last_executed_at': self.last_executed_at.isoformat() if self.last_executed_at else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'actions': [action.to_dict() for action in self.actions],
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

class AutomationAction(db.Model):
    """Ação de uma automação"""
    __tablename__ = 'automation_actions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id = db.Column(db.String(36), db.ForeignKey('automation_rules.id'), nullable=False)
    
    # Configuração da ação
    action_type = db.Column(db.Enum(ActionType), nullable=False)
    action_config = db.Column(db.JSON, default=dict)  # Configuração específica da ação
    
    # Ordem de execução
    order = db.Column(db.Integer, default=1)
    
    # Condições para execução da ação
    conditions = db.Column(db.JSON, default=dict)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'action_type': self.action_type.value if self.action_type else None,
            'action_config': self.action_config,
            'order': self.order,
            'conditions': self.conditions,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AutomationExecution(db.Model):
    """Execução de uma automação"""
    __tablename__ = 'automation_executions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id = db.Column(db.String(36), db.ForeignKey('automation_rules.id'), nullable=False)
    
    # Contexto da execução
    trigger_data = db.Column(db.JSON, default=dict)  # Dados que dispararam a automação
    target_type = db.Column(db.String(50))  # lead, opportunity, etc.
    target_id = db.Column(db.String(36))  # ID do objeto alvo
    
    # Status da execução
    status = db.Column(db.String(50), default='pending')  # pending, running, completed, failed, cancelled
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Resultados
    actions_executed = db.Column(db.Integer, default=0)
    actions_successful = db.Column(db.Integer, default=0)
    actions_failed = db.Column(db.Integer, default=0)
    
    # Logs e erros
    execution_log = db.Column(db.JSON, default=list)
    error_message = db.Column(db.Text)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'trigger_data': self.trigger_data,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'actions_executed': self.actions_executed,
            'actions_successful': self.actions_successful,
            'actions_failed': self.actions_failed,
            'execution_log': self.execution_log,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class EmailCampaign(db.Model):
    """Campanha de email para automações"""
    __tablename__ = 'email_campaigns'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Configuração do email
    subject = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)  # HTML content
    sender_name = db.Column(db.String(200))
    sender_email = db.Column(db.String(200))
    reply_to = db.Column(db.String(200))
    
    # Configuração de tracking
    track_opens = db.Column(db.Boolean, default=True)
    track_clicks = db.Column(db.Boolean, default=True)
    
    # Estatísticas
    sent_count = db.Column(db.Integer, default=0)
    delivered_count = db.Column(db.Integer, default=0)
    opened_count = db.Column(db.Integer, default=0)
    clicked_count = db.Column(db.Integer, default=0)
    bounced_count = db.Column(db.Integer, default=0)
    unsubscribed_count = db.Column(db.Integer, default=0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='email_campaigns')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'subject': self.subject,
            'content': self.content,
            'sender_name': self.sender_name,
            'sender_email': self.sender_email,
            'reply_to': self.reply_to,
            'track_opens': self.track_opens,
            'track_clicks': self.track_clicks,
            'sent_count': self.sent_count,
            'delivered_count': self.delivered_count,
            'opened_count': self.opened_count,
            'clicked_count': self.clicked_count,
            'bounced_count': self.bounced_count,
            'unsubscribed_count': self.unsubscribed_count,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

class CadenceSequence(db.Model):
    """Sequência de cadência para follow-up automático"""
    __tablename__ = 'cadence_sequences'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Configuração da cadência
    trigger_conditions = db.Column(db.JSON, default=dict)  # Condições para iniciar a cadência
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Estatísticas
    enrolled_count = db.Column(db.Integer, default=0)
    completed_count = db.Column(db.Integer, default=0)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='cadence_sequences')
    steps = db.relationship('CadenceStep', backref='sequence', cascade='all, delete-orphan')
    enrollments = db.relationship('CadenceEnrollment', backref='sequence', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'trigger_conditions': self.trigger_conditions,
            'is_active': self.is_active,
            'enrolled_count': self.enrolled_count,
            'completed_count': self.completed_count,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'steps': [step.to_dict() for step in sorted(self.steps, key=lambda x: x.order)],
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

class CadenceStep(db.Model):
    """Passo de uma sequência de cadência"""
    __tablename__ = 'cadence_steps'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sequence_id = db.Column(db.String(36), db.ForeignKey('cadence_sequences.id'), nullable=False)
    
    # Configuração do passo
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    
    # Timing
    delay_days = db.Column(db.Integer, default=0)
    delay_hours = db.Column(db.Integer, default=0)
    delay_minutes = db.Column(db.Integer, default=0)
    
    # Ação do passo
    action_type = db.Column(db.Enum(ActionType), nullable=False)
    action_config = db.Column(db.JSON, default=dict)
    
    # Condições para execução
    conditions = db.Column(db.JSON, default=dict)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sequence_id': self.sequence_id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'delay_days': self.delay_days,
            'delay_hours': self.delay_hours,
            'delay_minutes': self.delay_minutes,
            'action_type': self.action_type.value if self.action_type else None,
            'action_config': self.action_config,
            'conditions': self.conditions,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CadenceEnrollment(db.Model):
    """Inscrição de um lead em uma sequência de cadência"""
    __tablename__ = 'cadence_enrollments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sequence_id = db.Column(db.String(36), db.ForeignKey('cadence_sequences.id'), nullable=False)
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'), nullable=False)
    
    # Status da inscrição
    status = db.Column(db.String(50), default='active')  # active, paused, completed, cancelled
    current_step = db.Column(db.Integer, default=1)
    
    # Timing
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    next_action_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Estatísticas
    steps_completed = db.Column(db.Integer, default=0)
    emails_sent = db.Column(db.Integer, default=0)
    emails_opened = db.Column(db.Integer, default=0)
    emails_clicked = db.Column(db.Integer, default=0)
    tasks_created = db.Column(db.Integer, default=0)
    
    # Metadados
    enrolled_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    lead = db.relationship('Lead', backref='cadence_enrollments')
    enrollee = db.relationship('User', backref='cadence_enrollments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'sequence_id': self.sequence_id,
            'lead_id': self.lead_id,
            'status': self.status,
            'current_step': self.current_step,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
            'next_action_at': self.next_action_at.isoformat() if self.next_action_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'steps_completed': self.steps_completed,
            'emails_sent': self.emails_sent,
            'emails_opened': self.emails_opened,
            'emails_clicked': self.emails_clicked,
            'tasks_created': self.tasks_created,
            'enrolled_by': self.enrolled_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'lead': {
                'id': self.lead.id,
                'name': self.lead.name,
                'email': self.lead.email
            } if self.lead else None,
            'sequence': {
                'id': self.sequence.id,
                'name': self.sequence.name
            } if self.sequence else None
        }

