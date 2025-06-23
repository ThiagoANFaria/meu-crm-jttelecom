from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.lead import Lead
from src.models.pipeline import Opportunity
from src.models.proposal import Proposal
from src.models.contract import ContractTemplate, Contract, ContractAmendment
from src.services.d4sign_service import D4SignIntegration
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_, and_
import json
import io
import os
from dateutil.relativedelta import relativedelta
from flasgger import swag_from

contracts_bp = Blueprint("contracts", __name__)

# ==================== TEMPLATES DE CONTRATOS ====================

@contracts_bp.route("/contract-templates", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Contrato"],
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
            "name": "contract_type",
            "in": "query",
            "type": "string",
            "description": "Filtrar por tipo de contrato"
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
        "200": {"description": "Lista de templates de contratos"},
        "403": {"description": "Acesso negado"}
    }
})
def list_contract_templates():
    """Lista templates de contratos."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Filtros
        category = request.args.get("category")
        contract_type = request.args.get("contract_type")
        is_active = request.args.get("is_active", "true").lower() == "true"
        search = request.args.get("search", "").strip()
        
        # Query base
        query = ContractTemplate.query
        
        if category:
            query = query.filter(ContractTemplate.category == category)
        
        if contract_type:
            query = query.filter(ContractTemplate.contract_type == contract_type)
        
        if is_active is not None:
            query = query.filter(ContractTemplate.is_active == is_active)
        
        if search:
            query = query.filter(or_(
                ContractTemplate.name.ilike(f"%{search}%"),
                ContractTemplate.description.ilike(f"%{search}%")
            ))
        
        templates = query.order_by(ContractTemplate.name).all()
        
        return jsonify({
            "templates": [template.to_dict() for template in templates],
            "total": len(templates)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contract-templates", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Contrato"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ContractTemplateCreate",
                "required": ["name", "content"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do template"},
                    "description": {"type": "string", "description": "Descrição do template"},
                    "category": {"type": "string", "description": "Categoria do template"},
                    "contract_type": {"type": "string", "description": "Tipo de contrato"},
                    "title": {"type": "string", "description": "Título padrão do contrato"},
                    "content": {"type": "string", "description": "Conteúdo HTML/Markdown do template"},
                    "header_image": {"type": "string", "description": "URL da imagem do cabeçalho"},
                    "footer_text": {"type": "string", "description": "Texto do rodapé"},
                    "default_duration_months": {"type": "integer", "description": "Duração padrão em meses"},
                    "auto_renewal": {"type": "boolean", "description": "Renovação automática"},
                    "cancellation_notice_days": {"type": "integer", "description": "Dias de aviso para cancelamento"},
                    "d4sign_template_id": {"type": "string", "description": "ID do template D4Sign"},
                    "d4sign_folder_id": {"type": "string", "description": "ID da pasta D4Sign"},
                    "signature_positions": {"type": "array", "items": {"type": "object"}, "description": "Posições de assinatura"},
                    "is_active": {"type": "boolean", "description": "Se o template está ativo"},
                    "is_default": {"type": "boolean", "description": "Se é o template padrão"},
                    "requires_witness": {"type": "boolean", "description": "Requer testemunha"},
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
def create_contract_template():
    """Cria um novo template de contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:create"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Validações
        if not data.get("name"):
            return jsonify({"error": "Nome é obrigatório"}), 400
        
        if not data.get("content"):
            return jsonify({"error": "Conteúdo é obrigatório"}), 400
        
        # Criar template
        template = ContractTemplate(
            name=data["name"],
            description=data.get("description"),
            category=data.get("category"),
            contract_type=data.get("contract_type"),
            title=data.get("title"),
            content=data["content"],
            header_image=data.get("header_image"),
            footer_text=data.get("footer_text"),
            default_duration_months=data.get("default_duration_months", 12),
            auto_renewal=data.get("auto_renewal", False),
            cancellation_notice_days=data.get("cancellation_notice_days", 30),
            d4sign_template_id=data.get("d4sign_template_id"),
            d4sign_folder_id=data.get("d4sign_folder_id"),
            signature_positions=data.get("signature_positions", []),
            is_active=data.get("is_active", True),
            is_default=data.get("is_default", False),
            requires_witness=data.get("requires_witness", False),
            available_variables=data.get("available_variables", {}),
            created_by=current_user_id
        )
        
        # Se for template padrão, remover flag dos outros
        if template.is_default:
            ContractTemplate.query.filter_by(is_default=True).update({"is_default": False})
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            "message": "Template criado com sucesso",
            "template": template.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contract-templates/<template_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Contrato"],
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
def get_contract_template(template_id):
    """Obtém detalhes de um template."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        template = ContractTemplate.query.get(template_id)
        if not template:
            return jsonify({"error": "Template não encontrado"}), 404
        
        return jsonify({"template": template.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contract-templates/<template_id>/preview", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Templates de Contrato"],
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
                "id": "ContractTemplatePreview",
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
def preview_contract_template(template_id):
    """Gera preview do template com variáveis de exemplo."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        template = ContractTemplate.query.get(template_id)
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
                "contract_number": "CONT-2024-0001",
                "contract_value": "R$ 25.000,00",
                "start_date": datetime.now().strftime("%d/%m/%Y"),
                "end_date": (datetime.now() + relativedelta(months=12)).strftime("%d/%m/%Y"),
                "duration_months": "12",
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

