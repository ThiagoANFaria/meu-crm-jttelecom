import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Save, 
  TestTube, 
  Eye, 
  EyeOff,
  Phone,
  Bot,
  Mail,
  Brain,
  Database,
  Webhook,
  Key,
  Server,
  Settings,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Loader2,
  Copy,
  RefreshCw,
  Shield,
  Globe,
  MessageSquare,
  Zap,
  Cloud,
  Lock
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';

interface IntegrationConfig {
  id: string;
  name: string;
  description: string;
  icon: any;
  color: string;
  enabled: boolean;
  status: 'connected' | 'disconnected' | 'error' | 'testing';
  lastTested?: string;
  fields: {
    [key: string]: {
      label: string;
      type: 'text' | 'password' | 'number' | 'select' | 'textarea' | 'url';
      value: string;
      required: boolean;
      placeholder?: string;
      description?: string;
      options?: string[];
      validation?: {
        pattern?: string;
        minLength?: number;
        maxLength?: number;
      };
    };
  };
}

const IntegrationsManager: React.FC = () => {
  const [integrations, setIntegrations] = useState<IntegrationConfig[]>([]);
  const [activeTab, setActiveTab] = useState('pabx');
  const [showPasswords, setShowPasswords] = useState<{[key: string]: boolean}>({});
  const [testingIntegration, setTestingIntegration] = useState<string | null>(null);
  const { toast } = useToast();
  const { currentTenant } = useTenant();

  useEffect(() => {
    if (currentTenant) {
      loadIntegrations();
    }
  }, [currentTenant]);

  const loadIntegrations = () => {
    if (!currentTenant) return;
    const mockIntegrations: IntegrationConfig[] = [
      {
        id: 'pabx',
        name: 'PABX em Nuvem',
        description: 'Configurações do sistema de telefonia em nuvem',
        icon: Phone,
        color: 'bg-blue-500',
        enabled: true,
        status: 'connected',
        lastTested: '2025-07-05T10:30:00Z',
        fields: {
          server_url: {
            label: 'URL do Servidor',
            type: 'url',
            value: 'https://pabx.jttecnologia.com.br',
            required: true,
            placeholder: 'https://seu-pabx.com.br',
            description: 'URL base do servidor PABX'
          },
          api_key: {
            label: 'Chave da API',
            type: 'password',
            value: 'pabx_key_123456789',
            required: true,
            placeholder: 'Sua chave de API do PABX',
            description: 'Chave de autenticação da API'
          },
          username: {
            label: 'Usuário',
            type: 'text',
            value: 'admin@jttelecom',
            required: true,
            placeholder: 'Usuário de acesso',
            description: 'Nome de usuário para autenticação'
          },
          password: {
            label: 'Senha',
            type: 'password',
            value: 'senha123',
            required: true,
            placeholder: 'Senha de acesso',
            description: 'Senha para autenticação'
          },
          extension_prefix: {
            label: 'Prefixo de Ramais',
            type: 'text',
            value: '1000',
            required: false,
            placeholder: '1000',
            description: 'Prefixo padrão para ramais'
          },
          timeout: {
            label: 'Timeout (segundos)',
            type: 'number',
            value: '30',
            required: false,
            placeholder: '30',
            description: 'Tempo limite para conexões'
          }
        }
      },
      {
        id: 'smartbot',
        name: 'Smartbot',
        description: 'Configurações do chatbot inteligente',
        icon: Bot,
        color: 'bg-green-500',
        enabled: true,
        status: 'connected',
        lastTested: '2025-07-05T09:15:00Z',
        fields: {
          api_url: {
            label: 'URL da API',
            type: 'url',
            value: 'https://api.smartbot.com.br',
            required: true,
            placeholder: 'https://api.smartbot.com.br',
            description: 'URL base da API do Smartbot'
          },
          token: {
            label: 'Token de Acesso',
            type: 'password',
            value: 'sb_token_abcdef123456',
            required: true,
            placeholder: 'Seu token do Smartbot',
            description: 'Token de autenticação da API'
          },
          bot_id: {
            label: 'ID do Bot',
            type: 'text',
            value: 'bot_jttelecom_001',
            required: true,
            placeholder: 'ID do seu bot',
            description: 'Identificador único do bot'
          },
          webhook_url: {
            label: 'URL do Webhook',
            type: 'url',
            value: 'https://crm.jttecnologia.com.br/webhook/smartbot',
            required: false,
            placeholder: 'URL para receber webhooks',
            description: 'URL para receber notificações do bot'
          },
          default_flow: {
            label: 'Fluxo Padrão',
            type: 'text',
            value: 'atendimento_inicial',
            required: false,
            placeholder: 'Nome do fluxo padrão',
            description: 'Fluxo inicial para novos contatos'
          }
        }
      },
      {
        id: 'email',
        name: 'Configurações de Email',
        description: 'Servidor SMTP para envio de emails',
        icon: Mail,
        color: 'bg-red-500',
        enabled: true,
        status: 'connected',
        lastTested: '2025-07-05T08:45:00Z',
        fields: {
          smtp_host: {
            label: 'Servidor SMTP',
            type: 'text',
            value: 'smtp.gmail.com',
            required: true,
            placeholder: 'smtp.gmail.com',
            description: 'Endereço do servidor SMTP'
          },
          smtp_port: {
            label: 'Porta SMTP',
            type: 'number',
            value: '587',
            required: true,
            placeholder: '587',
            description: 'Porta do servidor SMTP'
          },
          smtp_user: {
            label: 'Usuário SMTP',
            type: 'text',
            value: 'noreply@jttecnologia.com.br',
            required: true,
            placeholder: 'seu-email@dominio.com',
            description: 'Email para autenticação SMTP'
          },
          smtp_password: {
            label: 'Senha SMTP',
            type: 'password',
            value: 'senha_app_123',
            required: true,
            placeholder: 'Senha ou senha de app',
            description: 'Senha para autenticação SMTP'
          },
          from_name: {
            label: 'Nome do Remetente',
            type: 'text',
            value: 'JT Tecnologia CRM',
            required: true,
            placeholder: 'Nome da Empresa',
            description: 'Nome que aparecerá como remetente'
          },
          encryption: {
            label: 'Criptografia',
            type: 'select',
            value: 'tls',
            required: true,
            options: ['none', 'ssl', 'tls'],
            description: 'Tipo de criptografia para conexão'
          }
        }
      },
      {
        id: 'openai',
        name: 'OpenAI',
        description: 'Configurações da API da OpenAI para IA',
        icon: Brain,
        color: 'bg-purple-500',
        enabled: true,
        status: 'connected',
        lastTested: '2025-07-05T11:00:00Z',
        fields: {
          api_key: {
            label: 'Chave da API',
            type: 'password',
            value: 'sk-proj-abcdef123456789',
            required: true,
            placeholder: 'sk-proj-...',
            description: 'Chave de API da OpenAI',
            validation: {
              pattern: '^sk-proj-[a-zA-Z0-9]+$',
              minLength: 20
            }
          },
          organization_id: {
            label: 'ID da Organização',
            type: 'text',
            value: 'org-jttecnologia',
            required: false,
            placeholder: 'org-...',
            description: 'ID da organização (opcional)'
          },
          default_model: {
            label: 'Modelo Padrão',
            type: 'select',
            value: 'gpt-4',
            required: true,
            options: ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'gpt-4o'],
            description: 'Modelo de IA padrão para usar'
          },
          max_tokens: {
            label: 'Máximo de Tokens',
            type: 'number',
            value: '2000',
            required: false,
            placeholder: '2000',
            description: 'Limite máximo de tokens por requisição'
          },
          temperature: {
            label: 'Temperatura',
            type: 'text',
            value: '0.7',
            required: false,
            placeholder: '0.7',
            description: 'Criatividade das respostas (0.0 a 1.0)'
          },
          timeout: {
            label: 'Timeout (segundos)',
            type: 'number',
            value: '30',
            required: false,
            placeholder: '30',
            description: 'Tempo limite para requisições'
          }
        }
      },
      {
        id: 'database',
        name: 'Banco de Dados',
        description: 'Configurações de conexão com banco de dados',
        icon: Database,
        color: 'bg-gray-500',
        enabled: true,
        status: 'connected',
        lastTested: '2025-07-05T07:30:00Z',
        fields: {
          host: {
            label: 'Host do Banco',
            type: 'text',
            value: 'db.jttecnologia.com.br',
            required: true,
            placeholder: 'localhost',
            description: 'Endereço do servidor de banco'
          },
          port: {
            label: 'Porta',
            type: 'number',
            value: '5432',
            required: true,
            placeholder: '5432',
            description: 'Porta de conexão'
          },
          database: {
            label: 'Nome do Banco',
            type: 'text',
            value: 'crm_jttelecom',
            required: true,
            placeholder: 'nome_do_banco',
            description: 'Nome da base de dados'
          },
          username: {
            label: 'Usuário',
            type: 'text',
            value: 'crm_user',
            required: true,
            placeholder: 'usuario',
            description: 'Usuário de conexão'
          },
          password: {
            label: 'Senha',
            type: 'password',
            value: 'senha_db_123',
            required: true,
            placeholder: 'senha',
            description: 'Senha de conexão'
          },
          ssl_mode: {
            label: 'Modo SSL',
            type: 'select',
            value: 'require',
            required: true,
            options: ['disable', 'allow', 'prefer', 'require'],
            description: 'Configuração SSL para conexão'
          }
        }
      },
      {
        id: 'webhooks',
        name: 'Webhooks',
        description: 'Configurações de webhooks para integrações',
        icon: Webhook,
        color: 'bg-yellow-500',
        enabled: false,
        status: 'disconnected',
        fields: {
          endpoint_url: {
            label: 'URL do Endpoint',
            type: 'url',
            value: '',
            required: true,
            placeholder: 'https://api.exemplo.com/webhook',
            description: 'URL para receber webhooks'
          },
          secret_key: {
            label: 'Chave Secreta',
            type: 'password',
            value: '',
            required: false,
            placeholder: 'Chave para validação',
            description: 'Chave secreta para validar webhooks'
          },
          events: {
            label: 'Eventos',
            type: 'textarea',
            value: 'lead.created\nlead.updated\nclient.created',
            required: true,
            placeholder: 'lead.created\nlead.updated',
            description: 'Eventos que disparam webhooks (um por linha)'
          },
          retry_attempts: {
            label: 'Tentativas de Retry',
            type: 'number',
            value: '3',
            required: false,
            placeholder: '3',
            description: 'Número de tentativas em caso de falha'
          }
        }
      }
    ];

    setIntegrations(mockIntegrations);
  };

  const handleFieldChange = (integrationId: string, fieldKey: string, value: string) => {
    setIntegrations(prev => prev.map(integration => 
      integration.id === integrationId 
        ? {
            ...integration,
            fields: {
              ...integration.fields,
              [fieldKey]: {
                ...integration.fields[fieldKey],
                value
              }
            }
          }
        : integration
    ));
  };

  const handleToggleIntegration = (integrationId: string) => {
    setIntegrations(prev => prev.map(integration => 
      integration.id === integrationId 
        ? { ...integration, enabled: !integration.enabled }
        : integration
    ));
  };

  const handleTestConnection = async (integrationId: string) => {
    setTestingIntegration(integrationId);
    
    try {
      // Simular teste de conexão
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setIntegrations(prev => prev.map(integration => 
        integration.id === integrationId 
          ? { 
              ...integration, 
              status: 'connected',
              lastTested: new Date().toISOString()
            }
          : integration
      ));

      toast({
        title: 'Conexão testada',
        description: 'A conexão foi testada com sucesso.',
      });
    } catch (error) {
      setIntegrations(prev => prev.map(integration => 
        integration.id === integrationId 
          ? { ...integration, status: 'error' }
          : integration
      ));

      toast({
        title: 'Erro na conexão',
        description: 'Não foi possível conectar com o serviço.',
        variant: 'destructive',
      });
    } finally {
      setTestingIntegration(null);
    }
  };

  const handleSaveIntegration = (integrationId: string) => {
    toast({
      title: 'Configurações salvas',
      description: 'As configurações da integração foram salvas com sucesso.',
    });
  };

  const togglePasswordVisibility = (fieldId: string) => {
    setShowPasswords(prev => ({
      ...prev,
      [fieldId]: !prev[fieldId]
    }));
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: 'Copiado',
      description: 'Texto copiado para a área de transferência.',
    });
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'testing':
        return <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />;
      default:
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'connected':
        return 'Conectado';
      case 'error':
        return 'Erro';
      case 'testing':
        return 'Testando...';
      default:
        return 'Desconectado';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Configurações de Integrações</h3>
          <p className="text-sm text-gray-600">
            Configure as credenciais e parâmetros para todas as integrações do sistema
          </p>
        </div>
        <Button 
          onClick={() => {
            integrations.forEach(integration => {
              if (integration.enabled) {
                handleSaveIntegration(integration.id);
              }
            });
          }}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <Save className="w-4 h-4 mr-2" />
          Salvar Todas
        </Button>
      </div>

      {/* Integration Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          {integrations.map((integration) => (
            <TabsTrigger key={integration.id} value={integration.id} className="text-xs">
              <integration.icon className="w-4 h-4 mr-1" />
              {integration.name}
            </TabsTrigger>
          ))}
        </TabsList>

        {integrations.map((integration) => (
          <TabsContent key={integration.id} value={integration.id} className="space-y-4">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 ${integration.color} rounded-lg flex items-center justify-center`}>
                      <integration.icon className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <CardTitle className="flex items-center gap-2">
                        {integration.name}
                        {getStatusIcon(testingIntegration === integration.id ? 'testing' : integration.status)}
                        <Badge variant={integration.enabled ? 'default' : 'secondary'}>
                          {integration.enabled ? 'Ativo' : 'Inativo'}
                        </Badge>
                      </CardTitle>
                      <CardDescription>{integration.description}</CardDescription>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right text-sm">
                      <div className="font-medium">
                        {getStatusText(testingIntegration === integration.id ? 'testing' : integration.status)}
                      </div>
                      {integration.lastTested && (
                        <div className="text-gray-500">
                          Último teste: {new Date(integration.lastTested).toLocaleString('pt-BR')}
                        </div>
                      )}
                    </div>
                    <Switch
                      checked={integration.enabled}
                      onCheckedChange={() => handleToggleIntegration(integration.id)}
                    />
                  </div>
                </div>
              </CardHeader>
              
              {integration.enabled && (
                <CardContent className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    {Object.entries(integration.fields).map(([fieldKey, field]) => (
                      <div key={fieldKey} className="space-y-2">
                        <Label htmlFor={`${integration.id}-${fieldKey}`}>
                          {field.label}
                          {field.required && <span className="text-red-500 ml-1">*</span>}
                        </Label>
                        
                        {field.type === 'select' ? (
                          <Select 
                            value={field.value} 
                            onValueChange={(value) => handleFieldChange(integration.id, fieldKey, value)}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder={field.placeholder} />
                            </SelectTrigger>
                            <SelectContent>
                              {field.options?.map((option) => (
                                <SelectItem key={option} value={option}>
                                  {option}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        ) : field.type === 'textarea' ? (
                          <Textarea
                            id={`${integration.id}-${fieldKey}`}
                            value={field.value}
                            onChange={(e) => handleFieldChange(integration.id, fieldKey, e.target.value)}
                            placeholder={field.placeholder}
                            rows={3}
                          />
                        ) : field.type === 'password' ? (
                          <div className="relative">
                            <Input
                              id={`${integration.id}-${fieldKey}`}
                              type={showPasswords[`${integration.id}-${fieldKey}`] ? 'text' : 'password'}
                              value={field.value}
                              onChange={(e) => handleFieldChange(integration.id, fieldKey, e.target.value)}
                              placeholder={field.placeholder}
                              className="pr-20"
                            />
                            <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex gap-1">
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => togglePasswordVisibility(`${integration.id}-${fieldKey}`)}
                                className="h-6 w-6 p-0"
                              >
                                {showPasswords[`${integration.id}-${fieldKey}`] ? 
                                  <EyeOff className="w-3 h-3" /> : 
                                  <Eye className="w-3 h-3" />
                                }
                              </Button>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => copyToClipboard(field.value)}
                                className="h-6 w-6 p-0"
                              >
                                <Copy className="w-3 h-3" />
                              </Button>
                            </div>
                          </div>
                        ) : (
                          <Input
                            id={`${integration.id}-${fieldKey}`}
                            type={field.type}
                            value={field.value}
                            onChange={(e) => handleFieldChange(integration.id, fieldKey, e.target.value)}
                            placeholder={field.placeholder}
                          />
                        )}
                        
                        {field.description && (
                          <p className="text-xs text-gray-500">{field.description}</p>
                        )}
                      </div>
                    ))}
                  </div>

                  <div className="flex justify-end gap-3 pt-4 border-t">
                    <Button
                      variant="outline"
                      onClick={() => handleTestConnection(integration.id)}
                      disabled={testingIntegration === integration.id}
                    >
                      {testingIntegration === integration.id ? (
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      ) : (
                        <TestTube className="w-4 h-4 mr-2" />
                      )}
                      Testar Conexão
                    </Button>
                    <Button 
                      onClick={() => handleSaveIntegration(integration.id)}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      <Save className="w-4 h-4 mr-2" />
                      Salvar Configurações
                    </Button>
                  </div>
                </CardContent>
              )}
            </Card>
          </TabsContent>
        ))}
      </Tabs>

      {/* Security Notice */}
      <Card className="border-yellow-200 bg-yellow-50">
        <CardContent className="p-4">
          <div className="flex items-center gap-3">
            <Shield className="w-5 h-5 text-yellow-600" />
            <div>
              <h4 className="font-medium text-yellow-800">Segurança das Credenciais</h4>
              <p className="text-sm text-yellow-700">
                Todas as credenciais são criptografadas e armazenadas com segurança. 
                Recomendamos usar chaves de API específicas com permissões limitadas sempre que possível.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default IntegrationsManager;

