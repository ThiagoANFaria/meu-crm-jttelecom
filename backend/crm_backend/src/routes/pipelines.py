from flask import Blueprint, request, jsonify
from datetime import datetime, date
import json

pipelines_bp = Blueprint("pipelines", __name__)

@pipelines_bp.route("/", methods=["GET"])
def list_pipelines():
    """Listar pipelines"""
    return jsonify([
        {
            "id": 1,
            "name": "Pipeline de Vendas",
            "description": "Pipeline principal de vendas",
            "stages": [
                {"id": 1, "name": "Prospecção", "order": 1},
                {"id": 2, "name": "Qualificação", "order": 2},
                {"id": 3, "name": "Proposta", "order": 3},
                {"id": 4, "name": "Fechamento", "order": 4}
            ]
        },
        {
            "id": 2,
            "name": "Pipeline de Suporte",
            "description": "Pipeline para atendimento ao cliente",
            "stages": [
                {"id": 5, "name": "Abertura", "order": 1},
                {"id": 6, "name": "Em Andamento", "order": 2},
                {"id": 7, "name": "Resolvido", "order": 3}
            ]
        }
    ])

@pipelines_bp.route("/", methods=["POST"])
def create_pipeline():
    """Criar novo pipeline"""
    try:
        data = request.get_json()
        return jsonify({
            "id": 3,
            "name": data.get('name'),
            "description": data.get('description'),
            "message": "Pipeline criado com sucesso"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pipelines_bp.route("/<int:pipeline_id>", methods=["GET"])
def get_pipeline(pipeline_id):
    """Obter pipeline específico"""
    return jsonify({
        "id": pipeline_id,
        "name": "Pipeline de Vendas",
        "description": "Pipeline principal de vendas",
        "stages": [
            {"id": 1, "name": "Prospecção", "order": 1},
            {"id": 2, "name": "Qualificação", "order": 2},
            {"id": 3, "name": "Proposta", "order": 3},
            {"id": 4, "name": "Fechamento", "order": 4}
        ]
    })

