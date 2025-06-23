# Módulo de Telefonia - Integração API JT Telecom

## Visão Geral

O módulo de telefonia do CRM JT Telecom oferece integração completa com o PABX em Nuvem da JT Telecom, permitindo funcionalidades avançadas de telefonia diretamente no CRM.

## Funcionalidades Principais

### 🔗 Integração com API Oficial
- Conectividade direta com a API do PABX JT Telecom
- Autenticação segura via usuário e token
- Suporte a todas as operações disponíveis na API

### ☎️ Click-to-Call
- Chamadas diretas do CRM para qualquer número
- Integração com leads e oportunidades
- Registro automático de chamadas no histórico
- Variáveis personalizáveis para cada chamada

### 📊 Gestão de Chamadas
- Histórico completo de chamadas
- Status em tempo real (em andamento, completada, perdida, falha)
- Duração e gravações (quando disponíveis)
- Filtros avançados por período, status, direção

### 👥 Gestão de Ramais
- Listagem de ramais configurados
- Criação, edição e exclusão de ramais
- Associação de ramais com usuários do CRM

### 🔢 Gestão de DIDs
- Listagem de números remotos (DIDs)
- Configuração e gerenciamento de DIDs
- Roteamento de chamadas

### 🧑‍💼 Controle de Operadores
- Login/logout de operadores no PABX
- Controle de pausas com motivos
- Monitoramento de status em tempo real

### 📈 Estatísticas e Relatórios
- Métricas de performance de chamadas
- Taxa de sucesso e duração média
- Relatórios por período e usuário
- Integração com dashboard principal

## Configuração

### Variáveis de Ambiente

```bash
# Credenciais da API JT Telecom
JTTELECOM_PABX_AUTH_USER=seu_usuario_api
JTTELECOM_PABX_AUTH_TOKEN=seu_token_api
```

### Endpoints da API

#### Conectividade
- `GET /api/telephony/test-connection` - Testa conexão com PABX

#### Click-to-Call
- `POST /api/telephony/click-to-call` - Realiza chamada

```json
{
  "ramal_origem": "100",
  "numero_destino": "11999999999",
  "lead_id": 123,
  "notes": "Chamada de follow-up",
  "variaveis": {
    "origem": "crm",
    "campanha": "vendas"
  }
}
```

#### Gestão de Chamadas
- `GET /api/telephony/calls` - Lista chamadas do CRM
- `GET /api/telephony/calls/{id}` - Detalhes da chamada
- `PUT /api/telephony/calls/{id}/update` - Atualiza chamada

#### Histórico do PABX
- `GET /api/telephony/pabx/history` - Histórico direto do PABX
- `GET /api/telephony/pabx/online-calls` - Chamadas em andamento

#### Ramais
- `GET /api/telephony/extensions` - Lista ramais
- `POST /api/telephony/extensions` - Cria ramal
- `PUT /api/telephony/extensions/{id}` - Atualiza ramal
- `DELETE /api/telephony/extensions/{id}` - Remove ramal

#### DIDs
- `GET /api/telephony/dids` - Lista DIDs
- `POST /api/telephony/dids` - Cria DID
- `PUT /api/telephony/dids/{id}` - Atualiza DID
- `DELETE /api/telephony/dids/{id}` - Remove DID

#### Operadores
- `POST /api/telephony/operators/{id}/login` - Login operador
- `POST /api/telephony/operators/{id}/logout` - Logout operador
- `POST /api/telephony/operators/{id}/pause` - Pausa operador
- `POST /api/telephony/operators/{id}/unpause` - Remove pausa

#### Estatísticas
- `GET /api/telephony/stats` - Estatísticas de telefonia

#### Webhooks
- `POST /api/telephony/webhook/call-status` - Recebe atualizações do PABX

## Modelos de Dados

### Call (Chamada)
```python
{
  "id": 1,
  "lead_id": 123,
  "opportunity_id": 456,
  "user_id": 1,
  "phone_number": "11999999999",
  "direction": "outbound",
  "duration": 180,
  "status": "completed",
  "start_time": "2024-12-23T10:00:00Z",
  "end_time": "2024-12-23T10:03:00Z",
  "recording_url": "https://...",
  "external_call_id": "pabx_call_123",
  "notes": "Chamada de follow-up"
}
```

### CallLog (Log de Chamada)
```python
{
  "id": 1,
  "call_id": 1,
  "event_type": "dialing",
  "event_data": {...},
  "timestamp": "2024-12-23T10:00:00Z"
}
```

## Status de Chamadas

- **in_progress**: Chamada em andamento
- **completed**: Chamada completada com sucesso
- **missed**: Chamada não atendida
- **failed**: Chamada falhou
- **busy**: Número ocupado

## Direções de Chamada

- **inbound**: Chamada recebida
- **outbound**: Chamada realizada

## Integração com Leads e Oportunidades

O módulo de telefonia está totalmente integrado com o sistema de leads e oportunidades:

- Chamadas podem ser associadas a leads específicos
- Histórico de chamadas visível na ficha do lead
- Click-to-call direto da interface do lead
- Estatísticas de chamadas por lead/oportunidade

## Webhooks

O sistema suporta webhooks para receber atualizações em tempo real do PABX:

```json
{
  "call_id": "pabx_call_123",
  "status": "completed",
  "duration": 180,
  "recording_url": "https://..."
}
```

## Tratamento de Erros

O módulo inclui tratamento robusto de erros:

- Validação de números de telefone
- Retry automático em falhas de rede
- Logs detalhados para debugging
- Fallback gracioso quando PABX indisponível

## Segurança

- Autenticação JWT obrigatória
- Validação de permissões por usuário
- Logs de auditoria para todas as operações
- Comunicação HTTPS com API do PABX

## Monitoramento

- Health check da conexão com PABX
- Métricas de performance
- Alertas para falhas de conectividade
- Dashboard de estatísticas em tempo real

## Limitações

- Módulo Click2Call deve estar contratado no PABX
- Algumas funcionalidades dependem da configuração do PABX
- Rate limiting da API do PABX deve ser respeitado

## Testes

Execute os testes do módulo:

```bash
cd /home/ubuntu/crm_jttelcom/backend/crm_backend
python test_telephony_integration.py
```

## Suporte

Para suporte técnico ou dúvidas sobre a integração, consulte:
- Documentação oficial da API: https://emnuvem.meupabxip.com.br/suite/api_doc.php
- Suporte JT Telecom: contato@jttelcom.com

