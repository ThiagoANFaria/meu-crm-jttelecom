from flask import Blueprint, jsonify, request, render_template_string, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.lead import Lead
from src.models.pipeline import Opportunity, Product
from src.models.proposal import ProposalTemplate, Proposal, ProposalItem
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_, and_
import json
import io
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import requests
from flasgger import swag_from

proposals_bp = Blueprint("proposals", __name__)

# ==================== TEMPLATES ====================

@proposals_bp.route("/proposal-templates", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Proposta"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "category",
            "in": "query",
            "type": "string",
            "description": "Filtrar por categoria"
        },
        {
            "name": "is_active",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por templates ativos",
            "default": True
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Pesquisar por nome ou descrição"
        }
    ],
    "responses": {
        "200": {"description": "Lista de templates de propostas"},
        "403": {"description": "Acesso negado"}
    }
})
def list_proposal_templates():
    """Lista templates de propostas."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Filtros
        category = request.args.get("category")
        is_active = request.args.get("is_active", "true").lower() == "true"
        search = request.args.get("search", "").strip()
        
        # Query base
        query = ProposalTemplate.query
        
        if category:
            query = query.filter(ProposalTemplate.category == category)
        
        if is_active is not None:
            query = query.filter(ProposalTemplate.is_active == is_active)
        
        if search:
            query = query.filter(or_(
                ProposalTemplate.name.ilike(f"%{search}%"),
                ProposalTemplate.description.ilike(f"%{search}%")
            ))
        
        templates = query.order_by(ProposalTemplate.name).all()
        
        return jsonify({
            "templates": [template.to_dict() for template in templates],
            "total": len(templates)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposal-templates", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Proposta"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ProposalTemplateCreate",
                "required": ["name", "content"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do template"},
                    "description": {"type": "string", "description": "Descrição do template"},
                    "category": {"type": "string", "description": "Categoria do template"},
                    "subject": {"type": "string", "description": "Assunto padrão da proposta"},
                    "content": {"type": "string", "description": "Conteúdo HTML/Markdown do template"},
                    "header_image": {"type": "string", "description": "URL da imagem do cabeçalho"},
                    "footer_text": {"type": "string", "description": "Texto do rodapé"},
                    "is_active": {"type": "boolean", "description": "Se o template está ativo", "default": True},
                    "is_default": {"type": "boolean", "description": "Se é o template padrão", "default": False},
                    "available_variables": {"type": "object", "description": "Variáveis disponíveis no template"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Template criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"}
    }
})
def create_proposal_template():
    """Cria um novo template de proposta."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:create"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Validações
        if not data.get("name"):
            return jsonify({"error": "Nome é obrigatório"}), 400
        
        if not data.get("content"):
            return jsonify({"error": "Conteúdo é obrigatório"}), 400
        
        # Criar template
        template = ProposalTemplate(
            name=data["name"],
            description=data.get("description"),
            category=data.get("category"),
            subject=data.get("subject"),
            content=data["content"],
            header_image=data.get("header_image"),
            footer_text=data.get("footer_text"),
            is_active=data.get("is_active", True),
            is_default=data.get("is_default", False),
            available_variables=data.get("available_variables", {}),
            created_by=current_user_id
        )
        
        # Se for template padrão, remover flag dos outros
        if template.is_default:
            ProposalTemplate.query.filter_by(is_default=True).update({"is_default": False})
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            "message": "Template criado com sucesso",
            "template": template.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposal-templates/<template_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Proposta"],
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
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de um template"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Template não encontrado"}
    }
})
def get_proposal_template(template_id):
    """Obtém detalhes de um template."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        template = ProposalTemplate.query.get(template_id)
        if not template:
            return jsonify({"error": "Template não encontrado"}), 404
        
        return jsonify({"template": template.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposal-templates/<template_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Proposta"],
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
                "id": "ProposalTemplateUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do template"},
                    "description": {"type": "string", "description": "Descrição do template"},
                    "category": {"type": "string", "description": "Categoria do template"},
                    "subject": {"type": "string", "description": "Assunto padrão da proposta"},
                    "content": {"type": "string", "description": "Conteúdo HTML/Markdown do template"},
                    "header_image": {"type": "string", "description": "URL da imagem do cabeçalho"},
                    "footer_text": {"type": "string", "description": "Texto do rodapé"},
                    "is_active": {"type": "boolean", "description": "Se o template está ativo"},
                    "is_default": {"type": "boolean", "description": "Se é o template padrão"},
                    "available_variables": {"type": "object", "description": "Variáveis disponíveis no template"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Template atualizado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Template não encontrado"}
    }
})
def update_proposal_template(template_id):
    """Atualiza um template de proposta."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:edit"):
            return jsonify({"error": "Acesso negado"}), 403
        
        template = ProposalTemplate.query.get(template_id)
        if not template:
            return jsonify({"error": "Template não encontrado"}), 404
        
        data = request.get_json()
        
        # Atualizar campos
        if "name" in data:
            template.name = data["name"]
        if "description" in data:
            template.description = data["description"]
        if "category" in data:
            template.category = data["category"]
        if "subject" in data:
            template.subject = data["subject"]
        if "content" in data:
            template.content = data["content"]
        if "header_image" in data:
            template.header_image = data["header_image"]
        if "footer_text" in data:
            template.footer_text = data["footer_text"]
        if "is_active" in data:
            template.is_active = data["is_active"]
        if "is_default" in data:
            template.is_default = data["is_default"]
        if "available_variables" in data:
            template.available_variables = data["available_variables"]
        
        # Se for template padrão, remover flag dos outros
        if template.is_default:
            ProposalTemplate.query.filter(
                ProposalTemplate.id != template_id,
                ProposalTemplate.is_default == True
            ).update({"is_default": False})
        
        template.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Template atualizado com sucesso",
            "template": template.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposal-templates/<template_id>/preview", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Proposta"],
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
                "id": "ProposalPreview",
                "properties": {
                    "variables": {"type": "object", "description": "Variáveis de exemplo para renderização"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Preview do template gerado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Template não encontrado"}
    }
})
def preview_proposal_template(template_id):
    """Gera preview do template com variáveis de exemplo."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        template = ProposalTemplate.query.get(template_id)
        if not template:
            return jsonify({"error": "Template não encontrado"}), 404
        
        data = request.get_json()
        variables_data = data.get("variables", {})
        
        # Variáveis de exemplo se não fornecidas
        if not variables_data:
            variables_data = {
                "name": "João Silva",
                "company_name": "Empresa Exemplo Ltda",
                "cnpj_cpf": "12.345.678/0001-90",
                "email": "joao@exemplo.com",
                "phone": "(11) 99999-9999",
                "address_city": "São Paulo",
                "address_state": "SP",
                "proposal_number": "PROP-202412-0001",
                "total_value": "R$ 15.000,00",
                "validity_days": "30",
                "current_date": datetime.now().strftime("%d/%m/%Y")
            }
        
        rendered = template.render_content(variables_data)
        
        return jsonify({
            "preview": rendered,
            "variables_used": template.get_variables_from_content(),
            "variables_data": variables_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

# ==================== PROPOSTAS ====================

@proposals_bp.route("/proposals", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
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
            "description": "Filtrar por status da proposta"
        },
        {
            "name": "priority",
            "in": "query",
            "type": "string",
            "description": "Filtrar por prioridade da proposta"
        },
        {
            "name": "assigned_to",
            "in": "query",
            "type": "string",
            "description": "Filtrar por usuário atribuído"
        },
        {
            "name": "lead_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do lead"
        },
        {
            "name": "opportunity_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID da oportunidade"
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Pesquisar por título, número da proposta, nome do lead ou nome da empresa"
        }
    ],
    "responses": {
        "200": {"description": "Lista de propostas com filtros e paginação"},
        "403": {"description": "Acesso negado"}
    }
})
def list_proposals():
    """Lista propostas com filtros."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Paginação
        page = int(request.args.get("page", 1))
        per_page = min(int(request.args.get("per_page", 20)), 100)
        
        # Filtros
        status = request.args.get("status")
        priority = request.args.get("priority")
        assigned_to = request.args.get("assigned_to")
        lead_id = request.args.get("lead_id")
        opportunity_id = request.args.get("opportunity_id")
        search = request.args.get("search", "").strip()
        
        # Query base
        query = Proposal.query
        
        if status:
            query = query.filter(Proposal.status == status)
        
        if priority:
            query = query.filter(Proposal.priority == priority)
        
        if assigned_to:
            query = query.filter(Proposal.assigned_to == assigned_to)
        
        if lead_id:
            query = query.filter(Proposal.lead_id == lead_id)
        
        if opportunity_id:
            query = query.filter(Proposal.opportunity_id == opportunity_id)
        
        if search:
            query = query.join(Lead).filter(or_(
                Proposal.title.ilike(f"%{search}%"),
                Proposal.proposal_number.ilike(f"%{search}%"),
                Lead.name.ilike(f"%{search}%"),
                Lead.company_name.ilike(f"%{search}%")
            ))
        
        # Ordenação
        query = query.order_by(Proposal.created_at.desc())
        
        # Paginação
        proposals = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "proposals": [proposal.to_dict() for proposal in proposals.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": proposals.total,
                "pages": proposals.pages,
                "has_next": proposals.has_next,
                "has_prev": proposals.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposals", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ProposalCreate",
                "required": ["title", "lead_id", "template_id"],
                "properties": {
                    "title": {"type": "string", "description": "Título da proposta"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "template_id": {"type": "string", "description": "ID do template de proposta"},
                    "total_value": {"type": "number", "format": "float", "description": "Valor total da proposta"},
                    "validity_days": {"type": "integer", "description": "Dias de validade da proposta"},
                    "priority": {"type": "string", "description": "Prioridade da proposta"},
                    "notes": {"type": "string", "description": "Notas adicionais"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "custom_variables": {"type": "object", "description": "Variáveis customizadas para o template"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "price": {"type": "number", "format": "float"},
                                "description": {"type": "string"}
                            }
                        },
                        "description": "Itens da proposta (produtos/serviços)"
                    }
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Proposta criada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Lead, template ou oportunidade não encontrado"}
    }
})
def create_proposal():
    """Cria uma nova proposta a partir de um template."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:create"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Validações
        if not data.get("title"):
            return jsonify({"error": "Título é obrigatório"}), 400
        
        if not data.get("lead_id"):
            return jsonify({"error": "Lead é obrigatório"}), 400
        
        if not data.get("template_id"):
            return jsonify({"error": "Template é obrigatório"}), 400
        
        # Verificar se lead existe
        lead = Lead.query.get(data["lead_id"])
        if not lead:
            return jsonify({"error": "Lead não encontrado"}), 404
        
        # Verificar se template existe
        template = ProposalTemplate.query.get(data["template_id"])
        if not template:
            return jsonify({"error": "Template não encontrado"}), 404
        
        # Verificar oportunidade se fornecida
        opportunity = None
        if data.get("opportunity_id"):
            opportunity = Opportunity.query.get(data["opportunity_id"])
            if not opportunity:
                return jsonify({"error": "Oportunidade não encontrada"}), 404
        
        # Preparar variáveis para renderização
        variables_data = {
            "name": lead.name,
            "company_name": lead.company_name or "",
            "cnpj_cpf": lead.cnpj_cpf or "",
            "email": lead.email or "",
            "phone": lead.phone or "",
            "whatsapp": lead.whatsapp or "",
            "address_street": lead.address_street or "",
            "address_number": lead.address_number or "",
            "address_neighborhood": lead.address_neighborhood or "",
            "address_city": lead.address_city or "",
            "address_state": lead.address_state or "",
            "address_zipcode": lead.address_zipcode or "",
            "current_date": datetime.now().strftime("%d/%m/%Y"),
            "current_year": datetime.now().year,
            "validity_days": data.get("validity_days", 30)
        }
        
        # Adicionar dados da oportunidade se disponível
        if opportunity:
            variables_data.update({
                "opportunity_title": opportunity.title,
                "opportunity_value": f"R$ {opportunity.value:,.2f}" if opportunity.value else "",
                "opportunity_probability": f"{opportunity.probability}%" if opportunity.probability else ""
            })
        
        # Adicionar variáveis customizadas
        if data.get("custom_variables"):
            variables_data.update(data["custom_variables"])
        
        # Renderizar conteúdo
        rendered = template.render_content(variables_data)
        
        # Calcular data de validade
        validity_days = data.get("validity_days", 30)
        valid_until = date.today() + timedelta(days=validity_days)
        
        # Criar proposta
        proposal = Proposal(
            title=data["title"],
            lead_id=data["lead_id"],
            opportunity_id=data.get("opportunity_id"),
            template_id=data["template_id"],
            subject=rendered["subject"],
            content=rendered["content"],
            footer_text=rendered["footer"],
            total_value=data.get("total_value"),
            validity_days=validity_days,
            valid_until=valid_until,
            priority=data.get("priority", "medium"),
            notes=data.get("notes"),
            created_by=current_user_id,
            assigned_to=data.get("assigned_to", current_user_id)
        )
        
        # Gerar número da proposta
        proposal.generate_proposal_number()
        
        # Atualizar variáveis com número da proposta
        variables_data["proposal_number"] = proposal.proposal_number
        variables_data["total_value"] = f"R$ {proposal.total_value:,.2f}" if proposal.total_value else ""
        
        # Re-renderizar com número da proposta
        rendered = template.render_content(variables_data)
        proposal.subject = rendered["subject"]
        proposal.content = rendered["content"]
        proposal.footer_text = rendered["footer"]
        
        db.session.add(proposal)
        db.session.flush()
        
        # Adicionar itens se fornecidos
        if data.get("items"):
            for item_data in data["items"]:
                item = ProposalItem(
                    proposal_id=proposal.id,
                    product_id=item_data.get("product_id"),
                    quantity=item_data.get("quantity"),
                    price=item_data.get("price"),
                    description=item_data.get("description")
                )
                db.session.add(item)
        
        db.session.commit()
        
        return jsonify({
            "message": "Proposta criada com sucesso",
            "proposal": proposal.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposals/<proposal_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "proposal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da proposta"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes da proposta"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Proposta não encontrada"}
    }
})
def get_proposal(proposal_id):
    """Obtém detalhes de uma proposta."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({"error": "Proposta não encontrada"}), 404
        
        return jsonify({"proposal": proposal.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposals/<proposal_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "proposal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da proposta"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ProposalUpdate",
                "properties": {
                    "title": {"type": "string", "description": "Título da proposta"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "template_id": {"type": "string", "description": "ID do template de proposta"},
                    "subject": {"type": "string", "description": "Assunto da proposta"},
                    "content": {"type": "string", "description": "Conteúdo HTML/Markdown da proposta"},
                    "footer_text": {"type": "string", "description": "Texto do rodapé da proposta"},
                    "total_value": {"type": "number", "format": "float", "description": "Valor total da proposta"},
                    "validity_days": {"type": "integer", "description": "Dias de validade da proposta"},
                    "valid_until": {"type": "string", "format": "date", "description": "Data de validade (YYYY-MM-DD)"},
                    "status": {"type": "string", "enum": ["draft", "sent", "viewed", "accepted", "rejected", "expired"], "description": "Status da proposta"},
                    "priority": {"type": "string", "description": "Prioridade da proposta"},
                    "notes": {"type": "string", "description": "Notas adicionais"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "price": {"type": "number", "format": "float"},
                                "description": {"type": "string"}
                            }
                        },
                        "description": "Itens da proposta (produtos/serviços)"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Proposta atualizada com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Proposta não encontrada"}
    }
})
def update_proposal(proposal_id):
    """Atualiza uma proposta."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:edit"):
            return jsonify({"error": "Acesso negado"}), 403
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({"error": "Proposta não encontrada"}), 404
        
        data = request.get_json()
        
        updatable_fields = [
            "title", "lead_id", "opportunity_id", "template_id", "subject",
            "content", "footer_text", "total_value", "validity_days",
            "valid_until", "status", "priority", "notes", "assigned_to"
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == "valid_until" and data[field]:
                    setattr(proposal, field, datetime.strptime(data[field], "%Y-%m-%d").date())
                else:
                    setattr(proposal, field, data[field])
        
        # Atualizar itens da proposta
        if "items" in data:
            # Remover itens existentes
            ProposalItem.query.filter_by(proposal_id=proposal.id).delete()
            db.session.flush()
            # Adicionar novos itens
            for item_data in data["items"]:
                item = ProposalItem(
                    proposal_id=proposal.id,
                    product_id=item_data.get("product_id"),
                    quantity=item_data.get("quantity"),
                    price=item_data.get("price"),
                    description=item_data.get("description")
                )
                db.session.add(item)
        
        db.session.commit()
        
        return jsonify({
            "message": "Proposta atualizada com sucesso",
            "proposal": proposal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposals/<proposal_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "proposal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da proposta"
        }
    ],
    "responses": {
        "200": {"description": "Proposta deletada com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Proposta não encontrada"}
    }
})
def delete_proposal(proposal_id):
    """Deleta uma proposta."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:delete"):
            return jsonify({"error": "Acesso negado"}), 403
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({"error": "Proposta não encontrada"}), 404
        
        db.session.delete(proposal)
        db.session.commit()
        
        return jsonify({"message": "Proposta deletada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@proposals_bp.route("/proposals/<proposal_id>/send-email", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "proposal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da proposta"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "SendProposalEmail",
                "required": ["to_email", "subject", "body"],
                "properties": {
                    "to_email": {"type": "string", "format": "email", "description": "Email do destinatário"},
                    "subject": {"type": "string", "description": "Assunto do email"},
                    "body": {"type": "string", "description": "Corpo do email (HTML)"},
                    "attach_pdf": {"type": "boolean", "description": "Anexar PDF da proposta", "default": True}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Email da proposta enviado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Proposta não encontrada"},
        "500": {"description": "Erro ao enviar email"}
    }
})
def send_proposal_email(proposal_id):
    """Envia a proposta por email."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:send"):
            return jsonify({"error": "Acesso negado"}), 403
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({"error": "Proposta não encontrada"}), 404
        
        data = request.get_json()
        to_email = data.get("to_email")
        subject = data.get("subject")
        body = data.get("body")
        attach_pdf = data.get("attach_pdf", True)
        
        if not to_email or not subject or not body:
            return jsonify({"error": "Email do destinatário, assunto e corpo são obrigatórios"}), 400
        
        # Configurações de SMTP (idealmente de variáveis de ambiente)
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if not smtp_server or not smtp_user or not smtp_password:
            return jsonify({"error": "Configurações de SMTP não encontradas"}), 500
        
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "html"))
        
        if attach_pdf:
            # Gerar PDF da proposta
            pdf_content = requests.post(
                f"http://localhost:5000/proposals/{proposal_id}/generate-pdf",
                headers={
                    "Authorization": request.headers.get("Authorization"),
                    "X-Tenant-ID": request.headers.get("X-Tenant-ID") # Passar tenant ID
                }
            ).content
            
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_content)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=proposta_{proposal.proposal_number}.pdf")
            msg.attach(part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        proposal.status = "sent"
        db.session.commit()
        
        return jsonify({"message": "Email da proposta enviado com sucesso"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao enviar email: {str(e)}"}), 500

@proposals_bp.route("/proposals/<proposal_id>/generate-pdf", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "proposal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da proposta"
        }
    ],
    "responses": {
        "200": {
            "description": "PDF da proposta gerado com sucesso",
            "content": {
                "application/pdf": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        },
        "403": {"description": "Acesso negado"},
        "404": {"description": "Proposta não encontrada"},
        "500": {"description": "Erro ao gerar PDF"}
    }
})
def generate_proposal_pdf(proposal_id):
    """Gera o PDF de uma proposta."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({"error": "Proposta não encontrada"}), 404
        
        # Renderizar o HTML completo da proposta
        full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{proposal.title}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20mm; }}
                    .header {{ text-align: center; margin-bottom: 20mm; }}
                    .content {{ line-height: 1.6; }}
                    .footer {{ text-align: center; margin-top: 20mm; font-size: 0.8em; color: #555; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="header">
                    {f'<img src="{proposal.template.header_image}" style="max-width: 200px;" />' if proposal.template.header_image else ''}
                    <h1>{proposal.title}</h1>
                    <p>Proposta Nº: {proposal.proposal_number}</p>
                    <p>Data: {proposal.created_at.strftime('%d/%m/%Y')}</p>
                    <p>Válida até: {proposal.valid_until.strftime('%d/%m/%Y')}</p>
                </div>
                <div class="content">
                    {proposal.content}
                </div>
        """
        
        if proposal.items:
            full_html += """
                <h2>Itens da Proposta</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Descrição</th>
                            <th>Quantidade</th>
                            <th>Preço Unitário</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for item in proposal.items:
                product_name = item.product.name if item.product else "Serviço/Item Customizado"
                item_description = item.description or product_name
                item_total = (item.quantity or 1) * (item.price or 0)
                full_html += f"""
                        <tr>
                            <td>{item_description}</td>
                            <td>{item.quantity or 1}</td>
                            <td>R$ {item.price:,.2f}</td>
                            <td>R$ {item_total:,.2f}</td>
                        </tr>
                """
            full_html += """
                    </tbody>
                </table>
                <p><strong>Valor Total: R$ {proposal.total_value:,.2f}</strong></p>
            """
        
        full_html += f"""
                <div class="footer">
                    {proposal.footer_text}
                </div>
            </body>
            </html>
        """
        
        # Usar WeasyPrint para gerar PDF
        # from weasyprint import HTML
        # pdf = HTML(string=full_html).write_pdf()
        
        # Temporariamente, retornar HTML para depuração ou usar uma ferramenta externa
        # Para produção, integrar com uma biblioteca de geração de PDF como WeasyPrint ou ReportLab
        # Por simplicidade e ambiente sandbox, vamos simular a geração de PDF
        
        # Simulação de geração de PDF (substituir por WeasyPrint em produção)
        pdf_content = io.BytesIO(full_html.encode("utf-8"))
        
        return send_file(
            pdf_content,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"proposta_{proposal.proposal_number}.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar PDF: {str(e)}"}), 500

@proposals_bp.route("/proposals/<proposal_id>/status", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Propostas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "proposal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID da proposta"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "UpdateProposalStatus",
                "required": ["status"],
                "properties": {
                    "status": {"type": "string", "enum": ["draft", "sent", "viewed", "accepted", "rejected", "expired"], "description": "Novo status da proposta"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Status da proposta atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Proposta não encontrada"}
    }
})
def update_proposal_status(proposal_id):
    """Atualiza o status de uma proposta."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("proposals:edit"):
            return jsonify({"error": "Acesso negado"}), 403
        
        proposal = Proposal.query.get(proposal_id)
        if not proposal:
            return jsonify({"error": "Proposta não encontrada"}), 404
        
        data = request.get_json()
        new_status = data.get("status")
        
        if not new_status or new_status not in ["draft", "sent", "viewed", "accepted", "rejected", "expired"]:
            return jsonify({"error": "Status inválido"}), 400
        
        proposal.status = new_status
        db.session.commit()
        
        return jsonify({"message": "Status da proposta atualizado com sucesso", "new_status": new_status}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500


