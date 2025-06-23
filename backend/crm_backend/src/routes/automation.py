from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.automation import (
    AutomationRule, AutomationAction, AutomationExecution,
    EmailCampaign, CadenceSequence, CadenceStep, CadenceEnrollment,
    TriggerType, ActionType, db
)
from src.models.lead import Lead
from src.models.user import User
from src.services.automation_service import AutomationEngine, CadenceService
from datetime import datetime, timedelta
import logging
from flasgger import swag_from

automation_bp = Blueprint("automation", __name__)
logger = logging.getLogger(__name__)

# Inicializar serviços
automation_engine = AutomationEngine()
cadence_service = CadenceService()

# ==================== REGRAS DE AUTOMAÇÃO ====================

@automation_bp.route("/rules", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Regras"],
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
            "name": "is_active",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por regras ativas"
        },
        {
            "name": "trigger_type",
            "in": "query",
            "type": "string",
            "description": "Filtrar por tipo de gatilho"
        }
    ],
    "responses": {
        "200": {"description": "Lista de regras de automação"},
        "400": {"description": "Tipo de gatilho inválido"},
        "401": {"description": "Não autorizado"}
    }
})
def list_automation_rules():
    """Lista regras de automação"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    is_active = request.args.get("is_active", type=bool)
    trigger_type = request.args.get("trigger_type")
    
    query = AutomationRule.query
    
    if is_active is not None:
        query = query.filter(AutomationRule.is_active == is_active)
    
    if trigger_type:
        try:
            trigger_enum = TriggerType(trigger_type)
            query = query.filter(AutomationRule.trigger_type == trigger_enum)
        except ValueError:
            return jsonify({"error": "Tipo de gatilho inválido"}), 400
    
    query = query.order_by(AutomationRule.priority.desc(), AutomationRule.created_at.desc())
    
    rules = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "rules": [rule.to_dict() for rule in rules.items],
        "total": rules.total,
        "pages": rules.pages,
        "current_page": page,
        "per_page": per_page
    }), 200

@automation_bp.route("/rules", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Regras"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "AutomationRuleCreate",
                "required": ["name", "trigger_type"],
                "properties": {
                    "name": {"type": "string", "description": "Nome da regra"},
                    "description": {"type": "string", "description": "Descrição da regra"},
                    "trigger_type": {"type": "string", "description": "Tipo de gatilho (e.g., LEAD_CREATED, LEAD_STATUS_CHANGED)"},
                    "trigger_conditions": {"type": "object", "description": "Condições para o gatilho"},
                    "filters": {"type": "object", "description": "Filtros adicionais para a regra"},
                    "delay_minutes": {"type": "integer", "description": "Atraso em minutos antes de executar as ações"},
                    "is_active": {"type": "boolean", "description": "Se a regra está ativa"},
                    "priority": {"type": "integer", "description": "Prioridade da regra"},
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["action_type"],
                            "properties": {
                                "action_type": {"type": "string", "description": "Tipo de ação (e.g., SEND_EMAIL, CREATE_TASK)"},
                                "action_config": {"type": "object", "description": "Configuração da ação"},
                                "order": {"type": "integer", "description": "Ordem de execução da ação"},
                                "conditions": {"type": "object", "description": "Condições para a ação"},
                                "is_active": {"type": "boolean", "description": "Se a ação está ativa"}
                            }
                        }
                    }
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Regra de automação criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"}
    }
})
def create_automation_rule():
    """Cria nova regra de automação"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validações
    required_fields = ["name", "trigger_type"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        trigger_type = TriggerType(data["trigger_type"])
    except ValueError:
        return jsonify({"error": "Tipo de gatilho inválido"}), 400
    
    try:
        rule = AutomationRule(
            name=data["name"],
            description=data.get("description"),
            trigger_type=trigger_type,
            trigger_conditions=data.get("trigger_conditions", {}),
            filters=data.get("filters", {}),
            delay_minutes=data.get("delay_minutes", 0),
            is_active=data.get("is_active", True),
            priority=data.get("priority", 1),
            created_by=current_user_id
        )
        
        db.session.add(rule)
        db.session.flush()  # Para obter o ID
        
        # Criar ações
        actions_data = data.get("actions", [])
        for action_data in actions_data:
            try:
                action_type = ActionType(action_data["action_type"])
            except ValueError:
                return jsonify({"error": f"Tipo de ação inválido: {action_data['action_type']}"}), 400
            
            action = AutomationAction(
                rule_id=rule.id,
                action_type=action_type,
                action_config=action_data.get("action_config", {}),
                order=action_data.get("order", 1),
                conditions=action_data.get("conditions", {}),
                is_active=action_data.get("is_active", True)
            )
            
            db.session.add(action)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Regra de automação criada com sucesso",
            "rule": rule.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar regra de automação: {e}")
        return jsonify({"error": f"Erro ao criar regra: {str(e)}"}), 500

@automation_bp.route("/rules/<rule_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Regras"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "rule_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da regra"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de uma regra de automação"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Regra não encontrada"}
    }
})
def get_automation_rule(rule_id):
    """Obtém detalhes de uma regra de automação"""
    rule = AutomationRule.query.get_or_404(rule_id)
    return jsonify(rule.to_dict()), 200

