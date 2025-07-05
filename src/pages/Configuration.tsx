import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Settings, 
  Users, 
  Tags, 
  Workflow, 
  Shield, 
  Plus,
  Edit,
  Trash2,
  Save,
  AlertTriangle,
  CheckCircle,
  Info,
  Database,
  Filter,
  Palette,
  Lock,
  Unlock,
  UserCheck,
  UserX,
  Eye,
  EyeOff
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';

// Importar subcomponentes
import CustomFieldsManager from '@/components/configuration/CustomFieldsManager';
import SalesFunnelManager from '@/components/configuration/SalesFunnelManager';
import TagsManager from '@/components/configuration/TagsManager';
import PermissionsManager from '@/components/configuration/PermissionsManager';
import OriginFieldsManager from '@/components/configuration/OriginFieldsManager';
import IntegrationsManager from '@/components/configuration/IntegrationsManager';
import ApiWebhookManager from '@/components/configuration/ApiWebhookManager';

const Configuration: React.FC = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [activeTab, setActiveTab] = useState('fields');
  const [isLoading, setIsLoading] = useState(false);

  // Verificar se o usuário tem permissão de administrador
  const isAdmin = user?.user_level === 'admin' || user?.user_level === 'master';

  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center h-64">
        <Card className="w-96">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mb-4">
              <Lock className="w-6 h-6 text-red-600" />
            </div>
            <CardTitle className="text-red-600">Acesso Negado</CardTitle>
            <CardDescription>
              Apenas administradores podem acessar as configurações do sistema.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  const configurationSections = [
    {
      id: 'fields',
      title: 'Campos Personalizados',
      description: 'Gerenciar campos adicionais para Leads e Clientes',
      icon: Database,
      color: 'bg-blue-500',
      component: CustomFieldsManager
    },
    {
      id: 'funnels',
      title: 'Funis de Vendas',
      description: 'Definir funis e etapas personalizadas',
      icon: Workflow,
      color: 'bg-green-500',
      component: SalesFunnelManager
    },
    {
      id: 'tags',
      title: 'Gestão de Tags',
      description: 'Criar e controlar tags com cores personalizáveis',
      icon: Tags,
      color: 'bg-purple-500',
      component: TagsManager
    },
    {
      id: 'permissions',
      title: 'Permissões',
      description: 'Configurar permissões por perfil de usuário',
      icon: Shield,
      color: 'bg-orange-500',
      component: PermissionsManager
    },
    {
      id: 'origins',
      title: 'Campos por Origem',
      description: 'Configurar campos específicos por origem do Lead',
      icon: Filter,
      color: 'bg-pink-500',
      component: OriginFieldsManager
    },
    {
      id: 'integrations',
      title: 'Integrações',
      description: 'PABX, Smartbot, Email, OpenAI e outras APIs',
      icon: Settings,
      color: 'bg-indigo-500',
      component: IntegrationsManager
    },
    {
      id: 'api-webhooks',
      title: 'API & Webhooks',
      description: 'Credenciais, endpoints e webhooks externos',
      icon: Globe,
      color: 'bg-teal-500',
      component: ApiWebhookManager
    }
  ];

  const handleSaveConfiguration = async () => {
    try {
      setIsLoading(true);
      // Simular salvamento
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toast({
        title: 'Configurações salvas',
        description: 'Todas as configurações foram salvas com sucesso.',
      });
    } catch (error) {
      toast({
        title: 'Erro',
        description: 'Não foi possível salvar as configurações.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Settings className="w-8 h-8 text-blue-600" />
          <div>
            <h1 className="text-3xl font-bold text-blue-600">Configurações</h1>
            <p className="text-gray-600">Gerenciar configurações avançadas do sistema</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
            <UserCheck className="w-3 h-3 mr-1" />
            Administrador
          </Badge>
          <Button 
            onClick={handleSaveConfiguration}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <Save className="w-4 h-4 mr-2" />
            {isLoading ? 'Salvando...' : 'Salvar Tudo'}
          </Button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid gap-4 md:grid-cols-7">
        {configurationSections.map((section) => {
          const IconComponent = section.icon;
          return (
            <Card 
              key={section.id}
              className={`cursor-pointer transition-all hover:shadow-md ${
                activeTab === section.id ? 'ring-2 ring-blue-500 bg-blue-50' : ''
              }`}
              onClick={() => setActiveTab(section.id)}
            >
              <CardHeader className="pb-3">
                <div className={`w-10 h-10 ${section.color} rounded-lg flex items-center justify-center mb-2`}>
                  <IconComponent className="w-5 h-5 text-white" />
                </div>
                <CardTitle className="text-sm font-medium">{section.title}</CardTitle>
                <CardDescription className="text-xs">{section.description}</CardDescription>
              </CardHeader>
            </Card>
          );
        })}
      </div>

      {/* Configuration Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-7">
          {configurationSections.map((section) => (
            <TabsTrigger key={section.id} value={section.id} className="text-xs">
              {section.title}
            </TabsTrigger>
          ))}
        </TabsList>

        {configurationSections.map((section) => {
          const ComponentToRender = section.component;
          return (
            <TabsContent key={section.id} value={section.id} className="space-y-4">
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className={`w-8 h-8 ${section.color} rounded-lg flex items-center justify-center`}>
                      <section.icon className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <CardTitle>{section.title}</CardTitle>
                      <CardDescription>{section.description}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <ComponentToRender />
                </CardContent>
              </Card>
            </TabsContent>
          );
        })}
      </Tabs>

      {/* System Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info className="w-5 h-5 text-blue-600" />
            Informações do Sistema
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <div>
                <div className="font-medium">Sistema Ativo</div>
                <div className="text-sm text-gray-500">Todas as configurações funcionais</div>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <Users className="w-5 h-5 text-blue-500" />
              <div>
                <div className="font-medium">Usuário: {user?.name}</div>
                <div className="text-sm text-gray-500">Nível: {user?.user_level}</div>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <Settings className="w-5 h-5 text-purple-500" />
              <div>
                <div className="font-medium">Última Atualização</div>
                <div className="text-sm text-gray-500">{new Date().toLocaleDateString('pt-BR')}</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Configuration;

