from flask_sqlalchemy import SQLAlchemy

# Instância única do SQLAlchemy
db = SQLAlchemy()

# Importar todos os modelos para garantir que sejam registrados
from .user import User
from .tenant import Tenant

__all__ = ['db', 'User', 'Tenant']

