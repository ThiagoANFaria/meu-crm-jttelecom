#!/usr/bin/env python3
import sys
import os

print("🧪 Testando importações...")

try:
    from routes.leads import leads_bp
    print("✅ leads_bp importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar leads_bp: {e}")

try:
    from routes.auth import auth_bp
    print("✅ auth_bp importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar auth_bp: {e}")

try:
    from routes.dashboard import dashboard_bp
    print("✅ dashboard_bp importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar dashboard_bp: {e}")

try:
    from services.auth_service import AuthService
    print("✅ AuthService importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar AuthService: {e}")

try:
    from services.email_service import EmailService
    print("✅ EmailService importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar EmailService: {e}")

try:
    from services.automation_service import AutomationService
    print("✅ AutomationService importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar AutomationService: {e}")

print("🎉 Teste de importações concluído!")
