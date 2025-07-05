# Guia de Instalação e Configuração - CRM JT Telecom

## Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Instalação Local](#instalação-local)
3. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
4. [Configuração de Variáveis de Ambiente](#configuração-de-variáveis-de-ambiente)
5. [Configuração de Integrações](#configuração-de-integrações)
6. [Primeiro Acesso](#primeiro-acesso)
7. [Configuração de Produção](#configuração-de-produção)
8. [Troubleshooting](#troubleshooting)

## Pré-requisitos

### Sistema Operacional
- Ubuntu 20.04+ (recomendado)
- CentOS 8+ 
- Windows 10+ (com WSL2)
- macOS 10.15+

### Software Necessário
- **Python 3.11+**
- **PostgreSQL 12+**
- **Redis 6+** (opcional, para cache)
- **Git**
- **Node.js 16+** (para ferramentas de build)

### Hardware Mínimo
- **CPU**: 2 cores
- **RAM**: 4GB
- **Disco**: 20GB SSD
- **Rede**: 100Mbps

### Hardware Recomendado (Produção)
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Disco**: 100GB+ SSD
- **Rede**: 1Gbps

## Instalação Local

### 1. Preparação do Ambiente

#### Ubuntu/Debian
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib redis-server git curl

# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### CentOS/RHEL
```bash
# Instalar EPEL
sudo dnf install -y epel-release

# Instalar dependências
sudo dnf install -y python3.11 python3-pip postgresql postgresql-server redis git curl nodejs npm

# Inicializar PostgreSQL
sudo postgresql-setup --initdb
sudo systemctl enable postgresql redis
sudo systemctl start postgresql redis
```

#### macOS
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependências
brew install python@3.11 postgresql redis git node
brew services start postgresql
brew services start redis
```

### 2. Clone do Repositório

```bash
# Clone o repositório
git clone https://github.com/jttelecom/crm-jttelcom.git
cd crm-jttelcom/backend/crm_backend

# Verificar estrutura
ls -la
```

### 3. Configuração do Ambiente Python

```bash
# Criar ambiente virtual
python3.11 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

## Configuração do Banco de Dados

### 1. PostgreSQL Setup

#### Criar Usuário e Banco
```bash
# Conectar como postgres
sudo -u postgres psql

# Criar usuário
CREATE USER crm_user WITH PASSWORD 'crm_password_secure_2024';

# Criar banco de dados
CREATE DATABASE crm_jttelcom OWNER crm_user;

# Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE crm_jttelcom TO crm_user;

# Sair do psql
\q
```

#### Configurar Acesso
```bash
# Editar pg_hba.conf
sudo nano /etc/postgresql/13/main/pg_hba.conf

# Adicionar linha (substitua 13 pela sua versão)
local   crm_jttelcom    crm_user                                md5

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### 2. Testar Conexão
```bash
# Testar conexão
psql -h localhost -U crm_user -d crm_jttelcom

# Se conectar com sucesso, sair
\q
```

## Configuração de Variáveis de Ambiente

### 1. Arquivo .env
```bash
# Criar arquivo de configuração
cp .env.example .env
nano .env
```

### 2. Configurações Essenciais
```bash
# .env
# ===========================================
# CONFIGURAÇÕES BÁSICAS
# ===========================================

# Ambiente
FLASK_ENV=development
FLASK_DEBUG=True

# Banco de Dados
DATABASE_URL=postgresql://crm_user:crm_password_secure_2024@localhost:5432/crm_jttelcom

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-2024
JWT_ACCESS_TOKEN_EXPIRES=24

# ===========================================
# CONFIGURAÇÕES DE EMAIL
# ===========================================

# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=sistema@jttelecom.com.br
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=True

# Email padrões
DEFAULT_FROM_EMAIL=sistema@jttelecom.com.br
ADMIN_EMAIL=admin@jttelecom.com.br
SUPPORT_EMAIL=suporte@jttelecom.com.br

# ===========================================
# INTEGRAÇÕES EXTERNAS
# ===========================================

# JT Telecom PABX API
JT_TELECOM_API_URL=https://emnuvem.meupabxip.com.br/suite/api
JT_TELECOM_API_KEY=your-jt-telecom-api-key
JT_TELECOM_API_SECRET=your-jt-telecom-api-secret

# FlyERP Integration
FLYERP_API_URL=https://api.flyerp.com.br
FLYERP_API_KEY=your-flyerp-api-key
FLYERP_API_SECRET=your-flyerp-api-secret

# D4Sign Integration
D4SIGN_API_URL=https://secure.d4sign.com.br/api/v1
D4SIGN_API_KEY=your-d4sign-api-key
D4SIGN_CRYPTO_KEY=your-d4sign-crypto-key

# ===========================================
# CONFIGURAÇÕES DE DOMÍNIO
# ===========================================

# Domínios
FRONTEND_URL=https://www.app.jttecnologia.com.br
API_URL=https://www.api.app.jttecnologia.com.br
DOCS_URL=https://docs.app.jttecnologia.com.br

# ===========================================
# CONFIGURAÇÕES DE CACHE E SESSÃO
# ===========================================

# Redis (opcional)
REDIS_URL=redis://localhost:6379/0

# ===========================================
# CONFIGURAÇÕES DE UPLOAD
# ===========================================

# Upload de arquivos
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
ALLOWED_EXTENSIONS=pdf,doc,docx,jpg,jpeg,png,gif

# ===========================================
# CONFIGURAÇÕES DE LOG
# ===========================================

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/crm.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5

# ===========================================
# CONFIGURAÇÕES DE SEGURANÇA
# ===========================================

# CORS
CORS_ORIGINS=https://www.app.jttecnologia.com.br,http://localhost:3000

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_DEFAULT=100 per hour

# ===========================================
# CONFIGURAÇÕES ESPECÍFICAS DO TENANT
# ===========================================

# Limites padrão por plano
TRIAL_USERS_LIMIT=2
TRIAL_LEADS_LIMIT=100
TRIAL_STORAGE_LIMIT=1  # GB

BASIC_USERS_LIMIT=5
BASIC_LEADS_LIMIT=1000
BASIC_STORAGE_LIMIT=5  # GB

PRO_USERS_LIMIT=15
PRO_LEADS_LIMIT=5000
PRO_STORAGE_LIMIT=20  # GB

ENTERPRISE_USERS_LIMIT=50
ENTERPRISE_LEADS_LIMIT=20000
ENTERPRISE_STORAGE_LIMIT=100  # GB
```

### 3. Configurações de Produção
```bash
# .env.production
FLASK_ENV=production
FLASK_DEBUG=False

# Usar senhas seguras
JWT_SECRET_KEY=$(openssl rand -base64 32)
DATABASE_URL=postgresql://crm_user:$(openssl rand -base64 32)@db-server:5432/crm_jttelcom

# SSL/TLS
SSL_CERT_PATH=/etc/ssl/certs/jttecnologia.crt
SSL_KEY_PATH=/etc/ssl/private/jttecnologia.key

# Monitoring
SENTRY_DSN=your-sentry-dsn
NEW_RELIC_LICENSE_KEY=your-newrelic-key
```

## Configuração de Integrações

### 1. JT Telecom PABX API

#### Obter Credenciais
1. Acesse o painel administrativo do PABX
2. Vá em **Configurações > API**
3. Gere uma nova chave de API
4. Anote a chave e o secret

#### Configurar no Sistema
```bash
# Adicionar ao .env
JT_TELECOM_API_KEY=sua-chave-aqui
JT_TELECOM_API_SECRET=seu-secret-aqui
```

#### Testar Integração
```bash
# Executar teste de telefonia
python test_telephony_integration.py
```

### 2. FlyERP Integration

#### Configuração
```bash
# Obter credenciais do FlyERP
# Adicionar ao .env
FLYERP_API_KEY=sua-chave-flyerp
FLYERP_API_SECRET=seu-secret-flyerp
```

#### Webhook Configuration
```bash
# Configurar webhook no FlyERP para receber atualizações
# URL: https://www.api.app.jttecnologia.com.br/webhooks/flyerp
```

### 3. D4Sign Integration

#### Configuração
```bash
# Obter credenciais do D4Sign
D4SIGN_API_KEY=sua-chave-d4sign
D4SIGN_CRYPTO_KEY=sua-chave-crypto
```

### 4. Configuração de Email (SMTP)

#### Gmail/Google Workspace
```bash
# 1. Ativar autenticação de 2 fatores
# 2. Gerar senha de app
# 3. Configurar no .env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=sistema@jttelecom.com.br
SMTP_PASSWORD=sua-senha-de-app
```

#### Outros Provedores
```bash
# Outlook/Hotmail
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587

# SendGrid
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587

# Amazon SES
SMTP_SERVER=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
```

## Primeiro Acesso

### 1. Inicializar Banco de Dados
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar aplicação para criar tabelas
python src/main.py
```

### 2. Criar Super Admin
```bash
# Executar script de inicialização
python scripts/create_super_admin.py

# Ou criar manualmente via API
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin JT Telecom",
    "email": "admin@jttelecom.com.br",
    "password": "admin123!@#",
    "role": "super_admin"
  }'
```

### 3. Criar Primeiro Tenant
```bash
# Login como super admin
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@jttelecom.com.br",
    "password": "admin123!@#"
  }'

# Usar o token retornado para criar tenant
curl -X POST http://localhost:5000/api/super-admin/tenants \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "JT Telecom",
    "slug": "jt-telecom",
    "email": "contato@jttelecom.com.br",
    "cnpj": "12.345.678/0001-90",
    "subscription_plan": "ENTERPRISE",
    "status": "ACTIVE"
  }'
```

### 4. Testar Sistema
```bash
# Executar testes completos
python test_complete_system.py --url http://localhost:5000 --verbose

# Acessar documentação
curl http://localhost:5000/apidocs/

# Verificar health check
curl http://localhost:5000/health
```

## Configuração de Produção

### 1. Servidor Web (Nginx)

#### Instalar Nginx
```bash
sudo apt install nginx
```

#### Configurar Virtual Host
```nginx
# /etc/nginx/sites-available/crm-api
server {
    listen 80;
    server_name www.api.app.jttecnologia.com.br;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.api.app.jttecnologia.com.br;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/jttecnologia.crt;
    ssl_certificate_key /etc/ssl/private/jttecnologia.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    # Proxy to Flask app
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files (if any)
    location /static/ {
        alias /var/www/crm/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check
    location /health {
        access_log off;
        proxy_pass http://127.0.0.1:5000/health;
    }
}
```

#### Ativar Site
```bash
sudo ln -s /etc/nginx/sites-available/crm-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. Processo Manager (Systemd)

#### Criar Service File
```ini
# /etc/systemd/system/crm-api.service
[Unit]
Description=CRM JT Telecom API
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/crm
Environment=PATH=/var/www/crm/venv/bin
ExecStart=/var/www/crm/venv/bin/python src/main.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/www/crm/logs /var/www/crm/uploads

[Install]
WantedBy=multi-user.target
```

#### Ativar Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable crm-api
sudo systemctl start crm-api
sudo systemctl status crm-api
```

### 3. Backup Automatizado

#### Script de Backup
```bash
#!/bin/bash
# /usr/local/bin/backup-crm.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/crm"
DB_NAME="crm_jttelcom"
DB_USER="crm_user"

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump -h localhost -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup dos uploads
tar -czf $BACKUP_DIR/uploads_backup_$DATE.tar.gz /var/www/crm/uploads/

# Backup dos logs
tar -czf $BACKUP_DIR/logs_backup_$DATE.tar.gz /var/www/crm/logs/

# Remover backups antigos (manter 30 dias)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup concluído: $DATE"
```

#### Configurar Cron
```bash
# Editar crontab
sudo crontab -e

# Adicionar linha para backup diário às 2h
0 2 * * * /usr/local/bin/backup-crm.sh >> /var/log/backup-crm.log 2>&1
```

### 4. Monitoramento

#### Log Rotation
```bash
# /etc/logrotate.d/crm-api
/var/www/crm/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload crm-api
    endscript
}
```

#### Health Check Script
```bash
#!/bin/bash
# /usr/local/bin/health-check-crm.sh

API_URL="https://www.api.app.jttecnologia.com.br/health"
ALERT_EMAIL="admin@jttelecom.com.br"

# Verificar se API está respondendo
if ! curl -f -s $API_URL > /dev/null; then
    echo "ALERTA: API CRM não está respondendo" | mail -s "CRM API Down" $ALERT_EMAIL
    systemctl restart crm-api
fi
```

## Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log

# Testar conexão manual
psql -h localhost -U crm_user -d crm_jttelcom
```

#### 2. Erro de Permissões
```bash
# Verificar permissões dos arquivos
ls -la /var/www/crm/

# Corrigir permissões
sudo chown -R www-data:www-data /var/www/crm/
sudo chmod -R 755 /var/www/crm/
sudo chmod -R 644 /var/www/crm/logs/
```

#### 3. Problemas de SSL
```bash
# Verificar certificado
openssl x509 -in /etc/ssl/certs/jttecnologia.crt -text -noout

# Testar SSL
curl -I https://www.api.app.jttecnologia.com.br/health
```

#### 4. Performance Issues
```bash
# Verificar uso de recursos
htop
iotop
netstat -tulpn

# Verificar logs de performance
tail -f /var/www/crm/logs/crm.log | grep "slow"
```

### Logs Importantes

#### Localização dos Logs
```bash
# Logs da aplicação
/var/www/crm/logs/crm.log

# Logs do Nginx
/var/log/nginx/access.log
/var/log/nginx/error.log

# Logs do PostgreSQL
/var/log/postgresql/postgresql-13-main.log

# Logs do sistema
/var/log/syslog
```

#### Comandos Úteis
```bash
# Monitorar logs em tempo real
tail -f /var/www/crm/logs/crm.log

# Buscar erros
grep -i error /var/www/crm/logs/crm.log

# Verificar últimas 100 linhas
tail -n 100 /var/www/crm/logs/crm.log

# Filtrar por data
grep "2024-06-23" /var/www/crm/logs/crm.log
```

### Comandos de Diagnóstico

```bash
# Verificar status geral
sudo systemctl status crm-api nginx postgresql

# Verificar portas em uso
sudo netstat -tulpn | grep :5000

# Verificar processos
ps aux | grep python

# Verificar espaço em disco
df -h

# Verificar memória
free -h

# Verificar conectividade
curl -I http://localhost:5000/health
```

### Contato para Suporte

Em caso de problemas não resolvidos:

- **Email**: suporte@jttelecom.com.br
- **Telefone**: (11) 3333-4444
- **WhatsApp**: (11) 99999-9999
- **Documentação**: https://docs.app.jttecnologia.com.br

---

**JT Telecom - Soluções em Telecomunicações**

