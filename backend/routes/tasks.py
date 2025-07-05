from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

tasks_bp = Blueprint('tasks', __name__)

tasks_data = [
    {"id": 1, "title": "Ligar para cliente", "status": "pendente", "priority": "alta"},
    {"id": 2, "title": "Enviar proposta", "status": "concluída", "priority": "média"}
]

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def list_tasks():
    """Listar tarefas"""
    return jsonify({"tasks": tasks_data}), 200

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """Criar tarefa"""
    data = request.get_json()
    new_task = {
        "id": len(tasks_data) + 1,
        "title": data.get('title'),
        "status": "pendente",
        "priority": data.get('priority', 'média')
    }
    tasks_data.append(new_task)
    return jsonify({"message": "Tarefa criada", "task": new_task}), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Obter tarefa específica"""
    task = next((t for t in tasks_data if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    return jsonify({"task": task}), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Atualizar tarefa"""
    task = next((t for t in tasks_data if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    data = request.get_json()
    task.update(data)
    return jsonify({"message": "Tarefa atualizada", "task": task}), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Deletar tarefa"""
    global tasks_data
    tasks_data = [t for t in tasks_data if t['id'] != task_id]
    return jsonify({"message": "Tarefa deletada"}), 200

