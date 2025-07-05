from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime
import uuid
import json
import re

class ProposalTemplate(db.Model):
    """Template de proposta com variáveis dinâmicas."""
    __tablename__ = 'proposal_templates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)  # Nome do template
    description = db.Column(db.Text)  # Descrição do template
    category = db.Column(db.String(100))  # Categoria (Telefonia, Consultoria, etc.)
    
    # Conteúdo do template
    subject = db.Column(db.String(500))  # Assunto do email
    content = db.Column(db.Text, nullable=False)  # Conteúdo HTML com variáveis
    header_image = db.Column(db.String(500))  # URL/path da imagem do cabeçalho
    footer_text = db.Column(db.Text)  # Texto do rodapé
    
    # Configurações
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    
    # Variáveis disponíveis (JSON)
    available_variables = db.Column(db.JSON, default=dict)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='proposal_templates')
    proposals = db.relationship('Proposal', backref='template', lazy='dynamic')
    
    def get_variables_from_content(self):
        """Extrai variáveis do conteúdo usando regex."""
        pattern = r'\{([^}]+)\}'
        variables = re.findall(pattern, self.content)
        if self.subject:
            variables.extend(re.findall(pattern, self.subject))
        if self.footer_text:
            variables.extend(re.findall(pattern, self.footer_text))
        return list(set(variables))
    
    def render_content(self, variables_data):
        """Renderiza o conteúdo substituindo as variáveis."""
        content = self.content
        subject = self.subject or ""
        footer = self.footer_text or ""
        
        for var_name, var_value in variables_data.items():
            placeholder = f"{{{var_name}}}"
            content = content.replace(placeholder, str(var_value or ""))
            subject = subject.replace(placeholder, str(var_value or ""))
            footer = footer.replace(placeholder, str(var_value or ""))
        
        return {
            'content': content,
            'subject': subject,
            'footer': footer
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'subject': self.subject,
            'content': self.content,
            'header_image': self.header_image,
            'footer_text': self.footer_text,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'available_variables': self.available_variables,
            'variables_in_content': self.get_variables_from_content(),
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

class Proposal(db.Model):
    """Proposta gerada a partir de um template."""
    __tablename__ = 'proposals'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(500), nullable=False)  # Título da proposta
    proposal_number = db.Column(db.String(50), unique=True)  # Número sequencial
    
    # Relacionamentos principais
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'), nullable=False)
    opportunity_id = db.Column(db.String(36), db.ForeignKey('opportunities.id'))
    template_id = db.Column(db.String(36), db.ForeignKey('proposal_templates.id'), nullable=False)
    
    # Conteúdo renderizado
    subject = db.Column(db.String(500))  # Assunto renderizado
    content = db.Column(db.Text, nullable=False)  # Conteúdo HTML renderizado
    footer_text = db.Column(db.Text)  # Rodapé renderizado
    
    # Dados da proposta
    total_value = db.Column(db.Numeric(15, 2))  # Valor total
    validity_days = db.Column(db.Integer, default=30)  # Validade em dias
    valid_until = db.Column(db.Date)  # Data de validade
    
    # Status e controle
    status = db.Column(db.String(50), default='draft')  # draft, sent, viewed, accepted, rejected, expired
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    
    # Envio por email
    sent_at = db.Column(db.DateTime)  # Data/hora do envio
    sent_to_email = db.Column(db.String(255))  # Email de destino
    email_subject = db.Column(db.String(500))  # Assunto do email
    
    # Visualização e interação
    viewed_at = db.Column(db.DateTime)  # Primeira visualização
    view_count = db.Column(db.Integer, default=0)  # Número de visualizações
    last_viewed_at = db.Column(db.DateTime)  # Última visualização
    
    # Assinatura digital
    signature_provider = db.Column(db.String(100))  # Provedor (DocuSign, etc.)
    signature_document_id = db.Column(db.String(255))  # ID no provedor
    signature_status = db.Column(db.String(50))  # pending, signed, declined
    signed_at = db.Column(db.DateTime)  # Data da assinatura
    signature_url = db.Column(db.String(500))  # URL para assinatura
    
    # Observações e notas
    notes = db.Column(db.Text)  # Notas internas
    client_feedback = db.Column(db.Text)  # Feedback do cliente
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    lead = db.relationship('Lead', backref='proposals')
    opportunity = db.relationship('Opportunity', backref='proposals')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_proposals')
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_proposals')
    
    @property
    def is_expired(self):
        """Verifica se a proposta está expirada."""
        if self.valid_until:
            from datetime import date
            return date.today() > self.valid_until
        return False
    
    @property
    def days_until_expiry(self):
        """Dias até a expiração."""
        if self.valid_until:
            from datetime import date
            delta = self.valid_until - date.today()
            return delta.days
        return None
    
    def generate_proposal_number(self):
        """Gera número sequencial da proposta."""
        from datetime import date
        today = date.today()
        year_month = today.strftime("%Y%m")
        
        # Conta propostas do mês atual
        count = Proposal.query.filter(
            Proposal.proposal_number.like(f"PROP-{year_month}-%")
        ).count()
        
        self.proposal_number = f"PROP-{year_month}-{count + 1:04d}"
    
    def mark_as_viewed(self):
        """Marca proposta como visualizada."""
        now = datetime.utcnow()
        if not self.viewed_at:
            self.viewed_at = now
        self.last_viewed_at = now
        self.view_count = (self.view_count or 0) + 1
        
        if self.status == 'sent':
            self.status = 'viewed'
    
    def to_dict(self, include_content=False):
        data = {
            'id': self.id,
            'title': self.title,
            'proposal_number': self.proposal_number,
            'lead_id': self.lead_id,
            'opportunity_id': self.opportunity_id,
            'template_id': self.template_id,
            'total_value': float(self.total_value) if self.total_value else None,
            'validity_days': self.validity_days,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'status': self.status,
            'priority': self.priority,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'sent_to_email': self.sent_to_email,
            'viewed_at': self.viewed_at.isoformat() if self.viewed_at else None,
            'view_count': self.view_count,
            'last_viewed_at': self.last_viewed_at.isoformat() if self.last_viewed_at else None,
            'signature_provider': self.signature_provider,
            'signature_status': self.signature_status,
            'signed_at': self.signed_at.isoformat() if self.signed_at else None,
            'signature_url': self.signature_url,
            'notes': self.notes,
            'client_feedback': self.client_feedback,
            'is_expired': self.is_expired,
            'days_until_expiry': self.days_until_expiry,
            'created_by': self.created_by,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'lead': {
                'id': self.lead.id,
                'name': self.lead.name,
                'company_name': self.lead.company_name,
                'email': self.lead.email
            } if self.lead else None,
            'opportunity': {
                'id': self.opportunity.id,
                'title': self.opportunity.title,
                'value': float(self.opportunity.value) if self.opportunity.value else None
            } if self.opportunity else None,
            'template': {
                'id': self.template.id,
                'name': self.template.name
            } if self.template else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None,
            'assignee': {
                'id': self.assignee.id,
                'name': f"{self.assignee.first_name} {self.assignee.last_name}"
            } if self.assignee else None
        }
        
        if include_content:
            data.update({
                'subject': self.subject,
                'content': self.content,
                'footer_text': self.footer_text,
                'email_subject': self.email_subject
            })
        
        return data

