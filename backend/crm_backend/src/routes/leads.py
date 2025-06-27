from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.lead import Lead, Tag
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

@leads_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Leads'],
    'summary': 'Listar todos os leads',
    'description': 'Retorna uma lista paginada de todos os leads do tenant',
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
            'description': 'Lista de leads retornada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'leads': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Lead'}
                    },
                    'total': {'type': 'integer'},
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'}
                }
            }
        }
    }
})
def get_leads():
    """Get all leads for the current tenant"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        leads_query = Lead.query.filter_by(tenant_id=user.tenant_id)
        leads_paginated = leads_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        leads_data = []
        for lead in leads_paginated.items:
            leads_data.append({
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "company": lead.company,
                "status": lead.status,
                "source": lead.source,
                "created_at": lead.created_at.isoformat() if lead.created_at else None
            })
        
        return jsonify({
            "leads": leads_data,
            "total": leads_paginated.total,
            "page": page,
            "per_page": per_page
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@leads_bp.route("/", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Leads'],
    'summary': 'Criar novo lead',
    'description': 'Cria um novo lead no sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'email'],
                'properties': {
                    'name': {'type': 'string', 'description': 'Nome do lead'},
                    'email': {'type': 'string', 'description': 'Email do lead'},
                    'phone': {'type': 'string', 'description': 'Telefone do lead'},
                    'company': {'type': 'string', 'description': 'Empresa do lead'},
                    'source': {'type': 'string', 'description': 'Origem do lead'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Lead criado com sucesso',
            'schema': {'$ref': '#/definitions/Lead'}
        },
        400: {'description': 'Dados inválidos'},
        409: {'description': 'Lead já existe'}
    }
})
def create_lead():
    """Create a new lead"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email'):
            return jsonify({"error": "Nome e email são obrigatórios"}), 400
        
        # Check if lead already exists
        existing_lead = Lead.query.filter_by(
            email=data['email'], 
            tenant_id=user.tenant_id
        ).first()
        
        if existing_lead:
            return jsonify({"error": "Lead com este email já existe"}), 409
        
        # Create new lead
        new_lead = Lead(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            company=data.get('company'),
            source=data.get('source', 'manual'),
            status='new',
            tenant_id=user.tenant_id,
            created_by=current_user_id
        )
        
        db.session.add(new_lead)
        db.session.commit()
        
        return jsonify({
            "id": new_lead.id,
            "name": new_lead.name,
            "email": new_lead.email,
            "phone": new_lead.phone,
            "company": new_lead.company,
            "status": new_lead.status,
            "source": new_lead.source,
            "created_at": new_lead.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@leads_bp.route("/<int:lead_id>", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Leads'],
    'summary': 'Obter lead por ID',
    'description': 'Retorna os detalhes de um lead específico',
    'parameters': [
        {
            'name': 'lead_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do lead'
        }
    ],
    'responses': {
        200: {
            'description': 'Lead encontrado',
            'schema': {'$ref': '#/definitions/Lead'}
        },
        404: {'description': 'Lead não encontrado'}
    }
})
def get_lead(lead_id):
    """Get a specific lead by ID"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        lead = Lead.query.filter_by(
            id=lead_id, 
            tenant_id=user.tenant_id
        ).first()
        
        if not lead:
            return jsonify({"error": "Lead não encontrado"}), 404
        
        return jsonify({
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "company": lead.company,
            "status": lead.status,
            "source": lead.source,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
            "updated_at": lead.updated_at.isoformat() if lead.updated_at else None
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

