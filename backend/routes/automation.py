from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

automation_bp = Blueprint('automation', __name__)

@automation_bp.route('/workflows', methods=['GET'])
@jwt_required()
def list_workflows():
    """Listar workflows"""
    workflows = [
        {"id": 1, "name": "Follow-up automático", "status": "ativo", "triggers": 3},
        {"id": 2, "name": "Boas-vindas", "status": "ativo", "triggers": 1}
    ]
    return jsonify({"workflows": workflows}), 200

@automation_bp.route('/workflows', methods=['POST'])
@jwt_required()
def create_workflow():
    """Criar workflow"""
    data = request.get_json()
    workflow = {
        "id": 3,
        "name": data.get('name'),
        "status": "rascunho",
        "triggers": 0
    }
    return jsonify({"message": "Workflow criado", "workflow": workflow}), 201

@automation_bp.route('/workflows/<int:workflow_id>', methods=['GET'])
@jwt_required()
def get_workflow(workflow_id):
    """Obter workflow específico"""
    workflow = {"id": workflow_id, "name": "Workflow exemplo", "status": "ativo"}
    return jsonify({"workflow": workflow}), 200

@automation_bp.route('/workflows/<int:workflow_id>', methods=['PUT'])
@jwt_required()
def update_workflow(workflow_id):
    """Atualizar workflow"""
    data = request.get_json()
    return jsonify({"message": "Workflow atualizado"}), 200

@automation_bp.route('/workflows/<int:workflow_id>', methods=['DELETE'])
@jwt_required()
def delete_workflow(workflow_id):
    """Deletar workflow"""
    return jsonify({"message": "Workflow deletado"}), 200

@automation_bp.route('/trigger', methods=['POST'])
@jwt_required()
def trigger_automation():
    """Disparar automação"""
    return jsonify({"message": "Automação disparada"}), 200

@automation_bp.route('/actions', methods=['GET'])
@jwt_required()
def list_actions():
    """Listar ações disponíveis"""
    actions = [
        {"id": 1, "name": "Enviar email", "type": "communication"},
        {"id": 2, "name": "Criar tarefa", "type": "task"},
        {"id": 3, "name": "Atualizar status", "type": "update"}
    ]
    return jsonify({"actions": actions}), 200

@automation_bp.route('/conditions', methods=['GET'])
@jwt_required()
def list_conditions():
    """Listar condições disponíveis"""
    conditions = [
        {"id": 1, "name": "Novo lead", "type": "trigger"},
        {"id": 2, "name": "Email aberto", "type": "engagement"},
        {"id": 3, "name": "Proposta enviada", "type": "sales"}
    ]
    return jsonify({"conditions": conditions}), 200

