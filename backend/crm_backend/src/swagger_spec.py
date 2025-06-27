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
                            "description": "Lista de tarefas"
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
                            "description": "Lista de propostas"
                        }
                    }
                }
            },
            "/chatbot": {
                "get": {
                    "tags": ["Chatbot"],
                    "summary": "Informações do chatbot",
                    "description": "Retorna informações sobre o módulo de chatbot",
                    "responses": {
                        "200": {
                            "description": "Informações do chatbot"
                        }
                    }
                }
            },
            "/telephony": {
                "get": {
                    "tags": ["Telefonia"],
                    "summary": "Informações de telefonia",
                    "description": "Retorna informações sobre o módulo de telefonia",
                    "responses": {
                        "200": {
                            "description": "Informações de telefonia"
                        }
                    }
                }
            },
            "/automation": {
                "get": {
                    "tags": ["Automação"],
                    "summary": "Informações de automação",
                    "description": "Retorna informações sobre o módulo de automação",
                    "responses": {
                        "200": {
                            "description": "Informações de automação"
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

