from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def auth_info():
    """Informações sobre autenticação"""
    return jsonify({
        "module": "auth",
        "description": "Módulo de autenticação",
        "endpoints": [
            {"path": "/login", "method": "POST", "description": "Login de usuário"},
            {"path": "/register", "method": "POST", "description": "Registro de usuário"},
            {"path": "/logout", "method": "POST", "description": "Logout de usuário"}
        ]
    })

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login de usuário"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Implementação básica de login
        if email and password:
            return jsonify({
                "message": "Login realizado com sucesso",
                "access_token": "jwt_token_example",
                "user": {
                    "id": 1,
                    "email": email,
                    "name": "Usuário Teste"
                }
            })
        else:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/register", methods=["POST"])
def register():
    """Registro de usuário"""
    try:
        data = request.get_json()
        return jsonify({
            "message": "Usuário registrado com sucesso",
            "user": {
                "id": 2,
                "email": data.get('email'),
                "name": data.get('name')
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout de usuário"""
    return jsonify({"message": "Logout realizado com sucesso"})