@automation_bp.route("/rules/<rule_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Regras"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "rule_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da regra"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "AutomationRuleUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome da regra"},
                    "description": {"type": "string", "description": "Descrição da regra"},
                    "trigger_conditions": {"type": "object", "description": "Condições para o gatilho"},
                    "filters": {"type": "object", "description": "Filtros adicionais para a regra"},
                    "delay_minutes": {"type": "integer", "description": "Atraso em minutos antes de executar as ações"},
                    "is_active": {"type": "boolean", "description": "Se a regra está ativa"},
                    "priority": {"type": "integer", "description": "Prioridade da regra"},
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["action_type"],
                            "properties": {
                                "action_type": {"type": "string", "description": "Tipo de ação (e.g., SEND_EMAIL, CREATE_TASK)"},
                                "action_config": {"type": "object", "description": "Configuração da ação"},
                                "order": {"type": "integer", "description": "Ordem de execução da ação"},
                                "conditions": {"type": "object", "description": "Condições para a ação"},
                                "is_active": {"type": "boolean", "description": "Se a ação está ativa"}
                            }
                        }
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Regra de automação atualizada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Regra não encontrada"}
    }
})
def update_automation_rule(rule_id):
    """Atualiza regra de automação"""
    rule = AutomationRule.query.get_or_404(rule_id)
    data = request.get_json()
    
    try:
        # Atualizar campos básicos
        if "name" in data:
            rule.name = data["name"]
        if "description" in data:
            rule.description = data["description"]
        if "trigger_conditions" in data:
            rule.trigger_conditions = data["trigger_conditions"]
        if "filters" in data:
            rule.filters = data["filters"]
        if "delay_minutes" in data:
            rule.delay_minutes = data["delay_minutes"]
        if "is_active" in data:
            rule.is_active = data["is_active"]
        if "priority" in data:
            rule.priority = data["priority"]
        
        rule.updated_at = datetime.utcnow()
        
        # Atualizar ações se fornecidas
        if "actions" in data:
            # Remover ações existentes
            AutomationAction.query.filter_by(rule_id=rule.id).delete()
            
            # Criar novas ações
            for action_data in data["actions"]:
                try:
                    action_type = ActionType(action_data["action_type"])
                except ValueError:
                    return jsonify({"error": f"Tipo de ação inválido: {action_data['action_type']}"}), 400
                
                action = AutomationAction(
                    rule_id=rule.id,
                    action_type=action_type,
                    action_config=action_data.get("action_config", {}),
                    order=action_data.get("order", 1),
                    conditions=action_data.get("conditions", {}),
                    is_active=action_data.get("is_active", True)
                )
                
                db.session.add(action)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Regra atualizada com sucesso",
            "rule": rule.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao atualizar regra: {e}")
        return jsonify({"error": f"Erro ao atualizar regra: {str(e)}"}), 500

