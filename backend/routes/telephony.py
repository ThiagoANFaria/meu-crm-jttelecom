from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

telephony_bp = Blueprint('telephony', __name__)

@telephony_bp.route('/calls', methods=['GET'])
@jwt_required()
def list_calls():
    """Listar chamadas"""
    calls = [
        {"id": 1, "number": "(11) 99999-9999", "duration": 120, "status": "completed"},
        {"id": 2, "number": "(11) 88888-8888", "duration": 45, "status": "missed"}
    ]
    return jsonify({"calls": calls}), 200

@telephony_bp.route('/calls', methods=['POST'])
@jwt_required()
def make_call():
    """Fazer chamada"""
    data = request.get_json()
    return jsonify({"message": "Chamada iniciada", "call_id": 123}), 200

@telephony_bp.route('/recordings', methods=['GET'])
@jwt_required()
def list_recordings():
    """Listar gravações"""
    recordings = [
        {"id": 1, "call_id": 1, "duration": 120, "url": "/recordings/1.mp3"},
        {"id": 2, "call_id": 2, "duration": 45, "url": "/recordings/2.mp3"}
    ]
    return jsonify({"recordings": recordings}), 200

