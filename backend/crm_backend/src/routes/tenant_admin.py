from flask import Blueprint, jsonify

# Blueprint para super admins (JT Telecom)
super_admin_bp = Blueprint("super_admin", __name__)

# Blueprint para admins de tenant
tenant_admin_bp = Blueprint("tenant_admin", __name__)

@super_admin_bp.route("/tenants", methods=["GET"])
def list_tenants():
    """Listar todos os tenants"""
    return jsonify([
        {
            "id": 1,
            "name": "JT Tecnologia",
            "domain": "jttecnologia.com.br",
            "status": "ativo",
            "plan": "premium",
            "created_at": "2025-01-01"
        },
        {
            "id": 2,
            "name": "Cliente Demo",
            "domain": "demo.jttecnologia.com.br", 
            "status": "ativo",
            "plan": "básico",
            "created_at": "2025-06-01"
        }
    ])

@tenant_admin_bp.route("/settings", methods=["GET"])
def get_tenant_settings():
    """Obter configurações do tenant"""
    return jsonify({
        "tenant_id": 1,
        "name": "JT Tecnologia",
        "settings": {
            "theme": "dark",
            "language": "pt-BR",
            "timezone": "America/Sao_Paulo",
            "features": ["leads", "pipelines", "dashboard", "reports"]
        }
    })

