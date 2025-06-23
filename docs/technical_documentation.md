# CRM JT Telecom - Documentação Técnica Completa

## Visão Geral do Sistema

O CRM JT Telecom é uma solução SaaS multi-tenant completa, desenvolvida especificamente para empresas de telecomunicações. O sistema oferece gestão completa de leads, oportunidades, propostas, contratos, automações, tarefas e integração total com PABX em nuvem.

### Arquitetura do Sistema

O sistema foi desenvolvido com arquitetura modular e escalável, utilizando as seguintes tecnologias:

- **Backend**: Flask (Python 3.11)
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Documentação**: Swagger/OpenAPI
- **Multi-tenancy**: Isolamento por tenant_id
- **API Externa**: RESTful com documentação completa

### Características Principais

#### 🏢 **Multi-Tenancy Completo**
- Isolamento total de dados entre empresas
- Gestão centralizada pela JT Telecom
- Planos de assinatura configuráveis
- Subdomínios personalizados

#### 🔐 **Segurança Avançada**
- Autenticação JWT
- Controle de acesso baseado em roles
- Middleware de detecção de tenant
- Validação de limites por plano

#### 📊 **Módulos Completos**
- Gestão de Leads e Scoring
- Pipelines de Vendas (Kanban)
- Propostas e Contratos Dinâmicos
- Automações e Cadência
- Tarefas e Atividades
- Telefonia Integrada
- Chatbot com IA
- Dashboard e Analytics

## Estrutura do Projeto

```
crm_jttelcom/
├── backend/
│   └── crm_backend/
│       ├── src/
│       │   ├── models/          # Modelos de dados
│       │   ├── routes/          # Rotas da API
│       │   ├── services/        # Lógica de negócio
│       │   ├── middleware/      # Middleware de tenant
│       │   └── main.py         # Aplicação principal
│       ├── docs/               # Documentação
│       ├── tests/              # Testes automatizados
│       └── requirements.txt    # Dependências
└── docs/                       # Documentação geral
```

## Modelos de Dados

### Tenant (Multi-tenancy)
```python
class Tenant(db.Model):
    id = db.Column(UUID, primary_key=True)
    name = db.Column(String(255), nullable=False)
    slug = db.Column(String(100), unique=True)
    email = db.Column(String(255))
    cnpj = db.Column(String(18))
    subscription_plan = db.Column(Enum(SubscriptionPlan))
    status = db.Column(Enum(TenantStatus))
    # ... outros campos
```

### User (Usuários)
```python
class User(db.Model):
    id = db.Column(UUID, primary_key=True)
    tenant_id = db.Column(UUID, ForeignKey('tenant.id'))
    name = db.Column(String(255), nullable=False)
    email = db.Column(String(255), unique=True)
    role = db.Column(Enum(UserRole))
    # ... outros campos
```

### Lead (Leads)
```python
class Lead(db.Model):
    id = db.Column(UUID, primary_key=True)
    tenant_id = db.Column(UUID, ForeignKey('tenant.id'))
    name = db.Column(String(255), nullable=False)
    email = db.Column(String(255))
    company = db.Column(String(255))
    cnpj = db.Column(String(18))
    score = db.Column(Integer, default=0)
    # ... outros campos
```

## API Endpoints

### Autenticação
- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Renovar token

### Leads
- `GET /api/leads` - Listar leads
- `POST /api/leads` - Criar lead
- `GET /api/leads/{id}` - Obter lead
- `PUT /api/leads/{id}` - Atualizar lead
- `DELETE /api/leads/{id}` - Remover lead

### Pipelines
- `GET /api/pipelines` - Listar pipelines
- `POST /api/pipelines` - Criar pipeline
- `GET /api/pipelines/opportunities` - Listar oportunidades
- `POST /api/pipelines/opportunities` - Criar oportunidade

### Propostas
- `GET /api/proposals` - Listar propostas
- `POST /api/proposals` - Criar proposta
- `GET /api/proposals/templates` - Listar templates
- `POST /api/proposals/templates` - Criar template

### Contratos
- `GET /api/contracts` - Listar contratos
- `POST /api/contracts` - Criar contrato
- `POST /api/contracts/{id}/send` - Enviar contrato
- `POST /api/contracts/{id}/sign` - Assinar contrato

### Tarefas
- `GET /api/tasks` - Listar tarefas
- `POST /api/tasks` - Criar tarefa
- `POST /api/tasks/{id}/complete` - Completar tarefa
- `POST /api/tasks/{id}/reschedule` - Reagendar tarefa

