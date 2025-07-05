from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.automation import AutomationRule, AutomationAction
from src.services.automation_service import AutomationService
# Importação opcional de flasgger
try:
    from flasgger import swag_from
except ImportError:
    # Fallback se flasgger não estiver disponível
    def swag_from(spec):
        def decorator(func):
            return func
        return decorator

automation_bp = Blueprint("automation", __name__)

class CadenceService:
    """Serviço para gerenciar cadências de email"""
    
    @staticmethod
    def create_cadence(cadence_data):
        """Cria uma nova cadência"""
        try:
            print(f"📧 Criando cadência: {cadence_data.get('name', 'Sem nome')}")
            return {'success': True, 'message': 'Cadência criada com sucesso'}
        except Exception as e:
            return {'success': False, 'message': f'Erro ao criar cadência: {str(e)}'}
    
    @staticmethod
    def execute_cadence(cadence_id):
        """Executa uma cadência"""
        try:
            print(f"🚀 Executando cadência {cadence_id}")
            return {'success': True, 'message': 'Cadência executada com sucesso'}
        except Exception as e:
            return {'success': False, 'message': f'Erro ao executar cadência: {str(e)}'}

@automation_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Automation'],
    'summary': 'Listar regras de automação',
    'description': 'Retorna uma lista de regras de automação do tenant',
    'responses': {
        200: {
            'description': 'Lista de automações retornada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'automations': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/AutomationRule'}
                    }
                }
            }
        }
    }
})
def get_automations():
    """Get automation rules"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        automations = AutomationRule.query.filter_by(tenant_id=user.tenant_id).all()
        
        automations_data = []
        for automation in automations:
            automations_data.append({
                "id": automation.id,
                "name": automation.name,
                "description": automation.description,
                "is_active": automation.is_active,
                "created_at": automation.created_at.isoformat() if automation.created_at else None
            })
        
        return jsonify({"automations": automations_data}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@automation_bp.route("/", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Automation'],
    'summary': 'Criar nova automação',
    'description': 'Cria uma nova regra de automação',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'trigger_type'],
                'properties': {
                    'name': {'type': 'string', 'description': 'Nome da automação'},
                    'description': {'type': 'string', 'description': 'Descrição da automação'},
                    'trigger_type': {'type': 'string', 'description': 'Tipo de gatilho'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Automação criada com sucesso',
            'schema': {'$ref': '#/definitions/AutomationRule'}
        }
    }
})
def create_automation():
    """Create automation rule"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        
        if not data.get('name') or not data.get('trigger_type'):
            return jsonify({"error": "Nome e tipo de gatilho são obrigatórios"}), 400
        
        # Usar o serviço de automação
        result = AutomationService.create_automation_rule(data)
        
        if result['success']:
            return jsonify({
                "id": "auto_123",
                "name": data['name'],
                "description": data.get('description', ''),
                "trigger_type": data['trigger_type'],
                "is_active": True,
                "created_at": "2024-06-27T12:00:00Z"
            }), 201
        else:
            return jsonify({"error": result['message']}), 400
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@automation_bp.route("/cadence", methods=["POST"])
@jwt_required()
@swag_from({
    'tags': ['Automation'],
    'summary': 'Criar cadência de email',
    'description': 'Cria uma nova cadência de email marketing',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name'],
                'properties': {
                    'name': {'type': 'string', 'description': 'Nome da cadência'},
                    'description': {'type': 'string', 'description': 'Descrição da cadência'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Cadência criada com sucesso'
        }
    }
})
def create_cadence():
    """Create email cadence"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({"error": "Nome da cadência é obrigatório"}), 400
        
        # Usar o serviço de cadência
        result = CadenceService.create_cadence(data)
        
        if result['success']:
            return jsonify({
                "id": "cadence_123",
                "name": data['name'],
                "description": data.get('description', ''),
                "created_at": "2024-06-27T12:00:00Z"
            }), 201
        else:
            return jsonify({"error": result['message']}), 400
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

