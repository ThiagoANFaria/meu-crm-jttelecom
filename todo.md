## To-Do List for CRM Development

### Phase 1: Planejamento da arquitetura e estrutura do projeto
- [ ] Definir a arquitetura geral do sistema (backend, frontend, banco de dados).
- [ ] Escolher as tecnologias específicas para cada componente (ex: Python/Flask para backend, React/Tailwind CSS para frontend, PostgreSQL para banco de dados).
- [ ] Esboçar o esquema do banco de dados para os módulos iniciais (Autenticação, Usuários, Leads).
- [ ] Planejar a estrutura de pastas e arquivos do projeto.
- [ ] Documentar as decisões de arquitetura.

### Phase 2: Configuração do ambiente e estrutura base
- [x] Configurar o ambiente de desenvolvimento local.
- [x] Criar a estrutura de pastas e arquivos do projeto.
- [x] Inicializar o repositório Git.
- [x] Configurar o ambiente de banco de dados.

### Phase 3: Desenvolvimento do sistema de autenticação e gestão de usuários
- [x] Implementar o modelo de usuário e autenticação (JWT/OAuth2).
- [x] Desenvolver as rotas de API para registro, login e logout.
- [x] Criar a interface de usuário para login e registro.
- [x] Implementar a gestão de papéis e permissões.
- [x] Adicionar recuperação de senha.

### Phase 4: Implementação do módulo de leads com lead scoring e campos adicionais
- [x] Definir o modelo de dados para leads com campos padrão e adicionais.
- [x] Desenvolver as rotas de API para CRUD de leads.
- [x] Implementar a lógica de Lead Score automático.
- [x] Criar sistema de campos adicionais opcionais com templates.
- [x] Adicionar filtros avançados e validações aprimoradas.
- [x] Implementar campos padrão: Nome, Contato, E-mail, WhatsApp, Razão Social, CNPJ/CPF, IE/RG, Telefone, Endereço completo.
- [x] Criar templates de campos customizáveis para flexibilidade.

### Phase 5: Criação dos funis de prospecção e vendas com interface Kanban
- [x] Definir o modelo de dados para funis, etapas, produtos e oportunidades.
- [x] Desenvolver as rotas de API para gestão de funis e movimentação de leads.
- [x] Implementar sistema de produtos com categorias e preços.
- [x] Criar funcionalidades de filtros por produtos, total de produtos e receita.
- [x] Implementar visualização em lista e Kanban (backend preparado).
- [x] Adicionar estatísticas detalhadas por funil e etapa.
- [x] Criar funis padrão (prospecção e vendas) com etapas pré-configuradas.
- [ ] Criar a interface Kanban com arrastar e soltar.
- [ ] Implementar histórico, anotações, tarefas e chamadas vinculadas aos cards.

### Phase 6: Desenvolvimento do dashboard com KPIs e módulo de propostas ✅
- [x] Criar rotas de API para dashboard com métricas de leads, oportunidades e vendas
- [x] Implementar KPIs: conversão por funil, taxa de sucesso por usuário, volume por etapa
- [x] **MÓDULO DE PROPOSTAS COMPLETO:**
  - [x] Modelos de dados: ProposalTemplate, Proposal, ProposalItem
  - [x] Sistema de templates com variáveis dinâmicas {name}, {company_name}, {cnpj_cpf}, etc.
  - [x] 3 templates padrão: PABX em Nuvem, Múltiplos Produtos, Proposta Simples
  - [x] APIs completas para CRUD de templates e propostas
  - [x] Sistema de numeração automática (PROP-YYYYMM-NNNN)
  - [x] Integração com leads e oportunidades do funil
  - [x] Envio por email com anexo HTML
  - [x] API preparada para assinatura digital (DocuSign, ClickSign)
  - [x] Controle de visualizações e status
  - [x] Sistema de itens/produtos com cálculo automático
  - [x] Estatísticas de propostas por status e período
  - [x] Suporte a imagens e rodapé personalizado
  - [x] Validação de expiração automática
  - [x] Controle de acesso baseado em permissões

