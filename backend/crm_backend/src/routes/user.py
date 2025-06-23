from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, Role, db
from flasgger import swag_from

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de todos os usuários"},
        "403": {"description": "Acesso negado"}
    }
})
def get_users():
    """Obter todos os usuários (apenas Admin)."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        users = User.query.all()
        return jsonify({
            "users": [user.to_dict() for user in users],
            "total": len(users)
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@user_bp.route("/users", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "UserCreate",
                "required": ["email", "password", "first_name", "last_name", "role_id"],
                "properties": {
                    "email": {"type": "string", "format": "email", "description": "Email do novo usuário"},
                    "password": {"type": "string", "format": "password", "description": "Senha do novo usuário"},
                    "first_name": {"type": "string", "description": "Primeiro nome do novo usuário"},
                    "last_name": {"type": "string", "description": "Sobrenome do novo usuário"},
                    "role_id": {"type": "string", "description": "ID do papel do novo usuário"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Usuário criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "409": {"description": "Usuário já existe"}
    }
})
def create_user():
    """Criar um novo usuário (apenas Admin)."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:create"):
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["email", "password", "first_name", "last_name", "role_id"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400
        
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

@user_bp.route("/users/<string:user_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do usuário"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes do usuário"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Usuário não encontrado"}
    }
})
def get_user(user_id):
    """Obter um usuário específico."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Users can view their own profile or admins can view any profile
        if current_user_id != user_id and not current_user.has_permission("users:read"):
            return jsonify({"error": "Acesso negado"}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify({"user": user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

@user_bp.route("/users/<string:user_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do usuário"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "UserUpdate",
                "properties": {
                    "first_name": {"type": "string", "description": "Primeiro nome do usuário"},
                    "last_name": {"type": "string", "description": "Sobrenome do usuário"},
                    "email": {"type": "string", "format": "email", "description": "Email do usuário (apenas admin)"},
                    "role_id": {"type": "string", "description": "ID do papel do usuário (apenas admin)"},
                    "is_active": {"type": "boolean", "description": "Status de atividade do usuário (apenas admin)"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Usuário atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Usuário não encontrado"}
    }
})
def update_user(user_id):
    """Atualizar um usuário."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        # Users can update their own profile (limited fields) or admins can update any profile
        is_self_update = current_user_id == user_id
        is_admin = current_user.has_permission("users:update")
        
        if not is_self_update and not is_admin:
            return jsonify({"error": "Acesso negado"}), 403
        
        data = request.get_json()
        
        # Fields that users can update on their own profile
        self_updatable_fields = ["first_name", "last_name"]
        
        # Fields that only admins can update
        admin_only_fields = ["email", "role_id", "is_active"]
        
        for field, value in data.items():
            if field in self_updatable_fields:
                setattr(user, field, value)
            elif field in admin_only_fields and is_admin:
                if field == "role_id":
                    # Validate role exists
                    role = Role.query.get(value)
                    if not role:
                        return jsonify({"error": "Papel inválido"}), 400
                setattr(user, field, value)
            elif field not in self_updatable_fields and field not in admin_only_fields:
                return jsonify({"error": f"Campo {field} não pode ser atualizado"}), 400
            elif field in admin_only_fields and not is_admin:
                return jsonify({"error": f"Apenas administradores podem atualizar o campo {field}"}), 403
        
        db.session.commit()
        return jsonify({
            "message": "Usuário atualizado com sucesso",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@user_bp.route("/users/<string:user_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do usuário"
        }
    ],
    "responses": {
        "200": {"description": "Usuário deletado com sucesso"},
        "400": {"description": "Não é possível deletar a própria conta"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Usuário não encontrado"}
    }
})
def delete_user(user_id):
    """Deletar um usuário (apenas Admin)."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:delete"):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Prevent self-deletion
        if current_user_id == user_id:
            return jsonify({"error": "Não é possível deletar sua própria conta"}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@user_bp.route("/users/<string:user_id>/toggle-status", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do usuário"
        }
    ],
    "responses": {
        "200": {"description": "Status do usuário alterado com sucesso"},
        "400": {"description": "Não é possível desativar a própria conta"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Usuário não encontrado"}
    }
})
def toggle_user_status(user_id):
    """Alternar status de atividade do usuário (apenas Admin)."""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission("users:update"):
            return jsonify({"error": "Acesso negado"}), 403
        
        # Prevent self-deactivation
        if current_user_id == user_id:
            return jsonify({"error": "Não é possível desativar sua própria conta"}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        user.is_active = not user.is_active
        db.session.commit()
        
        status = "ativado" if user.is_active else "desativado"
        return jsonify({
            "message": f"Usuário {status} com sucesso",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500


