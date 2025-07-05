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
  Copy, 
  RefreshCw,
  Eye, 
  EyeOff,
  Plus,
  Trash2,
  Edit,
  TestTube,
  Key,
  Server,
  Webhook,
  Globe,
  Shield,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Loader2,
  Code,
  Download,
  Upload,
  Link,
  Settings,
  Database,
  Lock,
  Unlock,
  Clock,
  Activity,
  FileText,
  Zap
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/AuthContext';
import { useTenant } from '@/contexts/TenantContext';

interface ApiCredential {
  id: string;
  name: string;
  description: string;
  token: string;
  permissions: string[];
  status: 'active' | 'inactive' | 'expired';
  createdAt: string;
  expiresAt?: string;
  lastUsed?: string;
  usageCount: number;
  ipWhitelist?: string[];
}

interface WebhookEndpoint {
  id: string;
  name: string;
  url: string;
  events: string[];
  status: 'active' | 'inactive' | 'error';
  secret: string;
  headers?: { [key: string]: string };
  retryAttempts: number;
  timeout: number;
  createdAt: string;
  lastTriggered?: string;
  successCount: number;
  errorCount: number;
}

const ApiWebhookManager: React.FC = () => {
  const [activeTab, setActiveTab] = useState('api-config');
  const [credentials, setCredentials] = useState<ApiCredential[]>([]);
  const [webhooks, setWebhooks] = useState<WebhookEndpoint[]>([]);
  const [showTokens, setShowTokens] = useState<{[key: string]: boolean}>({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [testingWebhook, setTestingWebhook] = useState<string | null>(null);
  const { toast } = useToast();
  const { user } = useAuth();
  const { currentTenant } = useTenant();

  // Configurações da API
  const [apiConfig, setApiConfig] = useState({
    baseUrl: 'https://api.app.jttecnologia.com.br',
    version: 'v1',
    rateLimit: 1000,
    timeout: 30,
    enableCors: true,
    enableSsl: true,
    documentation: 'https://docs.api.jttecnologia.com.br'
  });

  useEffect(() => {
    loadCredentials();
    loadWebhooks();
  }, []);

  const loadCredentials = () => {
    const mockCredentials: ApiCredential[] = [
      {
        id: '1',
        name: 'CRM Principal',
        description: 'Token principal para acesso completo ao CRM',
        token: 'jt_live_sk_1234567890abcdef',
        permissions: ['leads:read', 'leads:write', 'clients:read', 'clients:write', 'analytics:read'],
        status: 'active',
        createdAt: '2025-01-01T10:00:00Z',
        expiresAt: '2025-12-31T23:59:59Z',
        lastUsed: '2025-07-05T14:30:00Z',
        usageCount: 1250,
        ipWhitelist: ['192.168.1.100', '10.0.0.50']
      },
      {
        id: '2',
        name: 'Integração Smartbot',
        description: 'Token específico para integração com Smartbot',
        token: 'jt_live_sk_smartbot_9876543210',
        permissions: ['leads:write', 'webhooks:receive'],
        status: 'active',
        createdAt: '2025-02-15T09:00:00Z',
        lastUsed: '2025-07-05T13:45:00Z',
        usageCount: 856
      },
      {
        id: '3',
        name: 'Analytics Dashboard',
        description: 'Token somente leitura para dashboards externos',
        token: 'jt_live_sk_analytics_readonly',
        permissions: ['analytics:read', 'reports:read'],
        status: 'active',
        createdAt: '2025-03-10T11:30:00Z',
        lastUsed: '2025-07-05T12:00:00Z',
        usageCount: 342
      }
    ];
    setCredentials(mockCredentials);
  };

  const loadWebhooks = () => {
    const mockWebhooks: WebhookEndpoint[] = [
      {
        id: '1',
        name: 'Notificações Slack',
        url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX',
        events: ['lead.created', 'lead.converted', 'client.updated'],
        status: 'active',
        secret: 'whsec_1234567890abcdef',
        retryAttempts: 3,
        timeout: 30,
        createdAt: '2025-01-15T10:00:00Z',
        lastTriggered: '2025-07-05T14:25:00Z',
        successCount: 1456,
        errorCount: 12
      },
      {
        id: '2',
        name: 'Sistema Externo CRM',
        url: 'https://external-crm.exemplo.com/webhook/jt-telecom',
        events: ['client.created', 'contract.signed', 'payment.received'],
        status: 'active',
        secret: 'whsec_external_abcdef123456',
        headers: {
          'Authorization': 'Bearer external_token_123',
          'Content-Type': 'application/json'
        },
        retryAttempts: 5,
        timeout: 45,
        createdAt: '2025-02-20T14:30:00Z',
        lastTriggered: '2025-07-05T13:50:00Z',
        successCount: 892,
        errorCount: 8
      },
      {
        id: '3',
        name: 'Automação Marketing',
        url: 'https://automation.marketing.com/webhook/leads',
        events: ['lead.created', 'lead.qualified', 'lead.lost'],
        status: 'inactive',
        secret: 'whsec_marketing_xyz789',
        retryAttempts: 3,
        timeout: 30,
        createdAt: '2025-03-05T16:00:00Z',
        successCount: 234,
        errorCount: 45
      }
    ];
    setWebhooks(mockWebhooks);
  };

  const generateNewCredential = async () => {
    setIsGenerating(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const newToken = `jt_live_sk_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const newCredential: ApiCredential = {
        id: Date.now().toString(),
        name: 'Nova Credencial',
        description: 'Token gerado automaticamente',
        token: newToken,
        permissions: ['leads:read'],
        status: 'active',
        createdAt: new Date().toISOString(),
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(),
        usageCount: 0
      };

      setCredentials(prev => [...prev, newCredential]);
      
      toast({
        title: 'Credencial gerada',
        description: 'Nova credencial de API foi gerada com sucesso.',
      });
    } catch (error) {
      toast({
        title: 'Erro',
        description: 'Não foi possível gerar a credencial.',
        variant: 'destructive',
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const revokeCredential = (credentialId: string) => {
    setCredentials(prev => prev.map(cred => 
      cred.id === credentialId 
        ? { ...cred, status: 'inactive' as const }
        : cred
    ));
    
    toast({
      title: 'Credencial revogada',
      description: 'A credencial foi revogada com sucesso.',
    });
  };

  const testWebhook = async (webhookId: string) => {
    setTestingWebhook(webhookId);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setWebhooks(prev => prev.map(webhook => 
        webhook.id === webhookId 
          ? { 
              ...webhook, 
              status: 'active',
              lastTriggered: new Date().toISOString(),
              successCount: webhook.successCount + 1
            }
          : webhook
      ));

      toast({
        title: 'Webhook testado',
        description: 'O webhook foi testado com sucesso.',
      });
    } catch (error) {
      setWebhooks(prev => prev.map(webhook => 
        webhook.id === webhookId 
          ? { 
              ...webhook, 
              status: 'error',
              errorCount: webhook.errorCount + 1
            }
          : webhook
      ));

      toast({
        title: 'Erro no webhook',
        description: 'Não foi possível conectar com o endpoint.',
        variant: 'destructive',
      });
    } finally {
      setTestingWebhook(null);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: 'Copiado',
      description: 'Texto copiado para a área de transferência.',
    });
  };

  const toggleTokenVisibility = (tokenId: string) => {
    setShowTokens(prev => ({
      ...prev,
      [tokenId]: !prev[tokenId]
    }));
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'inactive':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      default:
        return <AlertTriangle className="w-4 h-4 text-gray-500" />;
    }
  };

  const availableEvents = [
    'lead.created', 'lead.updated', 'lead.deleted', 'lead.converted', 'lead.qualified', 'lead.lost',
    'client.created', 'client.updated', 'client.deleted',
    'contract.created', 'contract.signed', 'contract.cancelled',
    'proposal.created', 'proposal.sent', 'proposal.accepted', 'proposal.rejected',
    'payment.received', 'payment.failed', 'payment.refunded',
    'task.created', 'task.completed', 'task.overdue',
    'user.login', 'user.logout', 'user.created'
  ];

  const availablePermissions = [
    'leads:read', 'leads:write', 'leads:delete',
    'clients:read', 'clients:write', 'clients:delete',
    'contracts:read', 'contracts:write', 'contracts:delete',
    'proposals:read', 'proposals:write', 'proposals:delete',
    'analytics:read', 'reports:read',
    'webhooks:receive', 'webhooks:send',
    'admin:read', 'admin:write'
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">API & Webhooks</h3>
          <p className="text-sm text-gray-600">
            Configure credenciais de API e webhooks para integrações externas
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
            <Globe className="w-3 h-3 mr-1" />
            {apiConfig.baseUrl}
          </Badge>
          <Button 
            onClick={generateNewCredential}
            disabled={isGenerating}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {isGenerating ? (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Key className="w-4 h-4 mr-2" />
            )}
            Gerar Credencial
          </Button>
        </div>
      </div>

      {/* API & Webhook Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="api-config">Configuração API</TabsTrigger>
          <TabsTrigger value="credentials">Credenciais</TabsTrigger>
          <TabsTrigger value="webhooks">Webhooks</TabsTrigger>
          <TabsTrigger value="documentation">Documentação</TabsTrigger>
        </TabsList>

        {/* API Configuration Tab */}
        <TabsContent value="api-config" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Server className="w-5 h-5 text-blue-600" />
                Configurações da API
              </CardTitle>
              <CardDescription>
                Configure os parâmetros principais da API do sistema
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="base-url">URL Base da API</Label>
                  <Input
                    id="base-url"
                    value={apiConfig.baseUrl}
                    onChange={(e) => setApiConfig(prev => ({ ...prev, baseUrl: e.target.value }))}
                    placeholder="https://api.app.jttecnologia.com.br"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="version">Versão da API</Label>
                  <Select 
                    value={apiConfig.version} 
                    onValueChange={(value) => setApiConfig(prev => ({ ...prev, version: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="v1">v1 (Atual)</SelectItem>
                      <SelectItem value="v2">v2 (Beta)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="rate-limit">Rate Limit (req/min)</Label>
                  <Input
                    id="rate-limit"
                    type="number"
                    value={apiConfig.rateLimit}
                    onChange={(e) => setApiConfig(prev => ({ ...prev, rateLimit: parseInt(e.target.value) }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="timeout">Timeout (segundos)</Label>
                  <Input
                    id="timeout"
                    type="number"
                    value={apiConfig.timeout}
                    onChange={(e) => setApiConfig(prev => ({ ...prev, timeout: parseInt(e.target.value) }))}
                  />
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Switch
                    id="enable-cors"
                    checked={apiConfig.enableCors}
                    onCheckedChange={(checked) => setApiConfig(prev => ({ ...prev, enableCors: checked }))}
                  />
                  <Label htmlFor="enable-cors">Habilitar CORS</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Switch
                    id="enable-ssl"
                    checked={apiConfig.enableSsl}
                    onCheckedChange={(checked) => setApiConfig(prev => ({ ...prev, enableSsl: checked }))}
                  />
                  <Label htmlFor="enable-ssl">Forçar SSL/HTTPS</Label>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="documentation">URL da Documentação</Label>
                <Input
                  id="documentation"
                  value={apiConfig.documentation}
                  onChange={(e) => setApiConfig(prev => ({ ...prev, documentation: e.target.value }))}
                  placeholder="https://docs.api.jttecnologia.com.br"
                />
              </div>

              <div className="flex justify-end pt-4">
                <Button className="bg-blue-600 hover:bg-blue-700">
                  <Save className="w-4 h-4 mr-2" />
                  Salvar Configurações
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* API Status */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-green-600" />
                Status da API
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-4">
                <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <div>
                    <div className="font-medium">API Online</div>
                    <div className="text-sm text-gray-500">Funcionando normalmente</div>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                  <Clock className="w-5 h-5 text-blue-500" />
                  <div>
                    <div className="font-medium">Uptime</div>
                    <div className="text-sm text-gray-500">99.9% (30 dias)</div>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg">
                  <Zap className="w-5 h-5 text-purple-500" />
                  <div>
                    <div className="font-medium">Requisições/min</div>
                    <div className="text-sm text-gray-500">847 (média)</div>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                  <Shield className="w-5 h-5 text-yellow-500" />
                  <div>
                    <div className="font-medium">Rate Limit</div>
                    <div className="text-sm text-gray-500">1000/min configurado</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Credentials Tab */}
        <TabsContent value="credentials" className="space-y-4">
          <div className="grid gap-4">
            {credentials.map((credential) => (
              <Card key={credential.id}>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                        <Key className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="font-medium">{credential.name}</h4>
                          {getStatusIcon(credential.status)}
                          <Badge variant={credential.status === 'active' ? 'default' : 'secondary'}>
                            {credential.status === 'active' ? 'Ativo' : 'Inativo'}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600">{credential.description}</p>
                        <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                          <span>Uso: {credential.usageCount} requisições</span>
                          {credential.lastUsed && (
                            <span>Último uso: {new Date(credential.lastUsed).toLocaleString('pt-BR')}</span>
                          )}
                          {credential.expiresAt && (
                            <span>Expira: {new Date(credential.expiresAt).toLocaleDateString('pt-BR')}</span>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => toggleTokenVisibility(credential.id)}
                      >
                        {showTokens[credential.id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(credential.token)}
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => revokeCredential(credential.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                  
                  {/* Token Display */}
                  <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <code className="text-sm font-mono">
                        {showTokens[credential.id] 
                          ? credential.token 
                          : credential.token.replace(/./g, '•').substring(0, 20) + '...'
                        }
                      </code>
                    </div>
                  </div>

                  {/* Permissions */}
                  <div className="mt-3">
                    <Label className="text-xs font-medium text-gray-700">Permissões:</Label>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {credential.permissions.map((permission) => (
                        <Badge key={permission} variant="outline" className="text-xs">
                          {permission}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* IP Whitelist */}
                  {credential.ipWhitelist && (
                    <div className="mt-2">
                      <Label className="text-xs font-medium text-gray-700">IPs Permitidos:</Label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {credential.ipWhitelist.map((ip) => (
                          <Badge key={ip} variant="secondary" className="text-xs">
                            {ip}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Webhooks Tab */}
        <TabsContent value="webhooks" className="space-y-4">
          <div className="flex justify-end">
            <Button className="bg-green-600 hover:bg-green-700">
              <Plus className="w-4 h-4 mr-2" />
              Novo Webhook
            </Button>
          </div>

          <div className="grid gap-4">
            {webhooks.map((webhook) => (
              <Card key={webhook.id}>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <Webhook className="w-5 h-5 text-green-600" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="font-medium">{webhook.name}</h4>
                          {getStatusIcon(testingWebhook === webhook.id ? 'active' : webhook.status)}
                          <Badge variant={webhook.status === 'active' ? 'default' : 'secondary'}>
                            {webhook.status === 'active' ? 'Ativo' : webhook.status === 'error' ? 'Erro' : 'Inativo'}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 font-mono">{webhook.url}</p>
                        <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                          <span>Sucessos: {webhook.successCount}</span>
                          <span>Erros: {webhook.errorCount}</span>
                          {webhook.lastTriggered && (
                            <span>Último disparo: {new Date(webhook.lastTriggered).toLocaleString('pt-BR')}</span>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => testWebhook(webhook.id)}
                        disabled={testingWebhook === webhook.id}
                      >
                        {testingWebhook === webhook.id ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <TestTube className="w-4 h-4" />
                        )}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>

                  {/* Events */}
                  <div className="mt-3">
                    <Label className="text-xs font-medium text-gray-700">Eventos:</Label>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {webhook.events.map((event) => (
                        <Badge key={event} variant="outline" className="text-xs">
                          {event}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Configuration */}
                  <div className="mt-3 grid gap-2 md:grid-cols-3 text-xs">
                    <div>
                      <span className="font-medium text-gray-700">Timeout:</span> {webhook.timeout}s
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Tentativas:</span> {webhook.retryAttempts}
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Secret:</span> 
                      <code className="ml-1 bg-gray-100 px-1 rounded">
                        {webhook.secret.substring(0, 10)}...
                      </code>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Documentation Tab */}
        <TabsContent value="documentation" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-blue-600" />
                Documentação da API
              </CardTitle>
              <CardDescription>
                Exemplos de uso e referência completa da API
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Quick Start */}
              <div className="space-y-3">
                <h4 className="font-medium">Início Rápido</h4>
                <div className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm">
{`# Autenticação
curl -H "Authorization: Bearer jt_live_sk_your_token_here" \\
     -H "Content-Type: application/json" \\
     ${apiConfig.baseUrl}/${apiConfig.version}/leads

# Criar um novo lead
curl -X POST ${apiConfig.baseUrl}/${apiConfig.version}/leads \\
     -H "Authorization: Bearer jt_live_sk_your_token_here" \\
     -H "Content-Type: application/json" \\
     -d '{
       "name": "João Silva",
       "email": "joao@exemplo.com",
       "phone": "11999999999",
       "company": "Empresa ABC"
     }'`}
                  </pre>
                </div>
              </div>

              {/* Endpoints */}
              <div className="space-y-3">
                <h4 className="font-medium">Principais Endpoints</h4>
                <div className="space-y-2">
                  {[
                    { method: 'GET', path: '/leads', description: 'Listar todos os leads' },
                    { method: 'POST', path: '/leads', description: 'Criar novo lead' },
                    { method: 'GET', path: '/leads/{id}', description: 'Obter lead específico' },
                    { method: 'PUT', path: '/leads/{id}', description: 'Atualizar lead' },
                    { method: 'DELETE', path: '/leads/{id}', description: 'Deletar lead' },
                    { method: 'GET', path: '/clients', description: 'Listar todos os clientes' },
                    { method: 'POST', path: '/clients', description: 'Criar novo cliente' },
                    { method: 'GET', path: '/analytics/overview', description: 'Dados do dashboard' },
                    { method: 'POST', path: '/webhooks/receive', description: 'Receber webhook' }
                  ].map((endpoint, index) => (
                    <div key={index} className="flex items-center gap-3 p-2 bg-gray-50 rounded">
                      <Badge variant={endpoint.method === 'GET' ? 'default' : endpoint.method === 'POST' ? 'secondary' : 'outline'}>
                        {endpoint.method}
                      </Badge>
                      <code className="text-sm font-mono">{endpoint.path}</code>
                      <span className="text-sm text-gray-600">{endpoint.description}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Links */}
              <div className="flex gap-3">
                <Button variant="outline" asChild>
                  <a href={apiConfig.documentation} target="_blank" rel="noopener noreferrer">
                    <FileText className="w-4 h-4 mr-2" />
                    Documentação Completa
                  </a>
                </Button>
                <Button variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Download OpenAPI Spec
                </Button>
                <Button variant="outline">
                  <Code className="w-4 h-4 mr-2" />
                  Exemplos de Código
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ApiWebhookManager;

