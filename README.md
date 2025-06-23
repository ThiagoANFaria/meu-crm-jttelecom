# CRM JT Telecom

Sistema de CRM SaaS modular e escalável desenvolvido especificamente para a JT Telecom, com funcionalidades completas de gestão de leads, funis de vendas, automações e integração telefônica.

## 🚀 Funcionalidades Principais

- **Autenticação e Gestão de Usuários**: Sistema seguro com múltiplos papéis (Admin, SDR, Closer, Suporte)
- **Módulo de Leads**: Cadastro completo com lead scoring automático
- **Funis de Prospecção e Vendas**: Interface Kanban com arrastar e soltar
- **Dashboard Analítico**: KPIs de conversão e métricas de desempenho
- **Tarefas e Atividades**: Gerenciamento completo com notificações
- **Automações**: Engine de automação com cadência de follow-up
- **Integração Telefônica**: Click-to-call e histórico de chamadas via PABX em nuvem
- **API Externa**: RESTful com webhooks customizáveis
- **Interface Responsiva**: Design moderno seguindo a identidade visual da JT Telecom

## 🎨 Identidade Visual

- **Cor Primária**: Azul Royal (#4169E1)
- **Cores Secundárias**: Branco (#FFFFFF) e Cinza Claro (#F5F5F5)
- **Tipografia**: Inter/Montserrat/Roboto
- **Framework CSS**: Tailwind CSS

## 🏗️ Arquitetura

### Backend
- **Framework**: Flask (Python)
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT/OAuth2
- **Arquitetura**: Microsserviços

### Frontend
- **Framework**: React.js
- **Estilização**: Tailwind CSS
- **Tipo**: Single-Page Application (SPA)

## 📁 Estrutura do Projeto

```
crm_jttelcom/
├── backend/
│   └── crm_backend/        # Aplicação Flask
├── frontend/
│   └── crm_frontend/       # Aplicação React
├── docs/
│   └── architecture.md     # Documentação da arquitetura
├── todo.md                 # Lista de tarefas do projeto
└── README.md              # Este arquivo
```

## 🚀 Como Executar

### Backend (Flask)
```bash
cd backend/crm_backend
source venv/bin/activate
python src/main.py
```

### Frontend (React)
```bash
cd frontend/crm_frontend
pnpm run dev
```

## 📋 Status do Desenvolvimento

Consulte o arquivo `todo.md` para acompanhar o progresso das funcionalidades.

## 📖 Documentação

- [Arquitetura do Sistema](docs/architecture.md)
- [Lista de Tarefas](todo.md)

## 🤝 Contribuição

Este projeto está sendo desenvolvido especificamente para a JT Telecom seguindo os requisitos técnicos estabelecidos.

---

**Desenvolvido por Manus AI para JT Telecom**

