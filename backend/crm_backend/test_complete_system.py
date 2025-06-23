#!/usr/bin/env python3
"""
Script de Teste Completo - CRM JT Telecom
Testa todos os módulos e funcionalidades do sistema
"""

import requests
import json
import time
import sys
from datetime import datetime, date, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CRMTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.token = None
        self.tenant_id = None
        self.user_id = None
        self.lead_id = None
        self.opportunity_id = None
        self.proposal_id = None
        self.contract_id = None
        self.task_id = None
        self.automation_id = None
        
    def make_request(self, method, endpoint, data=None, headers=None):
        """Faz requisição HTTP com tratamento de erros"""
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        headers["Content-Type"] = "application/json"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            logger.info(f"{method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code >= 400:
                logger.error(f"Erro na requisição: {response.text}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão: {e}")
            return None
    
    def test_health_check(self):
        """Testa o health check da API"""
        logger.info("=== TESTE: Health Check ===")
        
        response = self.make_request("GET", "/health")
        
        if response and response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Health check OK: {data['message']}")
            logger.info(f"Módulos disponíveis: {', '.join(data['modules'])}")
            return True
        else:
            logger.error("❌ Health check falhou")
            return False
    
    def test_authentication(self):
        """Testa autenticação e criação de usuário"""
        logger.info("=== TESTE: Autenticação ===")
        
        # Criar usuário de teste
        user_data = {
            "name": "Teste Admin",
            "email": "admin@jttelecom.com.br",
            "password": "teste123",
            "role": "admin",
            "phone": "(11) 99999-9999"
        }
        
        response = self.make_request("POST", "/api/auth/register", user_data)
        
        if response and response.status_code == 201:
            logger.info("✅ Usuário criado com sucesso")
        else:
            logger.info("ℹ️ Usuário já existe ou erro na criação")
        
        # Login
        login_data = {
            "email": "admin@jttelecom.com.br",
            "password": "teste123"
        }
        
        response = self.make_request("POST", "/api/auth/login", login_data)
        
        if response and response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.user_id = data["user"]["id"]
            logger.info("✅ Login realizado com sucesso")
            return True
        else:
            logger.error("❌ Falha no login")
            return False
    
    def test_tenant_management(self):
        """Testa gestão de tenants (multi-tenancy)"""
        logger.info("=== TESTE: Gestão de Tenants ===")
        
        # Criar tenant de teste
        tenant_data = {
            "name": "Empresa Teste Ltda",
            "slug": "empresa-teste",
            "email": "contato@jttelecom.com.br",
            "cnpj": "12.345.678/0001-90",
            "phone": "(11) 3333-4444",
            "subscription_plan": "PRO",
            "status": "ACTIVE"
        }
        
        response = self.make_request("POST", "/api/super-admin/tenants", tenant_data)
        
        if response and response.status_code == 201:
            data = response.json()
            self.tenant_id = data["tenant"]["id"]
            logger.info("✅ Tenant criado com sucesso")
            
            # Testar listagem de tenants
            response = self.make_request("GET", "/api/super-admin/tenants")
            if response and response.status_code == 200:
                logger.info("✅ Listagem de tenants OK")
            
            return True
        else:
            logger.error("❌ Falha na criação do tenant")
            return False
    
    def test_leads_module(self):
        """Testa módulo de leads"""
        logger.info("=== TESTE: Módulo de Leads ===")
        
        # Criar lead
        lead_data = {
            "name": "João Silva",
            "email": "joao.silva@jttelecom.com.br",
            "phone": "(11) 98765-4321",
            "company": "Silva & Associados",
            "cnpj": "98.765.432/0001-10",
            "source": "website",
            "product_interest": "PABX em Nuvem",
            "status": "new",
            "notes": "Lead interessado em solução completa de telefonia"
        }
        
        response = self.make_request("POST", "/api/leads", lead_data)
        
        if response and response.status_code == 201:
            data = response.json()
            self.lead_id = data["lead"]["id"]
            logger.info("✅ Lead criado com sucesso")
            
            # Testar listagem de leads
            response = self.make_request("GET", "/api/leads")
            if response and response.status_code == 200:
                logger.info("✅ Listagem de leads OK")
            
            # Testar atualização de lead
            update_data = {"status": "qualified", "score": 85}
            response = self.make_request("PUT", f"/api/leads/{self.lead_id}", update_data)
            if response and response.status_code == 200:
                logger.info("✅ Atualização de lead OK")
            
            return True
        else:
            logger.error("❌ Falha na criação do lead")
            return False
    
    def test_pipelines_module(self):
        """Testa módulo de pipelines e oportunidades"""
        logger.info("=== TESTE: Módulo de Pipelines ===")
        
        # Criar pipeline
        pipeline_data = {
            "name": "Pipeline de Vendas",
            "description": "Pipeline principal para vendas de PABX",
            "stages": [
                {"name": "Qualificação", "order": 1},
                {"name": "Proposta", "order": 2},
                {"name": "Negociação", "order": 3},
                {"name": "Fechamento", "order": 4}
            ]
        }
        
        response = self.make_request("POST", "/api/pipelines", pipeline_data)
        
        if response and response.status_code == 201:
            data = response.json()
            pipeline_id = data["pipeline"]["id"]
            logger.info("✅ Pipeline criado com sucesso")
            
            # Criar oportunidade
            opportunity_data = {
                "title": "Venda PABX - Silva & Associados",
                "lead_id": self.lead_id,
                "pipeline_id": pipeline_id,
                "value": 15000.00,
                "probability": 70,
                "expected_close_date": (date.today() + timedelta(days=30)).isoformat()
            }
            
            response = self.make_request("POST", "/api/pipelines/opportunities", opportunity_data)
            if response and response.status_code == 201:
                data = response.json()
                self.opportunity_id = data["opportunity"]["id"]
                logger.info("✅ Oportunidade criada com sucesso")
            
            return True
        else:
            logger.error("❌ Falha na criação do pipeline")
            return False
    
    def test_proposals_module(self):
        """Testa módulo de propostas"""
        logger.info("=== TESTE: Módulo de Propostas ===")
        
        # Criar template de proposta
        template_data = {
            "name": "Template PABX Básico",
            "content": "Proposta para {company}\n\nValor: R$ {value}\n\nAtenciosamente,\nEquipe JT Telecom",
            "variables": ["company", "value"],
            "is_active": True
        }
        
        response = self.make_request("POST", "/api/proposals/templates", template_data)
        
        if response and response.status_code == 201:
            data = response.json()
            template_id = data["template"]["id"]
            logger.info("✅ Template de proposta criado")
            
            # Criar proposta
            proposal_data = {
                "title": "Proposta PABX - Silva & Associados",
                "lead_id": self.lead_id,
                "opportunity_id": self.opportunity_id,
                "template_id": template_id,
                "variables": {
                    "company": "Silva & Associados",
                    "value": "R$ 15.000,00"
                },
                "valid_until": (date.today() + timedelta(days=15)).isoformat()
            }
            
            response = self.make_request("POST", "/api/proposals", proposal_data)
            if response and response.status_code == 201:
                data = response.json()
                self.proposal_id = data["proposal"]["id"]
                logger.info("✅ Proposta criada com sucesso")
            
            return True
        else:
            logger.error("❌ Falha na criação do template de proposta")
            return False
    
    def test_contracts_module(self):
        """Testa módulo de contratos"""
        logger.info("=== TESTE: Módulo de Contratos ===")
        
        # Criar template de contrato
        template_data = {
            "name": "Contrato PABX Padrão",
            "content": "CONTRATO DE PRESTAÇÃO DE SERVIÇOS\n\nContratante: {company}\nCNPJ: {cnpj}\n\nValor: R$ {value}",
            "variables": ["company", "cnpj", "value"],
            "is_active": True
        }
        
        response = self.make_request("POST", "/api/contracts/templates", template_data)
        
        if response and response.status_code == 201:
            data = response.json()
            template_id = data["template"]["id"]
            logger.info("✅ Template de contrato criado")
            
            # Criar contrato
            contract_data = {
                "title": "Contrato PABX - Silva & Associados",
                "lead_id": self.lead_id,
                "opportunity_id": self.opportunity_id,
                "proposal_id": self.proposal_id,
                "template_id": template_id,
                "variables": {
                    "company": "Silva & Associados",
                    "cnpj": "98.765.432/0001-10",
                    "value": "R$ 15.000,00"
                },
                "contract_value": 15000.00
            }
            
            response = self.make_request("POST", "/api/contracts", contract_data)
            if response and response.status_code == 201:
                data = response.json()
                self.contract_id = data["contract"]["id"]
                logger.info("✅ Contrato criado com sucesso")
            
            return True
        else:
            logger.error("❌ Falha na criação do template de contrato")
            return False
    
    def test_tasks_module(self):
        """Testa módulo de tarefas"""
        logger.info("=== TESTE: Módulo de Tarefas ===")
        
        # Criar tarefa
        task_data = {
            "title": "Ligar para João Silva",
            "description": "Follow-up da proposta enviada",
            "assigned_to": self.user_id,
            "due_date": (date.today() + timedelta(days=1)).isoformat(),
            "due_time": "14:00",
            "task_type": "CALL",
            "priority": "HIGH",
            "lead_id": self.lead_id,
            "opportunity_id": self.opportunity_id
        }
        
        response = self.make_request("POST", "/api/tasks", task_data)
        
        if response and response.status_code == 201:
            data = response.json()
            self.task_id = data["task"]["id"]
            logger.info("✅ Tarefa criada com sucesso")
            
            # Testar listagem de tarefas
            response = self.make_request("GET", "/api/tasks")
            if response and response.status_code == 200:
                logger.info("✅ Listagem de tarefas OK")
            
            # Testar conclusão de tarefa
            response = self.make_request("POST", f"/api/tasks/{self.task_id}/complete", {"notes": "Ligação realizada com sucesso"})
            if response and response.status_code == 200:
                logger.info("✅ Conclusão de tarefa OK")
            
            return True
        else:
            logger.error("❌ Falha na criação da tarefa")
            return False
    
    def test_automations_module(self):
        """Testa módulo de automações"""
        logger.info("=== TESTE: Módulo de Automações ===")
        
        # Criar automação
        automation_data = {
            "name": "Welcome Email",
            "description": "Enviar email de boas-vindas para novos leads",
            "trigger_type": "LEAD_CREATED",
            "is_active": True,
            "actions": [
                {
                    "type": "SEND_EMAIL",
                    "config": {
                        "template": "welcome_template",
                        "subject": "Bem-vindo à JT Telecom!",
                        "delay_minutes": 0
                    }
                }
            ]
        }
        
        response = self.make_request("POST", "/api/automations", automation_data)
        
        if response and response.status_code == 201:
            data = response.json()
            self.automation_id = data["automation"]["id"]
            logger.info("✅ Automação criada com sucesso")
            
            # Testar listagem de automações
            response = self.make_request("GET", "/api/automations")
            if response and response.status_code == 200:
                logger.info("✅ Listagem de automações OK")
            
            return True
        else:
            logger.error("❌ Falha na criação da automação")
            return False
    
    def test_telephony_module(self):
        """Testa módulo de telefonia"""
        logger.info("=== TESTE: Módulo de Telefonia ===")
        
        # Testar configuração de ramal
        extension_data = {
            "extension": "1001",
            "user_id": self.user_id,
            "name": "Ramal Teste",
            "is_active": True
        }
        
        response = self.make_request("POST", "/api/telephony/extensions", extension_data)
        
        if response and response.status_code == 201:
            logger.info("✅ Ramal configurado com sucesso")
            
            # Testar listagem de chamadas
            response = self.make_request("GET", "/api/telephony/calls")
            if response and response.status_code == 200:
                logger.info("✅ Listagem de chamadas OK")
            
            return True
        else:
            logger.error("❌ Falha na configuração do ramal")
            return False
    
    def test_chatbot_module(self):
        """Testa módulo de chatbot"""
        logger.info("=== TESTE: Módulo de Chatbot ===")
        
        # Criar fluxo de chatbot
        flow_data = {
            "name": "Fluxo de Qualificação",
            "description": "Fluxo para qualificar leads",
            "is_active": True,
            "steps": [
                {
                    "id": "welcome",
                    "type": "message",
                    "content": "Olá! Como posso ajudá-lo?",
                    "next_step": "ask_name"
                },
                {
                    "id": "ask_name",
                    "type": "input",
                    "content": "Qual é o seu nome?",
                    "variable": "name",
                    "next_step": "ask_company"
                }
            ]
        }
        
        response = self.make_request("POST", "/api/chatbot/flows", flow_data)
        
        if response and response.status_code == 201:
            logger.info("✅ Fluxo de chatbot criado com sucesso")
            
            # Testar listagem de conversas
            response = self.make_request("GET", "/api/chatbot/conversations")
            if response and response.status_code == 200:
                logger.info("✅ Listagem de conversas OK")
            
            return True
        else:
            logger.error("❌ Falha na criação do fluxo de chatbot")
            return False
    
    def test_dashboard_module(self):
        """Testa módulo de dashboard"""
        logger.info("=== TESTE: Módulo de Dashboard ===")
        
        # Testar overview do dashboard
        response = self.make_request("GET", "/api/dashboard/overview")
        
        if response and response.status_code == 200:
            data = response.json()
            logger.info("✅ Dashboard overview OK")
            logger.info(f"Total de leads: {data.get('leads', {}).get('total', 0)}")
            
            # Testar funil de vendas
            response = self.make_request("GET", "/api/dashboard/sales-funnel")
            if response and response.status_code == 200:
                logger.info("✅ Funil de vendas OK")
            
            # Testar KPIs
            response = self.make_request("GET", "/api/dashboard/kpis")
            if response and response.status_code == 200:
                logger.info("✅ KPIs OK")
            
            return True
        else:
            logger.error("❌ Falha no dashboard")
            return False
    
    def test_api_documentation(self):
        """Testa acesso à documentação da API"""
        logger.info("=== TESTE: Documentação da API ===")
        
        response = self.make_request("GET", "/apidocs/")
        
        if response and response.status_code == 200:
            logger.info("✅ Documentação Swagger acessível")
            return True
        else:
            logger.error("❌ Falha no acesso à documentação")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        logger.info("🚀 INICIANDO TESTES COMPLETOS DO CRM JT TELECOM")
        logger.info("=" * 60)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Autenticação", self.test_authentication),
            ("Gestão de Tenants", self.test_tenant_management),
            ("Módulo de Leads", self.test_leads_module),
            ("Módulo de Pipelines", self.test_pipelines_module),
            ("Módulo de Propostas", self.test_proposals_module),
            ("Módulo de Contratos", self.test_contracts_module),
            ("Módulo de Tarefas", self.test_tasks_module),
            ("Módulo de Automações", self.test_automations_module),
            ("Módulo de Telefonia", self.test_telephony_module),
            ("Módulo de Chatbot", self.test_chatbot_module),
            ("Módulo de Dashboard", self.test_dashboard_module),
            ("Documentação da API", self.test_api_documentation)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                time.sleep(1)  # Pausa entre testes
            except Exception as e:
                logger.error(f"❌ Erro no teste {test_name}: {e}")
                results.append((test_name, False))
        
        # Relatório final
        logger.info("=" * 60)
        logger.info("📊 RELATÓRIO FINAL DOS TESTES")
        logger.info("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_name, result in results:
            status = "✅ PASSOU" if result else "❌ FALHOU"
            logger.info(f"{test_name}: {status}")
            
            if result:
                passed += 1
            else:
                failed += 1
        
        logger.info("=" * 60)
        logger.info(f"Total de testes: {len(results)}")
        logger.info(f"✅ Passaram: {passed}")
        logger.info(f"❌ Falharam: {failed}")
        logger.info(f"📈 Taxa de sucesso: {(passed/len(results)*100):.1f}%")
        
        if failed == 0:
            logger.info("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para produção.")
        else:
            logger.warning(f"⚠️ {failed} teste(s) falharam. Revisar antes da produção.")
        
        return failed == 0

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Testes do CRM JT Telecom")
    parser.add_argument("--url", default="http://localhost:5000", help="URL base da API")
    parser.add_argument("--verbose", action="store_true", help="Modo verboso")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    tester = CRMTester(args.url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

