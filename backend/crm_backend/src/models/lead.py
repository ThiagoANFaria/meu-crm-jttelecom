"""
Modelo para Leads
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Lead(db.Model):
    """Modelo para Leads"""
    __tablename__ = 'leads'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Campos obrigatórios
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    
    # Dados da empresa
    company_name = db.Column(db.String(200))  # Razão Social
    cnpj_cpf = db.Column(db.String(20))
    ie_rg = db.Column(db.String(20))
    
    # Endereço completo
    address = db.Column(db.String(300))
    address_number = db.Column(db.String(10))
    neighborhood = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(10))
    
    # Status e classificação
    status = db.Column(db.String(50), default='novo')
    source = db.Column(db.String(100))  # Origem do lead
    score = db.Column(db.Integer, default=0)  # Lead scoring
    tags = db.Column(db.Text)  # JSON com tags
    
    # Campos personalizados
    custom_fields = db.Column(db.Text)  # JSON com campos adicionais
    
    # Relacionamentos
    owner_id = db.Column(db.String(36))  # Responsável pelo lead
    tenant_id = db.Column(db.String(36), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contact = db.Column(db.DateTime)
    
    def to_dict(self):
        """Converte o lead para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'whatsapp': self.whatsapp,
            'company_name': self.company_name,
            'cnpj_cpf': self.cnpj_cpf,
            'status': self.status,
            'source': self.source,
            'score': self.score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

