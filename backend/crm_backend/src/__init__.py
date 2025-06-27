# src/__init__.py
"""
Módulo principal do CRM JT Tecnologia
"""

__version__ = "1.0.0"
__author__ = "JT Tecnologia"
__description__ = "Sistema CRM completo com automações, chatbot e telefonia"

# Facilitar importações
try:
    from .models import *
    print("✅ Modelos importados com sucesso em src/__init__.py")
except ImportError as e:
    print(f"⚠️  Erro ao importar modelos em src/__init__.py: {e}")

# Facilitar importações de rotas
try:
    from .routes import *
    print("✅ Rotas importadas com sucesso em src/__init__.py")
except ImportError as e:
    print(f"⚠️  Erro ao importar rotas em src/__init__.py: {e}")
