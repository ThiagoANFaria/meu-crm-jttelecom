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

tenant_admin_bp = Blueprint('tenant_admin', __name__, url_prefix='/tenant-admin')

def require_tenant_admin():
    """Decorator para verificar se o usuário é Admin da Tenant"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                user = User.query.get(current_user_id)
                if not user or not user.can_manage_users():
                    return jsonify({'error': 'Acesso negado. Apenas Admin pode acessar.'}), 403
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Erro de autenticação'}), 401
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@tenant_admin_bp.route('/users', methods=['GET'])
@jwt_required()
@require_tenant_admin()
def list_users():
    """Listar usuários da tenant do admin"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.is_master():
            # Admin Master pode ver todos os usuários
            users = User.query.filter(User.user_level != 'master').all()
        else:
            # Admin Tenant vê apenas usuários da sua tenant
            users = User.query.filter_by(tenant_id=current_user.tenant_id).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar usuários: {str(e)}'}), 500

@tenant_admin_bp.route('/users', methods=['POST'])
@jwt_required()
@require_tenant_admin()
def create_user():
    """Criar novo usuário na tenant"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Verificar se email já existe
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email já existe'}), 400
        
        # Gerar senha temporária
        temp_password = data.get('password') or ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        # Determinar tenant_id
        if current_user.is_master() and data.get('tenant_id'):
            tenant_id = data['tenant_id']
        else:
            tenant_id = current_user.tenant_id
        
        # Criar usuário
        new_user = User(
            name=data['name'],
            email=data['email'],
            tenant_id=tenant_id,
            user_level=data.get('user_level', 'user'),
            status='active'
        )
        new_user.set_password(temp_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': new_user.to_dict(),
            'temporary_password': temp_password if not data.get('password') else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar usuário: {str(e)}'}), 500

@tenant_admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@require_tenant_admin()
def get_user(user_id):
    """Obter detalhes de um usuário específico"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        user = User.query.get_or_404(user_id)
        
        # Verificar permissão
        if not current_user.is_master() and user.tenant_id != current_user.tenant_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao obter usuário: {str(e)}'}), 500

@tenant_admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_tenant_admin()
def update_user(user_id):
    """Atualizar usuário"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Verificar permissão
        if not current_user.is_master() and user.tenant_id != current_user.tenant_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Atualizar campos permitidos
        if 'name' in data:
            user.name = data['name']
        if 'status' in data:
            user.status = data['status']
        if 'user_level' in data and current_user.is_master():
            user.user_level = data['user_level']
        if 'password' in data:
            user.set_password(data['password'])
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar usuário: {str(e)}'}), 500

@tenant_admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_tenant_admin()
def delete_user(user_id):
    """Deletar usuário (soft delete)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        user = User.query.get_or_404(user_id)
        
        # Verificar permissão
        if not current_user.is_master() and user.tenant_id != current_user.tenant_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Não permitir deletar a si mesmo
        if user.id == current_user.id:
            return jsonify({'error': 'Não é possível deletar sua própria conta'}), 400
        
        # Soft delete
        user.status = 'inactive'
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Usuário desativado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao deletar usuário: {str(e)}'}), 500

@tenant_admin_bp.route('/tenant/info', methods=['GET'])
@jwt_required()
@require_tenant_admin()
def get_tenant_info():
    """Obter informações da tenant do admin"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.is_master():
            return jsonify({'error': 'Admin Master não possui tenant específica'}), 400
        
        tenant = Tenant.query.get(current_user.tenant_id)
        if not tenant:
            return jsonify({'error': 'Tenant não encontrada'}), 404
        
        # Estatísticas da tenant
        total_users = User.query.filter_by(tenant_id=tenant.id).count()
        active_users = User.query.filter_by(tenant_id=tenant.id, status='active').count()
        
        tenant_data = tenant.to_dict()
        tenant_data['stats'] = {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users
        }
        
        return jsonify(tenant_data), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao obter informações da tenant: {str(e)}'}), 500

@tenant_admin_bp.route('/tenant/settings', methods=['PUT'])
@jwt_required()
@require_tenant_admin()
def update_tenant_settings():
    """Atualizar configurações da tenant"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.is_master():
            return jsonify({'error': 'Admin Master não pode usar este endpoint'}), 400
        
        tenant = Tenant.query.get(current_user.tenant_id)
        if not tenant:
            return jsonify({'error': 'Tenant não encontrada'}), 404
        
        data = request.get_json()
        
        # Atualizar apenas campos permitidos para admin da tenant
        if 'name' in data:
            tenant.name = data['name']
        if 'admin_name' in data:
            tenant.admin_name = data['admin_name']
        
        tenant.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Configurações atualizadas com sucesso',
            'tenant': tenant.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar configurações: {str(e)}'}), 500

