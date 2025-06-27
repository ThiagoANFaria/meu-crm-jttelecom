from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.task import Task, TaskComment
from datetime import datetime
from flasgger import swag_from

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Listar todas as tarefas',
    'description': 'Retorna uma lista paginada de todas as tarefas do tenant',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'description': 'Número da página'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Itens por página'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de tarefas retornada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'tasks': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Task'}
                    },
                    'total': {'type': 'integer'},
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'}
                }
            }
        }
    }
})
def get_tasks():
    """Get all tasks for the current tenant"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        tasks_query = Task.query.filter_by(tenant_id=user.tenant_id)
        tasks_paginated = tasks_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        tasks_data = []
        for task in tasks_paginated.items:
            tasks_data.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat() if task.created_at else None
            })
        
        return jsonify({
            "tasks": tasks_data,
            "total": tasks_paginated.total,
            "page": page,
            "per_page": per_page
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@task_bp.route("/", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Criar nova tarefa',
    'description': 'Cria uma nova tarefa no sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['title'],
                'properties': {
                    'title': {'type': 'string', 'description': 'Título da tarefa'},
                    'description': {'type': 'string', 'description': 'Descrição da tarefa'},
                    'priority': {'type': 'string', 'description': 'Prioridade (low, medium, high)'},
                    'due_date': {'type': 'string', 'description': 'Data de vencimento (YYYY-MM-DD)'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Tarefa criada com sucesso',
            'schema': {'$ref': '#/definitions/Task'}
        },
        400: {'description': 'Dados inválidos'}
    }
})
def create_task():
    """Create a new task"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({"error": "Título é obrigatório"}), 400
        
        # Parse due date
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400
        
        # Create new task
        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            due_date=due_date,
            status='pending',
            tenant_id=user.tenant_id,
            assigned_to=current_user_id,
            created_by=current_user_id
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "status": new_task.status,
            "priority": new_task.priority,
            "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
            "created_at": new_task.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@task_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Obter tarefa por ID',
    'description': 'Retorna os detalhes de uma tarefa específica',
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da tarefa'
        }
    ],
    'responses': {
        200: {
            'description': 'Tarefa encontrada',
            'schema': {'$ref': '#/definitions/Task'}
        },
        404: {'description': 'Tarefa não encontrada'}
    }
})
def get_task(task_id):
    """Get a specific task by ID"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        task = Task.query.filter_by(
            id=task_id, 
            tenant_id=user.tenant_id
        ).first()
        
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

