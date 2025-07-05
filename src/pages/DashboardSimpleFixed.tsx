import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Users, 
  Building2, 
  Phone, 
  MessageSquare, 
  CheckCircle, 
  AlertCircle,
  TrendingUp,
  Activity,
  DollarSign,
  Target
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useTenant } from '@/contexts/TenantContext';

const DashboardSimple: React.FC = () => {
  const { user } = useAuth();
  const { currentTenant } = useTenant();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simular carregamento
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, [currentTenant]);

  const getUserLevelTitle = () => {
    if (user?.user_level === 'master') {
      return 'Painel Master - Multi-Tenant';
    }
    return `Dashboard - ${currentTenant?.name || 'Empresa'}`;
  };

  const getUserLevelDescription = () => {
    if (user?.user_level === 'master') {
      return 'Visão completa de todas as empresas e usuários';
    }
    return `Gestão completa da ${currentTenant?.name || 'sua empresa'}`;
  };

  const getMockData = () => {
    if (user?.user_level === 'master') {
      return {
        tenants: 15,
        totalUsers: 89,
        totalLeads: 1247,
        totalCalls: 3456,
        revenue: 125000,
        completedTasks: 234
      };
    } else {
      // Dados específicos do tenant atual
      const tenantMultiplier = currentTenant?.id === 'jt-telecom' ? 3 : 1;
      return {
        leads: Math.floor(45 * tenantMultiplier),
        clients: Math.floor(23 * tenantMultiplier),
        calls: Math.floor(156 * tenantMultiplier),
        messages: Math.floor(89 * tenantMultiplier),
        revenue: Math.floor(25000 * tenantMultiplier),
        completedTasks: Math.floor(12 * tenantMultiplier)
      };
    }
  };

  const mockData = getMockData();

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-blue-600">Dashboard</h1>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <Card key={i}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="h-4 bg-gray-200 rounded w-24 animate-pulse"></div>
                <div className="h-4 w-4 bg-gray-200 rounded animate-pulse"></div>
              </CardHeader>
              <CardContent>
                <div className="h-8 bg-gray-200 rounded w-16 animate-pulse mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-32 animate-pulse"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-blue-600">{getUserLevelTitle()}</h1>
          <p className="text-gray-600 mt-1">{getUserLevelDescription()}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Bem-vindo,</p>
          <p className="font-medium text-gray-900">{user?.name || 'Usuário'}</p>
        </div>
      </div>

      {/* Cards de Métricas */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {user?.user_level === 'master' && (
          <>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total de Empresas</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.tenants}</div>
                <p className="text-xs text-muted-foreground">Tenants ativas no sistema</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total de Usuários</CardTitle>
                <Building2 className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.totalUsers}</div>
                <p className="text-xs text-muted-foreground">Usuários ativos</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.totalLeads}</div>
                <p className="text-xs text-muted-foreground">Leads no sistema</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total de Ligações</CardTitle>
                <Phone className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.totalCalls}</div>
                <p className="text-xs text-muted-foreground">Ligações realizadas</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Receita Total</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">R$ {mockData.revenue.toLocaleString()}</div>
                <p className="text-xs text-muted-foreground">Receita do mês</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Tarefas Concluídas</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.completedTasks}</div>
                <p className="text-xs text-muted-foreground">Tarefas finalizadas</p>
              </CardContent>
            </Card>
          </>
        )}

        {user?.user_level !== 'master' && (
          <>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Leads</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.leads}</div>
                <p className="text-xs text-muted-foreground">
                  <span className="text-green-600">+12%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Clientes</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.clients}</div>
                <p className="text-xs text-muted-foreground">
                  <span className="text-green-600">+8%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Ligações</CardTitle>
                <Phone className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.calls}</div>
                <p className="text-xs text-muted-foreground">
                  <span className="text-blue-600">+5%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Mensagens</CardTitle>
                <MessageSquare className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.messages}</div>
                <p className="text-xs text-muted-foreground">
                  <span className="text-green-600">+15%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Receita</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">R$ {mockData.revenue.toLocaleString()}</div>
                <p className="text-xs text-muted-foreground">
                  <span className="text-green-600">+22%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Tarefas</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{mockData.completedTasks}</div>
                <p className="text-xs text-muted-foreground">Concluídas este mês</p>
              </CardContent>
            </Card>
          </>
        )}
      </div>

      {/* Status do Sistema */}
      <Card>
        <CardHeader>
          <CardTitle>Status do Sistema</CardTitle>
          <CardDescription>Monitoramento dos serviços</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm">Frontend: Funcionando</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm">Autenticação: Ativa</span>
            </div>
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-4 w-4 text-yellow-500" />
              <span className="text-sm">API: Em desenvolvimento</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardSimple;

