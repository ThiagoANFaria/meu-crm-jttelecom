#!/usr/bin/env python3
"""
Script de teste para o módulo de telefonia integrado com API JT Telecom
"""

import sys
import os
sys.path.append('/home/ubuntu/crm_jttelcom/backend/crm_backend')

import requests
import json
from datetime import datetime, timedelta

# Configurações
BASE_URL = "http://localhost:5000/api"
TEST_USER_EMAIL = "admin@jttelcom.com"
TEST_USER_PASSWORD = "Admin123!"

def get_auth_token():
    """Obtém token de autenticação"""
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Erro no login: {response.text}")
        return None

def test_telephony_endpoints():
    """Testa todos os endpoints de telefonia"""
    token = get_auth_token()
    if not token:
        print("❌ Falha na autenticação")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🔧 Testando módulo de telefonia integrado com API JT Telecom...")
    print("=" * 60)
    
    # 1. Teste de conectividade com PABX
    print("\n1. 🔗 Testando conectividade com PABX...")
    response = requests.get(f"{BASE_URL}/telephony/test-connection", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Conexão: {result.get('message', 'OK')}")
    else:
        print(f"❌ Erro: {response.text}")
    
    # 2. Listar ramais
    print("\n2. 📞 Listando ramais...")
    response = requests.get(f"{BASE_URL}/telephony/extensions?limit=5", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        extensions = response.json()
        print(f"✅ Ramais encontrados: {len(extensions.get('data', []))}")
    else:
        print(f"❌ Erro: {response.text}")
    
    # 3. Listar DIDs
    print("\n3. 🔢 Listando DIDs...")
    response = requests.get(f"{BASE_URL}/telephony/dids?limit=5", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        dids = response.json()
        print(f"✅ DIDs encontrados: {len(dids.get('data', []))}")
    else:
        print(f"❌ Erro: {response.text}")
    
    # 4. Listar chamadas online
    print("\n4. 📱 Listando chamadas online...")
    response = requests.get(f"{BASE_URL}/telephony/pabx/online-calls", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        online_calls = response.json()
        print(f"✅ Chamadas online: {len(online_calls.get('data', []))}")
    else:
        print(f"❌ Erro: {response.text}")
    
    # 5. Buscar histórico de chamadas do PABX
    print("\n5. 📋 Buscando histórico de chamadas...")
    today = datetime.now().strftime("%d/%m/%Y")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
    
    params = {
        "data_inicial": yesterday,
        "data_final": today,
        "limit": 10
    }
    response = requests.get(f"{BASE_URL}/telephony/pabx/history", headers=headers, params=params)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        history = response.json()
        print(f"✅ Histórico obtido: {len(history.get('data', []))} chamadas")
    else:
        print(f"❌ Erro: {response.text}")
    
    # 6. Listar campanhas
    print("\n6. 📢 Listando campanhas...")
    response = requests.get(f"{BASE_URL}/telephony/campaigns?limit=5", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        campaigns = response.json()
        print(f"✅ Campanhas encontradas: {len(campaigns.get('data', []))}")
    else:
        print(f"❌ Erro: {response.text}")
    
    # 7. Teste de click-to-call (simulado)
    print("\n7. ☎️ Testando click-to-call (simulado)...")
    call_data = {
        "ramal_origem": "100",
        "numero_destino": "11999999999",
        "notes": "Teste de chamada via CRM",
        "variaveis": {
            "origem": "crm_test",
            "usuario": "admin"
        }
    }
    
    # Nota: Este teste pode falhar se o módulo Click2Call não estiver contratado
    response = requests.post(f"{BASE_URL}/telephony/click-to-call", headers=headers, json=call_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Chamada iniciada: {result.get('message')}")
        call_id = result.get('call_id')
        if call_id:
            print(f"   ID da chamada no CRM: {call_id}")
    else:
        print(f"⚠️ Erro esperado (módulo Click2Call pode não estar ativo): {response.text}")
    
    # 8. Listar chamadas do CRM
    print("\n8. 📊 Listando chamadas do CRM...")
    response = requests.get(f"{BASE_URL}/telephony/calls?per_page=5", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        calls = response.json()
        print(f"✅ Chamadas no CRM: {calls.get('total', 0)}")
        for call in calls.get('calls', [])[:3]:
            print(f"   - {call['phone_number']} ({call['direction']}) - {call['status']}")
    else:
        print(f"❌ Erro: {response.text}")
    
    # 9. Estatísticas de telefonia
    print("\n9. 📈 Obtendo estatísticas...")
    response = requests.get(f"{BASE_URL}/telephony/stats?days=30", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Estatísticas dos últimos 30 dias:")
        print(f"   - Total de chamadas: {stats.get('total_calls', 0)}")
        print(f"   - Chamadas completadas: {stats.get('completed_calls', 0)}")
        print(f"   - Taxa de sucesso: {stats.get('success_rate', 0)}%")
        print(f"   - Duração média: {stats.get('average_duration_formatted', 'N/A')}")
    else:
        print(f"❌ Erro: {response.text}")
    
    print("\n" + "=" * 60)
    print("🎉 Teste do módulo de telefonia concluído!")

def test_operator_functions():
    """Testa funcionalidades de operador"""
    token = get_auth_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🧑‍💼 Testando funcionalidades de operador...")
    print("=" * 60)
    
    # Teste de login de operador (simulado)
    operador_id = "100"  # ID de exemplo
    
    print(f"\n1. 🔐 Testando login do operador {operador_id}...")
    response = requests.post(f"{BASE_URL}/telephony/operators/{operador_id}/login", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login realizado com sucesso")
    else:
        print(f"⚠️ Erro esperado: {response.text}")
    
    print(f"\n2. ⏸️ Testando pausa do operador {operador_id}...")
    pause_data = {"motivo_pausa": "Teste de pausa via CRM"}
    response = requests.post(f"{BASE_URL}/telephony/operators/{operador_id}/pause", headers=headers, json=pause_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Pausa realizada com sucesso")
    else:
        print(f"⚠️ Erro esperado: {response.text}")
    
    print(f"\n3. ▶️ Testando remoção de pausa do operador {operador_id}...")
    response = requests.post(f"{BASE_URL}/telephony/operators/{operador_id}/unpause", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Remoção de pausa realizada com sucesso")
    else:
        print(f"⚠️ Erro esperado: {response.text}")
    
    print(f"\n4. 🔓 Testando logout do operador {operador_id}...")
    response = requests.post(f"{BASE_URL}/telephony/operators/{operador_id}/logout", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Logout realizado com sucesso")
    else:
        print(f"⚠️ Erro esperado: {response.text}")

if __name__ == "__main__":
    print("🚀 Iniciando testes do módulo de telefonia JT Telecom...")
    
    try:
        test_telephony_endpoints()
        test_operator_functions()
        
        print("\n✨ Todos os testes foram executados!")
        print("\n📝 Notas importantes:")
        print("- Alguns testes podem falhar se o módulo Click2Call não estiver contratado")
        print("- As credenciais do PABX devem estar configuradas nas variáveis de ambiente")
        print("- JTTELECOM_PABX_AUTH_USER e JTTELECOM_PABX_AUTH_TOKEN")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

