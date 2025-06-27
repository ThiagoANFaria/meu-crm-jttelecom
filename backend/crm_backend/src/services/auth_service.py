"""
Serviço de autenticação do CRM
"""

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from src.models.user import User

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        """Autentica um usuário"""
        try:
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password_hash, password):
                access_token = create_access_token(identity=user.id)
                return {
                    'success': True,
                    'access_token': access_token,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    }
                }
            
            return {'success': False, 'message': 'Credenciais inválidas'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro interno: {str(e)}'}