class ProposalItem(db.Model):
    """Itens/produtos de uma proposta."""
    __tablename__ = 'proposal_items'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    proposal_id = db.Column(db.String(36), db.ForeignKey('proposals.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'))
    
    # Dados do item
    name = db.Column(db.String(255), nullable=False)  # Nome do produto/serviço
    description = db.Column(db.Text)  # Descrição detalhada
    quantity = db.Column(db.Integer, default=1)  # Quantidade
    unit_price = db.Column(db.Numeric(15, 2))  # Preço unitário
    total_price = db.Column(db.Numeric(15, 2))  # Preço total (quantity * unit_price)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)  # Desconto em %
    discount_amount = db.Column(db.Numeric(15, 2), default=0)  # Valor do desconto
    
    # Configurações
    order_index = db.Column(db.Integer, default=0)  # Ordem de exibição
    is_optional = db.Column(db.Boolean, default=False)  # Item opcional
    
    # Relacionamentos
    proposal = db.relationship('Proposal', backref='items')
    product = db.relationship('Product', backref='proposal_items')
    
    def calculate_total(self):
        """Calcula o total do item com desconto."""
        if self.unit_price and self.quantity:
            subtotal = float(self.unit_price) * self.quantity
            
            if self.discount_percent:
                discount = subtotal * (float(self.discount_percent) / 100)
                self.discount_amount = discount
                self.total_price = subtotal - discount
            elif self.discount_amount:
                self.total_price = subtotal - float(self.discount_amount)
            else:
                self.total_price = subtotal
        else:
            self.total_price = 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'proposal_id': self.proposal_id,
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'total_price': float(self.total_price) if self.total_price else None,
            'discount_percent': float(self.discount_percent) if self.discount_percent else None,
            'discount_amount': float(self.discount_amount) if self.discount_amount else None,
            'order_index': self.order_index,
            'is_optional': self.is_optional,
            'product': {
                'id': self.product.id,
                'name': self.product.name,
                'category': self.product.category
            } if self.product else None
        }