### Automações
- `GET /api/automations` - Listar automações
- `POST /api/automations` - Criar automação
- `POST /api/automations/{id}/execute` - Executar automação

### Telefonia
- `GET /api/telephony/calls` - Listar chamadas
- `POST /api/telephony/call` - Fazer chamada
- `GET /api/telephony/extensions` - Listar ramais
- `POST /api/telephony/extensions` - Criar ramal

### Chatbot
- `GET /api/chatbot/flows` - Listar fluxos
- `POST /api/chatbot/flows` - Criar fluxo
- `GET /api/chatbot/conversations` - Listar conversas
- `POST /api/chatbot/message` - Enviar mensagem

### Dashboard
- `GET /api/dashboard/overview` - Visão geral
- `GET /api/dashboard/sales-funnel` - Funil de vendas
- `GET /api/dashboard/kpis` - KPIs
- `GET /api/dashboard/team-performance` - Performance da equipe

### Gestão de Tenants (Super Admin)
- `GET /api/super-admin/tenants` - Listar todos os tenants
- `POST /api/super-admin/tenants` - Criar tenant
- `PUT /api/super-admin/tenants/{id}` - Atualizar tenant
- `POST /api/super-admin/tenants/{id}/suspend` - Suspender tenant

## Configuração e Instalação

### Pré-requisitos
- Python 3.11+
- PostgreSQL 12+
- Redis (para cache e sessões)

### Instalação

1. **Clone o repositório**
```bash
git clone <repository-url>
cd crm_jttelcom/backend/crm_backend
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure banco de dados**
```bash
# Criar banco PostgreSQL
createdb crm_jttelcom

# Configurar variáveis de ambiente
export DATABASE_URL="postgresql://user:password@localhost/crm_jttelcom"
export JWT_SECRET_KEY="your-secret-key"
```

5. **Execute migrações**
```bash
python src/main.py
```

### Configuração de Produção

#### Variáveis de Ambiente
```bash
# Banco de dados
DATABASE_URL=postgresql://user:password@host:port/database

# JWT
JWT_SECRET_KEY=your-super-secret-key
JWT_ACCESS_TOKEN_EXPIRES=24  # horas

# Email (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@jttelecom.com.br
SMTP_PASSWORD=your-password

# Telefonia (JT Telecom API)
JT_TELECOM_API_URL=https://emnuvem.meupabxip.com.br/suite/api
JT_TELECOM_API_KEY=your-api-key

# FlyERP Integration
FLYERP_API_URL=https://api.flyerp.com.br
FLYERP_API_KEY=your-flyerp-key

# D4Sign Integration
D4SIGN_API_URL=https://secure.d4sign.com.br/api/v1
D4SIGN_API_KEY=your-d4sign-key
```

## Testes

### Executar Testes Completos
```bash
# Testes automatizados
python test_complete_system.py

# Testes específicos
python test_complete_system.py --url http://localhost:5000 --verbose
```

### Testes Manuais
1. Acesse `http://localhost:5000/health` para verificar status
2. Acesse `http://localhost:5000/apidocs/` para documentação Swagger
3. Use Postman ou similar para testar endpoints

## Integração com Serviços Externos

### JT Telecom PABX API
```python
# Configuração da API
JT_TELECOM_CONFIG = {
    "base_url": "https://emnuvem.meupabxip.com.br/suite/api",
    "api_key": "your-api-key",
    "endpoints": {
        "calls": "/calls",
        "extensions": "/extensions",
        "dial": "/dial"
    }
}
```

### FlyERP Integration
```python
# Sincronização automática de contratos
def sync_contract_to_flyerp(contract_id):
    contract = Contract.query.get(contract_id)
    flyerp_service = FlyERPService()
    
    # Criar cliente no ERP
    customer_data = {
        "name": contract.lead.company,
        "cnpj": contract.lead.cnpj,
        "email": contract.lead.email
    }
    
    flyerp_service.create_customer(customer_data)
    
    # Criar contrato no ERP
    contract_data = {
        "customer_id": customer_id,
        "value": contract.contract_value,
        "start_date": contract.start_date
    }
    
    flyerp_service.create_contract(contract_data)
```

