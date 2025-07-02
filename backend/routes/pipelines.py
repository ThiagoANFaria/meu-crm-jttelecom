from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

pipelines_bp = Blueprint('pipelines', __name__)

@pipelines_bp.route('/', methods=['GET'])
@jwt_required()
def list_pipelines():
    """Listar pipelines"""
    pipelines = [
        {"id": 1, "name": "Vendas", "stages": ["Novo", "Qualificado", "Proposta", "Fechado"]},
        {"id": 2, "name": "Suporte", "stages": ["Aberto", "Em andamento", "Resolvido"]}
    ]
    return jsonify({"pipelines": pipelines}), 200

