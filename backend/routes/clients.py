from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

clients_bp = Blueprint('clients', __name__)

clients_data = [
    {
        "id": 1,
        "name": "Empresa ABC Ltda",
        "email": "contato@empresaabc.com",
        "phone": "(11) 3333-3333",
        "address": "Rua das Flores, 123",
        "status": "ativo"
    },
    {
        "id": 2,
        "name": "XYZ Tecnologia",
        "email": "info@xyztec.com",
        "phone": "(11) 4444-4444",
        "address": "Av. Paulista, 456",
        "status": "ativo"
    }
]

@clients_bp.route('/', methods=['GET'])
@jwt_required()
def list_clients():
    """Listar clientes"""
    return jsonify({"clients": clients_data, "total": len(clients_data)}), 200

@clients_bp.route('/', methods=['POST'])
@jwt_required()
def create_client():
    """Criar cliente"""
    data = request.get_json()
    new_client = {
        "id": len(clients_data) + 1,
        "name": data.get('name'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "address": data.get('address'),
        "status": "ativo"
    }
    clients_data.append(new_client)
    return jsonify({"message": "Cliente criado", "client": new_client}), 201

@clients_bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """Obter cliente específico"""
    client = next((c for c in clients_data if c['id'] == client_id), None)
    if not client:
        return jsonify({"error": "Cliente não encontrado"}), 404
    return jsonify({"client": client}), 200

@clients_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    """Atualizar cliente"""
    client = next((c for c in clients_data if c['id'] == client_id), None)
    if not client:
        return jsonify({"error": "Cliente não encontrado"}), 404
    
    data = request.get_json()
    client.update(data)
    return jsonify({"message": "Cliente atualizado", "client": client}), 200

@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    """Deletar cliente"""
    global clients_data
    clients_data = [c for c in clients_data if c['id'] != client_id]
    return jsonify({"message": "Cliente deletado"}), 200

@clients_bp.route('/<int:client_id>/interactions', methods=['GET'])
@jwt_required()
def get_client_interactions(client_id):
    """Histórico de interações"""
    interactions = [
        {"id": 1, "type": "call", "date": "2025-01-01", "notes": "Ligação de follow-up"},
        {"id": 2, "type": "email", "date": "2025-01-02", "notes": "Envio de proposta"}
    ]
    return jsonify({"interactions": interactions}), 200

@clients_bp.route('/<int:client_id>/interactions', methods=['POST'])
@jwt_required()
def create_client_interaction(client_id):
    """Registrar interação"""
    data = request.get_json()
    interaction = {
        "id": 3,
        "type": data.get('type'),
        "date": data.get('date'),
        "notes": data.get('notes')
    }
    return jsonify({"message": "Interação registrada", "interaction": interaction}), 201

@clients_bp.route('/<int:client_id>/stats', methods=['GET'])
@jwt_required()
def get_client_stats(client_id):
    """Estatísticas do cliente"""
    stats = {
        "total_interactions": 5,
        "total_proposals": 2,
        "total_revenue": 25000.00,
        "last_contact": "2025-01-02"
    }
    return jsonify({"stats": stats}), 200

