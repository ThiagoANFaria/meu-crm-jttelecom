from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Multi-tenant fields
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=True)
    user_level = db.Column(db.String(20), nullable=False, default='user')  # master, admin, user
    
    # Status and metadata
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Define a senha do usuário"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def is_master(self):
        """Verifica se é Admin Master"""
        return self.user_level == 'master'
    
    def is_tenant_admin(self):
        """Verifica se é Admin da Tenant"""
        return self.user_level == 'admin'
    
    def is_user(self):
        """Verifica se é usuário final"""
        return self.user_level == 'user'
    
    def can_manage_tenants(self):
        """Verifica se pode gerenciar tenants"""
        return self.user_level == 'master'
    
    def can_manage_users(self):
        """Verifica se pode gerenciar usuários"""
        return self.user_level in ['master', 'admin']
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'user_level': self.user_level,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if self.tenant_id:
            data['tenant_id'] = self.tenant_id
            if hasattr(self, 'tenant_ref') and self.tenant_ref:
                data['tenant_name'] = self.tenant_ref.name
        
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'

