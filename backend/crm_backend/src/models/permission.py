"""
Modelo para Permissões
"""
from datetime import datetime

class Permission:
    """Modelo para permissões do sistema"""
    
    def __init__(self, id=None, name=None, description=None, resource=None, action=None):
        self.id = id
        self.name = name
        self.description = description
        self.resource = resource
        self.action = action
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'resource': self.resource,
            'action': self.action,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Role:
    """Modelo para papéis/roles do sistema"""
    
    def __init__(self, id=None, name=None, description=None, permissions=None):
        self.id = id
        self.name = name
        self.description = description
        self.permissions = permissions or []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': [p.to_dict() if hasattr(p, 'to_dict') else p for p in self.permissions],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

