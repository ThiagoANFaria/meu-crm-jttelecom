from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime
import uuid
import json

class ChatFlow(db.Model):
    """Fluxos de conversa estilo Typebot."""
    __tablename__ = 'chat_flows'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)  # Nome do fluxo
    description = db.Column(db.Text)  # Descrição do fluxo
    
    # Configurações do fluxo
    trigger_keywords = db.Column(db.JSON, default=list)  # Palavras-chave que ativam o fluxo
    is_default = db.Column(db.Boolean, default=False)  # Fluxo padrão
    is_active = db.Column(db.Boolean, default=True)  # Fluxo ativo
    priority = db.Column(db.Integer, default=1)  # Prioridade (1=alta, 5=baixa)
    
    # Estrutura do fluxo (JSON)
    flow_data = db.Column(db.JSON, nullable=False)  # Estrutura completa do fluxo
    
    # Configurações de IA
    ai_enabled = db.Column(db.Boolean, default=False)  # IA habilitada neste fluxo
    ai_fallback = db.Column(db.Boolean, default=True)  # IA como fallback
    ai_context = db.Column(db.Text)  # Contexto específico para IA
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='chat_flows')
    conversations = db.relationship('ChatConversation', backref='flow', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'trigger_keywords': self.trigger_keywords,
            'is_default': self.is_default,
            'is_active': self.is_active,
            'priority': self.priority,
            'flow_data': self.flow_data,
            'ai_enabled': self.ai_enabled,
            'ai_fallback': self.ai_fallback,
            'ai_context': self.ai_context,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

class ChatConversation(db.Model):
    """Conversas do chatbot."""
    __tablename__ = 'chat_conversations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Identificação do contato
    phone_number = db.Column(db.String(20), nullable=False)  # Número do WhatsApp
    contact_name = db.Column(db.String(255))  # Nome do contato
    
    # Relacionamento com lead (se existir)
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'))
    
    # Fluxo e estado
    flow_id = db.Column(db.String(36), db.ForeignKey('chat_flows.id'))
    current_step = db.Column(db.String(100))  # Etapa atual do fluxo
    flow_variables = db.Column(db.JSON, default=dict)  # Variáveis coletadas no fluxo
    
    # Status da conversa
    status = db.Column(db.String(50), default='active')  # active, paused, completed, transferred
    is_ai_active = db.Column(db.Boolean, default=False)  # IA está ativa na conversa
    human_takeover = db.Column(db.Boolean, default=False)  # Atendente humano assumiu
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'))  # Atendente responsável
    
    # Configurações
    language = db.Column(db.String(10), default='pt-BR')  # Idioma da conversa
    timezone = db.Column(db.String(50), default='America/Sao_Paulo')  # Fuso horário
    
    # Metadados
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    
    # Relacionamentos
    lead = db.relationship('Lead', backref='chat_conversations')
    assignee = db.relationship('User', backref='assigned_conversations')
    messages = db.relationship('ChatMessage', backref='conversation', lazy='dynamic', order_by='ChatMessage.created_at')
    
    @property
    def last_message(self):
        """Última mensagem da conversa."""
        return self.messages.order_by(ChatMessage.created_at.desc()).first()
    
    @property
    def message_count(self):
        """Número total de mensagens."""
        return self.messages.count()
    
    @property
    def unread_count(self):
        """Número de mensagens não lidas."""
        return self.messages.filter_by(is_read=False, direction='incoming').count()
    
    def to_dict(self, include_messages=False):
        data = {
            'id': self.id,
            'phone_number': self.phone_number,
            'contact_name': self.contact_name,
            'lead_id': self.lead_id,
            'flow_id': self.flow_id,
            'current_step': self.current_step,
            'flow_variables': self.flow_variables,
            'status': self.status,
            'is_ai_active': self.is_ai_active,
            'human_takeover': self.human_takeover,
            'assigned_to': self.assigned_to,
            'language': self.language,
            'timezone': self.timezone,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'message_count': self.message_count,
            'unread_count': self.unread_count,
            'lead': {
                'id': self.lead.id,
                'name': self.lead.name,
                'company_name': self.lead.company_name,
                'email': self.lead.email
            } if self.lead else None,
            'flow': {
                'id': self.flow.id,
                'name': self.flow.name
            } if self.flow else None,
            'assignee': {
                'id': self.assignee.id,
                'name': f"{self.assignee.first_name} {self.assignee.last_name}"
            } if self.assignee else None,
            'last_message': self.last_message.to_dict() if self.last_message else None
        }
        
        if include_messages:
            data['messages'] = [msg.to_dict() for msg in self.messages.order_by(ChatMessage.created_at)]
        
        return data

class ChatMessage(db.Model):
    """Mensagens do chatbot."""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('chat_conversations.id'), nullable=False)
    
    # Conteúdo da mensagem
    message_type = db.Column(db.String(50), default='text')  # text, image, audio, document, button, list
    content = db.Column(db.Text, nullable=False)  # Conteúdo da mensagem
    media_url = db.Column(db.String(500))  # URL de mídia (se aplicável)
    
    # Direção e origem
    direction = db.Column(db.String(20), nullable=False)  # incoming, outgoing
    sender_type = db.Column(db.String(20), default='user')  # user, bot, human, system
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'))  # ID do usuário (se humano)
    
    # Status da mensagem
    is_read = db.Column(db.Boolean, default=False)  # Mensagem lida
    delivered_at = db.Column(db.DateTime)  # Data de entrega
    read_at = db.Column(db.DateTime)  # Data de leitura
    
    # Contexto do fluxo
    flow_step = db.Column(db.String(100))  # Etapa do fluxo quando enviada
    is_ai_generated = db.Column(db.Boolean, default=False)  # Gerada por IA
    ai_confidence = db.Column(db.Float)  # Confiança da IA (0-1)
    
    # Metadados externos (WhatsApp, etc.)
    external_id = db.Column(db.String(255))  # ID da mensagem no sistema externo
    external_status = db.Column(db.String(50))  # Status no sistema externo
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    sender = db.relationship('User', backref='sent_messages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'message_type': self.message_type,
            'content': self.content,
            'media_url': self.media_url,
            'direction': self.direction,
            'sender_type': self.sender_type,
            'sender_id': self.sender_id,
            'is_read': self.is_read,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'flow_step': self.flow_step,
            'is_ai_generated': self.is_ai_generated,
            'ai_confidence': self.ai_confidence,
            'external_id': self.external_id,
            'external_status': self.external_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'sender': {
                'id': self.sender.id,
                'name': f"{self.sender.first_name} {self.sender.last_name}"
            } if self.sender else None
        }