@automation_bp.route("/rules/<rule_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Regras"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "rule_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da regra"
        }
    ],
    "responses": {
        "200": {"description": "Regra removida com sucesso"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Regra não encontrada"}
    }
})
def delete_automation_rule(rule_id):
    """Remove regra de automação"""
    rule = AutomationRule.query.get_or_404(rule_id)
    
    try:
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Regra removida com sucesso"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao remover regra: {e}")
        return jsonify({"error": f"Erro ao remover regra: {str(e)}"}), 500

@automation_bp.route("/rules/<rule_id>/toggle", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Regras"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "rule_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da regra"
        }
    ],
    "responses": {
        "200": {"description": "Regra ativada/desativada com sucesso"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Regra não encontrada"}
    }
})
def toggle_automation_rule(rule_id):
    """Ativa/desativa regra de automação"""
    rule = AutomationRule.query.get_or_404(rule_id)
    
    rule.is_active = not rule.is_active
    rule.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    status = "ativada" if rule.is_active else "desativada"
    
    return jsonify({
        "success": True,
        "message": f"Regra {status} com sucesso",
        "is_active": rule.is_active
    }), 200

# ==================== EXECUÇÕES ====================

@automation_bp.route("/executions", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Execuções"],
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
            "name": "rule_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID da regra"
        },
        {
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "Filtrar por status da execução"
        },
        {
            "name": "target_type",
            "in": "query",
            "type": "string",
            "description": "Filtrar por tipo de alvo"
        }
    ],
    "responses": {
        "200": {"description": "Lista de execuções de automação"},
        "401": {"description": "Não autorizado"}
    }
})
def list_executions():
    """Lista execuções de automação"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    rule_id = request.args.get("rule_id")
    status = request.args.get("status")
    target_type = request.args.get("target_type")
    
    query = AutomationExecution.query
    
    if rule_id:
        query = query.filter(AutomationExecution.rule_id == rule_id)
    if status:
        query = query.filter(AutomationExecution.status == status)
    if target_type:
        query = query.filter(AutomationExecution.target_type == target_type)
    
    query = query.order_by(AutomationExecution.created_at.desc())
    
    executions = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "executions": [execution.to_dict() for execution in executions.items],
        "total": executions.total,
        "pages": executions.pages,
        "current_page": page,
        "per_page": per_page
    }), 200

@automation_bp.route("/executions/<execution_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Execuções"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "execution_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da execução"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de uma execução"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Execução não encontrada"}
    }
})
def get_execution(execution_id):
    """Obtém detalhes de uma execução"""
    execution = AutomationExecution.query.get_or_404(execution_id)
    return jsonify(execution.to_dict()), 200

@automation_bp.route("/trigger", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Execuções"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "AutomationTrigger",
                "required": ["trigger_type", "trigger_data"],
                "properties": {
                    "trigger_type": {"type": "string", "description": "Tipo de gatilho (e.g., LEAD_CREATED)"},
                    "trigger_data": {"type": "object", "description": "Dados do gatilho"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Automação disparada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"}
    }
})
def trigger_automation():
    """Dispara automação manualmente"""
    data = request.get_json()
    
    required_fields = ["trigger_type", "trigger_data"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        trigger_type = TriggerType(data["trigger_type"])
    except ValueError:
        return jsonify({"error": "Tipo de gatilho inválido"}), 400
    
    try:
        execution_ids = automation_engine.trigger_automation(trigger_type, data["trigger_data"])
        
        return jsonify({
            "success": True,
            "message": f"{len(execution_ids)} automações disparadas",
            "execution_ids": execution_ids
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao disparar automação: {e}")
        return jsonify({"error": f"Erro ao disparar automação: {str(e)}"}), 500

# ==================== CAMPANHAS DE EMAIL ====================

@automation_bp.route("/email-campaigns", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Campanhas de Email"],
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
            "name": "is_active",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por campanhas ativas"
        }
    ],
    "responses": {
        "200": {"description": "Lista de campanhas de email"},
        "401": {"description": "Não autorizado"}
    }
})
def list_email_campaigns():
    """Lista campanhas de email"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    is_active = request.args.get("is_active", type=bool)
    
    query = EmailCampaign.query
    
    if is_active is not None:
        query = query.filter(EmailCampaign.is_active == is_active)
    
    query = query.order_by(EmailCampaign.created_at.desc())
    
    campaigns = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "campaigns": [campaign.to_dict() for campaign in campaigns.items],
        "total": campaigns.total,
        "pages": campaigns.pages,
        "current_page": page,
        "per_page": per_page
    }), 200

