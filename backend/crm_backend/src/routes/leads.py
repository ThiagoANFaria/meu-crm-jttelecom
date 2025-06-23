from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.lead import Lead, Tag, LeadFieldTemplate
import re
from flasgger import swag_from

leads_bp = Blueprint("leads", __name__)

def validate_cnpj_cpf(document):
    """Validate CNPJ/CPF format (basic validation)."""
    if not document:
        return True  # Document is optional
    
    # Remove non-numeric characters
    document = re.sub(r"\D", "", document)
    
    # Check if it has 11 digits (CPF) or 14 digits (CNPJ)
    if len(document) not in [11, 14]:
        return False
    
    return True

def validate_email(email):
    """Validate email format."""
    if not email:
        return True  # Email is optional
    
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone format (basic validation)."""
    if not phone:
        return True  # Phone is optional
    
    # Remove non-numeric characters
    phone_digits = re.sub(r"\D", "", phone)
    
    # Check if it has at least 10 digits (Brazilian phone)
    return len(phone_digits) >= 10

def validate_cep(cep):
    """Validate CEP format."""
    if not cep:
        return True  # CEP is optional
    
    # Remove non-numeric characters
    cep_digits = re.sub(r"\D", "", cep)
    
    # Check if it has 8 digits
    return len(cep_digits) == 8

@leads_bp.route("/leads", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Leads"],
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
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "Filtrar por status do lead"
        },
        {
            "name": "origin",
            "in": "query",
            "type": "string",
            "description": "Filtrar por origem do lead"
        },
        {
            "name": "assigned_to",
            "in": "query",
            "type": "string",
            "description": "Filtrar por usuário atribuído"
        },
        {
            "name": "min_score",
            "in": "query",
            "type": "integer",
            "description": "Filtrar por score mínimo"
        },
        {
            "name": "max_score",
            "in": "query",
            "type": "integer",
            "description": "Filtrar por score máximo"
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Pesquisar por nome, empresa, email, telefone ou CNPJ/CPF"
        },
        {
            "name": "city",
            "in": "query",
            "type": "string",
            "description": "Filtrar por cidade"
        },
        {
            "name": "state",
            "in": "query",
            "type": "string",
            "description": "Filtrar por estado"
        }
    ],
    "responses": {
        "200": {"description": "Lista de leads com paginação"},
        "403": {"description": "Acesso negado"}
    }
})
def get_leads():
    """Obter todos os leads com filtragem e paginação."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        status = request.args.get("status")
        origin = request.args.get("origin")
        assigned_to = request.args.get("assigned_to")
        min_score = request.args.get("min_score", type=int)
        max_score = request.args.get("max_score", type=int)
        search = request.args.get("search")
        city = request.args.get("city")
        state = request.args.get("state")
        
        # Build query
        query = Lead.query
        
        # Apply filters
        if status:
            query = query.filter(Lead.status == status)
        
        if origin:
            query = query.filter(Lead.origin == origin)
        
        if assigned_to:
            query = query.filter(Lead.assigned_to == assigned_to)
        
        if min_score is not None:
            query = query.filter(Lead.score >= min_score)
        
        if max_score is not None:
            query = query.filter(Lead.score <= max_score)
        
        if city:
            query = query.filter(Lead.address_city.ilike(f"%{city}%"))
        
        if state:
            query = query.filter(Lead.address_state.ilike(f"%{state}%"))
        
        if search:
            search_filter = f"%{search}%";
            query = query.filter(
                db.or_(
                    Lead.name.ilike(search_filter),
                    Lead.company_name.ilike(search_filter),
                    Lead.email.ilike(search_filter),
                    Lead.phone.ilike(search_filter),
                    Lead.whatsapp.ilike(search_filter),
                    Lead.cnpj_cpf.ilike(search_filter)
                )
            )
        
        # If user is not admin, only show leads assigned to them or unassigned
        if not current_user.has_permission("users:manage"):
            query = query.filter(
                db.or_(
                    Lead.assigned_to == current_user_id,
                    Lead.assigned_to.is_(None)
                )
            )
        
        # Order by score (highest first) and creation date
        query = query.order_by(Lead.score.desc(), Lead.created_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        leads = pagination.items
        
        return jsonify({
            "leads": [lead.to_dict() for lead in leads],
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

@leads_bp.route("/leads", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Leads"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "LeadCreate",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do lead"},
                    "contact": {"type": "string", "description": "Nome do contato"},
                    "email": {"type": "string", "format": "email", "description": "Email do lead"},
                    "whatsapp": {"type": "string", "description": "Número do WhatsApp"},
                    "company_name": {"type": "string", "description": "Nome da empresa"},
                    "cnpj_cpf": {"type": "string", "description": "CNPJ ou CPF"},
                    "ie_rg": {"type": "string", "description": "Inscrição Estadual ou RG"},
                    "phone": {"type": "string", "description": "Telefone"},
                    "position": {"type": "string", "description": "Cargo"},
                    "origin": {"type": "string", "description": "Origem do lead"},
                    "product_interest": {"type": "string", "description": "Produto de interesse"},
                    "status": {"type": "string", "description": "Status do lead (e.g., Novo, Qualificado, Contato)", "default": "Novo"},
                    "observations": {"type": "string", "description": "Observações"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "address": {
                        "type": "object",
                        "properties": {
                            "street": {"type": "string"},
                            "number": {"type": "string"},
                            "complement": {"type": "string"},
                            "neighborhood": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "zipcode": {"type": "string"}
                        }
                    },
                    "additional_fields": {"type": "object", "description": "Campos adicionais customizáveis"},
                    "tag_ids": {"type": "array", "items": {"type": "string"}, "description": "Lista de IDs de tags"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Lead criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "409": {"description": "Lead já existe com este CNPJ/CPF"}
    }
})
def create_lead():
    """Criar um novo lead."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:create"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get("name"):
            return jsonify({"error": "Nome é obrigatório"}), 400
        
        # Validate optional fields
        if data.get("email") and not validate_email(data["email"]):
            return jsonify({"error": "Formato de email inválido"}), 400
        
        if data.get("phone") and not validate_phone(data["phone"]):
            return jsonify({"error": "Formato de telefone inválido"}), 400
        
        if data.get("whatsapp") and not validate_phone(data["whatsapp"]):
            return jsonify({"error": "Formato de WhatsApp inválido"}), 400
        
        if data.get("cnpj_cpf") and not validate_cnpj_cpf(data["cnpj_cpf"]):
            return jsonify({"error": "Formato de CNPJ/CPF inválido"}), 400
        
        if data.get("address", {}).get("zipcode") and not validate_cep(data["address"]["zipcode"]):
            return jsonify({"error": "Formato de CEP inválido"}), 400
        
        # Check if CNPJ/CPF already exists (if provided)
        if data.get("cnpj_cpf"):
            existing_lead = Lead.query.filter_by(cnpj_cpf=data["cnpj_cpf"]).first()
            if existing_lead:
                return jsonify({"error": "Já existe um lead com este CNPJ/CPF"}), 409
        
        # Validate assigned_to user exists (if provided)
        assigned_to = data.get("assigned_to")
        if assigned_to:
            assigned_user = User.query.get(assigned_to)
            if not assigned_user:
                return jsonify({"error": "Usuário atribuído não encontrado"}), 400
        
        # Create new lead
        lead = Lead(
            name=data["name"],
            contact=data.get("contact"),
            email=data.get("email"),
            whatsapp=data.get("whatsapp"),
            company_name=data.get("company_name"),
            cnpj_cpf=data.get("cnpj_cpf"),
            ie_rg=data.get("ie_rg"),
            phone=data.get("phone"),
            position=data.get("position"),
            origin=data.get("origin"),
            product_interest=data.get("product_interest"),
            status=data.get("status", "Novo"),
            observations=data.get("observations"),
            assigned_to=assigned_to
        )
        
        # Set address fields
        address_data = data.get("address", {})
        lead.address_street = address_data.get("street")
        lead.address_number = address_data.get("number")
        lead.address_complement = address_data.get("complement")
        lead.address_neighborhood = address_data.get("neighborhood")
        lead.address_city = address_data.get("city")
        lead.address_state = address_data.get("state")
        lead.address_zipcode = address_data.get("zipcode")
        
        # Set additional fields
        additional_fields = data.get("additional_fields", {})
        if additional_fields:
            lead.additional_fields = additional_fields
        
        # Calculate initial score
        lead.calculate_score()
        
        db.session.add(lead)
        
        # Add tags if provided
        tag_ids = data.get("tag_ids", [])
        if tag_ids:
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            lead.tags.extend(tags)
        
        db.session.commit()
        
        return jsonify({
            "message": "Lead criado com sucesso",
            "lead": lead.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/leads/<string:lead_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Leads"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "lead_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do lead"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes do lead"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Lead não encontrado"}
    }
})
def get_lead(lead_id):
    """Obter um lead específico."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead não encontrado"}), 404
        
        # Check if user can access this lead
        if not current_user.has_permission("users:manage"):
            if lead.assigned_to and lead.assigned_to != current_user_id:
                return jsonify({"error": "Acesso negado"}), 403
        
        return jsonify({"lead": lead.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/leads/<string:lead_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Leads"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "lead_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do lead"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "LeadUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do lead"},
                    "contact": {"type": "string", "description": "Nome do contato"},
                    "email": {"type": "string", "format": "email", "description": "Email do lead"},
                    "whatsapp": {"type": "string", "description": "Número do WhatsApp"},
                    "company_name": {"type": "string", "description": "Nome da empresa"},
                    "cnpj_cpf": {"type": "string", "description": "CNPJ ou CPF"},
                    "ie_rg": {"type": "string", "description": "Inscrição Estadual ou RG"},
                    "phone": {"type": "string", "description": "Telefone"},
                    "position": {"type": "string", "description": "Cargo"},
                    "origin": {"type": "string", "description": "Origem do lead"},
                    "product_interest": {"type": "string", "description": "Produto de interesse"},
                    "status": {"type": "string", "description": "Status do lead (e.g., Novo, Qualificado, Contato)"},
                    "observations": {"type": "string", "description": "Observações"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "address": {
                        "type": "object",
                        "properties": {
                            "street": {"type": "string"},
                            "number": {"type": "string"},
                            "complement": {"type": "string"},
                            "neighborhood": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "zipcode": {"type": "string"}
                        }
                    },
                    "additional_fields": {"type": "object", "description": "Campos adicionais customizáveis"},
                    "tag_ids": {"type": "array", "items": {"type": "string"}, "description": "Lista de IDs de tags"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Lead atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Lead não encontrado"},
        "409": {"description": "Lead já existe com este CNPJ/CPF"}
    }
})
def update_lead():
    """Atualizar um lead."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:update"):
            return jsonify({"error": "Acesso negado"}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead não encontrado"}), 404
        
        # Check if user can update this lead
        if not current_user.has_permission("users:manage"):
            if lead.assigned_to and lead.assigned_to != current_user_id:
                return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Validate fields if provided
        if "email" in data and data["email"] and not validate_email(data["email"]):
            return jsonify({"error": "Formato de email inválido"}), 400
        
        if "phone" in data and data["phone"] and not validate_phone(data["phone"]):
            return jsonify({"error": "Formato de telefone inválido"}), 400
        
        if "whatsapp" in data and data["whatsapp"] and not validate_phone(data["whatsapp"]):
            return jsonify({"error": "Formato de WhatsApp inválido"}), 400
        
        if "cnpj_cpf" in data and data["cnpj_cpf"] and not validate_cnpj_cpf(data["cnpj_cpf"]):
            return jsonify({"error": "Formato de CNPJ/CPF inválido"}), 400
        
        # Check if CNPJ/CPF already exists (if changing)
        if "cnpj_cpf" in data and data["cnpj_cpf"] and data["cnpj_cpf"] != lead.cnpj_cpf:
            existing_lead = Lead.query.filter_by(cnpj_cpf=data["cnpj_cpf"]).first()
            if existing_lead:
                return jsonify({"error": "Já existe um lead com este CNPJ/CPF"}), 409
        
        # Validate assigned_to user exists (if provided)
        if "assigned_to" in data and data["assigned_to"]:
            assigned_user = User.query.get(data["assigned_to"])
            if not assigned_user:
                return jsonify({"error": "Usuário atribuído não encontrado"}), 400
        
        # Update basic fields
        updatable_fields = [
            "name", "contact", "email", "whatsapp", "company_name", "cnpj_cpf", 
            "ie_rg", "phone", "position", "origin", "product_interest", 
            "status", "observations"
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(lead, field, data[field])
        
        # Update address fields
        if "address" in data:
            address_data = data["address"]
            address_fields = {
                "street": "address_street",
                "number": "address_number",
                "complement": "address_complement",
                "neighborhood": "address_neighborhood",
                "city": "address_city",
                "state": "address_state",
                "zipcode": "address_zipcode"
            }
            
            for field_key, model_field in address_fields.items():
                if field_key in address_data:
                    setattr(lead, model_field, address_data[field_key])
        
        # Update additional fields
        if "additional_fields" in data:
            lead.additional_fields = data["additional_fields"]
        
        # Only admins or users with assign permission can change assignment
        if "assigned_to" in data:
            if current_user.has_permission("leads:assign") or current_user.has_permission("users:manage"):
                lead.assigned_to = data["assigned_to"]
            else:
                return jsonify({"error": "Sem permissão para atribuir leads"}), 403
        
        # Update tags if provided
        if "tag_ids" in data:
            lead.tags.clear()
            if data["tag_ids"]:
                tags = Tag.query.filter(Tag.id.in_(data["tag_ids"])).all()
                lead.tags.extend(tags)
        
        # Recalculate score
        lead.calculate_score()
        
        db.session.commit()
        
        return jsonify({
            "message": "Lead atualizado com sucesso",
            "lead": lead.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/leads/<string:lead_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Leads"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "lead_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do lead"
        }
    ],
    "responses": {
        "200": {"description": "Lead deletado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Lead não encontrado"}
    }
})
def delete_lead(lead_id):
    """Deletar um lead."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:delete"):
            return jsonify({"error": "Acesso negado"}), 403
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({"error": "Lead não encontrado"}), 404
        
        db.session.delete(lead)
        db.session.commit()
        
        return jsonify({"message": "Lead deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

# Field Templates Management
@leads_bp.route("/lead-field-templates", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Templates de Campo"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de todos os templates de campo"},
        "403": {"description": "Acesso negado"}
    }
})
def get_field_templates():
    """Obter todos os templates de campo."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        templates = LeadFieldTemplate.query.filter_by(is_active=True).order_by(LeadFieldTemplate.name).all()
        
        return jsonify({
            "templates": [template.to_dict() for template in templates],
            "total": len(templates)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/lead-field-templates", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Templates de Campo"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "LeadFieldTemplateCreate",
                "required": ["name", "field_type", "is_required"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do campo"},
                    "field_type": {"type": "string", "enum": ["text", "number", "date", "select", "multiselect", "boolean"], "description": "Tipo do campo"},
                    "is_required": {"type": "boolean", "description": "Se o campo é obrigatório"},
                    "options": {"type": "array", "items": {"type": "string"}, "description": "Opções para campos select/multiselect"},
                    "default_value": {"type": "string", "description": "Valor padrão"},
                    "description": {"type": "string", "description": "Descrição do campo"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Template de campo criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "409": {"description": "Template de campo já existe com este nome"}
    }
})
def create_field_template():
    """Criar um novo template de campo."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:manage_templates"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        required_fields = ["name", "field_type", "is_required"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400
        
        if LeadFieldTemplate.query.filter_by(name=data["name"]).first():
            return jsonify({"error": "Já existe um template de campo com este nome"}), 409
        
        template = LeadFieldTemplate(
            name=data["name"],
            field_type=data["field_type"],
            is_required=data["is_required"],
            options=data.get("options"),
            default_value=data.get("default_value"),
            description=data.get("description")
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            "message": "Template de campo criado com sucesso",
            "template": template.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/lead-field-templates/<string:template_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Templates de Campo"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "template_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do template de campo"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "LeadFieldTemplateUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do campo"},
                    "field_type": {"type": "string", "enum": ["text", "number", "date", "select", "multiselect", "boolean"], "description": "Tipo do campo"},
                    "is_required": {"type": "boolean", "description": "Se o campo é obrigatório"},
                    "options": {"type": "array", "items": {"type": "string"}, "description": "Opções para campos select/multiselect"},
                    "default_value": {"type": "string", "description": "Valor padrão"},
                    "description": {"type": "string", "description": "Descrição do campo"},
                    "is_active": {"type": "boolean", "description": "Se o template está ativo"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Template de campo atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Template de campo não encontrado"},
        "409": {"description": "Template de campo já existe com este nome"}
    }
})
def update_field_template(template_id):
    """Atualizar um template de campo."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:manage_templates"):
            return jsonify({"error": "Acesso negado"}), 403
        
        template = LeadFieldTemplate.query.get(template_id)
        if not template:
            return jsonify({"error": "Template de campo não encontrado"}), 404
        
        data = request.get_json()
        
        if "name" in data and data["name"] != template.name:
            if LeadFieldTemplate.query.filter_by(name=data["name"]).first():
                return jsonify({"error": "Já existe um template de campo com este nome"}), 409
        
        updatable_fields = ["name", "field_type", "is_required", "options", "default_value", "description", "is_active"]
        for field in updatable_fields:
            if field in data:
                setattr(template, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            "message": "Template de campo atualizado com sucesso",
            "template": template.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/lead-field-templates/<string:template_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Templates de Campo"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "template_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do template de campo"
        }
    ],
    "responses": {
        "200": {"description": "Template de campo deletado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Template de campo não encontrado"}
    }
})
def delete_field_template(template_id):
    """Deletar um template de campo."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:manage_templates"):
            return jsonify({"error": "Acesso negado"}), 403
        
        template = LeadFieldTemplate.query.get(template_id)
        if not template:
            return jsonify({"error": "Template de campo não encontrado"}), 404
        
        db.session.delete(template)
        db.session.commit()
        
        return jsonify({"message": "Template de campo deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

# Tags Management
@leads_bp.route("/tags", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Tags"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de todas as tags"},
        "403": {"description": "Acesso negado"}
    }
})
def get_tags():
    """Obter todas as tags."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        tags = Tag.query.order_by(Tag.name).all()
        
        return jsonify({
            "tags": [tag.to_dict() for tag in tags],
            "total": len(tags)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/tags", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Tags"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TagCreate",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string", "description": "Nome da tag"},
                    "description": {"type": "string", "description": "Descrição da tag"},
                    "color": {"type": "string", "description": "Cor da tag (hex code)"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Tag criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "409": {"description": "Tag já existe com este nome"}
    }
})
def create_tag():
    """Criar uma nova tag."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:manage_tags"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        if not data.get("name"):
            return jsonify({"error": "Nome da tag é obrigatório"}), 400
        
        if Tag.query.filter_by(name=data["name"]).first():
            return jsonify({"error": "Já existe uma tag com este nome"}), 409
        
        tag = Tag(
            name=data["name"],
            description=data.get("description"),
            color=data.get("color")
        )
        
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            "message": "Tag criada com sucesso",
            "tag": tag.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/tags/<string:tag_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Tags"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tag_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tag"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TagUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome da tag"},
                    "description": {"type": "string", "description": "Descrição da tag"},
                    "color": {"type": "string", "description": "Cor da tag (hex code)"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Tag atualizada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tag não encontrada"},
        "409": {"description": "Tag já existe com este nome"}
    }
})
def update_tag(tag_id):
    """Atualizar uma tag."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:manage_tags"):
            return jsonify({"error": "Acesso negado"}), 403
        
        tag = Tag.query.get(tag_id)
        if not tag:
            return jsonify({"error": "Tag não encontrada"}), 404
        
        data = request.get_json()
        
        if "name" in data and data["name"] != tag.name:
            if Tag.query.filter_by(name=data["name"]).first():
                return jsonify({"error": "Já existe uma tag com este nome"}), 409
        
        updatable_fields = ["name", "description", "color"]
        for field in updatable_fields:
            if field in data:
                setattr(tag, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            "message": "Tag atualizada com sucesso",
            "tag": tag.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@leads_bp.route("/tags/<string:tag_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Leads - Tags"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tag_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da tag"
        }
    ],
    "responses": {
        "200": {"description": "Tag deletada com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tag não encontrada"}
    }
})
def delete_tag(tag_id):
    """Deletar uma tag."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("leads:manage_tags"):
            return jsonify({"error": "Acesso negado"}), 403
        
        tag = Tag.query.get(tag_id)
        if not tag:
            return jsonify({"error": "Tag não encontrada"}), 404
        
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({"message": "Tag deletada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500


