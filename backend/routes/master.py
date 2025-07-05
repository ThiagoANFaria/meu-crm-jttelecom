from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime
import secrets
import string

# Importar modelos
try:
    from ..models import db, User, Tenant
except ImportError:
    # Fallback para desenvolvimento
    class User:
        pass
    class Tenant:
        pass
    class db:
        @staticmethod
        def session():
            pass

master_bp = Blueprint('master', __name__, url_prefix='/master')

def require_master():
    """Decorator para verificar se o usuário é Admin Master"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                user = User.query.get(current_user_id)
                if not user or not user.is_master():
                    return jsonify({'error': 'Acesso negado. Apenas Admin Master pode acessar.'}), 403
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Erro de autenticação'}), 401
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@master_bp.route('/tenants', methods=['GET'])
@jwt_required()
@require_master()
def list_tenants():
    """Listar todas as tenants"""
    try:
        tenants = Tenant.query.all()
        return jsonify({
            'tenants': [tenant.to_dict() for tenant in tenants],
            'total': len(tenants)
        }), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar tenants: {str(e)}'}), 500

@master_bp.route('/tenants', methods=['POST'])
@jwt_required()
@require_master()
def create_tenant():
    """Criar nova tenant com admin"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['tenant_name', 'domain', 'admin_name', 'admin_email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Verificar se domain já existe
        existing_tenant = Tenant.query.filter_by(domain=data['domain']).first()
        if existing_tenant:
            return jsonify({'error': 'Domain já existe'}), 400
        
        # Verificar se admin_email já existe
        existing_user = User.query.filter_by(email=data['admin_email']).first()
        if existing_user:
            return jsonify({'error': 'Email do admin já existe'}), 400
        
        # Gerar senha temporária para o admin
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        # Criar tenant
        tenant = Tenant(
            name=data['tenant_name'],
            domain=data['domain'],
            admin_email=data['admin_email'],
            admin_name=data['admin_name']
        )
        db.session.add(tenant)
        db.session.flush()  # Para obter o ID da tenant
        
        # Criar admin da tenant
        admin_user = User(
            name=data['admin_name'],
            email=data['admin_email'],
            tenant_id=tenant.id,
            user_level='admin',
            status='active'
        )
        admin_user.set_password(temp_password)
        db.session.add(admin_user)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tenant criada com sucesso',
            'tenant': tenant.to_dict(),
            'admin_credentials': {
                'email': data['admin_email'],
                'temporary_password': temp_password,
                'note': 'Senha temporária - deve ser alterada no primeiro login'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar tenant: {str(e)}'}), 500

@master_bp.route('/tenants/<int:tenant_id>', methods=['GET'])
@jwt_required()
@require_master()
def get_tenant(tenant_id):
    """Obter detalhes de uma tenant específica"""
    try:
        tenant = Tenant.query.get_or_404(tenant_id)
        
        # Obter usuários da tenant
        users = User.query.filter_by(tenant_id=tenant_id).all()
        
        tenant_data = tenant.to_dict()
        tenant_data['users'] = [user.to_dict() for user in users]
        
        return jsonify(tenant_data), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao obter tenant: {str(e)}'}), 500

@master_bp.route('/tenants/<int:tenant_id>', methods=['PUT'])
@jwt_required()
@require_master()
def update_tenant(tenant_id):
    """Atualizar tenant"""
    try:
        tenant = Tenant.query.get_or_404(tenant_id)
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'name' in data:
            tenant.name = data['name']
        if 'status' in data:
            tenant.status = data['status']
        if 'admin_name' in data:
            tenant.admin_name = data['admin_name']
        
        tenant.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Tenant atualizada com sucesso',
            'tenant': tenant.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar tenant: {str(e)}'}), 500

@master_bp.route('/tenants/<int:tenant_id>', methods=['DELETE'])
@jwt_required()
@require_master()
def delete_tenant(tenant_id):
    """Deletar tenant (soft delete)"""
    try:
        tenant = Tenant.query.get_or_404(tenant_id)
        
        # Soft delete - marcar como inativa
        tenant.status = 'inactive'
        tenant.updated_at = datetime.utcnow()
        
        # Desativar todos os usuários da tenant
        users = User.query.filter_by(tenant_id=tenant_id).all()
        for user in users:
            user.status = 'inactive'
        
        db.session.commit()
        
        return jsonify({'message': 'Tenant desativada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao deletar tenant: {str(e)}'}), 500

@master_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_master()
def get_stats():
    """Obter estatísticas gerais do sistema"""
    try:
        total_tenants = Tenant.query.count()
        active_tenants = Tenant.query.filter_by(status='active').count()
        total_users = User.query.filter(User.user_level != 'master').count()
        active_users = User.query.filter(
            User.user_level != 'master',
            User.status == 'active'
        ).count()
        
        return jsonify({
            'tenants': {
                'total': total_tenants,
                'active': active_tenants,
                'inactive': total_tenants - active_tenants
            },
            'users': {
                'total': total_users,
                'active': active_users,
                'inactive': total_users - active_users
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao obter estatísticas: {str(e)}'}), 500

@master_bp.route('/init', methods=['POST'])
def init_master():
    """Inicializar Admin Master (apenas para setup inicial)"""
    try:
        # Verificar se já existe um Admin Master
        existing_master = User.query.filter_by(user_level='master').first()
        if existing_master:
            return jsonify({'error': 'Admin Master já existe'}), 400
        
        # Criar Admin Master
        master_user = User(
            name='Admin Master JT Telecom',
            email='master@jttecnologia.com.br',
            user_level='master',
            status='active'
        )
        master_user.set_password('MasterJT2024!')
        
        db.session.add(master_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Admin Master criado com sucesso',
            'credentials': {
                'email': 'master@jttecnologia.com.br',
                'password': 'MasterJT2024!'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar Admin Master: {str(e)}'}), 500

