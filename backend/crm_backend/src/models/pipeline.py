from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Import db from user model to maintain consistency
from src.models.user import db

class Pipeline(db.Model):
    """Funil de vendas (Pipeline)"""
    __tablename__ = 'pipelines'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    pipeline_type = db.Column(db.String(20), nullable=False)  # 'prospection' or 'sales'
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_pipelines', foreign_keys=[created_by])
    stages = db.relationship('PipelineStage', backref='pipeline', cascade='all, delete-orphan', order_by='PipelineStage.order')
    opportunities = db.relationship('Opportunity', backref='pipeline', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pipeline {self.name} ({self.pipeline_type})>'

    def to_dict(self, include_stages=True, include_stats=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'pipeline_type': self.pipeline_type,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'creator': {
                'id': self.creator.id,
                'first_name': self.creator.first_name,
                'last_name': self.creator.last_name,
                'email': self.creator.email
            } if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_stages:
            data['stages'] = [stage.to_dict() for stage in self.stages]
        
        if include_stats:
            data['stats'] = self.get_stats()
        
        return data

    def get_stats(self):
        """Get pipeline statistics"""
        total_opportunities = len(self.opportunities)
        total_value = sum(opp.value or 0 for opp in self.opportunities if opp.value)
        
        # Stats by stage
        stage_stats = {}
        for stage in self.stages:
            stage_opportunities = [opp for opp in self.opportunities if opp.stage_id == stage.id]
            stage_stats[stage.name] = {
                'count': len(stage_opportunities),
                'value': sum(opp.value or 0 for opp in stage_opportunities if opp.value)
            }
        
        return {
            'total_opportunities': total_opportunities,
            'total_value': total_value,
            'stage_stats': stage_stats
        }

class PipelineStage(db.Model):
    """Etapa do funil"""
    __tablename__ = 'pipeline_stages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pipeline_id = db.Column(db.String(36), db.ForeignKey('pipelines.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(7), default='#3B82F6')  # Hex color
    is_final = db.Column(db.Boolean, default=False)  # Indicates if this is a final stage (won/lost)
    stage_type = db.Column(db.String(20), default='active')  # 'active', 'won', 'lost'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    opportunities = db.relationship('Opportunity', backref='stage', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<PipelineStage {self.name} (Order: {self.order})>'

    def to_dict(self, include_opportunities=False):
        data = {
            'id': self.id,
            'pipeline_id': self.pipeline_id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'color': self.color,
            'is_final': self.is_final,
            'stage_type': self.stage_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_opportunities:
            data['opportunities'] = [opp.to_dict() for opp in self.opportunities]
            data['opportunity_count'] = len(self.opportunities)
            data['total_value'] = sum(opp.value or 0 for opp in self.opportunities if opp.value)
        
        return data

class Product(db.Model):
    """Produto/Serviço"""
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': float(self.price) if self.price else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Association table for opportunity-products many-to-many relationship
opportunity_products = db.Table('opportunity_products',
    db.Column('opportunity_id', db.String(36), db.ForeignKey('opportunities.id'), primary_key=True),
    db.Column('product_id', db.String(36), db.ForeignKey('products.id'), primary_key=True),
    db.Column('quantity', db.Integer, default=1),
    db.Column('unit_price', db.Numeric(10, 2)),
    db.Column('total_price', db.Numeric(10, 2))
)

class Opportunity(db.Model):
    """Oportunidade de venda"""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'), nullable=False)
    pipeline_id = db.Column(db.String(36), db.ForeignKey('pipelines.id'), nullable=False)
    stage_id = db.Column(db.String(36), db.ForeignKey('pipeline_stages.id'), nullable=False)
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # Financial information
    value = db.Column(db.Numeric(12, 2))  # Total opportunity value
    probability = db.Column(db.Integer, default=0)  # Probability of closing (0-100%)
    expected_close_date = db.Column(db.Date)
    actual_close_date = db.Column(db.Date)
    
    # Status and tracking
    status = db.Column(db.String(20), default='open')  # 'open', 'won', 'lost'
    priority = db.Column(db.String(10), default='medium')  # 'low', 'medium', 'high'
    source = db.Column(db.String(50))  # Where the opportunity came from
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = db.relationship('Lead', backref='opportunities')
    assigned_user = db.relationship('User', backref='assigned_opportunities', foreign_keys=[assigned_to])
    products = db.relationship('Product', secondary=opportunity_products, backref='opportunities')

    def __repr__(self):
        return f'<Opportunity {self.title} - {self.value}>'

    def calculate_total_value(self):
        """Calculate total value based on products"""
        # This would be implemented with proper product pricing logic
        # For now, return the manually set value
        return self.value or 0

    def get_products_summary(self):
        """Get summary of products in this opportunity"""
        if not self.products:
            return {
                'total_products': 0,
                'total_quantity': 0,
                'total_value': 0,
                'products': []
            }
        
        # For now, return basic info since we need to implement the association table properly
        return {
            'total_products': len(self.products),
            'total_quantity': len(self.products),  # Simplified
            'total_value': float(self.value or 0),
            'products': [product.to_dict() for product in self.products]
        }

    def to_dict(self, include_lead=True, include_products=True):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'lead_id': self.lead_id,
            'pipeline_id': self.pipeline_id,
            'stage_id': self.stage_id,
            'assigned_to': self.assigned_to,
            'value': float(self.value) if self.value else None,
            'probability': self.probability,
            'expected_close_date': self.expected_close_date.isoformat() if self.expected_close_date else None,
            'actual_close_date': self.actual_close_date.isoformat() if self.actual_close_date else None,
            'status': self.status,
            'priority': self.priority,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_lead and self.lead:
            data['lead'] = {
                'id': self.lead.id,
                'name': self.lead.name,
                'company_name': self.lead.company_name,
                'email': self.lead.email,
                'phone': self.lead.phone
            }
        
        if self.assigned_user:
            data['assigned_user'] = {
                'id': self.assigned_user.id,
                'first_name': self.assigned_user.first_name,
                'last_name': self.assigned_user.last_name,
                'email': self.assigned_user.email
            }
        
        if self.stage:
            data['stage'] = {
                'id': self.stage.id,
                'name': self.stage.name,
                'color': self.stage.color,
                'order': self.stage.order,
                'stage_type': self.stage.stage_type
            }
        
        if include_products:
            data['products_summary'] = self.get_products_summary()
        
        return data

