from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.task import (
    Task, TaskComment, TaskTimeLog, TaskTemplate, ActivitySummary,
    TaskType, TaskStatus, TaskPriority, RecurrenceType, db
)
from src.models.user import User
from src.models.lead import Lead
from src.services.task_service import TaskService
from datetime import datetime, date, timedelta
import logging
from flasgger import swag_from

task_bp = Blueprint("tasks", __name__)
logger = logging.getLogger(__name__)

# Inicializar serviço
task_service = TaskService()

# ==================== TAREFAS ====================

@task_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
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
            "name": "user_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do usuário responsável"
        },
        {
            "name": "status",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "description": "Filtrar por status da tarefa (e.g., PENDING, IN_PROGRESS, COMPLETED)"
        },
        {
            "name": "task_type",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "description": "Filtrar por tipo de tarefa (e.g., CALL, EMAIL, MEETING)"
        },
        {
            "name": "priority",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "description": "Filtrar por prioridade (e.g., LOW, MEDIUM, HIGH)"
        },
        {
            "name": "due_date_from",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data de vencimento a partir de (YYYY-MM-DD)"
        },
        {
            "name": "due_date_to",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data de vencimento até (YYYY-MM-DD)"
        },
        {
            "name": "lead_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do lead associado"
        },
        {
            "name": "opportunity_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID da oportunidade associada"
        },
        {
            "name": "tags",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "description": "Filtrar por tags"
        },
        {
            "name": "overdue_only",
            "in": "query",
            "type": "boolean",
            "description": "Mostrar apenas tarefas atrasadas"
        },
        {
            "name": "today_only",
            "in": "query",
            "type": "boolean",
            "description": "Mostrar apenas tarefas para hoje"
        },
        {
            "name": "sort_by",
            "in": "query",
            "type": "string",
            "description": "Campo para ordenação (e.g., due_date, created_at)",
            "default": "due_date"
        },
        {
            "name": "sort_order",
            "in": "query",
            "type": "string",
            "enum": ["asc", "desc"],
            "description": "Ordem de ordenação",
            "default": "asc"
        }
    ],
    "responses": {
        "200": {"description": "Lista de tarefas com filtros"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Sem permissão"}
    }
})
def list_tasks():
    """Lista tarefas com filtros"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros de paginação
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    
    # Filtros
    filters = {}
    
    # Usuário (padrão: usuário atual, admins podem ver de outros)
    user_id = request.args.get("user_id")
    if user_id:
        # Verificar permissão
        current_user = User.query.get(current_user_id)
        if current_user.role in ["admin", "manager"] or user_id == current_user_id:
            filters["user_id"] = user_id
        else:
            return jsonify({"error": "Sem permissão para ver tarefas de outros usuários"}), 403
    else:
        filters["user_id"] = current_user_id
    
    # Outros filtros
    if request.args.get("status"):
        filters["status"] = request.args.getlist("status")
    if request.args.get("task_type"):
        filters["task_type"] = request.args.getlist("task_type")
    if request.args.get("priority"):
        filters["priority"] = request.args.getlist("priority")
    if request.args.get("due_date_from"):
        filters["due_date_from"] = request.args.get("due_date_from")
    if request.args.get("due_date_to"):
        filters["due_date_to"] = request.args.get("due_date_to")
    if request.args.get("lead_id"):
        filters["lead_id"] = request.args.get("lead_id")
    if request.args.get("opportunity_id"):
        filters["opportunity_id"] = request.args.get("opportunity_id")
    if request.args.get("tags"):
        filters["tags"] = request.args.getlist("tags")
    if request.args.get("overdue_only") == "true":
        filters["overdue_only"] = True
    if request.args.get("today_only") == "true":
        filters["today_only"] = True
    
    # Ordenação
    filters["sort_by"] = request.args.get("sort_by", "due_date")
    filters["sort_order"] = request.args.get("sort_order", "asc")
    
    try:
        # Buscar tarefas
        tasks = task_service.get_user_tasks(filters["user_id"], filters)
        
        # Paginação manual (já que usamos método customizado)
        total = len(tasks)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_tasks = tasks[start:end]
        
        return jsonify({
            "tasks": paginated_tasks,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "current_page": page,
            "per_page": per_page
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar tarefas: {e}")
        return jsonify({"error": f"Erro ao listar tarefas: {str(e)}"}), 500

@task_bp.route("/", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TaskCreate",
                "required": ["title", "assigned_to"],
                "properties": {
                    "title": {"type": "string", "description": "Título da tarefa"},
                    "description": {"type": "string", "description": "Descrição da tarefa"},
                    "assigned_to": {"type": "string", "description": "ID do usuário responsável"},
                    "due_date": {"type": "string", "format": "date", "description": "Data de vencimento (YYYY-MM-DD)"},
                    "due_time": {"type": "string", "format": "time", "description": "Hora de vencimento (HH:MM)"},
                    "task_type": {"type": "string", "description": "Tipo de tarefa (e.g., CALL, EMAIL)"},
                    "status": {"type": "string", "description": "Status da tarefa (e.g., PENDING, IN_PROGRESS)"},
                    "priority": {"type": "string", "description": "Prioridade da tarefa (e.g., LOW, MEDIUM)"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags da tarefa"},
                    "is_recurring": {"type": "boolean", "description": "Se a tarefa é recorrente"},
                    "recurrence_type": {"type": "string", "description": "Tipo de recorrência (e.g., DAILY, WEEKLY)"},
                    "recurrence_interval": {"type": "integer", "description": "Intervalo da recorrência"},
                    "reminder_minutes": {"type": "integer", "description": "Minutos antes do vencimento para lembrete"},
                    "email_reminder": {"type": "boolean", "description": "Enviar lembrete por email"},
                    "sms_reminder": {"type": "boolean", "description": "Enviar lembrete por SMS"},
                    "custom_fields": {"type": "object", "description": "Campos customizados"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Tarefa criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"}
    }
})
def create_task():
    """Cria nova tarefa"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validações básicas
    required_fields = ["title", "assigned_to"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        result = task_service.create_task(data, current_user_id)
        
        if result.get("success"):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao criar tarefa: {e}")
        return jsonify({"error": f"Erro ao criar tarefa: {str(e)}"}), 500

@task_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de uma tarefa"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Sem permissão"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def get_task(task_id):
    """Obtém detalhes de uma tarefa"""
    current_user_id = get_jwt_identity()
    
    task = Task.query.get_or_404(task_id)
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if (task.assigned_to != current_user_id and 
        task.created_by != current_user_id and 
        current_user.role not in ["admin", "manager"]):
        return jsonify({"error": "Sem permissão para ver esta tarefa"}), 403
    
    # Incluir comentários e logs de tempo
    task_dict = task.to_dict()
    task_dict["comments"] = [comment.to_dict() for comment in task.comments]
    task_dict["time_logs"] = [log.to_dict() for log in task.time_logs]
    
    return jsonify(task_dict), 200

@task_bp.route("/<task_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TaskUpdate",
                "properties": {
                    "title": {"type": "string", "description": "Título da tarefa"},
                    "description": {"type": "string", "description": "Descrição da tarefa"},
                    "assigned_to": {"type": "string", "description": "ID do usuário responsável"},
                    "due_date": {"type": "string", "format": "date", "description": "Data de vencimento (YYYY-MM-DD)"},
                    "due_time": {"type": "string", "format": "time", "description": "Hora de vencimento (HH:MM)"},
                    "task_type": {"type": "string", "description": "Tipo de tarefa (e.g., CALL, EMAIL)"},
                    "status": {"type": "string", "description": "Status da tarefa (e.g., PENDING, IN_PROGRESS)"},
                    "priority": {"type": "string", "description": "Prioridade da tarefa (e.g., LOW, MEDIUM)"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags da tarefa"},
                    "is_recurring": {"type": "boolean", "description": "Se a tarefa é recorrente"},
                    "recurrence_type": {"type": "string", "description": "Tipo de recorrência (e.g., DAILY, WEEKLY)"},
                    "recurrence_interval": {"type": "integer", "description": "Intervalo da recorrência"},
                    "reminder_minutes": {"type": "integer", "description": "Minutos antes do vencimento para lembrete"},
                    "email_reminder": {"type": "boolean", "description": "Enviar lembrete por email"},
                    "sms_reminder": {"type": "boolean", "description": "Enviar lembrete por SMS"},
                    "custom_fields": {"type": "object", "description": "Campos customizados"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Tarefa atualizada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Sem permissão"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def update_task(task_id):
    """Atualiza tarefa"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        result = task_service.update_task(task_id, data, current_user_id)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao atualizar tarefa: {e}")
        return jsonify({"error": f"Erro ao atualizar tarefa: {str(e)}"}), 500

@task_bp.route("/<task_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        }
    ],
    "responses": {
        "200": {"description": "Tarefa removida com sucesso"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Sem permissão"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def delete_task(task_id):
    """Remove tarefa"""
    current_user_id = get_jwt_identity()
    
    task = Task.query.get_or_404(task_id)
    
    # Verificar permissões
    current_user = User.query.get(current_user_id)
    if (task.created_by != current_user_id and 
        current_user.role not in ["admin", "manager"]):
        return jsonify({"error": "Sem permissão para remover esta tarefa"}), 403
    
    try:
        # Soft delete
        task.is_active = False
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Tarefa removida com sucesso"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao remover tarefa: {e}")
        return jsonify({"error": f"Erro ao remover tarefa: {str(e)}"}), 500

@task_bp.route("/<task_id>/complete", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        },
        {
            "name": "body",
            "in": "body",
            "schema": {
                "id": "TaskComplete",
                "properties": {
                    "notes": {"type": "string", "description": "Notas de conclusão"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Tarefa marcada como completada"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def complete_task(task_id):
    """Marca tarefa como completada"""
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        result = task_service.complete_task(task_id, data, current_user_id)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao completar tarefa: {e}")
        return jsonify({"error": f"Erro ao completar tarefa: {str(e)}"}), 500

@task_bp.route("/<task_id>/reschedule", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TaskReschedule",
                "required": ["new_due_date"],
                "properties": {
                    "new_due_date": {"type": "string", "format": "date", "description": "Nova data de vencimento (YYYY-MM-DD)"},
                    "new_due_time": {"type": "string", "format": "time", "description": "Nova hora de vencimento (HH:MM)"},
                    "reason": {"type": "string", "description": "Motivo do reagendamento"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Tarefa reagendada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def reschedule_task(task_id):
    """Reagenda tarefa"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if "new_due_date" not in data:
        return jsonify({"error": "Campo new_due_date é obrigatório"}), 400
    
    try:
        result = task_service.reschedule_task(
            task_id=task_id,
            new_due_date=data["new_due_date"],
            new_due_time=data.get("new_due_time"),
            reason=data.get("reason"),
            rescheduled_by=current_user_id
        )
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao reagendar tarefa: {e}")
        return jsonify({"error": f"Erro ao reagendar tarefa: {str(e)}"}), 500

@task_bp.route("/<task_id>/start", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        }
    ],
    "responses": {
        "200": {"description": "Tarefa iniciada com sucesso"},
        "400": {"description": "Tarefa não está pendente"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Sem permissão"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def start_task(task_id):
    """Inicia tarefa"""
    current_user_id = get_jwt_identity()
    
    task = Task.query.get_or_404(task_id)
    
    # Verificar se é o responsável
    if task.assigned_to != current_user_id:
        return jsonify({"error": "Apenas o responsável pode iniciar a tarefa"}), 403
    
    if task.status != TaskStatus.PENDING:
        return jsonify({"error": "Tarefa não está pendente"}), 400
    
    try:
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Tarefa iniciada com sucesso",
            "task": task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao iniciar tarefa: {e}")
        return jsonify({"error": f"Erro ao iniciar tarefa: {str(e)}"}), 500

# ==================== COMENTÁRIOS ====================

@task_bp.route("/<task_id>/comments", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Comentários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        }
    ],
    "responses": {
        "200": {"description": "Lista de comentários de uma tarefa"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def list_task_comments(task_id):
    """Lista comentários de uma tarefa"""
    task = Task.query.get_or_404(task_id)
    
    comments = TaskComment.query.filter_by(task_id=task_id).order_by(TaskComment.created_at.desc()).all()
    
    return jsonify({
        "comments": [comment.to_dict() for comment in comments]
    }), 200

@task_bp.route("/<task_id>/comments", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Comentários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TaskCommentCreate",
                "required": ["content"],
                "properties": {
                    "content": {"type": "string", "description": "Conteúdo do comentário"},
                    "comment_type": {"type": "string", "description": "Tipo de comentário (e.g., comment, note)"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Comentário adicionado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def add_task_comment(task_id):
    """Adiciona comentário a uma tarefa"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if "content" not in data:
        return jsonify({"error": "Campo content é obrigatório"}), 400
    
    task = Task.query.get_or_404(task_id)
    
    try:
        comment = TaskComment(
            task_id=task_id,
            content=data["content"],
            comment_type=data.get("comment_type", "comment"),
            created_by=current_user_id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Comentário adicionado com sucesso",
            "comment": comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao adicionar comentário: {e}")
        return jsonify({"error": f"Erro ao adicionar comentário: {str(e)}"}), 500

# ==================== LOGS DE TEMPO ====================

@task_bp.route("/<task_id>/time-logs", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Logs de Tempo"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        }
    ],
    "responses": {
        "200": {"description": "Lista de logs de tempo de uma tarefa"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def list_task_time_logs(task_id):
    """Lista logs de tempo de uma tarefa"""
    task = Task.query.get_or_404(task_id)
    
    time_logs = TaskTimeLog.query.filter_by(task_id=task_id).order_by(TaskTimeLog.start_time.desc()).all()
    
    return jsonify({
        "time_logs": [log.to_dict() for log in time_logs],
        "total_time": sum(log.duration_minutes or 0 for log in time_logs)
    }), 200

@task_bp.route("/<task_id>/time-logs", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Logs de Tempo"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tarefa"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TaskTimeLogCreate",
                "required": ["start_time"],
                "properties": {
                    "start_time": {"type": "string", "format": "date-time", "description": "Hora de início do log (YYYY-MM-DDTHH:MM:SS)"},
                    "end_time": {"type": "string", "format": "date-time", "description": "Hora de fim do log (YYYY-MM-DDTHH:MM:SS)"},
                    "duration_minutes": {"type": "integer", "description": "Duração em minutos"},
                    "notes": {"type": "string", "description": "Notas do log de tempo"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Log de tempo adicionado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tarefa não encontrada"}
    }
})
def add_time_log(task_id):
    """Adiciona log de tempo a uma tarefa"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ["start_time"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        result = task_service.add_time_log(task_id, data, current_user_id)
        
        if result.get("success"):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao adicionar log de tempo: {e}")
        return jsonify({"error": f"Erro ao adicionar log de tempo: {str(e)}"}), 500

# ==================== TEMPLATES ====================

@task_bp.route("/templates", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Templates"],
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
            "name": "is_public",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por templates públicos"
        },
        {
            "name": "task_type",
            "in": "query",
            "type": "string",
            "description": "Filtrar por tipo de tarefa"
        },
        {
            "name": "category",
            "in": "query",
            "type": "string",
            "description": "Filtrar por categoria"
        }
    ],
    "responses": {
        "200": {"description": "Lista de templates de tarefas"},
        "401": {"description": "Não autorizado"}
    }
})
def list_task_templates():
    """Lista templates de tarefas"""
    current_user_id = get_jwt_identity()
    
    # Buscar templates públicos e do usuário
    templates = TaskTemplate.query.filter(
        (TaskTemplate.is_public == True) | (TaskTemplate.created_by == current_user_id),
        TaskTemplate.is_active == True
    ).order_by(TaskTemplate.name.asc()).all()
    
    return jsonify({
        "templates": [template.to_dict() for template in templates]
    }), 200

@task_bp.route("/templates", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Templates"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TaskTemplateCreate",
                "required": ["name", "title_template", "task_type"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do template"},
                    "description": {"type": "string", "description": "Descrição do template"},
                    "title_template": {"type": "string", "description": "Template do título da tarefa"},
                    "description_template": {"type": "string", "description": "Template da descrição da tarefa"},
                    "task_type": {"type": "string", "description": "Tipo de tarefa (e.g., CALL, EMAIL)"},
                    "category": {"type": "string", "description": "Categoria do template"},
                    "priority": {"type": "string", "description": "Prioridade padrão (e.g., LOW, MEDIUM)"},
                    "default_duration_minutes": {"type": "integer", "description": "Duração padrão em minutos"},
                    "default_reminder_minutes": {"type": "integer", "description": "Minutos antes do vencimento para lembrete padrão"},
                    "default_recurrence_type": {"type": "string", "description": "Tipo de recorrência padrão (e.g., DAILY, WEEKLY)"},
                    "default_recurrence_interval": {"type": "integer", "description": "Intervalo da recorrência padrão"},
                    "default_email_reminder": {"type": "boolean", "description": "Enviar lembrete por email por padrão"},
                    "default_sms_reminder": {"type": "boolean", "description": "Enviar lembrete por SMS por padrão"},
                    "custom_fields_config": {"type": "object", "description": "Configuração de campos customizados"},
                    "is_active": {"type": "boolean", "description": "Se o template está ativo"},
                    "is_public": {"type": "boolean", "description": "Se o template é público"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Template criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"}
    }
})
def create_task_template():
    """Cria template de tarefa"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ["name", "title_template", "task_type"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        template = TaskTemplate(
            name=data["name"],
            description=data.get("description"),
            title_template=data["title_template"],
            description_template=data.get("description_template"),
            task_type=TaskType(data["task_type"]),
            category=data.get("category"),
            priority=TaskPriority(data.get("priority", "medium")),
            default_duration_minutes=data.get("default_duration_minutes"),
            default_reminder_minutes=data.get("default_reminder_minutes"),
            default_recurrence_type=RecurrenceType(data.get("default_recurrence_type", "none")),
            default_recurrence_interval=data.get("default_recurrence_interval", 1),
            default_email_reminder=data.get("default_email_reminder", True),
            default_sms_reminder=data.get("default_sms_reminder", False),
            custom_fields_config=data.get("custom_fields_config", {}),
            is_active=data.get("is_active", True),
            is_public=data.get("is_public", False),
            created_by=current_user_id
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Template criado com sucesso",
            "template": template.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar template: {e}")
        return jsonify({"error": f"Erro ao criar template: {str(e)}"}), 500

@task_bp.route("/templates/<template_id>/create-task", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Templates"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "template_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do template"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TaskFromTemplateCreate",
                "required": ["assigned_to"],
                "properties": {
                    "assigned_to": {"type": "string", "description": "ID do usuário responsável"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "due_date": {"type": "string", "format": "date", "description": "Data de vencimento (YYYY-MM-DD)"},
                    "custom_data": {"type": "object", "description": "Dados customizados para a tarefa"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Tarefa criada a partir do template"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Template não encontrado"}
    }
})
def create_task_from_template(template_id):
    """Cria tarefa a partir de template"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    template = TaskTemplate.query.get_or_404(template_id)
    
    if "assigned_to" not in data:
        return jsonify({"error": "Campo assigned_to é obrigatório"}), 400
    
    try:
        # Processar data de vencimento
        due_date = None
        if data.get("due_date"):
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        
        # Criar tarefa a partir do template
        task = template.create_task_from_template(
            assigned_to=data["assigned_to"],
            created_by=current_user_id,
            lead_id=data.get("lead_id"),
            opportunity_id=data.get("opportunity_id"),
            due_date=due_date,
            custom_data=data.get("custom_data", {})
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Tarefa criada a partir do template",
            "task": task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar tarefa do template: {e}")
        return jsonify({"error": f"Erro ao criar tarefa do template: {str(e)}"}), 500

# ==================== DASHBOARDS E RELATÓRIOS ====================

@task_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Dashboard"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "user_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do usuário (para admins/managers)"
        },
        {
            "name": "start_date",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data de início para o dashboard (YYYY-MM-DD)"
        },
        {
            "name": "end_date",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data de fim para o dashboard (YYYY-MM-DD)"
        }
    ],
    "responses": {
        "200": {"description": "Estatísticas do dashboard de tarefas"},
        "401": {"description": "Não autorizado"}
    }
})
def get_task_dashboard_stats():
    """Obtém estatísticas para o dashboard de tarefas"""
    current_user_id = get_jwt_identity()
    
    user_id_filter = request.args.get("user_id")
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

    # Se não for admin/manager, só pode ver as próprias estatísticas
    current_user = User.query.get(current_user_id)
    if current_user.role not in ["admin", "manager"]:
        user_id_filter = current_user_id
    
    stats = task_service.get_dashboard_stats(user_id_filter, start_date, end_date)
    
    return jsonify(stats), 200

@task_bp.route("/activity-summary", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Tarefas - Relatórios"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "user_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do usuário (para admins/managers)"
        },
        {
            "name": "start_date",
            "in": "query",
            "type": "string",
            "format": "date",
            "required": True,
            "description": "Data de início para o resumo (YYYY-MM-DD)"
        },
        {
            "name": "end_date",
            "in": "query",
            "type": "string",
            "format": "date",
            "required": True,
            "description": "Data de fim para o resumo (YYYY-MM-DD)"
        }
    ],
    "responses": {
        "200": {"description": "Resumo de atividades por usuário e período"},
        "400": {"description": "Datas inválidas"},
        "401": {"description": "Não autorizado"}
    }
})
def get_activity_summary():
    """Obtém resumo de atividades por usuário e período"""
    current_user_id = get_jwt_identity()
    
    user_id_filter = request.args.get("user_id")
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    if not start_date_str or not end_date_str:
        return jsonify({"error": "start_date e end_date são obrigatórios"}), 400

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    # Se não for admin/manager, só pode ver as próprias estatísticas
    current_user = User.query.get(current_user_id)
    if current_user.role not in ["admin", "manager"]:
        user_id_filter = current_user_id

    summary = task_service.get_activity_summary(user_id_filter, start_date, end_date)
    
    return jsonify(summary), 200


