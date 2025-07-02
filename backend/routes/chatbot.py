from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/conversations', methods=['GET'])
@jwt_required()
def list_conversations():
    """Listar conversas"""
    conversations = [
        {"id": 1, "client": "João Silva", "status": "ativa", "messages": 5},
        {"id": 2, "client": "Maria Santos", "status": "finalizada", "messages": 12}
    ]
    return jsonify({"conversations": conversations}), 200

@chatbot_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """Enviar mensagem"""
    data = request.get_json()
    return jsonify({"message": "Mensagem enviada", "response": "Obrigado pelo contato!"}), 200