@automation_bp.route("/email-campaigns", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Campanhas de Email"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "EmailCampaignCreate",
                "required": ["name", "subject", "content"],
                "properties": {
                    "name": {"type": "string", "description": "Nome da campanha"},
                    "description": {"type": "string", "description": "Descrição da campanha"},
                    "subject": {"type": "string", "description": "Assunto do email"},
                    "content": {"type": "string", "description": "Conteúdo HTML do email"},
                    "sender_name": {"type": "string", "description": "Nome do remetente"},
                    "sender_email": {"type": "string", "format": "email", "description": "Email do remetente"},
                    "reply_to": {"type": "string", "format": "email", "description": "Email para resposta"},
                    "track_opens": {"type": "boolean", "description": "Rastrear aberturas"},
                    "track_clicks": {"type": "boolean", "description": "Rastrear cliques"},
                    "is_active": {"type": "boolean", "description": "Se a campanha está ativa"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Campanha criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"}
    }
})
def create_email_campaign():
    """Cria nova campanha de email"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ["name", "subject", "content"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        campaign = EmailCampaign(
            name=data["name"],
            description=data.get("description"),
            subject=data["subject"],
            content=data["content"],
            sender_name=data.get("sender_name"),
            sender_email=data.get("sender_email"),
            reply_to=data.get("reply_to"),
            track_opens=data.get("track_opens", True),
            track_clicks=data.get("track_clicks", True),
            is_active=data.get("is_active", True),
            created_by=current_user_id
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Campanha criada com sucesso",
            "campaign": campaign.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar campanha: {e}")
        return jsonify({"error": f"Erro ao criar campanha: {str(e)}"}), 500

# ==================== SEQUÊNCIAS DE CADÊNCIA ====================

@automation_bp.route("/cadence-sequences", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Cadências"],
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
            "name": "is_active",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por sequências ativas"
        }
    ],
    "responses": {
        "200": {"description": "Lista de sequências de cadência"},
        "401": {"description": "Não autorizado"}
    }
})
def list_cadence_sequences():
    """Lista sequências de cadência"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    is_active = request.args.get("is_active", type=bool)
    
    query = CadenceSequence.query
    
    if is_active is not None:
        query = query.filter(CadenceSequence.is_active == is_active)
    
    query = query.order_by(CadenceSequence.created_at.desc())
    
    sequences = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "sequences": [sequence.to_dict() for sequence in sequences.items],
        "total": sequences.total,
        "pages": sequences.pages,
        "current_page": page,
        "per_page": per_page
    }), 200

