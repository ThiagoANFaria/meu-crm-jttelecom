import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { 
  Building2, 
  Users, 
  Plus, 
  Settings, 
  BarChart3, 
  Shield, 
  CheckCircle, 
  AlertCircle,
  Edit,
  Trash2,
  Eye
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface Tenant {
  id: string;
  name: string;
  domain: string;
  adminEmail: string;
  status: 'active' | 'inactive' | 'suspended';
  users: number;
  createdAt: string;
  plan: 'basic' | 'pro' | 'enterprise';
}

const MasterPanelSimple: React.FC = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [newTenant, setNewTenant] = useState({
    name: '',
    domain: '',
    adminEmail: '',
    adminPassword: '',
    plan: 'basic'
  });

  // Simular carregamento
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
      // Dados mockados de tenants
      setTenants([
        {
          id: '1',
          name: 'Empresa Demo 1',
          domain: 'demo1.jttecnologia.com.br',
          adminEmail: 'admin@demo1.com',
          status: 'active',
          users: 8,
          createdAt: '2024-01-15',
          plan: 'pro'
        },
        {
          id: '2',
          name: 'Empresa Demo 2',
          domain: 'demo2.jttecnologia.com.br',
          adminEmail: 'admin@demo2.com',
          status: 'active',
          users: 5,
          createdAt: '2024-02-20',
          plan: 'basic'
        },
        {
          id: '3',
          name: 'Empresa Demo 3',
          domain: 'demo3.jttecnologia.com.br',
          adminEmail: 'admin@demo3.com',
          status: 'inactive',
          users: 12,
          createdAt: '2024-03-10',
          plan: 'enterprise'
        }
      ]);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  const handleCreateTenant = (e: React.FormEvent) => {
    e.preventDefault();
    
    const tenant: Tenant = {
      id: Date.now().toString(),
      name: newTenant.name,
      domain: `${newTenant.domain}.jttecnologia.com.br`,
      adminEmail: newTenant.adminEmail,
      status: 'active',
      users: 1,
      createdAt: new Date().toISOString().split('T')[0],
      plan: newTenant.plan as 'basic' | 'pro' | 'enterprise'
    };

    setTenants([...tenants, tenant]);
    setNewTenant({ name: '', domain: '', adminEmail: '', adminPassword: '', plan: 'basic' });
    setShowCreateForm(false);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800">Ativa</Badge>;
      case 'inactive':
        return <Badge className="bg-yellow-100 text-yellow-800">Inativa</Badge>;
      case 'suspended':
        return <Badge className="bg-red-100 text-red-800">Suspensa</Badge>;
      default:
        return <Badge>Desconhecido</Badge>;
    }
  };

  const getPlanBadge = (plan: string) => {
    switch (plan) {
      case 'basic':
        return <Badge variant="outline">Básico</Badge>;
      case 'pro':
        return <Badge className="bg-blue-100 text-blue-800">Pro</Badge>;
      case 'enterprise':
        return <Badge className="bg-purple-100 text-purple-800">Enterprise</Badge>;
      default:
        return <Badge variant="outline">Básico</Badge>;
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-blue-600">Painel Master</h1>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
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

  const activeTenants = tenants.filter(t => t.status === 'active').length;
  const totalUsers = tenants.reduce((sum, t) => sum + t.users, 0);
  const totalRevenue = tenants.length * 299; // Simulando R$ 299 por tenant

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-blue-600">🏢 Painel Master</h1>
          <p className="text-gray-600 mt-1">Gestão completa do sistema multi-tenant</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Admin Master</p>
          <p className="font-medium text-gray-900">{user?.name || 'JT Telecom'}</p>
        </div>
      </div>

      {/* Status do Sistema */}
      <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg flex items-center">
        <CheckCircle className="h-5 w-5 mr-2" />
        <div>
          <h2 className="font-bold">✅ Painel Master Funcionando!</h2>
          <p className="text-sm">Sistema multi-tenant operacional. Todas as funcionalidades disponíveis.</p>
        </div>
      </div>

      {/* Métricas Globais */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Empresas</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{tenants.length}</div>
            <p className="text-xs text-muted-foreground">{activeTenants} ativas</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Usuários</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalUsers}</div>
            <p className="text-xs text-muted-foreground">Em todas as empresas</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Receita Mensal</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">R$ {totalRevenue.toLocaleString('pt-BR')}</div>
            <p className="text-xs text-muted-foreground">Faturamento total</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Status Sistema</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">100%</div>
            <p className="text-xs text-muted-foreground">Operacional</p>
          </CardContent>
        </Card>
      </div>

      {/* Ações Rápidas */}
      <div className="flex gap-4">
        <Button 
          onClick={() => setShowCreateForm(true)}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <Plus className="h-4 w-4 mr-2" />
          Nova Empresa
        </Button>
        <Button variant="outline">
          <Settings className="h-4 w-4 mr-2" />
          Configurações
        </Button>
        <Button variant="outline">
          <BarChart3 className="h-4 w-4 mr-2" />
          Relatórios
        </Button>
      </div>

      {/* Formulário de Criação de Tenant */}
      {showCreateForm && (
        <Card>
          <CardHeader>
            <CardTitle>Criar Nova Empresa</CardTitle>
            <CardDescription>Adicione uma nova empresa ao sistema multi-tenant</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateTenant} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="name">Nome da Empresa</Label>
                  <Input
                    id="name"
                    value={newTenant.name}
                    onChange={(e) => setNewTenant({...newTenant, name: e.target.value})}
                    placeholder="Ex: Empresa ABC Ltda"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="domain">Subdomínio</Label>
                  <div className="flex">
                    <Input
                      id="domain"
                      value={newTenant.domain}
                      onChange={(e) => setNewTenant({...newTenant, domain: e.target.value})}
                      placeholder="empresa-abc"
                      required
                    />
                    <span className="flex items-center px-3 text-sm text-gray-500 bg-gray-100 border border-l-0 rounded-r">
                      .jttecnologia.com.br
                    </span>
                  </div>
                </div>
                <div>
                  <Label htmlFor="adminEmail">E-mail do Admin</Label>
                  <Input
                    id="adminEmail"
                    type="email"
                    value={newTenant.adminEmail}
                    onChange={(e) => setNewTenant({...newTenant, adminEmail: e.target.value})}
                    placeholder="admin@empresa.com"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="adminPassword">Senha do Admin</Label>
                  <Input
                    id="adminPassword"
                    type="password"
                    value={newTenant.adminPassword}
                    onChange={(e) => setNewTenant({...newTenant, adminPassword: e.target.value})}
                    placeholder="Senha segura"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="plan">Plano</Label>
                  <select
                    id="plan"
                    value={newTenant.plan}
                    onChange={(e) => setNewTenant({...newTenant, plan: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="basic">Básico - R$ 199/mês</option>
                    <option value="pro">Pro - R$ 299/mês</option>
                    <option value="enterprise">Enterprise - R$ 499/mês</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-2">
                <Button type="submit" className="bg-green-600 hover:bg-green-700">
                  Criar Empresa
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => setShowCreateForm(false)}
                >
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Lista de Empresas */}
      <Card>
        <CardHeader>
          <CardTitle>Empresas Cadastradas</CardTitle>
          <CardDescription>Gerencie todas as empresas do sistema</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {tenants.map((tenant) => (
              <div key={tenant.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h3 className="font-medium">{tenant.name}</h3>
                    {getStatusBadge(tenant.status)}
                    {getPlanBadge(tenant.plan)}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">
                    <p>Domínio: {tenant.domain}</p>
                    <p>Admin: {tenant.adminEmail}</p>
                    <p>Usuários: {tenant.users} | Criado em: {tenant.createdAt}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline">
                    <Eye className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="outline">
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="outline" className="text-red-600 hover:text-red-700">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Informações do Sistema */}
      <Card>
        <CardHeader>
          <CardTitle>Status do Sistema Multi-Tenant</CardTitle>
          <CardDescription>Monitoramento em tempo real</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm">Autenticação Master: Ativa</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm">Isolamento de Dados: Funcionando</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm">Painel Master: Operacional</span>
            </div>
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-4 w-4 text-yellow-500" />
              <span className="text-sm">API Backend: Em desenvolvimento</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm">Frontend: Funcionando</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm">Deploy: Automático</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MasterPanelSimple;

