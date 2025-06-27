from flask import Blueprint, request, jsonify
from flasgger import swag_from

leads_bp = Blueprint("leads", __name__)

@leads_bp.route("/", methods=["GET"])
@swag_from({
    "tags": ["Leads"],
    "summary": "Listar leads",
    "description": "Retorna lista de todos os leads",
    "responses": {
        "200": {
            "description": "Lista de leads",
            "schema": {
                "type": "array",
                "items": {"$ref": "#/definitions/Lead"}
            }
        }
    }
})
def get_leads():
    """Listar todos os leads"""
    leads = [
        {
            'id': '1',
            'name': 'João Silva',
            'email': 'joao@exemplo.com',
            'phone': '(11) 99999-9999',
            'status': 'novo'
        },
        {
            'id': '2', 
            'name': 'Maria Santos',
            'email': 'maria@exemplo.com',
            'phone': '(11) 88888-8888',
            'status': 'qualificado'
        }
    ]
    return jsonify(leads), 200

@leads_bp.route("/", methods=["POST"])
@swag_from({
    "tags": ["Leads"],
    "summary": "Criar lead",
    "description": "Cria um novo lead",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "João Silva"},
                    "email": {"type": "string", "example": "joao@exemplo.com"},
                    "phone": {"type": "string", "example": "(11) 99999-9999"},
                    "status": {"type": "string", "example": "novo"}
                },
                "required": ["name", "email"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Lead criado com sucesso",
            "schema": {"$ref": "#/definitions/Lead"}
        }
    }
})
def create_lead():
    """Criar novo lead"""
    try:
        data = request.get_json()
        
        new_lead = {
            'id': '3',
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'status': data.get('status', 'novo')
        }
        
        return jsonify(new_lead), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route("/<lead_id>", methods=["GET"])
@swag_from({
    "tags": ["Leads"],
    "summary": "Obter lead",
    "description": "Retorna um lead específico",
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
        "200": {
            "description": "Lead encontrado",
            "schema": {"$ref": "#/definitions/Lead"}
        },
        "404": {"description": "Lead não encontrado"}
    }
})
def get_lead(lead_id):
    """Obter lead por ID"""
    lead = {
        'id': lead_id,
        'name': 'João Silva',
        'email': 'joao@exemplo.com',
        'phone': '(11) 99999-9999',
        'status': 'novo'
    }
    return jsonify(lead), 200

@leads_bp.route("/<lead_id>", methods=["PUT"])
@swag_from({
    "tags": ["Leads"],
    "summary": "Atualizar lead",
    "description": "Atualiza um lead existente",
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
            "schema": {"$ref": "#/definitions/Lead"}
        }
    ],
    "responses": {
        "200": {
            "description": "Lead atualizado",
            "schema": {"$ref": "#/definitions/Lead"}
        }
    }
})
def update_lead(lead_id):
    """Atualizar lead"""
    try:
        data = request.get_json()
        
        updated_lead = {
            'id': lead_id,
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'status': data.get('status')
        }
        
        return jsonify(updated_lead), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route("/<lead_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Leads"],
    "summary": "Deletar lead",
    "description": "Remove um lead do sistema",
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
        "404": {"description": "Lead não encontrado"}
    }
})
def delete_lead(lead_id):
    """Deletar lead"""
    return jsonify({'message': f'Lead {lead_id} deletado com sucesso'}), 200