@automation_bp.route("/cadence-sequences", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Cadências"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "CadenceSequenceCreate",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string", "description": "Nome da sequência"},
                    "description": {"type": "string", "description": "Descrição da sequência"},
                    "trigger_conditions": {"type": "object", "description": "Condições para acionar a cadência"},
                    "is_active": {"type": "boolean", "description": "Se a sequência está ativa"},
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name", "order", "action_type"],
                            "properties": {
                                "name": {"type": "string", "description": "Nome do passo"},
                                "description": {"type": "string", "description": "Descrição do passo"},
                                "order": {"type": "integer", "description": "Ordem do passo na sequência"},
                                "delay_days": {"type": "integer", "description": "Atraso em dias"},
                                "delay_hours": {"type": "integer", "description": "Atraso em horas"},
                                "delay_minutes": {"type": "integer", "description": "Atraso em minutos"},
                                "action_type": {"type": "string", "description": "Tipo de ação (e.g., SEND_EMAIL, CREATE_TASK)"},
                                "action_config": {"type": "object", "description": "Configuração da ação"},
                                "conditions": {"type": "object", "description": "Condições para o passo"},
                                "is_active": {"type": "boolean", "description": "Se o passo está ativo"}
                            }
                        }
                    }
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Sequência de cadência criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"}
    }
})
def create_cadence_sequence():
    """Cria nova sequência de cadência"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ["name"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        sequence = CadenceSequence(
            name=data["name"],
            description=data.get("description"),
            trigger_conditions=data.get("trigger_conditions", {}),
            is_active=data.get("is_active", True),
            created_by=current_user_id
        )
        
        db.session.add(sequence)
        db.session.flush()  # Para obter o ID
        
        # Criar passos
        steps_data = data.get("steps", [])
        for step_data in steps_data:
            try:
                action_type = ActionType(step_data["action_type"])
            except ValueError:
                return jsonify({"error": f"Tipo de ação inválido: {step_data['action_type']}"}), 400
            
            step = CadenceStep(
                sequence_id=sequence.id,
                name=step_data["name"],
                description=step_data.get("description"),
                order=step_data["order"],
                delay_days=step_data.get("delay_days", 0),
                delay_hours=step_data.get("delay_hours", 0),
                delay_minutes=step_data.get("delay_minutes", 0),
                action_type=action_type,
                action_config=step_data.get("action_config", {}),
                conditions=step_data.get("conditions", {}),
                is_active=step_data.get("is_active", True)
            )
            
            db.session.add(step)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Sequência de cadência criada com sucesso",
            "sequence": sequence.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar sequência: {e}")
        return jsonify({"error": f"Erro ao criar sequência: {str(e)}"}), 500

@automation_bp.route("/cadence-sequences/<sequence_id>/enroll", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Cadências"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "sequence_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da sequência"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "CadenceEnrollment",
                "required": ["lead_id"],
                "properties": {
                    "lead_id": {"type": "string", "description": "ID do lead a ser inscrito"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Lead inscrito na cadência com sucesso"},
        "400": {"description": "Dados inválidos ou lead já inscrito"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Sequência ou lead não encontrado"}
    }
})
def enroll_lead_in_cadence(sequence_id):
    """Inscreve lead em sequência de cadência"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ["lead_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    sequence = CadenceSequence.query.get_or_404(sequence_id)
    lead = Lead.query.get_or_404(data["lead_id"])
    
    # Verifica se o lead já está inscrito nesta cadência
    existing_enrollment = CadenceEnrollment.query.filter_by(
        lead_id=lead.id,
        sequence_id=sequence.id,
        is_active=True
    ).first()
    
    if existing_enrollment:
        return jsonify({"error": "Lead já inscrito nesta cadência"}), 400
    
    try:
        enrollment = CadenceEnrollment(
            lead_id=lead.id,
            sequence_id=sequence.id,
            enrolled_by=current_user_id,
            current_step_index=0,
            is_active=True
        )
        db.session.add(enrollment)
        db.session.commit()
        
        # Executa o primeiro passo imediatamente se não houver delay
        cadence_service.execute_next_cadence_step(enrollment.id)
        
        return jsonify({
            "success": True,
            "message": "Lead inscrito na cadência com sucesso",
            "enrollment": enrollment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao inscrever lead na cadência: {e}")
        return jsonify({"error": f"Erro ao inscrever lead na cadência: {str(e)}"}), 500

@automation_bp.route("/cadence-sequences/<sequence_id>/unenroll", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Cadências"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "sequence_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da sequência"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "CadenceUnenrollment",
                "required": ["lead_id"],
                "properties": {
                    "lead_id": {"type": "string", "description": "ID do lead a ser desinscrito"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Lead desinscrito da cadência com sucesso"},
        "400": {"description": "Dados inválidos ou lead não inscrito"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Sequência ou lead não encontrado"}
    }
})
def unenroll_lead_from_cadence(sequence_id):
    """Desinscreve lead de sequência de cadência"""
    data = request.get_json()
    required_fields = ["lead_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    sequence = CadenceSequence.query.get_or_404(sequence_id)
    lead = Lead.query.get_or_404(data["lead_id"])
    
    enrollment = CadenceEnrollment.query.filter_by(
        lead_id=lead.id,
        sequence_id=sequence.id,
        is_active=True
    ).first()
    
    if not enrollment:
        return jsonify({"error": "Lead não está inscrito nesta cadência"}), 400
    
    try:
        enrollment.is_active = False
        enrollment.unenrollment_date = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Lead desinscrito da cadência com sucesso",
            "enrollment": enrollment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao desinscrever lead da cadência: {e}")
        return jsonify({"error": f"Erro ao desinscrever lead da cadência: {str(e)}"}), 500

@automation_bp.route("/cadence-enrollments", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Cadências"],
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
            "name": "lead_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do lead"
        },
        {
            "name": "sequence_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID da sequência"
        },
        {
            "name": "is_active",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por inscrições ativas"
        }
    ],
    "responses": {
        "200": {"description": "Lista de inscrições em cadências"},
        "401": {"description": "Não autorizado"}
    }
})
def list_cadence_enrollments():
    """Lista inscrições em cadências"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    lead_id = request.args.get("lead_id")
    sequence_id = request.args.get("sequence_id")
    is_active = request.args.get("is_active", type=bool)
    
    query = CadenceEnrollment.query
    
    if lead_id:
        query = query.filter(CadenceEnrollment.lead_id == lead_id)
    if sequence_id:
        query = query.filter(CadenceEnrollment.sequence_id == sequence_id)
    if is_active is not None:
        query = query.filter(CadenceEnrollment.is_active == is_active)
    
    query = query.order_by(CadenceEnrollment.enrolled_at.desc())
    
    enrollments = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "enrollments": [enrollment.to_dict() for enrollment in enrollments.items],
        "total": enrollments.total,
        "pages": enrollments.pages,
        "current_page": page,
        "per_page": per_page
    }), 200

@automation_bp.route("/cadence-enrollments/<enrollment_id>/next-step", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Automação - Cadências"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "enrollment_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da inscrição"
        }
    ],
    "responses": {
        "200": {"description": "Próximo passo da cadência executado com sucesso"},
        "400": {"description": "Inscrição não ativa ou sem próximos passos"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Inscrição não encontrada"}
    }
})
def execute_next_cadence_step(enrollment_id):
    """Executa o próximo passo de uma cadência para uma inscrição."""
    enrollment = CadenceEnrollment.query.get_or_404(enrollment_id)
    
    if not enrollment.is_active:
        return jsonify({"error": "Inscrição não está ativa"}), 400
    
    try:
        success = cadence_service.execute_next_cadence_step(enrollment.id)
        if success:
            return jsonify({"message": "Próximo passo da cadência executado com sucesso"}), 200
        else:
            return jsonify({"message": "Nenhum próximo passo para executar ou cadência finalizada"}), 200
            
    except Exception as e:
        logger.error(f"Erro ao executar próximo passo da cadência: {e}")
        return jsonify({"error": f"Erro ao executar próximo passo da cadência: {str(e)}"}), 500


