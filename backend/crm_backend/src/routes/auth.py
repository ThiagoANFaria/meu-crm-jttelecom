from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, Role, Permission, db
from datetime import timedelta
import re
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__)
jwt = JWTManager()

def validate_email(email):
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"
    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula"
    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula"
    if not re.search(r"\d", password):
        return False, "A senha deve conter pelo menos um número"
    return True, "Senha válida"

@auth_bp.route("/register", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "UserRegister",
                "required": ["email", "password", "first_name", "last_name", "role_id"],
                "properties": {
                    "email": {"type": "string", "format": "email", "description": "Email do usuário"},
                    "password": {"type": "string", "format": "password", "description": "Senha do usuário"},
                    "first_name": {"type": "string", "description": "Primeiro nome do usuário"},
                    "last_name": {"type": "string", "description": "Sobrenome do usuário"},
                    "role_id": {"type": "string", "description": "ID do papel do usuário"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Usuário criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "409": {"description": "Usuário já existe"}
    }
})
def register():
    """Registrar um novo usuário."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["email", "password", "first_name", "last_name", "role_id"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400
        
        # Validate email format
        if not validate_email(data["email"]):
            return jsonify({"error": "Formato de email inválido"}), 400
        
        # Validate password strength
        is_valid, message = validate_password(data["password"])
        if not is_valid:
            return jsonify({"error": message}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Usuário já existe com este email"}), 409
        
        # Validate role exists
        role = Role.query.get(data["role_id"])
        if not role:
            return jsonify({"error": "Papel inválido"}), 400
        
        # Create new user
        user = User(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            role_id=data["role_id"]
        )
        user.set_password(data["password"])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/login", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "UserLogin",
                "required": ["email", "password"],
                "properties": {
                    "email": {"type": "string", "format": "email", "description": "Email do usuário"},
                    "password": {"type": "string", "format": "password", "description": "Senha do usuário"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Autenticação bem-sucedida, retorna token JWT"},
        "400": {"description": "Email e/ou senha são obrigatórios"},
        "401": {"description": "Credenciais inválidas ou conta desativada"}
    }
})
def login():
    """Autenticar usuário e retornar token JWT."""
    try:
        data = request.get_json()
        
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data["email"]).first()
        
        if not user or not user.check_password(data["password"]):
            return jsonify({"error": "Credenciais inválidas"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Conta desativada"}), 401
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        
        return jsonify({
            "access_token": access_token,
            "user": user.to_dict(include_sensitive=True),
            "expires_in": 86400  # 24 hours in seconds
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/me", methods=["GET"])
@swag_from({
    "tags": ["Autenticação"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Informações do usuário autenticado"},
        "401": {"description": "Token JWT inválido ou ausente"},
        "404": {"description": "Usuário não encontrado"}
    }
})
def get_current_user():
    """Obter informações do usuário autenticado atualmente."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify({"user": user.to_dict(include_sensitive=True)}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/change-password", methods=["POST"])
@swag_from({
    "tags": ["Autenticação"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChangePassword",
                "required": ["current_password", "new_password"],
                "properties": {
                    "current_password": {"type": "string", "format": "password", "description": "Senha atual do usuário"},
                    "new_password": {"type": "string", "format": "password", "description": "Nova senha do usuário"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Senha alterada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Senha atual incorreta ou token inválido"},
        "404": {"description": "Usuário não encontrado"}
    }
})
def change_password():
    """Alterar a senha do usuário."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data = request.get_json()
        
        if not data.get("current_password") or not data.get("new_password"):
            return jsonify({"error": "Senha atual e nova senha são obrigatórias"}), 400
        
        # Verify current password
        if not user.check_password(data["current_password"]):
            return jsonify({"error": "Senha atual incorreta"}), 401
        
        # Validate new password
        is_valid, message = validate_password(data["new_password"])
        if not is_valid:
            return jsonify({"error": message}), 400
        
        # Update password
        user.set_password(data["new_password"])
        db.session.commit()
        
        return jsonify({"message": "Senha alterada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/roles", methods=["GET"])
@swag_from({
    "tags": ["Autenticação"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de papéis disponíveis"},
        "403": {"description": "Acesso negado"}
    }
})
def get_roles():
    """Obter todos os papéis disponíveis."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        roles = Role.query.all()
        return jsonify({"roles": [role.to_dict() for role in roles]}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/permissions", methods=["GET"])
@swag_from({
    "tags": ["Autenticação"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de permissões disponíveis"},
        "403": {"description": "Acesso negado"}
    }
})
def get_permissions():
    """Obter todas as permissões disponíveis."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.has_permission("users:manage"):
            return jsonify({"error": "Acesso negado"}), 403
        
        permissions = Permission.query.all()
        return jsonify({"permissions": [perm.to_dict() for perm in permissions]}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500


