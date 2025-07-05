"""
Modelos para Tarefas e Atividades
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Task(db.Model):
    """Modelo para Tarefas"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Status e prioridade
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    priority = db.Column(db.String(10), default='medium')  # low, medium, high, urgent
    
    # Datas
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relacionamentos
    assigned_to = db.Column(db.String(36), nullable=False)  # Usuário responsável
    created_by = db.Column(db.String(36), nullable=False)  # Quem criou
    lead_id = db.Column(db.String(36))  # Lead relacionado (opcional)
    opportunity_id = db.Column(db.String(36))  # Oportunidade relacionada (opcional)
    tenant_id = db.Column(db.String(36), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    comments = db.relationship('TaskComment', backref='task', lazy=True, cascade='all, delete-orphan')
    time_logs = db.relationship('TimeLog', backref='task', lazy=True, cascade='all, delete-orphan')

class TaskComment(db.Model):
    """Modelo para Comentários de Tarefas"""
    __tablename__ = 'task_comments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'), nullable=False)
    author_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TimeLog(db.Model):
    """Modelo para Log de Tempo"""
    __tablename__ = 'time_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = db.Column(db.String(500))
    hours = db.Column(db.Decimal(4, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Activity(db.Model):
    """Modelo para Atividades/Histórico"""
    __tablename__ = 'activities'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.String(50), nullable=False)  # call, email, meeting, note, etc.
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Relacionamentos
    lead_id = db.Column(db.String(36))
    opportunity_id = db.Column(db.String(36))
    user_id = db.Column(db.String(36), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_at = db.Column(db.DateTime)  # Para atividades agendadas

