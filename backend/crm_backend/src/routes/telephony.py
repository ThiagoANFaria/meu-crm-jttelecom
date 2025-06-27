from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.telephony_service import TelephonyService
import logging
from flasgger import swag_from

telephony_bp = Blueprint('telephony', __name__)
logger = logging.getLogger(__name__)

# Inicializar serviço
telephony_service = TelephonyService()

@telephony_bp.route('/call', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Telefonia'],
    'security': [{'BearerAuth': []}],
    'summary': 'Iniciar chamada',
    'description': 'Inicia uma chamada telefônica',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'to_number': {'type': 'string', 'description': 'Número de destino'},
                    'lead_id': {'type': 'string', 'description': 'ID do lead (opcional)'}
                },
                'required': ['to_number']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Chamada iniciada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'call_id': {'type': 'string'},
                    'status': {'type': 'string'}
                }
            }
        }
    }
})
def make_call():
    """Iniciar chamada"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        to_number = data.get('to_number')
        lead_id = data.get('lead_id')
        from_number = '+5511999999999'  # Número da empresa
        
        result = telephony_service.make_call(from_number, to_number, user_id, lead_id)
        
        return jsonify(result), 200 if result.get('success') else 500
        
    except Exception as e:
        logger.error(f"Erro ao iniciar chamada: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@telephony_bp.route('/history', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Telefonia'],
    'security': [{'BearerAuth': []}],
    'summary': 'Obter histórico de chamadas',
    'parameters': [
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'default': 50,
            'description': 'Limite de registros'
        }
    ],
    'responses': {
        200: {
            'description': 'Histórico obtido com sucesso'
        }
    }
})
def get_call_history():
    """Obter histórico de chamadas"""
    try:
        user_id = get_jwt_identity()
        tenant_id = request.headers.get('X-Tenant-ID', 'default')
        limit = int(request.args.get('limit', 50))
        
        result = telephony_service.get_call_history(user_id, tenant_id, limit)
        
        return jsonify(result), 200 if result.get('success') else 500
        
    except Exception as e:
        logger.error(f"Erro ao obter histórico: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@telephony_bp.route('/call/<call_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Telefonia'],
    'security': [{'BearerAuth': []}],
    'summary': 'Obter detalhes da chamada',
    'parameters': [
        {
            'name': 'call_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID da chamada'
        }
    ],
    'responses': {
        200: {
            'description': 'Detalhes obtidos com sucesso'
        }
    }
})
def get_call_details(call_id):
    """Obter detalhes da chamada"""
    try:
        result = telephony_service.get_call_details(call_id)
        
        return jsonify(result), 200 if result.get('success') else 500
        
    except Exception as e:
        logger.error(f"Erro ao obter detalhes: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@telephony_bp.route('/call/<call_id>/notes', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Telefonia'],
    'security': [{'BearerAuth': []}],
    'summary': 'Atualizar anotações da chamada',
    'parameters': [
        {
            'name': 'call_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID da chamada'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'notes': {'type': 'string', 'description': 'Anotações da chamada'}
                },
                'required': ['notes']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Anotações atualizadas com sucesso'
        }
    }
})
def update_call_notes(call_id):
    """Atualizar anotações da chamada"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        notes = data.get('notes')
        
        result = telephony_service.update_call_notes(call_id, notes, user_id)
        
        return jsonify(result), 200 if result.get('success') else 500
        
    except Exception as e:
        logger.error(f"Erro ao atualizar anotações: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@telephony_bp.route('/status', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Telefonia'],
    'security': [{'BearerAuth': []}],
    'summary': 'Obter status do telefone',
    'responses': {
        200: {
            'description': 'Status obtido com sucesso'
        }
    }
})
def get_phone_status():
    """Obter status do telefone"""
    try:
        user_id = get_jwt_identity()
        
        result = telephony_service.get_phone_status(user_id)
        
        return jsonify(result), 200 if result.get('success') else 500
        
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

