"""
Especificação completa do Swagger para a API do CRM JT Telecom
"""

def get_swagger_spec():
    """Retorna a especificação completa do Swagger"""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "CRM JT Telecom API",
            "description": "API completa do Sistema de CRM da JT Telecom com todos os módulos funcionais",
            "version": "1.0.0",
            "contact": {
                "name": "JT Tecnologia",
                "url": "https://jttecnologia.com.br"
            }
        },
        "servers": [
            {
                "url": "https://api.app.jttecnologia.com.br",
                "description": "Servidor de Produção"
            }
        ],
        "paths": {
            "/": {
                "get": {
                    "tags": ["Sistema"],
                    "summary": "Informações da API",
                    "description": "Retorna informações básicas sobre a API",
                    "responses": {
                        "200": {
                            "description": "Informações da API",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "version": {"type": "string"},
                                            "documentation": {"type": "string"},
                                            "health": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/health": {
                "get": {
                    "tags": ["Sistema"],
                    "summary": "Status de saúde",
                    "description": "Verifica se a API está funcionando",
                    "responses": {
                        "200": {
                            "description": "API funcionando",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "message": {"type": "string"},
                                            "version": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/auth": {
                "get": {
                    "tags": ["Autenticação"],
                    "summary": "Informações do módulo de autenticação",
                    "description": "Retorna informações sobre o módulo de autenticação",
                    "responses": {
                        "200": {
                            "description": "Informações do módulo",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "module": {"type": "string"},
                                            "description": {"type": "string"},
                                            "endpoints": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "path": {"type": "string"},
                                                        "method": {"type": "string"},
                                                        "description": {"type": "string"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/auth/login": {
                "post": {
                    "tags": ["Autenticação"],
                    "summary": "Login de usuário",
                    "description": "Realiza login do usuário no sistema",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string", "example": "usuario@exemplo.com"},
                                        "password": {"type": "string", "example": "senha123"}
                                    },
                                    "required": ["email", "password"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login realizado com sucesso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "access_token": {"type": "string"},
                                            "user": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "email": {"type": "string"},
                                                    "name": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Credenciais inválidas"
                        }
                    }
                }
            },
            "/auth/register": {
                "post": {
                    "tags": ["Autenticação"],
                    "summary": "Registro de usuário",
                    "description": "Registra um novo usuário no sistema",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "João Silva"},
                                        "email": {"type": "string", "example": "joao@exemplo.com"},
                                        "password": {"type": "string", "example": "senha123"}
                                    },
                                    "required": ["name", "email", "password"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Usuário criado com sucesso"
                        },
                        "400": {
                            "description": "Dados inválidos"
                        }
                    }
                }
            },
            "/leads": {
                "get": {
                    "tags": ["Leads"],
                    "summary": "Listar leads",
                    "description": "Retorna lista de todos os leads",
                    "responses": {
                        "200": {
                            "description": "Lista de leads",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "name": {"type": "string"},
                                                "email": {"type": "string"},
                                                "phone": {"type": "string"},
                                                "status": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Leads"],
                    "summary": "Criar lead",
                    "description": "Cria um novo lead",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "Maria Santos"},
                                        "email": {"type": "string", "example": "maria@exemplo.com"},
                                        "phone": {"type": "string", "example": "(11) 99999-9999"},
                                        "status": {"type": "string", "example": "novo"}
                                    },
                                    "required": ["name", "email"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Lead criado com sucesso"
                        }
                    }
                }
            },
            "/pipelines": {
                "get": {
                    "tags": ["Pipelines"],
                    "summary": "Listar pipelines",
                    "description": "Retorna lista de todos os pipelines",
                    "responses": {
                        "200": {
                            "description": "Lista de pipelines",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "integer"},
                                                "name": {"type": "string"},
                                                "description": {"type": "string"},
                                                "stages": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "integer"},
                                                            "name": {"type": "string"},
                                                            "order": {"type": "integer"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/dashboard": {
                "get": {
                    "tags": ["Dashboard"],
                    "summary": "Dados do dashboard",
                    "description": "Retorna dados para o dashboard",
                    "responses": {
                        "200": {
                            "description": "Dados do dashboard"
                        }
                    }
                }
            },
            "/tasks": {
                "get": {
                    "tags": ["Tarefas"],
                    "summary": "Listar tarefas",
                    "description": "Retorna lista de todas as tarefas",
                    "responses": {
                        "200": {
                            "description": "Lista de tarefas",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "title": {"type": "string"},
                                                "description": {"type": "string"},
                                                "status": {"type": "string"},
                                                "priority": {"type": "string"},
                                                "due_date": {"type": "string"},
                                                "assigned_to": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Tarefas"],
                    "summary": "Criar tarefa",
                    "description": "Cria uma nova tarefa",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "example": "Ligar para cliente"},
                                        "description": {"type": "string", "example": "Fazer follow-up da proposta"},
                                        "priority": {"type": "string", "example": "alta"},
                                        "due_date": {"type": "string", "example": "2024-01-15"},
                                        "assigned_to": {"type": "string", "example": "user123"}
                                    },
                                    "required": ["title", "priority"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Tarefa criada com sucesso"
                        }
                    }
                }
            },
            "/tasks/{id}": {
                "get": {
                    "tags": ["Tarefas"],
                    "summary": "Obter tarefa específica",
                    "description": "Retorna detalhes de uma tarefa específica",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "ID da tarefa"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Detalhes da tarefa"
                        },
                        "404": {
                            "description": "Tarefa não encontrada"
                        }
                    }
                },
                "put": {
                    "tags": ["Tarefas"],
                    "summary": "Atualizar tarefa",
                    "description": "Atualiza uma tarefa existente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "ID da tarefa"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "status": {"type": "string"},
                                        "priority": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Tarefa atualizada com sucesso"
                        }
                    }
                },
                "delete": {
                    "tags": ["Tarefas"],
                    "summary": "Deletar tarefa",
                    "description": "Remove uma tarefa",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "ID da tarefa"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Tarefa deletada com sucesso"
                        }
                    }
                }
            },
            "/proposals": {
                "get": {
                    "tags": ["Propostas"],
                    "summary": "Listar propostas",
                    "description": "Retorna lista de todas as propostas",
                    "responses": {
                        "200": {
                            "description": "Lista de propostas",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "title": {"type": "string"},
                                                "client": {"type": "string"},
                                                "value": {"type": "number"},
                                                "status": {"type": "string"},
                                                "created_date": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Propostas"],
                    "summary": "Criar proposta",
                    "description": "Cria uma nova proposta",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "example": "Proposta de Internet Fibra"},
                                        "client": {"type": "string", "example": "Empresa ABC"},
                                        "value": {"type": "number", "example": 299.90},
                                        "description": {"type": "string", "example": "Plano de internet 100MB"}
                                    },
                                    "required": ["title", "client", "value"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Proposta criada com sucesso"
                        }
                    }
                }
            },
            "/proposals/{id}": {
                "get": {
                    "tags": ["Propostas"],
                    "summary": "Obter proposta específica",
                    "description": "Retorna detalhes de uma proposta específica",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "ID da proposta"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Detalhes da proposta"
                        }
                    }
                },
                "put": {
                    "tags": ["Propostas"],
                    "summary": "Atualizar proposta",
                    "description": "Atualiza uma proposta existente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "ID da proposta"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "value": {"type": "number"},
                                        "status": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Proposta atualizada com sucesso"
                        }
                    }
                }
            },
            "/automation/workflows": {
                "get": {
                    "tags": ["Automação"],
                    "summary": "Listar workflows",
                    "description": "Retorna lista de todos os workflows de automação",
                    "responses": {
                        "200": {
                            "description": "Lista de workflows",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "name": {"type": "string"},
                                                "trigger": {"type": "string"},
                                                "actions": {"type": "array"},
                                                "active": {"type": "boolean"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Automação"],
                    "summary": "Criar workflow",
                    "description": "Cria um novo workflow de automação",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "Email de Boas-vindas"},
                                        "trigger": {"type": "string", "example": "novo_lead"},
                                        "actions": {
                                            "type": "array",
                                            "example": ["enviar_email", "criar_tarefa"]
                                        }
                                    },
                                    "required": ["name", "trigger", "actions"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Workflow criado com sucesso"
                        }
                    }
                }
            },
            "/automation/trigger": {
                "post": {
                    "tags": ["Automação"],
                    "summary": "Disparar automação",
                    "description": "Dispara uma automação específica",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "workflow_id": {"type": "string", "example": "workflow123"},
                                        "data": {"type": "object", "example": {"lead_id": "lead456"}}
                                    },
                                    "required": ["workflow_id"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Automação disparada com sucesso"
                        }
                    }
                }
            },
            "/telephony/calls": {
                "get": {
                    "tags": ["Telefonia"],
                    "summary": "Listar chamadas",
                    "description": "Retorna lista de todas as chamadas",
                    "responses": {
                        "200": {
                            "description": "Lista de chamadas",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "phone": {"type": "string"},
                                                "duration": {"type": "integer"},
                                                "status": {"type": "string"},
                                                "date": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Telefonia"],
                    "summary": "Fazer chamada",
                    "description": "Inicia uma nova chamada",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "phone": {"type": "string", "example": "(11) 99999-9999"},
                                        "lead_id": {"type": "string", "example": "lead123"}
                                    },
                                    "required": ["phone"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Chamada iniciada com sucesso"
                        }
                    }
                }
            },
            "/telephony/recordings": {
                "get": {
                    "tags": ["Telefonia"],
                    "summary": "Listar gravações",
                    "description": "Retorna lista de todas as gravações",
                    "responses": {
                        "200": {
                            "description": "Lista de gravações",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "call_id": {"type": "string"},
                                                "duration": {"type": "integer"},
                                                "file_url": {"type": "string"},
                                                "date": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/chatbot/conversations": {
                "get": {
                    "tags": ["Chatbot"],
                    "summary": "Listar conversas",
                    "description": "Retorna lista de todas as conversas do chatbot",
                    "responses": {
                        "200": {
                            "description": "Lista de conversas",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "user": {"type": "string"},
                                                "messages": {"type": "array"},
                                                "status": {"type": "string"},
                                                "created_at": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/chatbot/message": {
                "post": {
                    "tags": ["Chatbot"],
                    "summary": "Enviar mensagem",
                    "description": "Envia uma mensagem para o chatbot",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string", "example": "Olá, preciso de ajuda"},
                                        "user_id": {"type": "string", "example": "user123"},
                                        "conversation_id": {"type": "string", "example": "conv456"}
                                    },
                                    "required": ["message", "user_id"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Mensagem enviada e resposta recebida",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "response": {"type": "string"},
                                            "conversation_id": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/dashboard/stats": {
                "get": {
                    "tags": ["Dashboard"],
                    "summary": "Estatísticas gerais",
                    "description": "Retorna estatísticas gerais do CRM",
                    "responses": {
                        "200": {
                            "description": "Estatísticas do dashboard",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "total_leads": {"type": "integer"},
                                            "total_tasks": {"type": "integer"},
                                            "total_proposals": {"type": "integer"},
                                            "conversion_rate": {"type": "number"},
                                            "revenue": {"type": "number"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/dashboard/charts": {
                "get": {
                    "tags": ["Dashboard"],
                    "summary": "Dados para gráficos",
                    "description": "Retorna dados para gráficos do dashboard",
                    "responses": {
                        "200": {
                            "description": "Dados dos gráficos",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "leads_by_month": {"type": "array"},
                                            "conversion_funnel": {"type": "array"},
                                            "revenue_by_period": {"type": "array"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/contracts": {
                "get": {
                    "tags": ["Contratos"],
                    "summary": "Listar contratos",
                    "description": "Retorna lista de todos os contratos",
                    "responses": {
                        "200": {
                            "description": "Lista de contratos",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "client": {"type": "string"},
                                                "value": {"type": "number"},
                                                "start_date": {"type": "string"},
                                                "end_date": {"type": "string"},
                                                "status": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Contratos"],
                    "summary": "Criar contrato",
                    "description": "Cria um novo contrato",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "client": {"type": "string", "example": "Empresa XYZ"},
                                        "value": {"type": "number", "example": 1500.00},
                                        "start_date": {"type": "string", "example": "2024-01-01"},
                                        "duration_months": {"type": "integer", "example": 12}
                                    },
                                    "required": ["client", "value", "start_date"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Contrato criado com sucesso"
                        }
                    }
                }
            },
            "/contracts/{id}": {
                "get": {
                    "tags": ["Contratos"],
                    "summary": "Obter contrato específico",
                    "description": "Retorna detalhes de um contrato específico",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "ID do contrato"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Detalhes do contrato"
                        }
                    }
                }
            }
        },
        "tags": [
            {"name": "Sistema", "description": "Endpoints do sistema"},
            {"name": "Autenticação", "description": "Módulo de autenticação"},
            {"name": "Leads", "description": "Gestão de leads"},
            {"name": "Pipelines", "description": "Gestão de pipelines"},
            {"name": "Dashboard", "description": "Dashboard e estatísticas"},
            {"name": "Tarefas", "description": "Gestão de tarefas"},
            {"name": "Propostas", "description": "Gestão de propostas"},
            {"name": "Chatbot", "description": "Módulo de chatbot"},
            {"name": "Telefonia", "description": "Módulo de telefonia"},
            {"name": "Automação", "description": "Módulo de automação"}
        ]
    }

