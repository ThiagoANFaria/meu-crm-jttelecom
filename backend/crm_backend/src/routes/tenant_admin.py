from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src.models.tenant import Tenant, SubscriptionPlan, TenantStatus
from src.services.tenant_service import TenantService
from src.middleware.tenant_middleware import require_tenant, get_current_tenant
from datetime import datetime, date
import logging
from functools import wraps
from flasgger import swag_from

# Blueprint para super admins (JT Telecom)
super_admin_bp = Blueprint("super_admin", __name__)

# Blueprint para admins de tenant
tenant_admin_bp = Blueprint("tenant_admin", __name__)

logger = logging.getLogger(__name__)

# Inicializar serviço
tenant_service = TenantService()

# ==================== SUPER ADMIN ROUTES ====================

def require_super_admin(f):
    """Decorador que exige super admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role != "super_admin":
            return jsonify({"error": "Acesso negado. Apenas super admins."}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

@super_admin_bp.route("/tenants", methods=["GET"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "Filtrar por status do tenant"
        },
        {
            "name": "plan",
            "in": "query",
            "type": "string",
            "description": "Filtrar por plano de assinatura"
        },
        {
            "name": "search",
            "in": "query",
            "type": "string",
            "description": "Termo de busca para nome ou CNPJ"
        },
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "description": "Número da página",
            "default": 1
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "description": "Itens por página",
            "default": 20
        }
    ],
    "responses": {
        "200": {"description": "Lista de todos os tenants"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"}
    }
})
def list_all_tenants():
    """Lista todos os tenants (super admin)"""
    try:
        # Parâmetros de filtro
        filters = {}
        
        if request.args.get("status"):
            filters["status"] = request.args.get("status")
        
        if request.args.get("plan"):
            filters["plan"] = request.args.get("plan")
        
        if request.args.get("search"):
            filters["search"] = request.args.get("search")
        
        # Paginação
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        
        result = tenant_service.list_tenants(filters, page, per_page)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar tenants: {e}")
        return jsonify({"error": f"Erro ao listar tenants: {str(e)}"}), 500

@super_admin_bp.route("/tenants", methods=["POST"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TenantCreate",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string", "description": "Nome do tenant"},
                    "slug": {"type": "string", "description": "Slug do tenant para subdomínio"},
                    "email": {"type": "string", "format": "email", "description": "Email do admin do tenant (padrão: admin@jttelecom.com.br)", "default": "admin@jttelecom.com.br"},
                    "phone": {"type": "string", "description": "Telefone do tenant"},
                    "cnpj": {"type": "string", "description": "CNPJ do tenant"},
                    "address": {"type": "string", "description": "Endereço do tenant"},
                    "subscription_plan": {"type": "string", "description": "Plano de assinatura (e.g., BASIC, PRO)"},
                    "status": {"type": "string", "description": "Status do tenant (e.g., ACTIVE, TRIAL)"},
                    "logo_url": {"type": "string", "description": "URL do logo do tenant"},
                    "custom_css": {"type": "string", "description": "CSS customizado para o tenant"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Novo tenant criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"}
    }
})
def create_tenant():
    """Cria novo tenant (super admin)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validações básicas
    required_fields = ["name"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    try:
        result = tenant_service.create_tenant(data, created_by=current_user_id)
        
        if result.get("success"):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao criar tenant: {e}")
        return jsonify({"error": f"Erro ao criar tenant: {str(e)}"}), 500

@super_admin_bp.route("/tenants/<tenant_id>", methods=["GET"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tenant_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do tenant"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de um tenant"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def get_tenant_details(tenant_id):
    """Obtém detalhes de um tenant (super admin)"""
    try:
        tenant = Tenant.query.get_or_404(tenant_id)
        
        # Incluir analytics
        analytics = tenant_service.get_tenant_analytics(tenant_id, days=30)
        
        return jsonify({
            "tenant": tenant.to_dict(),
            "analytics": analytics
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter tenant: {e}")
        return jsonify({"error": f"Erro ao obter tenant: {str(e)}"}), 500

@super_admin_bp.route("/tenants/<tenant_id>", methods=["PUT"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tenant_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do tenant"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TenantUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do tenant"},
                    "slug": {"type": "string", "description": "Slug do tenant para subdomínio"},
                    "email": {"type": "string", "format": "email", "description": "Email do admin do tenant (padrão: admin@jttelecom.com.br)", "default": "admin@jttelecom.com.br"},
                    "phone": {"type": "string", "description": "Telefone do tenant"},
                    "cnpj": {"type": "string", "description": "CNPJ do tenant"},
                    "address": {"type": "string", "description": "Endereço do tenant"},
                    "subscription_plan": {"type": "string", "description": "Plano de assinatura (e.g., BASIC, PRO)"},
                    "status": {"type": "string", "description": "Status do tenant (e.g., ACTIVE, TRIAL)"},
                    "logo_url": {"type": "string", "description": "URL do logo do tenant"},
                    "custom_css": {"type": "string", "description": "CSS customizado para o tenant"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Tenant atualizado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def update_tenant(tenant_id):
    """Atualiza tenant (super admin)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        result = tenant_service.update_tenant(tenant_id, data, updated_by=current_user_id)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao atualizar tenant: {e}")
        return jsonify({"error": f"Erro ao atualizar tenant: {str(e)}"}), 500

@super_admin_bp.route("/tenants/<tenant_id>/change-plan", methods=["POST"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tenant_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do tenant"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ChangePlan",
                "required": ["plan"],
                "properties": {
                    "plan": {"type": "string", "description": "Novo plano de assinatura (e.g., PRO, ENTERPRISE)"},
                    "billing_cycle": {"type": "string", "description": "Ciclo de cobrança (e.g., MONTHLY, ANNUALLY)"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Plano do tenant alterado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def change_tenant_plan(tenant_id):
    """Altera plano do tenant (super admin)"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if "plan" not in data:
        return jsonify({"error": "Campo plan é obrigatório"}), 400
    
    try:
        result = tenant_service.change_subscription_plan(
            tenant_id=tenant_id,
            new_plan=data["plan"],
            billing_cycle=data.get("billing_cycle"),
            changed_by=current_user_id
        )
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao alterar plano: {e}")
        return jsonify({"error": f"Erro ao alterar plano: {str(e)}"}), 500

@super_admin_bp.route("/tenants/<tenant_id>/suspend", methods=["POST"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tenant_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do tenant"
        },
        {
            "name": "body",
            "in": "body",
            "schema": {
                "id": "SuspendTenant",
                "properties": {
                    "reason": {"type": "string", "description": "Motivo da suspensão"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Tenant suspenso com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def suspend_tenant(tenant_id):
    """Suspende tenant (super admin)"""
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        result = tenant_service.suspend_tenant(
            tenant_id=tenant_id,
            reason=data.get("reason"),
            suspended_by=current_user_id
        )
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao suspender tenant: {e}")
        return jsonify({"error": f"Erro ao suspender tenant: {str(e)}"}), 500

@super_admin_bp.route("/tenants/<tenant_id>/reactivate", methods=["POST"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tenant_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do tenant"
        }
    ],
    "responses": {
        "200": {"description": "Tenant reativado com sucesso"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def reactivate_tenant(tenant_id):
    """Reativa tenant (super admin)"""
    current_user_id = get_jwt_identity()
    
    try:
        result = tenant_service.reactivate_tenant(
            tenant_id=tenant_id,
            reactivated_by=current_user_id
        )
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao reativar tenant: {e}")
        return jsonify({"error": f"Erro ao reativar tenant: {str(e)}"}), 500

@super_admin_bp.route("/tenants/<tenant_id>/cancel", methods=["POST"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tenant_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do tenant"
        },
        {
            "name": "body",
            "in": "body",
            "schema": {
                "id": "CancelTenant",
                "properties": {
                    "reason": {"type": "string", "description": "Motivo do cancelamento"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Tenant cancelado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def cancel_tenant(tenant_id):
    """Cancela tenant (super admin)"""
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        result = tenant_service.cancel_tenant(
            tenant_id=tenant_id,
            reason=data.get("reason"),
            cancelled_by=current_user_id
        )
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao cancelar tenant: {e}")
        return jsonify({"error": f"Erro ao cancelar tenant: {str(e)}"}), 500

@super_admin_bp.route("/tenants/<tenant_id>/usage", methods=["PUT"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Tenants"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "tenant_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do tenant"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "UpdateTenantUsage",
                "properties": {
                    "leads_count": {"type": "integer", "description": "Número de leads usados"},
                    "users_count": {"type": "integer", "description": "Número de usuários usados"},
                    "storage_gb": {"type": "number", "format": "float", "description": "Armazenamento usado em GB"},
                    "email_sent_count": {"type": "integer", "description": "Número de emails enviados"},
                    "api_calls_count": {"type": "integer", "description": "Número de chamadas de API"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Métricas de uso do tenant atualizadas com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def update_tenant_usage(tenant_id):
    """Atualiza métricas de uso do tenant (super admin)"""
    data = request.get_json()
    
    try:
        result = tenant_service.update_usage_metrics(tenant_id, data)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao atualizar uso: {e}")
        return jsonify({"error": f"Erro ao atualizar uso: {str(e)}"}), 500

@super_admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@require_super_admin
@swag_from({
    "tags": ["Super Admin - Dashboard"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Dashboard do super admin com métricas globais"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"}
    }
})
def super_admin_dashboard():
    """Dashboard do super admin com métricas globais"""
    try:
        # Estatísticas gerais
        total_tenants = Tenant.query.count()
        active_tenants = Tenant.query.filter_by(status=TenantStatus.ACTIVE).count()
        trial_tenants = Tenant.query.filter_by(status=TenantStatus.TRIAL).count()
        suspended_tenants = Tenant.query.filter_by(status=TenantStatus.SUSPENDED).count()
        
        # Tenants por plano
        tenants_by_plan = {}
        for plan in SubscriptionPlan:
            count = Tenant.query.filter_by(subscription_plan=plan).count()
            tenants_by_plan[plan.value] = count
        
        # Tenants criados nos últimos 30 dias
        thirty_days_ago = date.today() - timedelta(days=30)
        new_tenants_30d = Tenant.query.filter(
            Tenant.created_at >= thirty_days_ago
        ).count()
        
        # Receita estimada mensal
        from sqlalchemy import func
        monthly_revenue = Tenant.query.filter(
            Tenant.status.in_([TenantStatus.ACTIVE, TenantStatus.TRIAL])
        ).with_entities(
            func.sum(Tenant.monthly_value)
        ).scalar() or 0
        
        # Tenants próximos do vencimento (próximos 7 dias)
        seven_days_ahead = date.today() + timedelta(days=7)
        expiring_soon = Tenant.query.filter(
            Tenant.subscription_end_date <= seven_days_ahead,
            Tenant.subscription_end_date >= date.today(),
            Tenant.status == TenantStatus.ACTIVE
        ).count()
        
        # Últimos tenants criados
        recent_tenants = Tenant.query.order_by(
            Tenant.created_at.desc()
        ).limit(10).all()
        
        dashboard_data = {
            "summary": {
                "total_tenants": total_tenants,
                "active_tenants": active_tenants,
                "trial_tenants": trial_tenants,
                "suspended_tenants": suspended_tenants,
                "new_tenants_30d": new_tenants_30d,
                "monthly_revenue": float(monthly_revenue),
                "expiring_soon": expiring_soon
            },
            "tenants_by_plan": tenants_by_plan,
            "recent_tenants": [tenant.to_dict() for tenant in recent_tenants]
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Erro no dashboard super admin: {e}")
        return jsonify({"error": f"Erro no dashboard: {str(e)}"}), 500

# ==================== TENANT ADMIN ROUTES ====================

def require_tenant_admin(f):
    """Decorador que exige admin do tenant"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role not in ["admin", "super_admin"]:
            return jsonify({"error": "Acesso negado. Apenas admins."}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

@tenant_admin_bp.route("/tenant/info", methods=["GET"])
@jwt_required()
@require_tenant
@swag_from({
    "tags": ["Tenant Admin - Gerenciamento"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Informações do tenant atual"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def get_tenant_info():
    """Obtém informações do tenant atual"""
    try:
        tenant = get_current_tenant()
        
        # Incluir analytics básicas
        analytics = tenant_service.get_tenant_analytics(tenant.id, days=30)
        
        return jsonify({
            "tenant": tenant.to_dict(),
            "analytics": analytics
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter info do tenant: {e}")
        return jsonify({"error": f"Erro ao obter informações: {str(e)}"}), 500

@tenant_admin_bp.route("/tenant/settings", methods=["PUT"])
@jwt_required()
@require_tenant
@require_tenant_admin
@swag_from({
    "tags": ["Tenant Admin - Gerenciamento"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TenantSettingsUpdate",
                "properties": {
                    "name": {"type": "string", "description": "Nome do tenant"},
                    "phone": {"type": "string", "description": "Telefone do tenant"},
                    "cnpj": {"type": "string", "description": "CNPJ do tenant"},
                    "address": {"type": "string", "description": "Endereço do tenant"},
                    "logo_url": {"type": "string", "description": "URL do logo do tenant"},
                    "custom_css": {"type": "string", "description": "CSS customizado para o tenant"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Configurações do tenant atualizadas com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def update_tenant_settings():
    """Atualiza configurações do tenant"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    tenant = get_current_tenant()
    
    try:
        result = tenant_service.update_tenant(tenant.id, data, updated_by=current_user_id)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao atualizar configurações: {e}")
        return jsonify({"error": f"Erro ao atualizar configurações: {str(e)}"}), 500

@tenant_admin_bp.route("/tenant/usage", methods=["GET"])
@jwt_required()
@require_tenant
@swag_from({
    "tags": ["Tenant Admin - Gerenciamento"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Uso atual do tenant"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def get_tenant_usage():
    """Obtém uso atual do tenant"""
    try:
        tenant = get_current_tenant()
        usage_limits = tenant.check_usage_limits()
        
        return jsonify({
            "usage_limits": usage_limits,
            "subscription_info": {
                "plan": tenant.subscription_plan.value,
                "status": tenant.status.value,
                "trial_days_remaining": tenant.trial_days_remaining,
                "subscription_days_remaining": tenant.subscription_days_remaining
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter uso: {e}")
        return jsonify({"error": f"Erro ao obter uso: {str(e)}"}), 500

@tenant_admin_bp.route("/tenant/invitations", methods=["GET"])
@jwt_required()
@require_tenant
@require_tenant_admin
@swag_from({
    "tags": ["Tenant Admin - Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de convites do tenant"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def list_tenant_invitations():
    """Lista convites do tenant"""
    try:
        tenant = get_current_tenant()
        
        invitations = TenantInvitation.query.filter_by(
            tenant_id=tenant.id
        ).order_by(TenantInvitation.created_at.desc()).all()
        
        return jsonify({
            "invitations": [invitation.to_dict() for invitation in invitations]
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar convites: {e}")
        return jsonify({"error": f"Erro ao listar convites: {str(e)}"}), 500

@tenant_admin_bp.route("/tenant/invitations", methods=["POST"])
@jwt_required()
@require_tenant
@require_tenant_admin
@swag_from({
    "tags": ["Tenant Admin - Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "TenantInvitationCreate",
                "required": ["email", "role"],
                "properties": {
                    "email": {"type": "string", "format": "email", "description": "Email do usuário a ser convidado (padrão: @jttelecom.com.br)", "pattern": ".*@jttelecom\\.com\\.br$"},
                    "role": {"type": "string", "description": "Papel do usuário (e.g., SDR, CLOSER, SUPPORT)"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Convite criado com sucesso"},
        "400": {"description": "Dados inválidos"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"}
    }
})
def create_tenant_invitation():
    """Cria convite para usuário"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    tenant = get_current_tenant()
    
    required_fields = ["email", "role"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    # Validar domínio do email
    if not data["email"].endswith("@jttelecom.com.br"):
        return jsonify({"error": "O email deve ter o domínio @jttelecom.com.br"}), 400

    try:
        result = tenant_service.create_invitation(
            tenant_id=tenant.id,
            email=data["email"],
            role=data["role"],
            invited_by=current_user_id
        )
        
        if result.get("success"):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro ao criar convite: {e}")
        return jsonify({"error": f"Erro ao criar convite: {str(e)}"}), 500

@tenant_admin_bp.route("/tenant/users", methods=["GET"])
@jwt_required()
@require_tenant
@require_tenant_admin
@swag_from({
    "tags": ["Tenant Admin - Usuários"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de usuários do tenant"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def list_tenant_users():
    """Lista usuários do tenant"""
    try:
        tenant = get_current_tenant()
        
        users = User.query.filter_by(
            tenant_id=tenant.id,
            is_active=True
        ).order_by(User.created_at.desc()).all()
        
        return jsonify({
            "users": [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        return jsonify({"error": f"Erro ao listar usuários: {str(e)}"}), 500

@tenant_admin_bp.route("/tenant/billing", methods=["GET"])
@jwt_required()
@require_tenant
@require_tenant_admin
@swag_from({
    "tags": ["Tenant Admin - Gerenciamento"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Informações de cobrança do tenant"},
        "401": {"description": "Não autorizado"},
        "403": {"description": "Acesso negado"},
        "404": {"description": "Tenant não encontrado"}
    }
})
def get_tenant_billing():
    """Obtém informações de cobrança do tenant"""
    try:
        tenant = get_current_tenant()
        
        # Buscar histórico de assinaturas
        subscriptions = TenantSubscription.query.filter_by(
            tenant_id=tenant.id
        ).order_by(TenantSubscription.start_date.desc()).all()
        
        return jsonify({
            "current_plan": tenant.subscription_plan.value,
            "status": tenant.status.value,
            "monthly_value": float(tenant.monthly_value),
            "trial_end_date": tenant.trial_end_date.isoformat() if tenant.trial_end_date else None,
            "subscription_end_date": tenant.subscription_end_date.isoformat() if tenant.subscription_end_date else None,
            "subscriptions_history": [sub.to_dict() for sub in subscriptions]
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter informações de cobrança: {e}")
        return jsonify({"error": f"Erro ao obter informações de cobrança: {str(e)}"}), 500


