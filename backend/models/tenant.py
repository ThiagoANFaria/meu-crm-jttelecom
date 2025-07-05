from . import db
from datetime import datetime

class Tenant(db.Model):
    __tablename__ = 'tenants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), unique=True, nullable=False)
    admin_email = db.Column(db.String(120), nullable=False)
    admin_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, suspended, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    users = db.relationship('User', backref='tenant_ref', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'admin_email': self.admin_email,
            'admin_name': self.admin_name,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'users_count': len(self.users) if self.users else 0
        }
    
    def __repr__(self):
        return f'<Tenant {self.name}>'

