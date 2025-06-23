from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.lead import Lead
from src.models.chatbot import ChatFlow, ChatConversation, ChatMessage, ChatIntegration, ChatAIConfig
from src.services.chatbot_service import WhatsAppBusinessService, EvolutionAPIService, OpenAIService, ChatFlowEngine
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, desc
import uuid
import json
import asyncio
from flasgger import swag_from

chatbot_bp = Blueprint("chatbot", __name__)

# ==================== CHAT FLOWS ====================

@chatbot_bp.route("/chat-flows", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Fluxos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "description": "Número da página",
            "default": 1
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "description": "Itens por página",
            "default": 20
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Pesquisar por nome ou descrição"
        },
        {
            "name": "is_active",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por fluxos ativos"
        }
    ],
    "responses": {
        "200": {"description": "Lista de fluxos de chat"},
        "401": {"description": "Não autorizado"}
    }
})
def get_chat_flows():
    """Lista todos os fluxos de chat."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)
        search = request.args.get("search", "")
        is_active = request.args.get("is_active")
        
        query = ChatFlow.query
        
        if search:
            query = query.filter(or_(
                ChatFlow.name.ilike(f"%{search}%"),
                ChatFlow.description.ilike(f"%{search}%")
            ))
        
        if is_active is not None:
            query = query.filter(ChatFlow.is_active == (is_active.lower() == "true"))
        
        query = query.order_by(ChatFlow.priority, ChatFlow.created_at.desc())
        flows = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "flows": [flow.to_dict() for flow in flows.items],
            "total": flows.total,
            "pages": flows.pages,
            "current_page": page,
            "per_page": per_page
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/chat-flows", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Fluxos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChatFlowCreate",
                "required": ["name", "flow_data"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do fluxo"},
                    "description": {"type": "string", "description": "Descrição do fluxo"},
                    "trigger_keywords": {"type": "array", "items": {"type": "string"}, "description": "Palavras-chave para acionar o fluxo"},
                    "is_default": {"type": "boolean", "description": "Se é o fluxo padrão"},
                    "is_active": {"type": "boolean", "description": "Se o fluxo está ativo"},
                    "priority": {"type": "integer", "description": "Prioridade do fluxo (menor é maior prioridade)"},
                    "flow_data": {"type": "object", "description": "Dados JSON do fluxo (estrutura Typebot)"},
                    "ai_enabled": {"type": "boolean", "description": "Se a IA está habilitada para este fluxo"},
                    "ai_fallback": {"type": "boolean", "description": "Se a IA deve ser usada como fallback"},
                    "ai_context": {"type": "string", "description": "Contexto para a IA"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Fluxo criado com sucesso"},
        "400": {"description": "Dados inválidos ou fluxo já existente"},
        "401": {"description": "Não autorizado"}
    }
})
def create_chat_flow():
    """Cria um novo fluxo de chat."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validações
        if not data.get("name"):
            return jsonify({"error": "Nome é obrigatório"}), 400
        
        if not data.get("flow_data"):
            return jsonify({"error": "Dados do fluxo são obrigatórios"}), 400
        
        # Verifica se já existe fluxo com mesmo nome
        existing = ChatFlow.query.filter_by(name=data["name"]).first()
        if existing:
            return jsonify({"error": "Já existe um fluxo com este nome"}), 400
        
        flow = ChatFlow(
            name=data["name"],
            description=data.get("description", ""),
            trigger_keywords=data.get("trigger_keywords", []),
            is_default=data.get("is_default", False),
            is_active=data.get("is_active", True),
            priority=data.get("priority", 1),
            flow_data=data["flow_data"],
            ai_enabled=data.get("ai_enabled", False),
            ai_fallback=data.get("ai_fallback", True),
            ai_context=data.get("ai_context", ""),
            created_by=current_user_id
        )
        
        # Se é fluxo padrão, remove flag de outros fluxos
        if flow.is_default:
            ChatFlow.query.filter_by(is_default=True).update({"is_default": False})
        
        db.session.add(flow)
        db.session.commit()
        
        return jsonify(flow.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/chat-flows/<flow_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Fluxos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "flow_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do fluxo"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de um fluxo específico"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Fluxo não encontrado"}
    }
})
def get_chat_flow(flow_id):
    """Obtém detalhes de um fluxo específico."""
    try:
        flow = ChatFlow.query.get_or_404(flow_id)
        return jsonify(flow.to_dict())
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/chat-flows/<flow_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Fluxos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "flow_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do fluxo"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChatFlowUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do fluxo"},
                    "description": {"type": "string", "description": "Descrição do fluxo"},
                    "trigger_keywords": {"type": "array", "items": {"type": "string"}, "description": "Palavras-chave para acionar o fluxo"},
                    "is_default": {"type": "boolean", "description": "Se é o fluxo padrão"},
                    "is_active": {"type": "boolean", "description": "Se o fluxo está ativo"},
                    "priority": {"type": "integer", "description": "Prioridade do fluxo (menor é maior prioridade)"},
                    "flow_data": {"type": "object", "description": "Dados JSON do fluxo (estrutura Typebot)"},
                    "ai_enabled": {"type": "boolean", "description": "Se a IA está habilitada para este fluxo"},
                    "ai_fallback": {"type": "boolean", "description": "Se a IA deve ser usada como fallback"},
                    "ai_context": {"type": "string", "description": "Contexto para a IA"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Fluxo atualizado com sucesso"},
        "400": {"description": "Dados inválidos ou fluxo já existente"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Fluxo não encontrado"}
    }
})
def update_chat_flow(flow_id):
    """Atualiza um fluxo de chat."""
    try:
        flow = ChatFlow.query.get_or_404(flow_id)
        data = request.get_json()
        
        # Atualiza campos
        if "name" in data:
            # Verifica se já existe outro fluxo com mesmo nome
            existing = ChatFlow.query.filter(
                ChatFlow.name == data["name"],
                ChatFlow.id != flow_id
            ).first()
            if existing:
                return jsonify({"error": "Já existe um fluxo com este nome"}), 400
            flow.name = data["name"]
        
        if "description" in data:
            flow.description = data["description"]
        if "trigger_keywords" in data:
            flow.trigger_keywords = data["trigger_keywords"]
        if "is_default" in data:
            flow.is_default = data["is_default"]
            # Se é fluxo padrão, remove flag de outros fluxos
            if flow.is_default:
                ChatFlow.query.filter(
                    ChatFlow.is_default == True,
                    ChatFlow.id != flow_id
                ).update({"is_default": False})
        if "is_active" in data:
            flow.is_active = data["is_active"]
        if "priority" in data:
            flow.priority = data["priority"]
        if "flow_data" in data:
            flow.flow_data = data["flow_data"]
        if "ai_enabled" in data:
            flow.ai_enabled = data["ai_enabled"]
        if "ai_fallback" in data:
            flow.ai_fallback = data["ai_fallback"]
        if "ai_context" in data:
            flow.ai_context = data["ai_context"]
        
        flow.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(flow.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/chat-flows/<flow_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Fluxos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "flow_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do fluxo"
        }
    ],
    "responses": {
        "200": {"description": "Fluxo excluído com sucesso"},
        "400": {"description": "Não é possível excluir, há conversas ativas usando este fluxo"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Fluxo não encontrado"}
    }
})
def delete_chat_flow(flow_id):
    """Exclui um fluxo de chat."""
    try:
        flow = ChatFlow.query.get_or_404(flow_id)
        
        # Verifica se há conversas ativas usando este fluxo
        active_conversations = ChatConversation.query.filter_by(
            flow_id=flow_id,
            status="active"
        ).count()
        
        if active_conversations > 0:
            return jsonify({
                "error": f"Não é possível excluir. Há {active_conversations} conversas ativas usando este fluxo."
            }), 400
        
        db.session.delete(flow)
        db.session.commit()
        
        return jsonify({"message": "Fluxo excluído com sucesso"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/chat-flows/<flow_id>/test", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Fluxos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "flow_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do fluxo"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChatFlowTest",
                "properties": {
                    "step": {"type": "string", "description": "Passo atual do fluxo"},
                    "user_input": {"type": "string", "description": "Entrada do usuário"},
                    "variables": {"type": "object", "description": "Variáveis da conversa"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Resultado do teste do fluxo"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Fluxo não encontrado"}
    }
})
def test_chat_flow(flow_id):
    """Testa um fluxo de chat."""
    try:
        flow = ChatFlow.query.get_or_404(flow_id)
        data = request.get_json()
        
        step = data.get("step", "start")
        user_input = data.get("user_input", "")
        variables = data.get("variables", {})
        
        engine = ChatFlowEngine()
        result = engine.process_flow_step(flow.flow_data, step, user_input, variables)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== CONVERSATIONS ====================