### D4Sign Integration
```python
# Envio automático para assinatura
def send_contract_for_signature(contract_id):
    contract = Contract.query.get(contract_id)
    d4sign_service = D4SignService()
    
    # Upload do documento
    document_id = d4sign_service.upload_document(
        contract.generated_content,
        f"contrato_{contract.id}.pdf"
    )
    
    # Adicionar signatários
    d4sign_service.add_signer(
        document_id,
        contract.lead.email,
        contract.lead.name
    )
    
    # Enviar para assinatura
    d4sign_service.send_for_signature(document_id)
```

## Monitoramento e Logs

### Configuração de Logs
```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crm.log'),
        logging.StreamHandler()
    ]
)
```

### Métricas de Performance
- Tempo de resposta das APIs
- Uso de recursos por tenant
- Taxa de conversão por funil
- Performance das automações

## Segurança

### Autenticação e Autorização
- JWT tokens com expiração configurável
- Refresh tokens para renovação automática
- Controle de acesso baseado em roles (RBAC)
- Middleware de validação de tenant

### Proteção de Dados
- Isolamento completo entre tenants
- Criptografia de dados sensíveis
- Logs de auditoria
- Backup automático

### Validação de Entrada
- Sanitização de dados de entrada
- Validação de tipos e formatos
- Proteção contra SQL injection
- Rate limiting por tenant

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  crm-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/crm
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: crm
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

volumes:
  postgres_data:
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crm-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crm-api
  template:
    metadata:
      labels:
        app: crm-api
    spec:
      containers:
      - name: crm-api
        image: jttelecom/crm-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: crm-secrets
              key: database-url
```

## Manutenção e Suporte

### Backup e Recuperação
```bash
# Backup do banco de dados
pg_dump crm_jttelcom > backup_$(date +%Y%m%d).sql

# Restauração
psql crm_jttelcom < backup_20240623.sql
```

### Monitoramento de Saúde
```python
@app.route('/health')
def health_check():
    checks = {
        'database': check_database_connection(),
        'redis': check_redis_connection(),
        'external_apis': check_external_apis()
    }
    
    status = 'healthy' if all(checks.values()) else 'unhealthy'
    
    return jsonify({
        'status': status,
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    })
```

### Atualizações e Migrações
```python
# Script de migração
def migrate_database():
    # Backup antes da migração
    create_backup()
    
    # Executar migrações
    db.create_all()
    
    # Verificar integridade
    verify_data_integrity()
```

## Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com Banco
```bash
# Verificar status do PostgreSQL
sudo systemctl status postgresql

# Verificar logs
tail -f /var/log/postgresql/postgresql-13-main.log
```

#### 2. Problemas de Autenticação
```python
# Verificar token JWT
import jwt
token = "your-token-here"
decoded = jwt.decode(token, verify=False)
print(decoded)
```

#### 3. Problemas de Multi-tenancy
```python
# Verificar tenant atual
from flask import g
print(f"Current tenant: {g.current_tenant}")
```

### Logs de Debug
```bash
# Ativar modo debug
export FLASK_DEBUG=1
export LOG_LEVEL=DEBUG

# Visualizar logs em tempo real
tail -f crm.log | grep ERROR
```

## Roadmap e Melhorias Futuras

### Versão 2.0
- [ ] Interface web completa (React)
- [ ] Aplicativo mobile (React Native)
- [ ] Integração com WhatsApp Business
- [ ] BI e relatórios avançados
- [ ] Machine Learning para scoring

### Versão 2.1
- [ ] Integração com redes sociais
- [ ] Campanhas de marketing automatizadas
- [ ] Gestão de inventário
- [ ] Portal do cliente

### Versão 2.2
- [ ] Inteligência artificial avançada
- [ ] Análise preditiva
- [ ] Automação de processos (RPA)
- [ ] Integração com ERPs adicionais

## Suporte e Contato

### Equipe de Desenvolvimento
- **Email**: dev@jttelecom.com.br
- **Suporte**: suporte@jttelecom.com.br
- **Documentação**: https://docs.app.jttecnologia.com.br
- **API**: https://www.api.app.jttecnologia.com.br

### Recursos Adicionais
- [Documentação da API](https://www.api.app.jttecnologia.com.br/apidocs/)
- [Guia de Integração](https://docs.app.jttecnologia.com.br/integration)
- [FAQ](https://docs.app.jttecnologia.com.br/faq)
- [Status do Sistema](https://status.app.jttecnologia.com.br)

---

**Desenvolvido por JT Telecom - Soluções em Telecomunicações**