# ==================== CONTRATOS ====================

@contracts_bp.route("/contracts", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
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
            "description": "Filtrar por status do contrato"
        },
        {
            "name": "priority",
            "in": "query",
            "type": "string",
            "description": "Filtrar por prioridade do contrato"
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
            "name": "proposal_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID da proposta"
        },
        {
            "name": "contract_type",
            "in": "query",
            "type": "string",
            "description": "Filtrar por tipo de contrato"
        },
        {
            "name": "expiring_soon",
            "in": "query",
            "type": "boolean",
            "description": "Filtrar por contratos vencendo em breve",
            "default": False
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Pesquisar por título, número do contrato, nome do lead ou nome da empresa"
        }
    ],
    "responses": {
        "200": {"description": "Lista de contratos com filtros e paginação"},
        "403": {"description": "Acesso negado"}
    }
})
def list_contracts():
    """Lista contratos com filtros."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
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
        proposal_id = request.args.get("proposal_id")
        contract_type = request.args.get("contract_type")
        expiring_soon = request.args.get("expiring_soon", "false").lower() == "true"
        search = request.args.get("search", "").strip()
        
        # Query base
        query = Contract.query
        
        if status:
            query = query.filter(Contract.status == status)
        
        if priority:
            query = query.filter(Contract.priority == priority)
        
        if assigned_to:
            query = query.filter(Contract.assigned_to == assigned_to)
        
        if lead_id:
            query = query.filter(Contract.lead_id == lead_id)
        
        if opportunity_id:
            query = query.filter(Contract.opportunity_id == opportunity_id)
        
        if proposal_id:
            query = query.filter(Contract.proposal_id == proposal_id)
        
        if contract_type:
            query = query.join(ContractTemplate).filter(ContractTemplate.contract_type == contract_type)
        
        if expiring_soon:
            # Contratos que vencem nos próximos 30 dias
            thirty_days_from_now = date.today() + timedelta(days=30)
            query = query.filter(
                Contract.end_date.isnot(None),
                Contract.end_date <= thirty_days_from_now,
                Contract.status == "active"
            )
        
        if search:
            query = query.join(Lead).filter(or_(
                Contract.title.ilike(f"%{search}%"),
                Contract.contract_number.ilike(f"%{search}%"),
                Lead.name.ilike(f"%{search}%"),
                Lead.company_name.ilike(f"%{search}%")
            ))
        
        # Ordenação
        query = query.order_by(Contract.created_at.desc())
        
        # Paginação
        contracts = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "contracts": [contract.to_dict() for contract in contracts.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": contracts.total,
                "pages": contracts.pages,
                "has_next": contracts.has_next,
                "has_prev": contracts.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ContractCreate",
                "required": ["title", "lead_id", "template_id"],
                "properties": {
                    "title": {"type": "string", "description": "Título do contrato"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "proposal_id": {"type": "string", "description": "ID da proposta associada"},
                    "template_id": {"type": "string", "description": "ID do template de contrato"},
                    "contract_value": {"type": "number", "format": "float", "description": "Valor total do contrato"},
                    "currency": {"type": "string", "description": "Moeda do contrato"},
                    "payment_terms": {"type": "string", "description": "Termos de pagamento"},
                    "start_date": {"type": "string", "format": "date", "description": "Data de início (YYYY-MM-DD)"},
                    "duration_months": {"type": "integer", "description": "Duração em meses"},
                    "auto_renewal": {"type": "boolean", "description": "Renovação automática"},
                    "cancellation_notice_days": {"type": "integer", "description": "Dias de aviso para cancelamento"},
                    "priority": {"type": "string", "description": "Prioridade do contrato"},
                    "notes": {"type": "string", "description": "Notas adicionais"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "legal_reviewer": {"type": "string", "description": "Revisor legal"},
                    "custom_variables": {"type": "object", "description": "Variáveis customizadas para o template"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Contrato criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Lead, template, oportunidade ou proposta não encontrado"}
    }
})
def create_contract():
    """Cria um novo contrato a partir de um template."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:create"):
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
        template = ContractTemplate.query.get(data["template_id"])
        if not template:
            return jsonify({"error": "Template não encontrado"}), 404
        
        # Verificar oportunidade se fornecida
        opportunity = None
        if data.get("opportunity_id"):
            opportunity = Opportunity.query.get(data["opportunity_id"])
            if not opportunity:
                return jsonify({"error": "Oportunidade não encontrada"}), 404
        
        # Verificar proposta se fornecida
        proposal = None
        if data.get("proposal_id"):
            proposal = Proposal.query.get(data["proposal_id"])
            if not proposal:
                return jsonify({"error": "Proposta não encontrada"}), 404
        
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
            "current_year": datetime.now().year
        }
        
        # Adicionar dados da oportunidade se disponível
        if opportunity:
            variables_data.update({
                "opportunity_title": opportunity.title,
                "opportunity_value": f"R$ {opportunity.value:,.2f}" if opportunity.value else ""
            })
        
        # Adicionar dados da proposta se disponível
        if proposal:
            variables_data.update({
                "proposal_number": proposal.proposal_number,
                "proposal_value": f"R$ {proposal.total_value:,.2f}" if proposal.total_value else ""
            })
        
        # Adicionar variáveis customizadas
        if data.get("custom_variables"):
            variables_data.update(data["custom_variables"])
        
        # Calcular datas
        start_date = datetime.strptime(data.get("start_date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d").date()
        duration_months = data.get("duration_months", template.default_duration_months)
        end_date = start_date + relativedelta(months=duration_months)
        
        # Adicionar datas às variáveis
        variables_data.update({
            "start_date": start_date.strftime("%d/%m/%Y"),
            "end_date": end_date.strftime("%d/%m/%Y"),
            "duration_months": str(duration_months),
            "contract_value": f"R$ {data.get("contract_value", 0):,.2f}" if data.get("contract_value") else ""
        })
        
        # Renderizar conteúdo
        rendered = template.render_content(variables_data)
        
        # Criar contrato
        contract = Contract(
            title=data["title"],
            lead_id=data["lead_id"],
            opportunity_id=data.get("opportunity_id"),
            proposal_id=data.get("proposal_id"),
            template_id=data["template_id"],
            rendered_title=rendered["title"],
            content=rendered["content"],
            footer_text=rendered["footer"],
            contract_value=data.get("contract_value"),
            currency=data.get("currency", "BRL"),
            payment_terms=data.get("payment_terms"),
            start_date=start_date,
            duration_months=duration_months,
            auto_renewal=data.get("auto_renewal", template.auto_renewal),
            cancellation_notice_days=data.get("cancellation_notice_days", template.cancellation_notice_days),
            priority=data.get("priority", "medium"),
            notes=data.get("notes"),
            created_by=current_user_id,
            assigned_to=data.get("assigned_to", current_user_id),
            legal_reviewer=data.get("legal_reviewer")
        )
        
        # Gerar número do contrato
        contract.generate_contract_number()
        
        # Calcular data de término
        contract.end_date = contract.start_date + relativedelta(months=contract.duration_months)
        
        db.session.add(contract)
        db.session.commit()
        
        return jsonify({
            "message": "Contrato criado com sucesso",
            "contract": contract.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes do contrato"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado"}
    }
})
def get_contract(contract_id):
    """Obtém detalhes de um contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"error": "Contrato não encontrado"}), 404
        
        return jsonify({"contract": contract.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ContractUpdate",
                "properties": {
                    "title": {"type": "string", "description": "Título do contrato"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "proposal_id": {"type": "string", "description": "ID da proposta associada"},
                    "template_id": {"type": "string", "description": "ID do template de contrato"},
                    "rendered_title": {"type": "string", "description": "Título renderizado do contrato"},
                    "content": {"type": "string", "description": "Conteúdo HTML/Markdown do contrato"},
                    "footer_text": {"type": "string", "description": "Texto do rodapé do contrato"},
                    "contract_value": {"type": "number", "format": "float", "description": "Valor total do contrato"},
                    "currency": {"type": "string", "description": "Moeda do contrato"},
                    "payment_terms": {"type": "string", "description": "Termos de pagamento"},
                    "start_date": {"type": "string", "format": "date", "description": "Data de início (YYYY-MM-DD)"},
                    "duration_months": {"type": "integer", "description": "Duração em meses"},
                    "end_date": {"type": "string", "format": "date", "description": "Data de término (YYYY-MM-DD)"},
                    "auto_renewal": {"type": "boolean", "description": "Renovação automática"},
                    "cancellation_notice_days": {"type": "integer", "description": "Dias de aviso para cancelamento"},
                    "status": {"type": "string", "enum": ["draft", "sent_for_signature", "signed", "active", "expired", "cancelled", "amended"], "description": "Status do contrato"},
                    "priority": {"type": "string", "description": "Prioridade do contrato"},
                    "notes": {"type": "string", "description": "Notas adicionais"},
                    "assigned_to": {"type": "string", "description": "ID do usuário atribuído"},
                    "legal_reviewer": {"type": "string", "description": "Revisor legal"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Contrato atualizado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado"}
    }
})
def update_contract(contract_id):
    """Atualiza um contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:edit"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"error": "Contrato não encontrado"}), 404
        
        data = request.get_json()
        
        updatable_fields = [
            "title", "lead_id", "opportunity_id", "proposal_id", "template_id",
            "rendered_title", "content", "footer_text", "contract_value",
            "currency", "payment_terms", "start_date", "duration_months",
            "end_date", "auto_renewal", "cancellation_notice_days",
            "status", "priority", "notes", "assigned_to", "legal_reviewer"
        ]
        
        for field in updatable_fields:
            if field in data:
                if field in ["start_date", "end_date"] and data[field]:
                    setattr(contract, field, datetime.strptime(data[field], "%Y-%m-%d").date())
                else:
                    setattr(contract, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            "message": "Contrato atualizado com sucesso",
            "contract": contract.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        }
    ],
    "responses": {
        "200": {"description": "Contrato deletado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado"}
    }
})
def delete_contract(contract_id):
    """Deleta um contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:delete"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"error": "Contrato não encontrado"}), 404
        
        db.session.delete(contract)
        db.session.commit()
        
        return jsonify({"message": "Contrato deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>/send-for-signature", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "SendForSignature",
                "required": ["signers"],
                "properties": {
                    "signers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name", "email", "type"],
                            "properties": {
                                "name": {"type": "string", "description": "Nome do signatário"},
                                "email": {"type": "string", "format": "email", "description": "Email do signatário"},
                                "type": {"type": "string", "enum": ["sign", "witness"], "description": "Tipo de signatário (sign ou witness)"},
                                "phone": {"type": "string", "description": "Telefone do signatário (opcional para SMS)"}
                            }
                        },
                        "description": "Lista de signatários e testemunhas"
                    },
                    "due_date": {"type": "string", "format": "date", "description": "Data limite para assinatura (YYYY-MM-DD)"},
                    "message": {"type": "string", "description": "Mensagem personalizada para os signatários"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Contrato enviado para assinatura com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado"},
        "500": {"description": "Erro ao enviar para assinatura"}
    }
})
def send_contract_for_signature(contract_id):
    """Envia um contrato para assinatura eletrônica via D4Sign."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:sign"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"error": "Contrato não encontrado"}), 404
        
        data = request.get_json()
        signers = data.get("signers")
        due_date = data.get("due_date")
        message = data.get("message")
        
        if not signers or not isinstance(signers, list) or len(signers) == 0:
            return jsonify({"error": "Signatários são obrigatórios"}), 400
        
        # Inicializar serviço D4Sign
        d4sign_service = D4SignIntegration()
        
        # Gerar PDF do contrato
        # Para este exemplo, vamos simular que o PDF já existe ou é gerado internamente
        # Em um cenário real, você geraria o PDF do contrato renderizado aqui
        # pdf_content = contract.generate_pdf() # Exemplo de função para gerar PDF
        
        # Usar um PDF de exemplo ou o conteúdo HTML do contrato para enviar ao D4Sign
        # Para fins de demonstração, vamos usar um conteúdo HTML simples
        pdf_content_base64 = base64.b64encode(contract.content.encode("utf-8")).decode("utf-8")
        
        # Criar documento no D4Sign
        document_key = d4sign_service.create_document(
            folder_id=contract.template.d4sign_folder_id or os.getenv("D4SIGN_DEFAULT_FOLDER_ID"),
            # Usar folder_id do template ou default
            base64_pdf=pdf_content_base64,
            filename=f"Contrato_{contract.contract_number}.pdf",
            # flow_id=contract.template.d4sign_template_id # Se usar flow_id
        )
        
        if not document_key:
            return jsonify({"error": "Erro ao criar documento no D4Sign"}), 500
        
        # Adicionar signatários
        for signer_data in signers:
            d4sign_service.add_signer(
                document_key=document_key,
                email=signer_data["email"],
                name=signer_data["name"],
                type=signer_data["type"],
                phone_number=signer_data.get("phone"),
                # positions=contract.template.signature_positions # Se usar posições fixas
            )
        
        # Enviar para assinatura
        d4sign_service.send_document_to_sign(document_key, message=message)
        
        # Atualizar status do contrato
        contract.d4sign_document_key = document_key
        contract.status = "sent_for_signature"
        db.session.commit()
        
        return jsonify({"message": "Contrato enviado para assinatura com sucesso", "document_key": document_key}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao enviar para assinatura: {str(e)}"}), 500

@contracts_bp.route("/contracts/<contract_id>/status-d4sign", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        }
    ],
    "responses": {
        "200": {"description": "Status do documento D4Sign"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado ou sem documento D4Sign associado"},
        "500": {"description": "Erro ao consultar D4Sign"}
    }
})
def get_d4sign_status(contract_id):
    """Consulta o status de um documento no D4Sign."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract or not contract.d4sign_document_key:
            return jsonify({"error": "Contrato não encontrado ou sem documento D4Sign associado"}), 404
        
        d4sign_service = D4SignIntegration()
        status = d4sign_service.get_document_status(contract.d4sign_document_key)
        
        return jsonify({"document_key": contract.d4sign_document_key, "status": status}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao consultar D4Sign: {str(e)}"}), 500

@contracts_bp.route("/contracts/<contract_id>/download-d4sign-document", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Contratos"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        }
    ],
    "responses": {
        "200": {
            "description": "Documento assinado baixado com sucesso",
            "content": {
                "application/pdf": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        },
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado ou sem documento D4Sign associado"},
        "500": {"description": "Erro ao baixar documento do D4Sign"}
    }
})
def download_d4sign_document(contract_id):
    """Baixa o documento assinado do D4Sign."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract or not contract.d4sign_document_key:
            return jsonify({"error": "Contrato não encontrado ou sem documento D4Sign associado"}), 404
        
        d4sign_service = D4SignIntegration()
        pdf_content = d4sign_service.download_document(contract.d4sign_document_key)
        
        if not pdf_content:
            return jsonify({"error": "Documento não encontrado no D4Sign ou erro ao baixar"}), 500
        
        return send_file(
            io.BytesIO(pdf_content),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"contrato_assinado_{contract.contract_number}.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": f"Erro ao baixar documento do D4Sign: {str(e)}"}), 500

