from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

leads_bp = Blueprint('leads', __name__)

# Dados de exemplo para leads
leads_data = [
    {
        "id": 1,
        "name": "João Silva",
        "email": "joao@exemplo.com",
        "phone": "(11) 99999-9999",
        "company": "Empresa ABC",
        "status": "novo",
        "created_at": "2025-01-01T10:00:00Z"
    },
    {
        "id": 2,
        "name": "Maria Santos",
        "email": "maria@exemplo.com",
        "phone": "(11) 88888-8888",
        "company": "Empresa XYZ",
        "status": "qualificado",
        "created_at": "2025-01-02T14:30:00Z"
    }
]

@leads_bp.route('/', methods=['GET'])
@jwt_required()
def list_leads():
    """Listar leads"""
    return jsonify({
        "leads": leads_data,
        "total": len(leads_data)
    }), 200

@leads_bp.route('/', methods=['POST'])
@jwt_required()
def create_lead():
    """Criar lead"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "JSON inválido"}), 400
    
    # Simular criação de lead
    new_lead = {
        "id": len(leads_data) + 1,
        "name": data.get('name'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "company": data.get('company'),
        "status": "novo",
        "created_at": "2025-01-03T12:00:00Z"
    }
    
    leads_data.append(new_lead)
    
    return jsonify({
        "message": "Lead criado com sucesso",
        "lead": new_lead
    }), 201

