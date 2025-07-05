from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

contracts_bp = Blueprint('contracts', __name__)

contracts_data = [
    {"id": 1, "title": "Contrato CRM", "client_id": 1, "value": 15000.00, "status": "ativo"},
    {"id": 2, "title": "Contrato Telefonia", "client_id": 2, "value": 8500.00, "status": "ativo"}
]

@contracts_bp.route('/', methods=['GET'])
@jwt_required()
def list_contracts():
    """Listar contratos"""
    return jsonify({"contracts": contracts_data}), 200

@contracts_bp.route('/', methods=['POST'])
@jwt_required()
def create_contract():
    """Criar contrato"""
    data = request.get_json()
    new_contract = {
        "id": len(contracts_data) + 1,
        "title": data.get('title'),
        "client_id": data.get('client_id'),
        "value": data.get('value'),
        "status": "rascunho"
    }
    contracts_data.append(new_contract)
    return jsonify({"message": "Contrato criado", "contract": new_contract}), 201

@contracts_bp.route('/<int:contract_id>', methods=['GET'])
@jwt_required()
def get_contract(contract_id):
    """Obter contrato específico"""
    contract = next((c for c in contracts_data if c['id'] == contract_id), None)
    if not contract:
        return jsonify({"error": "Contrato não encontrado"}), 404
    return jsonify({"contract": contract}), 200