@chatbot_bp.route("/conversations", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Conversas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "description": "Número da página",
            "default": 1
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "description": "Itens por página",
            "default": 20
        },
        {
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "Filtrar por status da conversa"
        },
        {
            "name": "assigned_to",
            "in": "query",
            "type": "string",
            "description": "Filtrar por usuário atribuído"
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Pesquisar por número de telefone ou nome de contato"
        }
    ],
    "responses": {
        "200": {"description": "Lista de conversas do chatbot"},
        "401": {"description": "Não autorizado"}
    }
})
def get_conversations():
    """Lista conversas do chatbot."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)
        status = request.args.get("status")
        assigned_to = request.args.get("assigned_to")
        search = request.args.get("search", "")
        
        query = ChatConversation.query
        
        if status:
            query = query.filter(ChatConversation.status == status)
        
        if assigned_to:
            query = query.filter(ChatConversation.assigned_to == assigned_to)
        
        if search:
            query = query.filter(or_(
                ChatConversation.phone_number.ilike(f"%{search}%"),
                ChatConversation.contact_name.ilike(f"%{search}%")
            ))
        
        query = query.order_by(ChatConversation.last_activity.desc())
        conversations = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "conversations": [conv.to_dict() for conv in conversations.items],
            "total": conversations.total,
            "pages": conversations.pages,
            "current_page": page,
            "per_page": per_page
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/conversations/<conversation_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Conversas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "conversation_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da conversa"
        },
        {
            "name": "include_messages",
            "in": "query",
            "type": "boolean",
            "description": "Incluir mensagens na resposta",
            "default": True
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de uma conversa"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Conversa não encontrada"}
    }
})
def get_conversation(conversation_id):
    """Obtém detalhes de uma conversa."""
    try:
        conversation = ChatConversation.query.get_or_404(conversation_id)
        include_messages = request.args.get("include_messages", "true").lower() == "true"
        
        return jsonify(conversation.to_dict(include_messages=include_messages))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/conversations/<conversation_id>/messages", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Conversas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "conversation_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da conversa"
        },
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "description": "Número da página",
            "default": 1
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "description": "Itens por página",
            "default": 50
        }
    ],
    "responses": {
        "200": {"description": "Mensagens de uma conversa"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Conversa não encontrada"}
    }
})
def get_conversation_messages(conversation_id):
    """Obtém mensagens de uma conversa."""
    try:
        conversation = ChatConversation.query.get_or_404(conversation_id)
        
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 50, type=int), 100)
        
        messages = conversation.messages.order_by(ChatMessage.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "messages": [msg.to_dict() for msg in reversed(messages.items)],
            "total": messages.total,
            "pages": messages.pages,
            "current_page": page,
            "per_page": per_page
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/conversations/<conversation_id>/send-message", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Conversas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "conversation_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da conversa"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChatMessageSend",
                "required": ["content"],
                "properties": {
                    "type": {"type": "string", "description": "Tipo da mensagem (e.g., text, image)", "default": "text"},
                    "content": {"type": "string", "description": "Conteúdo da mensagem"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Mensagem enviada com sucesso"},
        "400": {"description": "Conteúdo da mensagem é obrigatório"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Conversa não encontrada"}
    }
})
def send_message(conversation_id):
    """Envia mensagem em uma conversa."""
    try:
        current_user_id = get_jwt_identity()
        conversation = ChatConversation.query.get_or_404(conversation_id)
        data = request.get_json()
        
        message_type = data.get("type", "text")
        content = data.get("content", "")
        
        if not content:
            return jsonify({"error": "Conteúdo da mensagem é obrigatório"}), 400
        
        # Cria mensagem no banco
        message = ChatMessage(
            conversation_id=conversation_id,
            message_type=message_type,
            content=content,
            direction="outgoing",
            sender_type="human",
            sender_id=current_user_id,
            flow_step=conversation.current_step
        )
        
        db.session.add(message)
        
        # Atualiza conversa
        conversation.last_activity = datetime.utcnow()
        conversation.human_takeover = True
        conversation.assigned_to = current_user_id
        
        db.session.commit()
        
        # Envia via integração (WhatsApp, etc.)
        # TODO: Implementar envio real
        
        return jsonify(message.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/conversations/<conversation_id>/takeover", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Conversas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "conversation_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da conversa"
        }
    ],
    "responses": {
        "200": {"description": "Atendente assumiu controle da conversa"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Conversa não encontrada"}
    }
})
def takeover_conversation(conversation_id):
    """Atendente assume controle da conversa."""
    try:
        current_user_id = get_jwt_identity()
        conversation = ChatConversation.query.get_or_404(conversation_id)
        
        conversation.human_takeover = True
        conversation.assigned_to = current_user_id
        conversation.is_ai_active = False
        conversation.last_activity = datetime.utcnow()
        
        # Cria mensagem de sistema
        system_message = ChatMessage(
            conversation_id=conversation_id,
            message_type="text",
            content="Atendente assumiu a conversa",
            direction="outgoing",
            sender_type="system",
            sender_id=current_user_id
        )
        
        db.session.add(system_message)
        db.session.commit()
        
        return jsonify(conversation.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/conversations/<conversation_id>/release", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Conversas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "conversation_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da conversa"
        }
    ],
    "responses": {
        "200": {"description": "Libera conversa para o bot"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Conversa não encontrada"}
    }
})
def release_conversation(conversation_id):
    """Libera conversa para o bot."""
    try:
        conversation = ChatConversation.query.get_or_404(conversation_id)
        
        conversation.human_takeover = False
        conversation.is_ai_active = True
        conversation.last_activity = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(conversation.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== INTEGRATIONS ====================

@chatbot_bp.route("/integrations", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Integrações"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de integrações configuradas"},
        "401": {"description": "Não autorizado"}
    }
})
def get_integrations():
    """Lista integrações configuradas."""
    try:
        integrations = ChatIntegration.query.order_by(ChatIntegration.created_at.desc()).all()
        return jsonify([integration.to_dict() for integration in integrations])
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/integrations", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Integrações"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChatIntegrationCreate",
                "required": ["name", "provider"],
                "properties": {
                    "name": {"type": "string", "description": "Nome da integração"},
                    "provider": {"type": "string", "description": "Provedor da integração (e.g., whatsapp_business, evolution_api)"},
                    "api_url": {"type": "string", "description": "URL da API"},
                    "api_token": {"type": "string", "description": "Token da API"},
                    "webhook_url": {"type": "string", "description": "URL do webhook"},
                    "webhook_token": {"type": "string", "description": "Token do webhook"},
                    "phone_number": {"type": "string", "description": "Número de telefone associado"},
                    "business_account_id": {"type": "string", "description": "ID da conta comercial (para WhatsApp Business)"},
                    "app_id": {"type": "string", "description": "ID do aplicativo"},
                    "app_secret": {"type": "string", "description": "Segredo do aplicativo"},
                    "settings": {"type": "object", "description": "Configurações adicionais JSON"},
                    "is_active": {"type": "boolean", "description": "Se a integração está ativa"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Integração criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"}
    }
})
def create_integration():
    """Cria nova integração."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        integration = ChatIntegration(
            name=data["name"],
            provider=data["provider"],
            api_url=data.get("api_url"),
            api_token=data.get("api_token"),
            webhook_url=data.get("webhook_url"),
            webhook_token=data.get("webhook_token"),
            phone_number=data.get("phone_number"),
            business_account_id=data.get("business_account_id"),
            app_id=data.get("app_id"),
            app_secret=data.get("app_secret"),
            settings=data.get("settings", {}),
            is_active=data.get("is_active", True),
            created_by=current_user_id
        )
        
        db.session.add(integration)
        db.session.commit()
        
        return jsonify(integration.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/integrations/<integration_id>/test", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Integrações"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "integration_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da integração"
        }
    ],
    "responses": {
        "200": {"description": "Resultado do teste da integração"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Integração não encontrada"},
        "500": {"description": "Erro ao testar integração"}
    }
})
def test_integration(integration_id):
    """Testa uma integração."""
    try:
        integration = ChatIntegration.query.get_or_404(integration_id)
        
        if integration.provider == "whatsapp_business":
            service = WhatsAppBusinessService(
                integration.api_token,
                integration.phone_number,
                integration.business_account_id
            )
            # Teste básico - enviar mensagem para número de teste
            result = service.send_text_message(
                integration.phone_number,
                "Teste de integração WhatsApp Business"
            )
        elif integration.provider == "evolution_api":
            service = EvolutionAPIService(
                integration.api_url,
                integration.api_token,
                integration.settings.get("instance_name", "default")
            )
            result = service.get_instance_status()
        else:
            return jsonify({"error": "Provedor de integração não suportado para teste"}), 400
        
        return jsonify({"message": "Teste de integração executado", "result": str(result)}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== AI CONFIG ====================

@chatbot_bp.route("/ai-config", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Configuração de IA"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Configuração de IA"},
        "401": {"description": "Não autorizado"}
    }
})
def get_ai_config():
    """Obtém a configuração de IA."""
    try:
        config = ChatAIConfig.query.first()
        if not config:
            return jsonify({"error": "Configuração de IA não encontrada"}), 404
        return jsonify(config.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/ai-config", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Chatbot - Configuração de IA"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChatAIConfigUpdate",
                "properties": {
                    "model": {"type": "string", "description": "Modelo de IA (e.g., gpt-4, gemini-pro)"},
                    "temperature": {"type": "number", "format": "float", "description": "Temperatura da IA"},
                    "max_tokens": {"type": "integer", "description": "Máximo de tokens para resposta"},
                    "system_prompt": {"type": "string", "description": "Prompt do sistema para a IA"},
                    "context_memory_enabled": {"type": "boolean", "description": "Habilitar memória de contexto"},
                    "context_memory_duration_minutes": {"type": "integer", "description": "Duração da memória de contexto em minutos"},
                    "ai_fallback_enabled": {"type": "boolean", "description": "Habilitar fallback para IA"},
                    "human_handoff_keywords": {"type": "array", "items": {"type": "string"}, "description": "Palavras-chave para transferência para humano"},
                    "typing_delay_ms": {"type": "integer", "description": "Atraso de digitação em milissegundos"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Configuração de IA atualizada com sucesso"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Configuração de IA não encontrada"}
    }
})
def update_ai_config():
    """Atualiza a configuração de IA."""
    try:
        config = ChatAIConfig.query.first()
        if not config:
            return jsonify({"error": "Configuração de IA não encontrada"}), 404
        
        data = request.get_json()
        
        if "model" in data:
            config.model = data["model"]
        if "temperature" in data:
            config.temperature = data["temperature"]
        if "max_tokens" in data:
            config.max_tokens = data["max_tokens"]
        if "system_prompt" in data:
            config.system_prompt = data["system_prompt"]
        if "context_memory_enabled" in data:
            config.context_memory_enabled = data["context_memory_enabled"]
        if "context_memory_duration_minutes" in data:
            config.context_memory_duration_minutes = data["context_memory_duration_minutes"]
        if "ai_fallback_enabled" in data:
            config.ai_fallback_enabled = data["ai_fallback_enabled"]
        if "human_handoff_keywords" in data:
            config.human_handoff_keywords = data["human_handoff_keywords"]
        if "typing_delay_ms" in data:
            config.typing_delay_ms = data["typing_delay_ms"]
        
        db.session.commit()
        return jsonify(config.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== WEBHOOKS ====================

@chatbot_bp.route("/webhooks/whatsapp", methods=["POST"])
@swag_from({
    "tags": ["Chatbot - Webhooks"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "description": "Payload do webhook do WhatsApp Business API"
            }
        }
    ],
    "responses": {
        "200": {"description": "Webhook recebido com sucesso"}
    }
})
def whatsapp_webhook():
    """Webhook para receber mensagens do WhatsApp Business API."""
    try:
        data = request.get_json()
        # Processar o payload do WhatsApp
        # Exemplo: whatsapp_service.process_webhook(data)
        print("Webhook WhatsApp recebido:", json.dumps(data, indent=2))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/webhooks/evolution", methods=["POST"])
@swag_from({
    "tags": ["Chatbot - Webhooks"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "description": "Payload do webhook da Evolution API"
            }
        }
    ],
    "responses": {
        "200": {"description": "Webhook recebido com sucesso"}
    }
})
def evolution_webhook():
    """Webhook para receber mensagens da Evolution API."""
    try:
        data = request.get_json()
        # Processar o payload da Evolution API
        # Exemplo: evolution_service.process_webhook(data)
        print("Webhook Evolution API recebido:", json.dumps(data, indent=2))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/webhooks/generic", methods=["POST"])
@swag_from({
    "tags": ["Chatbot - Webhooks"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "description": "Payload do webhook genérico"
            }
        }
    ],
    "responses": {
        "200": {"description": "Webhook recebido com sucesso"}
    }
})
def generic_webhook():
    """Webhook genérico para receber mensagens de outras fontes."""
    try:
        data = request.get_json()
        # Processar o payload genérico
        print("Webhook Genérico recebido:", json.dumps(data, indent=2))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


