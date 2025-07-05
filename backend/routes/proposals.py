from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

proposals_bp = Blueprint('proposals', __name__)

proposals_data = [
    {"id": 1, "title": "Proposta Sistema CRM", "value": 15000.00, "status": "enviada"},
    {"id": 2, "title": "Proposta Telefonia", "value": 8500.00, "status": "aprovada"}
]

@proposals_bp.route('/', methods=['GET'])
@jwt_required()
def list_proposals():
    """Listar propostas"""
    return jsonify({"proposals": proposals_data}), 200

@proposals_bp.route('/', methods=['POST'])
@jwt_required()
def create_proposal():
    """Criar proposta"""
    data = request.get_json()
    new_proposal = {
        "id": len(proposals_data) + 1,
        "title": data.get('title'),
        "value": data.get('value'),
        "status": "rascunho"
    }
    proposals_data.append(new_proposal)
    return jsonify({"message": "Proposta criada", "proposal": new_proposal}), 201

@proposals_bp.route('/<int:proposal_id>', methods=['GET'])
@jwt_required()
def get_proposal(proposal_id):
    """Obter proposta específica"""
    proposal = next((p for p in proposals_data if p['id'] == proposal_id), None)
    if not proposal:
        return jsonify({"error": "Proposta não encontrada"}), 404
    return jsonify({"proposal": proposal}), 200

@proposals_bp.route('/<int:proposal_id>', methods=['PUT'])
@jwt_required()
def update_proposal(proposal_id):
    """Atualizar proposta"""
    proposal = next((p for p in proposals_data if p['id'] == proposal_id), None)
    if not proposal:
        return jsonify({"error": "Proposta não encontrada"}), 404
    
    data = request.get_json()
    proposal.update(data)
    return jsonify({"message": "Proposta atualizada", "proposal": proposal}), 200

@proposals_bp.route('/<int:proposal_id>', methods=['DELETE'])
@jwt_required()
def delete_proposal(proposal_id):
    """Deletar proposta"""
    global proposals_data
    proposals_data = [p for p in proposals_data if p['id'] != proposal_id]
    return jsonify({"message": "Proposta deletada"}), 200

@proposals_bp.route('/<int:proposal_id>/approve', methods=['POST'])
@jwt_required()
def approve_proposal(proposal_id):
    """Aprovar proposta"""
    proposal = next((p for p in proposals_data if p['id'] == proposal_id), None)
    if not proposal:
        return jsonify({"error": "Proposta não encontrada"}), 404
    
    proposal['status'] = 'aprovada'
    return jsonify({"message": "Proposta aprovada", "proposal": proposal}), 200

@proposals_bp.route('/<int:proposal_id>/reject', methods=['POST'])
@jwt_required()
def reject_proposal(proposal_id):
    """Rejeitar proposta"""
    proposal = next((p for p in proposals_data if p['id'] == proposal_id), None)
    if not proposal:
        return jsonify({"error": "Proposta não encontrada"}), 404
    
    proposal['status'] = 'rejeitada'
    return jsonify({"message": "Proposta rejeitada", "proposal": proposal}), 200

@proposals_bp.route('/<int:proposal_id>/send', methods=['POST'])
@jwt_required()
def send_proposal(proposal_id):
    """Enviar proposta"""
    proposal = next((p for p in proposals_data if p['id'] == proposal_id), None)
    if not proposal:
        return jsonify({"error": "Proposta não encontrada"}), 404
    
    proposal['status'] = 'enviada'
    return jsonify({"message": "Proposta enviada", "proposal": proposal}), 200

@proposals_bp.route('/<int:proposal_id>/duplicate', methods=['POST'])
@jwt_required()
def duplicate_proposal(proposal_id):
    """Duplicar proposta"""
    proposal = next((p for p in proposals_data if p['id'] == proposal_id), None)
    if not proposal:
        return jsonify({"error": "Proposta não encontrada"}), 404
    
    new_proposal = proposal.copy()
    new_proposal['id'] = len(proposals_data) + 1
    new_proposal['title'] = f"{proposal['title']} (Cópia)"
    new_proposal['status'] = 'rascunho'
    
    proposals_data.append(new_proposal)
    return jsonify({"message": "Proposta duplicada", "proposal": new_proposal}), 201

