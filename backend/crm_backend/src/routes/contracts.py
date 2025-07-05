from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.contract import Contract, ContractTemplate
from src.models.lead import Lead
from datetime import datetime
# Importação opcional de flasgger
try:
    from flasgger import swag_from
except ImportError:
    # Fallback se flasgger não estiver disponível
    def swag_from(spec):
        def decorator(func):
            return func
        return decorator

contracts_bp = Blueprint("contracts", __name__)

@contracts_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Listar todos os contratos',
    'description': 'Retorna uma lista paginada de todos os contratos do tenant',
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
            'description': 'Lista de contratos retornada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'contracts': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Contract'}
                    },
                    'total': {'type': 'integer'},
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'}
                }
            }
        }
    }
})
def get_contracts():
    """Get all contracts for the current tenant"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        contracts_query = Contract.query.filter_by(tenant_id=user.tenant_id)
        contracts_paginated = contracts_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        contracts_data = []
        for contract in contracts_paginated.items:
            contracts_data.append({
                "id": contract.id,
                "title": contract.title,
                "status": contract.status,
                "value": float(contract.value) if contract.value else 0,
                "start_date": contract.start_date.isoformat() if contract.start_date else None,
                "end_date": contract.end_date.isoformat() if contract.end_date else None,
                "created_at": contract.created_at.isoformat() if contract.created_at else None
            })
        
        return jsonify({
            "contracts": contracts_data,
            "total": contracts_paginated.total,
            "page": page,
            "per_page": per_page
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@contracts_bp.route("/", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Criar novo contrato',
    'description': 'Cria um novo contrato no sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['title', 'lead_id'],
                'properties': {
                    'title': {'type': 'string', 'description': 'Título do contrato'},
                    'lead_id': {'type': 'integer', 'description': 'ID do lead'},
                    'value': {'type': 'number', 'description': 'Valor do contrato'},
                    'start_date': {'type': 'string', 'description': 'Data de início (YYYY-MM-DD)'},
                    'end_date': {'type': 'string', 'description': 'Data de fim (YYYY-MM-DD)'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Contrato criado com sucesso',
            'schema': {'$ref': '#/definitions/Contract'}
        },
        400: {'description': 'Dados inválidos'},
        404: {'description': 'Lead não encontrado'}
    }
})
def create_contract():
    """Create a new contract"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('lead_id'):
            return jsonify({"error": "Título e lead_id são obrigatórios"}), 400
        
        # Check if lead exists
        lead = Lead.query.filter_by(
            id=data['lead_id'], 
            tenant_id=user.tenant_id
        ).first()
        
        if not lead:
            return jsonify({"error": "Lead não encontrado"}), 404
        
        # Parse dates
        start_date = None
        end_date = None
        
        if data.get('start_date'):
            try:
                start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Formato de data inválido para start_date. Use YYYY-MM-DD"}), 400
        
        if data.get('end_date'):
            try:
                end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Formato de data inválido para end_date. Use YYYY-MM-DD"}), 400
        
        # Create new contract
        new_contract = Contract(
            title=data['title'],
            lead_id=data['lead_id'],
            value=data.get('value', 0),
            start_date=start_date,
            end_date=end_date,
            status='draft',
            tenant_id=user.tenant_id,
            created_by=current_user_id
        )
        
        db.session.add(new_contract)
        db.session.commit()
        
        return jsonify({
            "id": new_contract.id,
            "title": new_contract.title,
            "status": new_contract.status,
            "value": float(new_contract.value) if new_contract.value else 0,
            "start_date": new_contract.start_date.isoformat() if new_contract.start_date else None,
            "end_date": new_contract.end_date.isoformat() if new_contract.end_date else None,
            "created_at": new_contract.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@contracts_bp.route("/<int:contract_id>", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Contracts'],
    'summary': 'Obter contrato por ID',
    'description': 'Retorna os detalhes de um contrato específico',
    'parameters': [
        {
            'name': 'contract_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do contrato'
        }
    ],
    'responses': {
        200: {
            'description': 'Contrato encontrado',
            'schema': {'$ref': '#/definitions/Contract'}
        },
        404: {'description': 'Contrato não encontrado'}
    }
})
def get_contract(contract_id):
    """Get a specific contract by ID"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        contract = Contract.query.filter_by(
            id=contract_id, 
            tenant_id=user.tenant_id
        ).first()
        
        if not contract:
            return jsonify({"error": "Contrato não encontrado"}), 404
        
        return jsonify({
            "id": contract.id,
            "title": contract.title,
            "status": contract.status,
            "value": float(contract.value) if contract.value else 0,
            "start_date": contract.start_date.isoformat() if contract.start_date else None,
            "end_date": contract.end_date.isoformat() if contract.end_date else None,
            "created_at": contract.created_at.isoformat() if contract.created_at else None,
            "updated_at": contract.updated_at.isoformat() if contract.updated_at else None
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

