from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime, date
import uuid
import json
import re

class ContractTemplate(db.Model):
    """Template de contrato com variáveis dinâmicas."""
    __tablename__ = 'contract_templates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)  # Nome do template
    description = db.Column(db.Text)  # Descrição do template
    category = db.Column(db.String(100))  # Categoria (Telefonia, Consultoria, etc.)
    contract_type = db.Column(db.String(100))  # Tipo (Prestação de Serviços, Licenciamento, etc.)
    
    # Conteúdo do template
    title = db.Column(db.String(500))  # Título do contrato
    content = db.Column(db.Text, nullable=False)  # Conteúdo HTML/texto com variáveis
    header_image = db.Column(db.String(500))  # URL/path da imagem do cabeçalho
    footer_text = db.Column(db.Text)  # Texto do rodapé
    
    # Configurações contratuais
    default_duration_months = db.Column(db.Integer, default=12)  # Duração padrão em meses
    auto_renewal = db.Column(db.Boolean, default=False)  # Renovação automática
    cancellation_notice_days = db.Column(db.Integer, default=30)  # Aviso prévio para cancelamento
    
    # Configurações D4Sign
    d4sign_template_id = db.Column(db.String(255))  # ID do template no D4Sign
    d4sign_folder_id = db.Column(db.String(255))  # Pasta no D4Sign
    signature_positions = db.Column(db.JSON, default=list)  # Posições de assinatura
    
    # Configurações
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    requires_witness = db.Column(db.Boolean, default=False)  # Requer testemunha
    
    # Variáveis disponíveis (JSON)
    available_variables = db.Column(db.JSON, default=dict)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='contract_templates')
    contracts = db.relationship('Contract', backref='template', lazy='dynamic')
    
    def get_variables_from_content(self):
        """Extrai variáveis do conteúdo usando regex."""
        pattern = r'\{([^}]+)\}'
        variables = re.findall(pattern, self.content)
        if self.title:
            variables.extend(re.findall(pattern, self.title))
        if self.footer_text:
            variables.extend(re.findall(pattern, self.footer_text))
        return list(set(variables))
    
    def render_content(self, variables_data):
        """Renderiza o conteúdo substituindo as variáveis."""
        content = self.content
        title = self.title or ""
        footer = self.footer_text or ""
        
        for var_name, var_value in variables_data.items():
            placeholder = f"{{{var_name}}}"
            content = content.replace(placeholder, str(var_value or ""))
            title = title.replace(placeholder, str(var_value or ""))
            footer = footer.replace(placeholder, str(var_value or ""))
        
        return {
            'content': content,
            'title': title,
            'footer': footer
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'contract_type': self.contract_type,
            'title': self.title,
            'content': self.content,
            'header_image': self.header_image,
            'footer_text': self.footer_text,
            'default_duration_months': self.default_duration_months,
            'auto_renewal': self.auto_renewal,
            'cancellation_notice_days': self.cancellation_notice_days,
            'd4sign_template_id': self.d4sign_template_id,
            'd4sign_folder_id': self.d4sign_folder_id,
            'signature_positions': self.signature_positions,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'requires_witness': self.requires_witness,
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

class Contract(db.Model):
    """Contrato gerado a partir de um template."""
    __tablename__ = 'contracts'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(500), nullable=False)  # Título do contrato
    contract_number = db.Column(db.String(50), unique=True)  # Número sequencial
    
    # Relacionamentos principais
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'), nullable=False)
    opportunity_id = db.Column(db.String(36), db.ForeignKey('opportunities.id'))
    proposal_id = db.Column(db.String(36), db.ForeignKey('proposals.id'))  # Contrato originado de proposta
    template_id = db.Column(db.String(36), db.ForeignKey('contract_templates.id'), nullable=False)
    
    # Conteúdo renderizado
    rendered_title = db.Column(db.String(500))  # Título renderizado
    content = db.Column(db.Text, nullable=False)  # Conteúdo HTML renderizado
    footer_text = db.Column(db.Text)  # Rodapé renderizado
    
    # Dados contratuais
    contract_value = db.Column(db.Numeric(15, 2))  # Valor do contrato
    currency = db.Column(db.String(3), default='BRL')  # Moeda
    payment_terms = db.Column(db.Text)  # Condições de pagamento
    
    # Datas contratuais
    start_date = db.Column(db.Date)  # Data de início
    end_date = db.Column(db.Date)  # Data de término
    duration_months = db.Column(db.Integer)  # Duração em meses
    auto_renewal = db.Column(db.Boolean, default=False)  # Renovação automática
    cancellation_notice_days = db.Column(db.Integer, default=30)  # Aviso prévio
    
    # Status e controle
    status = db.Column(db.String(50), default='draft')  # draft, sent, signed, active, expired, cancelled, terminated
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    
    # Integração D4Sign
    d4sign_document_id = db.Column(db.String(255))  # ID do documento no D4Sign
    d4sign_safe_id = db.Column(db.String(255))  # ID do cofre no D4Sign
    d4sign_status = db.Column(db.String(50))  # Status no D4Sign
    d4sign_url = db.Column(db.String(500))  # URL para assinatura
    d4sign_webhook_url = db.Column(db.String(500))  # URL do webhook
    
    # Assinaturas
    signature_status = db.Column(db.String(50), default='pending')  # pending, partial, completed, declined
    signed_at = db.Column(db.DateTime)  # Data da assinatura completa
    client_signed_at = db.Column(db.DateTime)  # Data da assinatura do cliente
    company_signed_at = db.Column(db.DateTime)  # Data da assinatura da empresa
    witness_signed_at = db.Column(db.DateTime)  # Data da assinatura da testemunha
    
    # Documentos e anexos
    original_document_path = db.Column(db.String(500))  # Caminho do documento original
    signed_document_path = db.Column(db.String(500))  # Caminho do documento assinado
    attachments = db.Column(db.JSON, default=list)  # Lista de anexos
    
    # Renovação e cancelamento
    renewal_date = db.Column(db.Date)  # Data de renovação
    cancellation_date = db.Column(db.Date)  # Data de cancelamento
    cancellation_reason = db.Column(db.Text)  # Motivo do cancelamento
    termination_date = db.Column(db.Date)  # Data de rescisão
    termination_reason = db.Column(db.Text)  # Motivo da rescisão
    
    # Observações e notas
    notes = db.Column(db.Text)  # Notas internas
    client_feedback = db.Column(db.Text)  # Feedback do cliente
    legal_notes = db.Column(db.Text)  # Observações jurídicas
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'))  # Responsável
    legal_reviewer = db.Column(db.String(36), db.ForeignKey('users.id'))  # Revisor jurídico
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos de integração com ERP
    erp_contract_id = db.Column(db.String(100))  # ID do contrato no FlyERP
    erp_sync_status = db.Column(db.String(50), default='pending')  # pending, synced, error
    erp_sync_date = db.Column(db.DateTime)
    erp_sync_error = db.Column(db.Text)
    
    # Relacionamentos
    lead = db.relationship('Lead', backref='contracts')
    opportunity = db.relationship('Opportunity', backref='contracts')
    proposal = db.relationship('Proposal', backref='contracts')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_contracts')
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_contracts')
    reviewer = db.relationship('User', foreign_keys=[legal_reviewer], backref='reviewed_contracts')
    
    @property
    def is_active(self):
        """Verifica se o contrato está ativo."""
        return self.status == 'active' and self.start_date <= date.today() <= self.end_date
    
    @property
    def is_expired(self):
        """Verifica se o contrato está expirado."""
        return self.end_date and date.today() > self.end_date
    
    @property
    def days_until_expiry(self):
        """Dias até a expiração."""
        if self.end_date:
            delta = self.end_date - date.today()
            return delta.days
        return None
    
    @property
    def days_until_renewal(self):
        """Dias até a renovação."""
        if self.renewal_date:
            delta = self.renewal_date - date.today()
            return delta.days
        return None
    
    def generate_contract_number(self):
        """Gera número sequencial do contrato."""
        today = date.today()
        year = today.strftime("%Y")
        
        # Conta contratos do ano atual
        count = Contract.query.filter(
            Contract.contract_number.like(f"CONT-{year}-%")
        ).count()
        
        self.contract_number = f"CONT-{year}-{count + 1:04d}"
    
    def calculate_end_date(self):
        """Calcula data de término baseada na duração."""
        if self.start_date and self.duration_months:
            from dateutil.relativedelta import relativedelta
            self.end_date = self.start_date + relativedelta(months=self.duration_months)
            
            # Calcular data de renovação (30 dias antes do vencimento)
            if self.auto_renewal:
                self.renewal_date = self.end_date - relativedelta(days=30)
    
    def mark_as_signed(self, signer_type='client'):
        """Marca assinatura por tipo de signatário."""
        now = datetime.utcnow()
        
        if signer_type == 'client':
            self.client_signed_at = now
        elif signer_type == 'company':
            self.company_signed_at = now
        elif signer_type == 'witness':
            self.witness_signed_at = now
        
        # Verificar se todas as assinaturas necessárias foram coletadas
        signatures_needed = ['client', 'company']
        if self.template.requires_witness:
            signatures_needed.append('witness')
        
        signatures_completed = []
        if self.client_signed_at:
            signatures_completed.append('client')
        if self.company_signed_at:
            signatures_completed.append('company')
        if self.witness_signed_at:
            signatures_completed.append('witness')
        
        if all(sig in signatures_completed for sig in signatures_needed):
            self.signature_status = 'completed'
            self.signed_at = now
            self.status = 'signed'
        else:
            self.signature_status = 'partial'
    
    def to_dict(self, include_content=False):
        data = {
            'id': self.id,
            'title': self.title,
            'contract_number': self.contract_number,
            'lead_id': self.lead_id,
            'opportunity_id': self.opportunity_id,
            'proposal_id': self.proposal_id,
            'template_id': self.template_id,
            'contract_value': float(self.contract_value) if self.contract_value else None,
            'currency': self.currency,
            'payment_terms': self.payment_terms,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'duration_months': self.duration_months,
            'auto_renewal': self.auto_renewal,
            'cancellation_notice_days': self.cancellation_notice_days,
            'status': self.status,
            'priority': self.priority,
            'd4sign_document_id': self.d4sign_document_id,
            'd4sign_status': self.d4sign_status,
            'd4sign_url': self.d4sign_url,
            'signature_status': self.signature_status,
            'signed_at': self.signed_at.isoformat() if self.signed_at else None,
            'client_signed_at': self.client_signed_at.isoformat() if self.client_signed_at else None,
            'company_signed_at': self.company_signed_at.isoformat() if self.company_signed_at else None,
            'witness_signed_at': self.witness_signed_at.isoformat() if self.witness_signed_at else None,
            'renewal_date': self.renewal_date.isoformat() if self.renewal_date else None,
            'cancellation_date': self.cancellation_date.isoformat() if self.cancellation_date else None,
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'attachments': self.attachments,
            'notes': self.notes,
            'client_feedback': self.client_feedback,
            'legal_notes': self.legal_notes,
            'is_active': self.is_active,
            'is_expired': self.is_expired,
            'days_until_expiry': self.days_until_expiry,
            'days_until_renewal': self.days_until_renewal,
            'created_by': self.created_by,
            'assigned_to': self.assigned_to,
            'legal_reviewer': self.legal_reviewer,
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
            'proposal': {
                'id': self.proposal.id,
                'title': self.proposal.title,
                'proposal_number': self.proposal.proposal_number
            } if self.proposal else None,
            'template': {
                'id': self.template.id,
                'name': self.template.name,
                'contract_type': self.template.contract_type
            } if self.template else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None,
            'assignee': {
                'id': self.assignee.id,
                'name': f"{self.assignee.first_name} {self.assignee.last_name}"
            } if self.assignee else None,
            'reviewer': {
                'id': self.reviewer.id,
                'name': f"{self.reviewer.first_name} {self.reviewer.last_name}"
            } if self.reviewer else None
        }
        
        if include_content:
            data.update({
                'rendered_title': self.rendered_title,
                'content': self.content,
                'footer_text': self.footer_text
            })
        
        return data

