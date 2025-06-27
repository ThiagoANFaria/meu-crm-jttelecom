from flask import Blueprint, jsonify, request
from datetime import datetime
import logging

tasks_bp = Blueprint("tasks", __name__)
logger = logging.getLogger(__name__)

@tasks_bp.route("/", methods=["GET"])
def list_tasks():
    """Listar todas as tarefas"""
    return jsonify([
        {
            "id": 1,
            "title": "Ligar para lead João Silva",
            "description": "Fazer follow-up da proposta enviada",
            "status": "pendente",
            "priority": "alta",
            "due_date": "2025-06-28",
            "assigned_to": "Vendedor 1",
            "created_at": "2025-06-27T10:00:00"
        },
        {
            "id": 2,
            "title": "Enviar contrato para Maria Santos",
            "description": "Preparar e enviar contrato final",
            "status": "em_andamento",
            "priority": "media",
            "due_date": "2025-06-29",
            "assigned_to": "Vendedor 2",
            "created_at": "2025-06-27T11:30:00"
        }
    ])

@tasks_bp.route("/", methods=["POST"])
def create_task():
    """Criar nova tarefa"""
    data = request.get_json() or {}
    
    new_task = {
        "id": 3,
        "title": data.get("title", "Nova tarefa"),
        "description": data.get("description", ""),
        "status": "pendente",
        "priority": data.get("priority", "media"),
        "due_date": data.get("due_date"),
        "assigned_to": data.get("assigned_to"),
        "created_at": datetime.now().isoformat()
    }
    
    return jsonify(new_task), 201

@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Obter tarefa específica"""
    return jsonify({
        "id": task_id,
        "title": f"Tarefa {task_id}",
        "description": "Descrição da tarefa",
        "status": "pendente",
        "priority": "media",
        "due_date": "2025-06-30",
        "assigned_to": "Usuário",
        "created_at": "2025-06-27T12:00:00"
    })

@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Atualizar tarefa"""
    data = request.get_json() or {}
    
    updated_task = {
        "id": task_id,
        "title": data.get("title", f"Tarefa {task_id}"),
        "description": data.get("description", ""),
        "status": data.get("status", "pendente"),
        "priority": data.get("priority", "media"),
        "due_date": data.get("due_date"),
        "assigned_to": data.get("assigned_to"),
        "updated_at": datetime.now().isoformat()
    }
    
    return jsonify(updated_task)

@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletar tarefa"""
    return jsonify({"message": f"Tarefa {task_id} deletada com sucesso"})

