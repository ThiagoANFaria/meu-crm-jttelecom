from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.pipeline import Pipeline, PipelineStage, Opportunity, Product
from datetime import datetime, date
import json
from flasgger import swag_from

pipelines_bp = Blueprint("pipelines", __name__)

@pipelines_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Funis"],
    "security": [{"BearerAuth": []}],
    "summary": "Listar pipelines",
    "description": "Retorna lista de pipelines do tenant",
    "responses": {
        200: {
            "description": "Lista de pipelines obtida com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "pipelines": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "is_active": {"type": "boolean"}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_pipelines():
    """Listar pipelines"""
    try:
        tenant_id = request.headers.get('X-Tenant-ID', 'default')
        
        # Simulação de dados para demonstração
        pipelines = [
            {
                "id": "pipeline_1",
                "name": "Vendas Principais",
                "description": "Pipeline principal de vendas",
                "is_active": True,
                "stages_count": 5,
                "opportunities_count": 23
            },
            {
                "id": "pipeline_2", 
                "name": "Upsell",
                "description": "Pipeline para vendas adicionais",
                "is_active": True,
                "stages_count": 3,
                "opportunities_count": 8
            }
        ]
        
        return jsonify({
            "success": True,
            "pipelines": pipelines
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@pipelines_bp.route("/", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Funis"],
    "security": [{"BearerAuth": []}],
    "summary": "Criar pipeline",
    "description": "Cria um novo pipeline",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "stages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "order": {"type": "integer"}
                            }
                        }
                    }
                },
                "required": ["name"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Pipeline criado com sucesso"
        }
    }
})
def create_pipeline():
    """Criar pipeline"""
    try:
        data = request.get_json()
        tenant_id = request.headers.get('X-Tenant-ID', 'default')
        user_id = get_jwt_identity()
        
        # Simulação de criação para demonstração
        pipeline = {
            "id": f"pipeline_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "name": data.get('name'),
            "description": data.get('description', ''),
            "is_active": True,
            "tenant_id": tenant_id,
            "created_at": datetime.utcnow().isoformat()
        }
        
        return jsonify({
            "success": True,
            "pipeline": pipeline,
            "message": "Pipeline criado com sucesso"
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@pipelines_bp.route("/<pipeline_id>/stages", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Funis"],
    "security": [{"BearerAuth": []}],
    "summary": "Listar estágios do pipeline",
    "parameters": [
        {
            "name": "pipeline_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do pipeline"
        }
    ],
    "responses": {
        200: {
            "description": "Estágios obtidos com sucesso"
        }
    }
})
def get_pipeline_stages(pipeline_id):
    """Listar estágios do pipeline"""
    try:
        # Simulação de dados para demonstração
        stages = [
            {"id": "stage_1", "name": "Prospecção", "order": 1, "color": "#4169E1"},
            {"id": "stage_2", "name": "Qualificação", "order": 2, "color": "#32CD32"},
            {"id": "stage_3", "name": "Proposta", "order": 3, "color": "#FFD700"},
            {"id": "stage_4", "name": "Negociação", "order": 4, "color": "#FF8C00"},
            {"id": "stage_5", "name": "Fechamento", "order": 5, "color": "#228B22"}
        ]
        
        return jsonify({
            "success": True,
            "stages": stages
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@pipelines_bp.route("/<pipeline_id>/opportunities", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Funis"],
    "security": [{"BearerAuth": []}],
    "summary": "Listar oportunidades do pipeline",
    "parameters": [
        {
            "name": "pipeline_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do pipeline"
        }
    ],
    "responses": {
        200: {
            "description": "Oportunidades obtidas com sucesso"
        }
    }
})
def get_pipeline_opportunities(pipeline_id):
    """Listar oportunidades do pipeline"""
    try:
        # Simulação de dados para demonstração
        opportunities = [
            {
                "id": "opp_1",
                "title": "Venda para Empresa ABC",
                "value": 15000.00,
                "stage_id": "stage_2",
                "probability": 60,
                "lead_name": "João Silva",
                "expected_close_date": "2024-07-15"
            },
            {
                "id": "opp_2", 
                "title": "Upsell Cliente XYZ",
                "value": 8500.00,
                "stage_id": "stage_3",
                "probability": 80,
                "lead_name": "Maria Santos",
                "expected_close_date": "2024-07-10"
            }
        ]
        
        return jsonify({
            "success": True,
            "opportunities": opportunities
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

