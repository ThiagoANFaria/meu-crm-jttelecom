from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import json

# Import db from user model to maintain consistency
from src.models.user import db

# Association table for lead-tags many-to-many relationship
lead_tags = db.Table('lead_tags',
    db.Column('lead_id', db.String(36), db.ForeignKey('leads.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Campos padrão obrigatórios
    name = db.Column(db.String(255), nullable=False)  # Nome
    contact = db.Column(db.String(255))  # Contato (pessoa de contato)
    email = db.Column(db.String(255))  # E-mail
    whatsapp = db.Column(db.String(20))  # WhatsApp
    
    # Dados da empresa/pessoa
    company_name = db.Column(db.String(255))  # Razão Social
    cnpj_cpf = db.Column(db.String(18))  # CNPJ/CPF
    ie_rg = db.Column(db.String(20))  # IE/RG
    phone = db.Column(db.String(20))  # Telefone
    
    # Endereço completo
    address_street = db.Column(db.String(255))  # Endereço (rua)
    address_number = db.Column(db.String(10))  # Número
    address_complement = db.Column(db.String(100))  # Complemento
    address_neighborhood = db.Column(db.String(100))  # Bairro
    address_city = db.Column(db.String(100))  # Cidade
    address_state = db.Column(db.String(2))  # Estado (UF)
    address_zipcode = db.Column(db.String(10))  # CEP
    
    # Campos do sistema original (mantidos para compatibilidade)
    position = db.Column(db.String(100))  # Cargo
    origin = db.Column(db.String(100))  # Origem
    product_interest = db.Column(db.Text)  # Produto de interesse
    status = db.Column(db.String(50), nullable=False, default='Novo')
    observations = db.Column(db.Text)  # Observações
    
    # Campos adicionais opcionais (JSON flexível)
    additional_fields = db.Column(db.JSON, default=dict)  # Campos customizados
    
    # Sistema de scoring e controle
    score = db.Column(db.Integer, default=0)
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assigned_user = db.relationship('User', backref='assigned_leads', foreign_keys=[assigned_to])
    tags = db.relationship('Tag', secondary=lead_tags, backref='leads')

    def calculate_score(self):
        """Calculate lead score based on various criteria."""
        score = 0
        
        # Base score for having contact information
        if self.email:
            score += 10
        if self.phone:
            score += 10
        if self.whatsapp:
            score += 8
        if self.company_name:
            score += 15
        if self.cnpj_cpf:
            score += 20  # CNPJ/CPF indicates business/personal lead
        
        # Complete address information
        address_fields = [self.address_street, self.address_city, self.address_state, self.address_zipcode]
        complete_address_count = sum(1 for field in address_fields if field)
        score += complete_address_count * 3  # Up to 12 points for complete address
        
        # Score based on origin
        origin_scores = {
            'Site': 15,
            'Indicação': 25,
            'Campanha': 20,
            'LinkedIn': 18,
            'Cold Call': 10,
            'Email Marketing': 12,
            'Evento': 22,
            'Parceiro': 30,
            'WhatsApp': 16
        }
        score += origin_scores.get(self.origin, 5)
        
        # Score based on product interest
        if self.product_interest:
            if len(self.product_interest) > 50:  # Detailed interest
                score += 15
            else:
                score += 8
        
        # Score based on position (decision makers get higher scores)
        decision_maker_keywords = [
            'CEO', 'CTO', 'CFO', 'Diretor', 'Gerente', 'Coordenador',
            'Supervisor', 'Responsável', 'Head', 'VP', 'Vice-Presidente',
            'Proprietário', 'Sócio', 'Presidente'
        ]
        if self.position:
            for keyword in decision_maker_keywords:
                if keyword.lower() in self.position.lower():
                    score += 20
                    break
            else:
                score += 5  # Any position is better than none
        
        # Score based on engagement (status progression)
        status_scores = {
            'Novo': 0,
            'Contatado': 10,
            'Qualificado': 20,
            'Interessado': 30,
            'Proposta': 40,
            'Negociação': 50,
            'Fechado': 100,
            'Perdido': -10
        }
        score += status_scores.get(self.status, 0)
        
        # Bonus for having tags (indicates categorization/attention)
        if self.tags:
            score += len(self.tags) * 5
        
        # Bonus for additional fields (shows detailed information)
        if self.additional_fields:
            score += len(self.additional_fields) * 2
        
        # Ensure score is within reasonable bounds
        self.score = max(0, min(100, score))
        return self.score

    def update_score(self):
        """Update the lead score and save to database."""
        self.calculate_score()
        db.session.commit()

    def set_additional_field(self, field_name, field_value):
        """Set an additional field value."""
        if not self.additional_fields:
            self.additional_fields = {}
        self.additional_fields[field_name] = field_value

    def get_additional_field(self, field_name, default=None):
        """Get an additional field value."""
        if not self.additional_fields:
            return default
        return self.additional_fields.get(field_name, default)

    def remove_additional_field(self, field_name):
        """Remove an additional field."""
        if self.additional_fields and field_name in self.additional_fields:
            del self.additional_fields[field_name]

    def get_full_address(self):
        """Get formatted full address."""
        address_parts = []
        
        if self.address_street:
            street_part = self.address_street
            if self.address_number:
                street_part += f", {self.address_number}"
            if self.address_complement:
                street_part += f", {self.address_complement}"
            address_parts.append(street_part)
        
        if self.address_neighborhood:
            address_parts.append(self.address_neighborhood)
        
        if self.address_city:
            city_part = self.address_city
            if self.address_state:
                city_part += f" - {self.address_state}"
            address_parts.append(city_part)
        
        if self.address_zipcode:
            address_parts.append(f"CEP: {self.address_zipcode}")
        
        return ", ".join(address_parts) if address_parts else None

    def __repr__(self):
        return f'<Lead {self.name} - {self.company_name or "Pessoa Física"}>'

    def to_dict(self, include_sensitive=False):
        """Convert lead to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'email': self.email,
            'whatsapp': self.whatsapp,
            'company_name': self.company_name,
            'cnpj_cpf': self.cnpj_cpf,
            'ie_rg': self.ie_rg,
            'phone': self.phone,
            'address': {
                'street': self.address_street,
                'number': self.address_number,
                'complement': self.address_complement,
                'neighborhood': self.address_neighborhood,
                'city': self.address_city,
                'state': self.address_state,
                'zipcode': self.address_zipcode,
                'full_address': self.get_full_address()
            },
            'position': self.position,
            'origin': self.origin,
            'product_interest': self.product_interest,
            'status': self.status,
            'observations': self.observations,
            'additional_fields': self.additional_fields or {},
            'score': self.score,
            'assigned_to': self.assigned_to,
            'assigned_user': {
                'id': self.assigned_user.id,
                'first_name': self.assigned_user.first_name,
                'last_name': self.assigned_user.last_name,
                'email': self.assigned_user.email
            } if self.assigned_user else None,
            'tags': [tag.to_dict() for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        return data

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#3B82F6')  # Default blue color
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tag {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LeadFieldTemplate(db.Model):
    """Template for additional fields that can be added to leads."""
    __tablename__ = 'lead_field_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # Field name/key
    label = db.Column(db.String(100), nullable=False)  # Display label
    field_type = db.Column(db.String(20), nullable=False)  # text, number, date, select, boolean
    options = db.Column(db.JSON)  # For select fields, store options
    is_required = db.Column(db.Boolean, default=False)
    default_value = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<LeadFieldTemplate {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label,
            'field_type': self.field_type,
            'options': self.options,
            'is_required': self.is_required,
            'default_value': self.default_value,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

