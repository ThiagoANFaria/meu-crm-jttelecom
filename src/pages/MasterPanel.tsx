import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';

interface Tenant {
  id: number;
  name: string;
  domain: string;
  admin_email: string;
  admin_name: string;
  status: string;
  created_at: string;
  users_count: number;
}

interface Stats {
  tenants: {
    total: number;
    active: number;
    inactive: number;
  };
  users: {
    total: number;
    active: number;
    inactive: number;
  };
}

export default function MasterPanel() {
  const { user, logout } = useAuth();
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTenant, setNewTenant] = useState({
    tenant_name: '',
    domain: '',
    admin_name: '',
    admin_email: ''
  });

  useEffect(() => {
    if (user?.user_level !== 'master') {
      logout();
      return;
    }
    loadData();
  }, [user]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [tenantsResponse, statsResponse] = await Promise.all([
        api.get('/master/tenants'),
        api.get('/master/stats')
      ]);
      setTenants(tenantsResponse.data.tenants);
      setStats(statsResponse.data);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const createTenant = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/master/tenants', newTenant);
      alert(`Tenant criada com sucesso!\n\nCredenciais do Admin:\nEmail: ${response.data.admin_credentials.email}\nSenha temporária: ${response.data.admin_credentials.temporary_password}`);
      setNewTenant({ tenant_name: '', domain: '', admin_name: '', admin_email: '' });
      setShowCreateForm(false);
      loadData();
    } catch (error: any) {
      alert(`Erro ao criar tenant: ${error.response?.data?.error || error.message}`);
    }
  };

  const updateTenantStatus = async (tenantId: number, status: string) => {
    try {
      await api.put(`/master/tenants/${tenantId}`, { status });
      loadData();
    } catch (error: any) {
      alert(`Erro ao atualizar tenant: ${error.response?.data?.error || error.message}`);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando painel Master...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                🏢 Painel Master - JT Telecom
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Olá, {user?.name}
              </span>
              <button
                onClick={logout}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Estatísticas */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Total de Tenants</h3>
              <p className="text-3xl font-bold text-blue-600">{stats.tenants.total}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Tenants Ativas</h3>
              <p className="text-3xl font-bold text-green-600">{stats.tenants.active}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Total de Usuários</h3>
              <p className="text-3xl font-bold text-purple-600">{stats.users.total}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Usuários Ativos</h3>
              <p className="text-3xl font-bold text-indigo-600">{stats.users.active}</p>
            </div>
          </div>
        )}

        {/* Ações */}
        <div className="mb-6">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            {showCreateForm ? 'Cancelar' : '+ Nova Tenant'}
          </button>
        </div>

        {/* Formulário de criação */}
        {showCreateForm && (
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h2 className="text-lg font-medium mb-4">Criar Nova Tenant</h2>
            <form onSubmit={createTenant} className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome da Empresa
                </label>
                <input
                  type="text"
                  value={newTenant.tenant_name}
                  onChange={(e) => setNewTenant({...newTenant, tenant_name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Domínio
                </label>
                <input
                  type="text"
                  value={newTenant.domain}
                  onChange={(e) => setNewTenant({...newTenant, domain: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="exemplo.com"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome do Admin
                </label>
                <input
                  type="text"
                  value={newTenant.admin_name}
                  onChange={(e) => setNewTenant({...newTenant, admin_name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email do Admin
                </label>
                <input
                  type="email"
                  value={newTenant.admin_email}
                  onChange={(e) => setNewTenant({...newTenant, admin_email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>
              <div className="md:col-span-2">
                <button
                  type="submit"
                  className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
                >
                  Criar Tenant
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Lista de Tenants */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium">Tenants Cadastradas</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Empresa
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Domínio
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Admin
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Usuários
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tenants.map((tenant) => (
                  <tr key={tenant.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{tenant.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{tenant.domain}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{tenant.admin_name}</div>
                      <div className="text-sm text-gray-500">{tenant.admin_email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{tenant.users_count}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        tenant.status === 'active' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {tenant.status === 'active' ? 'Ativa' : 'Inativa'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      {tenant.status === 'active' ? (
                        <button
                          onClick={() => updateTenantStatus(tenant.id, 'inactive')}
                          className="text-red-600 hover:text-red-900 mr-3"
                        >
                          Desativar
                        </button>
                      ) : (
                        <button
                          onClick={() => updateTenantStatus(tenant.id, 'active')}
                          className="text-green-600 hover:text-green-900 mr-3"
                        >
                          Ativar
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

