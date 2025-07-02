from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def auth_info():
    """Informações do módulo de autenticação"""
    return jsonify({
        "message": "Módulo de autenticação do CRM JT Telecom",
        "version": "1.0.0",
        "endpoints": {
            "login": "POST /auth/login",
            "register": "POST /auth/register",
            "verify": "POST /auth/verify"
        }
    }), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login de usuário com JWT REAL"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "JSON inválido"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        # Buscar usuário no banco de dados
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Criar usuário padrão se não existir (para compatibilidade)
            if email == "admin@jttecnologia.com.br" and password == "admin123":
                user = User(
                    email=email,
                    name="Usuário Teste",
                    password_hash=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
            else:
                return jsonify({"error": "Credenciais inválidas"}), 401
        
        # Verificar senha
        if not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Credenciais inválidas"}), 401
        
        # Gerar JWT token REAL (não mais "jwt_token_example")
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24),
            additional_claims={
                'email': user.email,
                'name': user.name
            }
        )
        
        # Resposta com JWT REAL
        response = {
            "access_token": access_token,
            "message": "Login realizado com sucesso",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    ENDPOINT DESABILITADO - SISTEMA MULTI-TENANT
    
    Em um sistema multi-tenant, o cadastro público não é permitido.
    Usuários devem ser criados pelo administrador da tenant.
    """
    return jsonify({
        'error': 'Cadastro público não permitido',
        'message': 'Este é um sistema multi-tenant. Entre em contato com o administrador da sua empresa para obter acesso.',
        'code': 'REGISTRATION_DISABLED',
        'contact': 'admin@jttecnologia.com.br'
    }), 403

@auth_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_token():
    """Verificar se um token JWT é válido"""
    try:
        # O decorador @jwt_required() já faz a verificação
        # Se chegou até aqui, o token é válido
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"valid": False, "error": "Usuário não encontrado"}), 404
        
        return jsonify({
            "valid": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }), 200
        
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 401