### Phase 7: Implementação do módulo de tarefas e atividades
- [ ] Definir o modelo de dados para tarefas e atividades.
- [ ] Desenvolver as rotas de API para CRUD de tarefas.
- [ ] Criar a interface de usuário para criação e gerenciamento de tarefas.
- [ ] Implementar notificações internas e por e-mail.
- [ ] (Opcional) Integrar com calendários externos.

### Phase 8: Desenvolvimento das automações e cadência
- [ ] Definir o modelo de dados para automações e cadências.
- [ ] Desenvolver a engine de automação com gatilhos.
- [ ] Implementar envio automático de e-mails (SMTP/Amazon SES).
- [ ] Criar tarefas automáticas.
- [ ] Configurar cadência de follow-up.

### Phase 14: Atualização do módulo de telefonia com API JT Telecom 🔄
- [ ] Criar modelos de dados para chamadas e histórico (se necessário)
- [ ] Implementar serviço de integração com a API do PABX em Nuvem da JT Telecom
- [ ] Criar APIs para funcionalidades de telefonia (click-to-call, histórico, gravações)
- [ ] Integrar com o módulo de leads e oportunidades
- [ ] Realizar testes unitários e de integração.
- [ ] Realizar testes de segurança.
- [ ] Documentar o código e a arquitetura.
- [ ] Preparar o ambiente de produção e realizar o deploy.

### Phase 10: Criação da API externa e sistema de webhooks
- [ ] Expor API RESTful com endpoints para os módulos.
- [ ] Implementar suporte a Webhooks customizáveis.
- [ ] Gerar documentação Swagger/OpenAPI.

### Phase 11: Implementação da identidade visual e interface responsiva
- [ ] Aplicar a paleta de cores da JT Telecom.
- [ ] Implementar layout clean, responsivo e acessível.
- [ ] Integrar a logo da JT Telecom.
- [ ] Definir e aplicar a tipografia.
- [ ] Garantir compatibilidade com React.js + Tailwind CSS.

### Phase 12: Desenvolvimento do módulo de contratos com templates dinâmicos ✅
- [x] **MÓDULO DE CONTRATOS COMPLETO COM INTEGRAÇÃO D4SIGN:**
  - [x] Modelos de dados: ContractTemplate, Contract, ContractAmendment
  - [x] Sistema de templates com variáveis dinâmicas {name}, {company_name}, {cnpj_cpf}, etc.
  - [x] 3 templates padrão: Prestação de Serviços PABX, Licenciamento, Consultoria
  - [x] Integração completa com D4Sign para assinatura digital
  - [x] Serviço D4SignService com todas as funcionalidades necessárias
  - [x] APIs completas para CRUD de templates e contratos
  - [x] Sistema de numeração automática (CONT-YYYY-NNNN)
  - [x] Integração com leads, oportunidades e propostas
  - [x] Controle de assinaturas (cliente, empresa, testemunha)
  - [x] Sistema de aditivos contratuais
  - [x] Webhook para receber notificações do D4Sign
  - [x] Download de documentos assinados
  - [x] Estatísticas de contratos por status e período
  - [x] Controle de vigência, renovação e cancelamento
  - [x] Suporte a múltiplos signatários e posições de assinatura
  - [x] Validação automática de expiração e renovação
  - [x] Controle de acesso baseado em permissões

### Phase 13: Desenvolvimento do módulo de chatbot com IA e fluxos ✅
- [x] Criar modelos de dados para chatbot (ChatFlow, ChatConversation, ChatMessage, ChatIntegration, ChatAIConfig)
- [x] Implementar serviços de integração (WhatsApp Business API, Evolution API, OpenAI)
- [x] Criar engine de processamento de fluxos estilo Typebot
- [x] Implementar sistema de IA com GPT-4o
- [x] Criar APIs completas para gestão de conversas
- [x] Implementar webhooks para recebimento de mensagens
- [x] Criar interface de atendimento humano
- [x] Implementar fluxos padrão (Boas-vindas e Suporte Técnico)
- [x] Criar sistema de estatísticas e relatórios
- [x] Integrar com sistema de leads do CRM
- [ ] Realizar testes unitários e de integração.
- [ ] Realizar testes de segurança.
- [ ] Documentar o código e a arquitetura.
- [ ] Preparar o ambiente de produção e realizar o deploy.
- [ ] Entregar a solução e o playbook ao cliente.


