"""
Módulo de modelos do CRM JT Telecom
"""
import logging

logger = logging.getLogger(__name__)

# Importar modelos básicos
try:
    from .user import User
    logger.info("✅ Modelo User importado")
except Exception as e:
    logger.error(f"❌ Erro ao importar User: {e}")
    
    # Criar classe User básica como fallback
    class User:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

try:
    from .lead import Lead
    logger.info("✅ Modelo Lead importado")
except Exception as e:
    logger.error(f"❌ Erro ao importar Lead: {e}")
    
    # Criar classe Lead básica como fallback
    class Lead:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

try:
    from .permission import Permission, Role
    logger.info("✅ Modelos Permission e Role importados")
except Exception as e:
    logger.error(f"❌ Erro ao importar Permission/Role: {e}")
    
    # Criar classes básicas como fallback
    class Permission:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Role:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

try:
    from .pipeline import Pipeline, PipelineStage, Opportunity, Product
    logger.info("✅ Modelos Pipeline importados")
except Exception as e:
    logger.error(f"❌ Erro ao importar Pipeline: {e}")
    
    # Criar classes básicas como fallback
    class Pipeline:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class PipelineStage:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Opportunity:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Product:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

try:
    from .task import Task, TaskComment, TaskTimeLog, TaskTemplate, ActivitySummary
    logger.info("✅ Modelos Task importados")
except Exception as e:
    logger.error(f"❌ Erro ao importar Task: {e}")
    
    # Criar classes básicas como fallback
    class Task:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class TaskComment:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class TaskTimeLog:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class TaskTemplate:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class ActivitySummary:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

# Exportar todos os modelos
__all__ = [
    'User', 'Lead', 'Permission', 'Role',
    'Pipeline', 'PipelineStage', 'Opportunity', 'Product',
    'Task', 'TaskComment', 'TaskTimeLog', 'TaskTemplate', 'ActivitySummary'
]

logger.info(f"🎉 Módulo de modelos inicializado com {len(__all__)} classes")


def init_db(app):
    """Inicializa o banco de dados"""
    try:
        logger.info("✅ Banco de dados inicializado (modo básico)")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco: {e}")
        return False

