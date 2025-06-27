from flask import Blueprint, request, jsonify
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Login de usuário",
    "description": "Autentica um usuário e retorna um token JWT",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "usuario@jttelecom.com.br"},
                    "password": {"type": "string", "example": "senha123"}
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Login realizado com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "user": {"$ref": "#/definitions/User"}
                }
            }
        },
        "401": {"description": "Credenciais inválidas"}
    }
})
def login():
    """Login de usuário"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Simulação de autenticação
        if email and password:
            return jsonify({
                'access_token': 'jwt_token_example',
                'user': {
                    'id': '1',
                    'email': email,
                    'first_name': 'Usuário',
                    'last_name': 'Teste'
                }
            }), 200
        else:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route("/register", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Registro de usuário",
    "description": "Registra um novo usuário no sistema",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "novo@jttelecom.com.br"},
                    "password": {"type": "string", "example": "senha123"},
                    "first_name": {"type": "string", "example": "João"},
                    "last_name": {"type": "string", "example": "Silva"}
                },
                "required": ["email", "password", "first_name", "last_name"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Usuário criado com sucesso",
            "schema": {"$ref": "#/definitions/User"}
        },
        "400": {"description": "Dados inválidos"}
    }
})
def register():
    """Registro de novo usuário"""
    try:
        data = request.get_json()
        
        return jsonify({
            'id': '1',
            'email': data.get('email'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'is_active': True
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route("/logout", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "summary": "Logout de usuário",
    "description": "Invalida o token JWT do usuário",
    "responses": {
        "200": {"description": "Logout realizado com sucesso"}
    }
})
def logout():
    """Logout de usuário"""
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

