from flask import Blueprint, jsonify

proposals_bp = Blueprint("proposals", __name__)

@proposals_bp.route("/", methods=["GET"])
def list_proposals():
    """Listar propostas"""
    return jsonify([
        {
            "id": 1,
            "title": "Proposta de Serviços de Telecomunicações",
            "client": "Empresa ABC",
            "value": 15000.00,
            "status": "enviada",
            "created_at": "2025-06-27"
        },
        {
            "id": 2,
            "title": "Proposta de Infraestrutura de Rede",
            "client": "Empresa XYZ", 
            "value": 25000.00,
            "status": "aprovada",
            "created_at": "2025-06-25"
        }
    ])

@proposals_bp.route("/<int:proposal_id>", methods=["GET"])
def get_proposal(proposal_id):
    """Obter proposta específica"""
    return jsonify({
        "id": proposal_id,
        "title": "Proposta de Serviços de Telecomunicações",
        "client": "Empresa ABC",
        "value": 15000.00,
        "status": "enviada",
        "items": [
            {"description": "Instalação de fibra óptica", "quantity": 1, "price": 10000.00},
            {"description": "Configuração de rede", "quantity": 1, "price": 5000.00}
        ],
        "created_at": "2025-06-27"
    })

