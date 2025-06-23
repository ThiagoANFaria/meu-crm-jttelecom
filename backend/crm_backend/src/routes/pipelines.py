from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.lead import Lead
from src.models.pipeline import Pipeline, PipelineStage, Product, Opportunity
from datetime import datetime, date
import json
from flasgger import swag_from

pipelines_bp = Blueprint("pipelines", __name__)

# Pipeline Management
@pipelines_bp.route("/pipelines", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Funis"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "type",
            "in": "query",
            "type": "string",
            "enum": ["prospection", "sales"],
            "description": "Filtrar por tipo de funil"
        },
        {
            "name": "include_stats",
            "in": "query",
            "type": "boolean",
            "description": "Incluir estatísticas do funil",
            "default": False
        }
    ],
    "responses": {
        "200": {"description": "Lista de funis"},
        "403": {"description": "Acesso negado"}
    }
})
def get_pipelines():
    """Obter todos os funis com filtragem opcional."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        pipeline_type = request.args.get("type")  # "prospection" or "sales"
        include_stats = request.args.get("include_stats", "false").lower() == "true"
        
        query = Pipeline.query.filter_by(is_active=True)
        
        if pipeline_type:
            query = query.filter(Pipeline.pipeline_type == pipeline_type)
        
        pipelines = query.order_by(Pipeline.created_at.desc()).all()
        
        return jsonify({
            "pipelines": [pipeline.to_dict(include_stats=include_stats) for pipeline in pipelines],
            "total": len(pipelines)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/pipelines", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Funis"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "PipelineCreate",
                "required": ["name", "pipeline_type"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do funil"},
                    "description": {"type": "string", "description": "Descrição do funil"},
                    "pipeline_type": {"type": "string", "enum": ["prospection", "sales"], "description": "Tipo do funil"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Funil criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"}
    }
})
def create_pipeline():
    """Criar um novo funil."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        if not data.get("name"):
            return jsonify({"error": "Nome do funil é obrigatório"}), 400
        
        if not data.get("pipeline_type") or data["pipeline_type"] not in ["prospection", "sales"]:
            return jsonify({"error": "Tipo de funil deve ser \"prospection\" ou \"sales\""}), 400
        
        pipeline = Pipeline(
            name=data["name"],
            description=data.get("description"),
            pipeline_type=data["pipeline_type"],
            created_by=current_user_id
        )
        
        db.session.add(pipeline)
        db.session.flush()  # Get the pipeline ID
        
        # Create default stages based on pipeline type
        if data["pipeline_type"] == "prospection":
            default_stages = [
                ("Novo Lead", "Leads recém-chegados", 1, "#94A3B8", False, "active"),
                ("Qualificação", "Qualificando interesse e fit", 2, "#3B82F6", False, "active"),
                ("Contato Inicial", "Primeiro contato realizado", 3, "#8B5CF6", False, "active"),
                ("Interesse Confirmado", "Lead demonstrou interesse", 4, "#10B981", False, "active"),
                ("Qualificado", "Lead qualificado para vendas", 5, "#059669", True, "won"),
                ("Desqualificado", "Lead não tem fit", 6, "#EF4444", True, "lost")
            ]
        else:  # sales
            default_stages = [
                ("Oportunidade", "Nova oportunidade de venda", 1, "#94A3B8", False, "active"),
                ("Apresentação", "Apresentando solução", 2, "#3B82F6", False, "active"),
                ("Proposta", "Proposta enviada", 3, "#8B5CF6", False, "active"),
                ("Negociação", "Negociando termos", 4, "#F59E0B", False, "active"),
                ("Fechado - Ganho", "Venda realizada", 5, "#10B981", True, "won"),
                ("Fechado - Perdido", "Oportunidade perdida", 6, "#EF4444", True, "lost")
            ]
        
        for name, description, order, color, is_final, stage_type in default_stages:
            stage = PipelineStage(
                pipeline_id=pipeline.id,
                name=name,
                description=description,
                order=order,
                color=color,
                is_final=is_final,
                stage_type=stage_type
            )
            db.session.add(stage)
        
        db.session.commit()
        
        return jsonify({
            "message": "Funil criado com sucesso",
            "pipeline": pipeline.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/pipelines/<string:pipeline_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Funis"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "pipeline_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do funil"
        },
        {
            "name": "view",
            "in": "query",
            "type": "string",
            "enum": ["kanban", "list"],
            "description": "Tipo de visualização (kanban ou lista)",
            "default": "kanban"
        },
        {
            "name": "include_opportunities",
            "in": "query",
            "type": "boolean",
            "description": "Incluir oportunidades no retorno",
            "default": True
        },
        {
            "name": "assigned_to",
            "in": "query",
            "type": "string",
            "description": "Filtrar oportunidades por usuário atribuído"
        },
        {
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "Filtrar oportunidades por status"
        },
        {
            "name": "priority",
            "in": "query",
            "type": "string",
            "description": "Filtrar oportunidades por prioridade"
        },
        {
            "name": "min_value",
            "in": "query",
            "type": "number",
            "format": "float",
            "description": "Filtrar oportunidades por valor mínimo"
        },
        {
            "name": "max_value",
            "in": "query",
            "type": "number",
            "format": "float",
            "description": "Filtrar oportunidades por valor máximo"
        },
        {
            "name": "product_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar oportunidades por ID do produto"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes do funil com estágios e oportunidades"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Funil não encontrado"}
    }
})
def get_pipeline(pipeline_id):
    """Obter um funil específico com estágios e oportunidades."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        pipeline = Pipeline.query.get(pipeline_id)
        if not pipeline:
            return jsonify({"error": "Funil não encontrado"}), 404
        
        view_type = request.args.get("view", "kanban")  # "kanban" or "list"
        include_opportunities = request.args.get("include_opportunities", "true").lower() == "true"
        
        # Filters
        assigned_to = request.args.get("assigned_to")
        status = request.args.get("status")
        priority = request.args.get("priority")
        min_value = request.args.get("min_value", type=float)
        max_value = request.args.get("max_value", type=float)
        product_id = request.args.get("product_id")
        
        pipeline_data = pipeline.to_dict(include_stages=True, include_stats=True)
        
        if include_opportunities:
            # Get opportunities with filters
            opportunities_query = Opportunity.query.filter_by(pipeline_id=pipeline_id)
            
            if assigned_to:
                opportunities_query = opportunities_query.filter(Opportunity.assigned_to == assigned_to)
            
            if status:
                opportunities_query = opportunities_query.filter(Opportunity.status == status)
            
            if priority:
                opportunities_query = opportunities_query.filter(Opportunity.priority == priority)
            
            if min_value is not None:
                opportunities_query = opportunities_query.filter(Opportunity.value >= min_value)
            
            if max_value is not None:
                opportunities_query = opportunities_query.filter(Opportunity.value <= max_value)
            
            if product_id:
                opportunities_query = opportunities_query.join(Opportunity.products).filter(Product.id == product_id)
            
            opportunities = opportunities_query.order_by(Opportunity.created_at.desc()).all()
            
            if view_type == "kanban":
                # Group opportunities by stage for Kanban view
                for stage in pipeline_data["stages"]:
                    stage_opportunities = [opp for opp in opportunities if opp.stage_id == stage["id"]]
                    stage["opportunities"] = [opp.to_dict() for opp in stage_opportunities]
                    stage["opportunity_count"] = len(stage_opportunities)
                    stage["total_value"] = sum(opp.value or 0 for opp in stage_opportunities if opp.value)
            else:
                # List view - return all opportunities
                pipeline_data["opportunities"] = [opp.to_dict() for opp in opportunities]
        
        return jsonify({"pipeline": pipeline_data}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

# Opportunity Management
@pipelines_bp.route("/opportunities", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Oportunidades"],
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
            "name": "pipeline_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do funil"
        },
        {
            "name": "stage_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do estágio"
        },
        {
            "name": "assigned_to",
            "in": "query",
            "type": "string",
            "description": "Filtrar por usuário atribuído"
        },
        {
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "Filtrar por status da oportunidade"
        },
        {
            "name": "priority",
            "in": "query",
            "type": "string",
            "description": "Filtrar por prioridade da oportunidade"
        },
        {
            "name": "min_value",
            "in": "query",
            "type": "number",
            "format": "float",
            "description": "Filtrar por valor mínimo da oportunidade"
        },
        {
            "name": "max_value",
            "in": "query",
            "type": "number",
            "format": "float",
            "description": "Filtrar por valor máximo da oportunidade"
        },
        {
            "name": "product_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do produto"
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Pesquisar por título, descrição, nome do lead ou nome da empresa"
        }
    ],
    "responses": {
        "200": {"description": "Lista de oportunidades com filtragem e paginação"},
        "403": {"description": "Acesso negado"}
    }
})
def get_opportunities():
    """Obter oportunidades com filtragem e paginação."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Pagination
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        
        # Filters
        pipeline_id = request.args.get("pipeline_id")
        stage_id = request.args.get("stage_id")
        assigned_to = request.args.get("assigned_to")
        status = request.args.get("status")
        priority = request.args.get("priority")
        min_value = request.args.get("min_value", type=float)
        max_value = request.args.get("max_value", type=float)
        product_id = request.args.get("product_id")
        search = request.args.get("search")
        
        query = Opportunity.query
        
        # Apply filters
        if pipeline_id:
            query = query.filter(Opportunity.pipeline_id == pipeline_id)
        
        if stage_id:
            query = query.filter(Opportunity.stage_id == stage_id)
        
        if assigned_to:
            query = query.filter(Opportunity.assigned_to == assigned_to)
        
        if status:
            query = query.filter(Opportunity.status == status)
        
        if priority:
            query = query.filter(Opportunity.priority == priority)
        
        if min_value is not None:
            query = query.filter(Opportunity.value >= min_value)
        
        if max_value is not None:
            query = query.filter(Opportunity.value <= max_value)
        
        if product_id:
            query = query.join(Opportunity.products).filter(Product.id == product_id)
        
        if search:
            search_filter = f"%{search}%";
            query = query.join(Opportunity.lead).filter(
                db.or_(
                    Opportunity.title.ilike(search_filter),
                    Opportunity.description.ilike(search_filter),
                    Lead.name.ilike(search_filter),
                    Lead.company_name.ilike(search_filter)
                )
            )
        
        # If user is not admin, only show opportunities assigned to them or unassigned
        if not current_user.has_permission("users:manage"):
            query = query.filter(
                db.or_(
                    Opportunity.assigned_to == current_user_id,
                    Opportunity.assigned_to.is_(None)
                )
            )
        
        # Order by value (highest first) and creation date
        query = query.order_by(Opportunity.value.desc().nullslast(), Opportunity.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        opportunities = pagination.items
        
        return jsonify({
            "opportunities": [opp.to_dict() for opp in opportunities],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/opportunities", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Oportunidades"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "OpportunityCreate",
                "required": ["title", "lead_id", "pipeline_id", "stage_id"],
                "properties": {
                    "title": {"type": "string", "description": "Título da oportunidade"},
                    "description": {"type": "string", "description": "Descrição da oportunidade"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "pipeline_id": {"type": "string", "description": "ID do funil associado"},
                    "stage_id": {"type": "string", "description": "ID do estágio atual"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "value": {"type": "number", "format": "float", "description": "Valor da oportunidade"},
                    "probability": {"type": "integer", "description": "Probabilidade de fechamento (0-100)"},
                    "expected_close_date": {"type": "string", "format": "date", "description": "Data esperada de fechamento (YYYY-MM-DD)"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "Prioridade da oportunidade"},
                    "source": {"type": "string", "description": "Fonte da oportunidade"},
                    "product_ids": {"type": "array", "items": {"type": "string"}, "description": "Lista de IDs de produtos associados"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Oportunidade criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Lead, funil ou estágio não encontrado"}
    }
})
def create_opportunity():
    """Criar uma nova oportunidade."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:create"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["title", "lead_id", "pipeline_id", "stage_id"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400
        
        # Validate relationships
        lead = Lead.query.get(data["lead_id"])
        if not lead:
            return jsonify({"error": "Lead não encontrado"}), 404
        
        pipeline = Pipeline.query.get(data["pipeline_id"])
        if not pipeline:
            return jsonify({"error": "Funil não encontrado"}), 404
        
        stage = PipelineStage.query.get(data["stage_id"])
        if not stage or stage.pipeline_id != data["pipeline_id"]:
            return jsonify({"error": "Etapa inválida para este funil"}), 400
        
        # Validate assigned user if provided
        assigned_to = data.get("assigned_to")
        if assigned_to:
            assigned_user = User.query.get(assigned_to)
            if not assigned_user:
                return jsonify({"error": "Usuário atribuído não encontrado"}), 400
        
        opportunity = Opportunity(
            title=data["title"],
            description=data.get("description"),
            lead_id=data["lead_id"],
            pipeline_id=data["pipeline_id"],
            stage_id=data["stage_id"],
            assigned_to=assigned_to,
            value=data.get("value"),
            probability=data.get("probability", 0),
            expected_close_date=datetime.strptime(data["expected_close_date"], "%Y-%m-%d").date() if data.get("expected_close_date") else None,
            priority=data.get("priority", "medium"),
            source=data.get("source")
        )
        
        db.session.add(opportunity)
        db.session.flush()
        
        # Add products if provided
        product_ids = data.get("product_ids", [])
        if product_ids:
            products = Product.query.filter(Product.id.in_(product_ids)).all()
            opportunity.products.extend(products)
        
        db.session.commit()
        
        return jsonify({
            "message": "Oportunidade criada com sucesso",
            "opportunity": opportunity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/opportunities/<string:opportunity_id>/move", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Oportunidades"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "opportunity_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da oportunidade"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "OpportunityMove",
                "required": ["stage_id"],
                "properties": {
                    "stage_id": {"type": "string", "description": "ID da nova etapa"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Oportunidade movida com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Oportunidade ou etapa não encontrada"}
    }
})
def move_opportunity(opportunity_id):
    """Mover oportunidade para uma etapa diferente."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:update"):
            return jsonify({"error": "Acesso negado"}), 403
        
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return jsonify({"error": "Oportunidade não encontrada"}), 404
        
        data = request.get_json()
        new_stage_id = data.get("stage_id")
        
        if not new_stage_id:
            return jsonify({"error": "ID da nova etapa é obrigatório"}), 400
        
        new_stage = PipelineStage.query.get(new_stage_id)
        if not new_stage:
            return jsonify({"error": "Etapa não encontrada"}), 404
        
        if new_stage.pipeline_id != opportunity.pipeline_id:
            return jsonify({"error": "Etapa não pertence ao mesmo funil"}), 400
        
        # Check if user can update this opportunity
        if not current_user.has_permission("users:manage"):
            if opportunity.assigned_to and opportunity.assigned_to != current_user_id:
                return jsonify({"error": "Acesso negado"}), 403
        
        old_stage_id = opportunity.stage_id
        opportunity.stage_id = new_stage_id
        
        # Update status based on stage type
        if new_stage.stage_type == "won":
            opportunity.status = "won"
            opportunity.actual_close_date = date.today()
        elif new_stage.stage_type == "lost":
            opportunity.status = "lost"
            opportunity.actual_close_date = date.today()
        else:
            opportunity.status = "active"
            opportunity.actual_close_date = None
        
        db.session.commit()
        
        return jsonify({
            "message": "Oportunidade movida com sucesso",
            "opportunity": opportunity.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/opportunities/<string:opportunity_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Oportunidades"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "opportunity_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da oportunidade"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "OpportunityUpdate",
                "properties": {
                    "title": {"type": "string", "description": "Título da oportunidade"},
                    "description": {"type": "string", "description": "Descrição da oportunidade"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "pipeline_id": {"type": "string", "description": "ID do funil associado"},
                    "stage_id": {"type": "string", "description": "ID do estágio atual"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "value": {"type": "number", "format": "float", "description": "Valor da oportunidade"},
                    "probability": {"type": "integer", "description": "Probabilidade de fechamento (0-100)"},
                    "expected_close_date": {"type": "string", "format": "date", "description": "Data esperada de fechamento (YYYY-MM-DD)"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "Prioridade da oportunidade"},
                    "source": {"type": "string", "description": "Fonte da oportunidade"},
                    "product_ids": {"type": "array", "items": {"type": "string"}, "description": "Lista de IDs de produtos associados"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Oportunidade atualizada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Oportunidade não encontrada"}
    }
})
def update_opportunity(opportunity_id):
    """Atualizar uma oportunidade."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:update"):
            return jsonify({"error": "Acesso negado"}), 403
        
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return jsonify({"error": "Oportunidade não encontrada"}), 404
        
        # Check if user can update this opportunity
        if not current_user.has_permission("users:manage"):
            if opportunity.assigned_to and opportunity.assigned_to != current_user_id:
                return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        updatable_fields = [
            "title", "description", "lead_id", "pipeline_id", "stage_id",
            "assigned_to", "value", "probability", "expected_close_date",
            "priority", "source"
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == "expected_close_date" and data[field]:
                    setattr(opportunity, field, datetime.strptime(data[field], "%Y-%m-%d").date())
                else:
                    setattr(opportunity, field, data[field])
        
        # Update products if provided
        if "product_ids" in data:
            opportunity.products.clear()
            if data["product_ids"]:
                products = Product.query.filter(Product.id.in_(data["product_ids"])).all()
                opportunity.products.extend(products)
        
        db.session.commit()
        
        return jsonify({
            "message": "Oportunidade atualizada com sucesso",
            "opportunity": opportunity.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/opportunities/<string:opportunity_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Oportunidades"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "opportunity_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da oportunidade"
        }
    ],
    "responses": {
        "200": {"description": "Oportunidade deletada com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Oportunidade não encontrada"}
    }
})
def delete_opportunity(opportunity_id):
    """Deletar uma oportunidade."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:delete"):
            return jsonify({"error": "Acesso negado"}), 403
        
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return jsonify({"error": "Oportunidade não encontrada"}), 404
        
        db.session.delete(opportunity)
        db.session.commit()
        
        return jsonify({"message": "Oportunidade deletada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

# Pipeline Stage Management
@pipelines_bp.route("/pipelines/<string:pipeline_id>/stages", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Estágios de Funil"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "pipeline_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do funil"
        }
    ],
    "responses": {
        "200": {"description": "Lista de estágios do funil"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Funil não encontrado"}
    }
})
def get_pipeline_stages(pipeline_id):
    """Obter todos os estágios de um funil."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        pipeline = Pipeline.query.get(pipeline_id)
        if not pipeline:
            return jsonify({"error": "Funil não encontrado"}), 404
        
        stages = PipelineStage.query.filter_by(pipeline_id=pipeline_id).order_by(PipelineStage.order).all()
        
        return jsonify({
            "stages": [stage.to_dict() for stage in stages],
            "total": len(stages)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/pipelines/<string:pipeline_id>/stages", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Estágios de Funil"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "pipeline_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do funil"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "PipelineStageCreate",
                "required": ["name", "order"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do estágio"},
                    "description": {"type": "string", "description": "Descrição do estágio"},
                    "order": {"type": "integer", "description": "Ordem do estágio no funil"},
                    "color": {"type": "string", "description": "Cor do estágio (hex code)"},
                    "is_final": {"type": "boolean", "description": "Se é um estágio final (ganho/perdido)"},
                    "stage_type": {"type": "string", "enum": ["active", "won", "lost"], "description": "Tipo do estágio"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Estágio criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Funil não encontrado"}
    }
})
def create_pipeline_stage(pipeline_id):
    """Criar um novo estágio para um funil."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        pipeline = Pipeline.query.get(pipeline_id)
        if not pipeline:
            return jsonify({"error": "Funil não encontrado"}), 404
        
        data = request.get_json()
        
        required_fields = ["name", "order"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400
        
        stage = PipelineStage(
            pipeline_id=pipeline_id,
            name=data["name"],
            description=data.get("description"),
            order=data["order"],
            color=data.get("color"),
            is_final=data.get("is_final", False),
            stage_type=data.get("stage_type", "active")
        )
        
        db.session.add(stage)
        db.session.commit()
        
        return jsonify({
            "message": "Estágio criado com sucesso",
            "stage": stage.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/pipelines/<string:pipeline_id>/stages/<string:stage_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Estágios de Funil"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "pipeline_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do funil"
        },
        {
            "name": "stage_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do estágio"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "PipelineStageUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do estágio"},
                    "description": {"type": "string", "description": "Descrição do estágio"},
                    "order": {"type": "integer", "description": "Ordem do estágio no funil"},
                    "color": {"type": "string", "description": "Cor do estágio (hex code)"},
                    "is_final": {"type": "boolean", "description": "Se é um estágio final (ganho/perdido)"},
                    "stage_type": {"type": "string", "enum": ["active", "won", "lost"], "description": "Tipo do estágio"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Estágio atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Funil ou estágio não encontrado"}
    }
})
def update_pipeline_stage(pipeline_id, stage_id):
    """Atualizar um estágio de funil."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        pipeline = Pipeline.query.get(pipeline_id)
        if not pipeline:
            return jsonify({"error": "Funil não encontrado"}), 404
        
        stage = PipelineStage.query.get(stage_id)
        if not stage or stage.pipeline_id != pipeline_id:
            return jsonify({"error": "Estágio não encontrado ou não pertence a este funil"}), 404
        
        data = request.get_json()
        
        updatable_fields = ["name", "description", "order", "color", "is_final", "stage_type"]
        for field in updatable_fields:
            if field in data:
                setattr(stage, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            "message": "Estágio atualizado com sucesso",
            "stage": stage.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/pipelines/<string:pipeline_id>/stages/<string:stage_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Estágios de Funil"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "pipeline_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do funil"
        },
        {
            "name": "stage_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do estágio"
        }
    ],
    "responses": {
        "200": {"description": "Estágio deletado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Funil ou estágio não encontrado"}
    }
})
def delete_pipeline_stage(pipeline_id, stage_id):
    """Deletar um estágio de funil."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        pipeline = Pipeline.query.get(pipeline_id)
        if not pipeline:
            return jsonify({"error": "Funil não encontrado"}), 404
        
        stage = PipelineStage.query.get(stage_id)
        if not stage or stage.pipeline_id != pipeline_id:
            return jsonify({"error": "Estágio não encontrado ou não pertence a este funil"}), 404
        
        db.session.delete(stage)
        db.session.commit()
        
        return jsonify({"message": "Estágio deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

# Product Management
@pipelines_bp.route("/products", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Produtos"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de todos os produtos"},
        "403": {"description": "Acesso negado"}
    }
})
def get_products():
    """Obter todos os produtos."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        products = Product.query.order_by(Product.name).all()
        
        return jsonify({
            "products": [product.to_dict() for product in products],
            "total": len(products)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/products", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Produtos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ProductCreate",
                "required": ["name", "price"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do produto"},
                    "description": {"type": "string", "description": "Descrição do produto"},
                    "price": {"type": "number", "format": "float", "description": "Preço do produto"},
                    "is_active": {"type": "boolean", "description": "Se o produto está ativo", "default": True}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Produto criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "409": {"description": "Produto já existe com este nome"}
    }
})
def create_product():
    """Criar um novo produto."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        required_fields = ["name", "price"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400
        
        if Product.query.filter_by(name=data["name"]).first():
            return jsonify({"error": "Já existe um produto com este nome"}), 409
        
        product = Product(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            is_active=data.get("is_active", True)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            "message": "Produto criado com sucesso",
            "product": product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/products/<string:product_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Produtos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do produto"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ProductUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do produto"},
                    "description": {"type": "string", "description": "Descrição do produto"},
                    "price": {"type": "number", "format": "float", "description": "Preço do produto"},
                    "is_active": {"type": "boolean", "description": "Se o produto está ativo"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Produto atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Produto não encontrado"},
        "409": {"description": "Produto já existe com este nome"}
    }
})
def update_product(product_id):
    """Atualizar um produto."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Produto não encontrado"}), 404
        
        data = request.get_json()
        
        if "name" in data and data["name"] != product.name:
            if Product.query.filter_by(name=data["name"]).first():
                return jsonify({"error": "Já existe um produto com este nome"}), 409
        
        updatable_fields = ["name", "description", "price", "is_active"]
        for field in updatable_fields:
            if field in data:
                setattr(product, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            "message": "Produto atualizado com sucesso",
            "product": product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@pipelines_bp.route("/products/<string:product_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Produtos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do produto"
        }
    ],
    "responses": {
        "200": {"description": "Produto deletado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Produto não encontrado"}
    }
})
def delete_product(product_id):
    """Deletar um produto."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Produto não encontrado"}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({"message": "Produto deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500


