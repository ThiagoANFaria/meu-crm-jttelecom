"""
Modelos para Pipeline e Funis de Vendas
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Pipeline(db.Model):
    """Modelo para Pipeline de Vendas"""
    __tablename__ = 'pipelines'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    tenant_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    stages = db.relationship('PipelineStage', backref='pipeline', lazy=True, cascade='all, delete-orphan')
    opportunities = db.relationship('Opportunity', backref='pipeline', lazy=True)

class PipelineStage(db.Model):
    """Modelo para Estágios do Pipeline"""
    __tablename__ = 'pipeline_stages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(7), default='#4169E1')  # Azul Royal
    pipeline_id = db.Column(db.String(36), db.ForeignKey('pipelines.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    opportunities = db.relationship('Opportunity', backref='stage', lazy=True)

class Opportunity(db.Model):
    """Modelo para Oportunidades"""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    value = db.Column(db.Decimal(10, 2))
    probability = db.Column(db.Integer, default=0)  # 0-100%
    expected_close_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='open')  # open, won, lost
    
    # Relacionamentos
    pipeline_id = db.Column(db.String(36), db.ForeignKey('pipelines.id'), nullable=False)
    stage_id = db.Column(db.String(36), db.ForeignKey('pipeline_stages.id'), nullable=False)
    lead_id = db.Column(db.String(36), nullable=False)  # Referência ao Lead
    owner_id = db.Column(db.String(36), nullable=False)  # Responsável
    tenant_id = db.Column(db.String(36), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Model):
    """Modelo para Produtos"""
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Decimal(10, 2))
    category = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    tenant_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