class ChatIntegration(db.Model):
    """Configurações de integração (WhatsApp, Evolution API, etc.)."""
    __tablename__ = 'chat_integrations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)  # Nome da integração
    provider = db.Column(db.String(100), nullable=False)  # whatsapp_business, evolution_api, etc.
    
    # Configurações da API
    api_url = db.Column(db.String(500))  # URL base da API
    api_token = db.Column(db.String(500))  # Token de acesso
    webhook_url = db.Column(db.String(500))  # URL do webhook
    webhook_token = db.Column(db.String(255))  # Token do webhook
    
    # Configurações específicas
    phone_number = db.Column(db.String(20))  # Número do WhatsApp Business
    business_account_id = db.Column(db.String(255))  # ID da conta business
    app_id = db.Column(db.String(255))  # ID da aplicação
    app_secret = db.Column(db.String(255))  # Secret da aplicação
    
    # Configurações adicionais (JSON)
    settings = db.Column(db.JSON, default=dict)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_connected = db.Column(db.Boolean, default=False)
    last_sync = db.Column(db.DateTime)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='chat_integrations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'api_url': self.api_url,
            'webhook_url': self.webhook_url,
            'phone_number': self.phone_number,
            'business_account_id': self.business_account_id,
            'app_id': self.app_id,
            'settings': self.settings,
            'is_active': self.is_active,
            'is_connected': self.is_connected,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

class ChatAIConfig(db.Model):
    """Configurações da IA (OpenAI)."""
    __tablename__ = 'chat_ai_config'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)  # Nome da configuração
    
    # Configurações OpenAI
    api_key = db.Column(db.String(500), nullable=False)  # Chave da API
    model = db.Column(db.String(100), default='gpt-4o')  # Modelo a usar
    max_tokens = db.Column(db.Integer, default=1000)  # Máximo de tokens
    temperature = db.Column(db.Float, default=0.7)  # Criatividade (0-1)
    
    # Prompt do sistema
    system_prompt = db.Column(db.Text, nullable=False)  # Prompt base do sistema
    context_window = db.Column(db.Integer, default=10)  # Janela de contexto (mensagens)
    
    # Configurações de comportamento
    fallback_enabled = db.Column(db.Boolean, default=True)  # IA como fallback
    auto_handoff = db.Column(db.Boolean, default=True)  # Transferir para humano automaticamente
    handoff_keywords = db.Column(db.JSON, default=list)  # Palavras que ativam transferência
    
    # Configurações de resposta
    typing_delay = db.Column(db.Integer, default=2)  # Delay para simular digitação (segundos)
    max_response_time = db.Column(db.Integer, default=30)  # Tempo máximo de resposta
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    
    # Metadados
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='ai_configs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'system_prompt': self.system_prompt,
            'context_window': self.context_window,
            'fallback_enabled': self.fallback_enabled,
            'auto_handoff': self.auto_handoff,
            'handoff_keywords': self.handoff_keywords,
            'typing_delay': self.typing_delay,
            'max_response_time': self.max_response_time,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'creator': {
                'id': self.creator.id,
                'name': f"{self.creator.first_name} {self.creator.last_name}"
            } if self.creator else None
        }

