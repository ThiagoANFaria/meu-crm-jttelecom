from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.chatbot import ChatFlow, ChatConversation, ChatMessage
# Importação opcional de flasgger
try:
    from flasgger import swag_from
except ImportError:
    # Fallback se flasgger não estiver disponível
    def swag_from(spec):
        def decorator(func):
            return func
        return decorator

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Chatbot'],
    'summary': 'Listar conversas do chatbot',
    'description': 'Retorna uma lista de conversas do chatbot',
    'responses': {
        200: {
            'description': 'Lista de conversas retornada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'conversations': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/ChatConversation'}
                    }
                }
            }
        }
    }
})
def get_conversations():
    """Get chatbot conversations"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        conversations = ChatConversation.query.filter_by(tenant_id=user.tenant_id).all()
        
        conversations_data = []
        for conv in conversations:
            conversations_data.append({
                "id": conv.id,
                "title": conv.title,
                "status": conv.status,
                "created_at": conv.created_at.isoformat() if conv.created_at else None
            })
        
        return jsonify({"conversations": conversations_data}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@chatbot_bp.route("/message", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Chatbot'],
    'summary': 'Enviar mensagem para o chatbot',
    'description': 'Envia uma mensagem para o chatbot e recebe uma resposta',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['message'],
                'properties': {
                    'message': {'type': 'string', 'description': 'Mensagem para o chatbot'},
                    'conversation_id': {'type': 'string', 'description': 'ID da conversa (opcional)'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Resposta do chatbot',
            'schema': {
                'type': 'object',
                'properties': {
                    'response': {'type': 'string'},
                    'conversation_id': {'type': 'string'}
                }
            }
        }
    }
})
def send_message():
    """Send message to chatbot"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        # Simular resposta do chatbot
        bot_response = f"Olá! Recebi sua mensagem: '{message}'. Como posso ajudá-lo?"
        
        return jsonify({
            "response": bot_response,
            "conversation_id": "conv_123",
            "timestamp": "2024-06-27T12:00:00Z"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