# ==================== ADITIVOS DE CONTRATOS ====================

@contracts_bp.route("/contracts/<contract_id>/amendments", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Aditivos de Contrato"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        }
    ],
    "responses": {
        "200": {"description": "Lista de aditivos para o contrato"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado"}
    }
})
def list_contract_amendments(contract_id):
    """Lista aditivos de um contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"error": "Contrato não encontrado"}), 404
        
        amendments = ContractAmendment.query.filter_by(contract_id=contract_id).order_by(ContractAmendment.created_at.desc()).all()
        
        return jsonify({
            "amendments": [amendment.to_dict() for amendment in amendments],
            "total": len(amendments)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>/amendments", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Aditivos de Contrato"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ContractAmendmentCreate",
                "required": ["title", "content"],
                "properties": {
                    "title": {"type": "string", "description": "Título do aditivo"},
                    "content": {"type": "string", "description": "Conteúdo HTML/Markdown do aditivo"},
                    "effective_date": {"type": "string", "format": "date", "description": "Data de efetivação do aditivo (YYYY-MM-DD)"},
                    "notes": {"type": "string", "description": "Notas adicionais"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Aditivo criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato não encontrado"}
    }
})
def create_contract_amendment(contract_id):
    """Cria um novo aditivo para um contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:edit"):
            return jsonify({"error": "Acesso negado"}), 403
        
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"error": "Contrato não encontrado"}), 404
        
        data = request.get_json()
        
        if not data.get("title"):
            return jsonify({"error": "Título é obrigatório"}), 400
        
        if not data.get("content"):
            return jsonify({"error": "Conteúdo é obrigatório"}), 400
        
        amendment = ContractAmendment(
            contract_id=contract_id,
            title=data["title"],
            content=data["content"],
            effective_date=datetime.strptime(data["effective_date"], "%Y-%m-%d").date() if data.get("effective_date") else date.today(),
            notes=data.get("notes"),
            created_by=current_user_id
        )
        
        db.session.add(amendment)
        db.session.commit()
        
        # Opcional: Atualizar o status do contrato para 'amended' se necessário
        contract.status = "amended"
        db.session.commit()
        
        return jsonify({
            "message": "Aditivo criado com sucesso",
            "amendment": amendment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>/amendments/<amendment_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Aditivos de Contrato"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        },
        {
            "name": "amendment_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do aditivo"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes do aditivo"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato ou aditivo não encontrado"}
    }
})
def get_contract_amendment(contract_id, amendment_id):
    """Obtém detalhes de um aditivo."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:view"):
            return jsonify({"error": "Acesso negado"}), 403
        
        amendment = ContractAmendment.query.filter_by(contract_id=contract_id, id=amendment_id).first()
        if not amendment:
            return jsonify({"error": "Aditivo não encontrado ou não pertence a este contrato"}), 404
        
        return jsonify({"amendment": amendment.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>/amendments/<amendment_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Aditivos de Contrato"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        },
        {
            "name": "amendment_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do aditivo"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ContractAmendmentUpdate",
                "properties": {
                    "title": {"type": "string", "description": "Título do aditivo"},
                    "content": {"type": "string", "description": "Conteúdo HTML/Markdown do aditivo"},
                    "effective_date": {"type": "string", "format": "date", "description": "Data de efetivação do aditivo (YYYY-MM-DD)"},
                    "notes": {"type": "string", "description": "Notas adicionais"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Aditivo atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato ou aditivo não encontrado"}
    }
})
def update_contract_amendment(contract_id, amendment_id):
    """Atualiza um aditivo de contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:edit"):
            return jsonify({"error": "Acesso negado"}), 403
        
        amendment = ContractAmendment.query.filter_by(contract_id=contract_id, id=amendment_id).first()
        if not amendment:
            return jsonify({"error": "Aditivo não encontrado ou não pertence a este contrato"}), 404
        
        data = request.get_json()
        
        updatable_fields = ["title", "content", "effective_date", "notes"]
        for field in updatable_fields:
            if field in data:
                if field == "effective_date" and data[field]:
                    setattr(amendment, field, datetime.strptime(data[field], "%Y-%m-%d").date())
                else:
                    setattr(amendment, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            "message": "Aditivo atualizado com sucesso",
            "amendment": amendment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@contracts_bp.route("/contracts/<contract_id>/amendments/<amendment_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Aditivos de Contrato"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "contract_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do contrato"
        },
        {
            "name": "amendment_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do aditivo"
        }
    ],
    "responses": {
        "200": {"description": "Aditivo deletado com sucesso"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Contrato ou aditivo não encontrado"}
    }
})
def delete_contract_amendment(contract_id, amendment_id):
    """Deleta um aditivo de contrato."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("contracts:edit"):
            return jsonify({"error": "Acesso negado"}), 403
        
        amendment = ContractAmendment.query.filter_by(contract_id=contract_id, id=amendment_id).first()
        if not amendment:
            return jsonify({"error": "Aditivo não encontrado ou não pertence a este contrato"}), 404
        
        db.session.delete(amendment)
        db.session.commit()
        
        return jsonify({"message": "Aditivo deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500