class ContractAmendment(db.Model):
    """Aditivos contratuais."""
    __tablename__ = 'contract_amendments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = db.Column(db.String(36), db.ForeignKey('contracts.id'), nullable=False)
    amendment_number = db.Column(db.Integer, nullable=False)  # Número sequencial do aditivo
    
    # Dados do aditivo
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)  # Descrição das alterações
    amendment_type = db.Column(db.String(100))  # Tipo: valor, prazo, escopo, etc.
    
    # Alterações
    old_value = db.Column(db.Numeric(15, 2))  # Valor anterior
    new_value = db.Column(db.Numeric(15, 2))  # Novo valor
    old_end_date = db.Column(db.Date)  # Data de término anterior
    new_end_date = db.Column(db.Date)  # Nova data de término
    
    # Conteúdo do aditivo
    content = db.Column(db.Text)  # Conteúdo do aditivo
    
    # Status e assinatura
    status = db.Column(db.String(50), default='draft')  # draft, sent, signed, active
    d4sign_document_id = db.Column(db.String(255))  # ID no D4Sign
    signed_at = db.Column(db.DateTime)  # Data da assinatura
    effective_date = db.Column(db.Date)  # Data de vigência
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    contract = db.relationship('Contract', backref='amendments')
    creator = db.relationship('User', backref='created_amendments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'contract_id': self.contract_id,
            'amendment_number': self.amendment_number,
            'title': self.title,
            'description': self.description,
            'amendment_type': self.amendment_type,
            'old_value': float(self.old_value) if self.old_value else None,
            'new_value': float(self.new_value) if self.new_value else None,
            'old_end_date': self.old_end_date.isoformat() if self.old_end_date else None,
            'new_end_date': self.new_end_date.isoformat() if self.new_end_date else None,
            'content': self.content,
            'status': self.status,
            'd4sign_document_id': self.d4sign_document_id,
            'signed_at': self.signed_at.isoformat() if self.signed_at else None,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

