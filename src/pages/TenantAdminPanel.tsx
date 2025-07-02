import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';
import { Users, UserPlus, Settings, BarChart3, Shield, Eye, EyeOff } from 'lucide-react';

interface TenantUser {
  id: number;
  name: string;
  email: string;
  role: string;
  status: string;
  created_at: string;
  last_login: string;
}

interface TenantStats {
  users: {
    total: number;
    active: number;
    inactive: number;
  };
  activity: {
    logins_today: number;
    logins_week: number;
    logins_month: number;
  };
}

interface TenantInfo {
  id: number;
  name: string;
  domain: string;
  status: string;
  created_at: string;
}

export default function TenantAdminPanel() {
  const { user, logout } = useAuth();
  const [users, setUsers] = useState<TenantUser[]>([]);
  const [stats, setStats] = useState<TenantStats | null>(null);
  const [tenantInfo, setTenantInfo] = useState<TenantInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [newUser, setNewUser] = useState({
    name: '',
    email: '',
    password: '',
    role: 'user'
  });

  useEffect(() => {
    if (user?.user_level !== 'admin') {
      logout();
      return;
    }
    loadData();
  }, [user]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [usersResponse, statsResponse, tenantResponse] = await Promise.all([
        api.get('/tenant-admin/users'),
        api.get('/tenant-admin/stats'),
        api.get('/tenant-admin/info')
      ]);
      setUsers(usersResponse.data.users);
      setStats(statsResponse.data);
      setTenantInfo(tenantResponse.data.tenant);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const createUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/tenant-admin/users', newUser);
      alert(`Usuário criado com sucesso!\n\nCredenciais:\nEmail: ${response.data.user.email}\nSenha: ${newUser.password}\n\nO usuário deve alterar a senha no primeiro login.`);
      setNewUser({ name: '', email: '', password: '', role: 'user' });
      setShowCreateForm(false);
      loadData();
    } catch (error: any) {
      alert(`Erro ao criar usuário: ${error.response?.data?.error || error.message}`);
    }
  };

  const updateUserStatus = async (userId: number, status: string) => {
    try {
      await api.put(`/tenant-admin/users/${userId}`, { status });
      loadData();
    } catch (error: any) {
      alert(`Erro ao atualizar usuário: ${error.response?.data?.error || error.message}`);
    }
  };

  const resetUserPassword = async (userId: number) => {
    if (!confirm('Tem certeza que deseja resetar a senha deste usuário?')) return;
    
    try {
      const response = await api.post(`/tenant-admin/users/${userId}/reset-password`);
      alert(`Senha resetada com sucesso!\n\nNova senha temporária: ${response.data.temporary_password}\n\nO usuário deve alterar a senha no próximo login.`);
    } catch (error: any) {
      alert(`Erro ao resetar senha: ${error.response?.data?.error || error.message}`);
    }
  };

  const generatePassword = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%';
    let password = '';
    for (let i = 0; i < 12; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setNewUser({...newUser, password});
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando painel administrativo...</p>
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
            <div className="flex items-center space-x-4">
              <Shield className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-semibold text-gray-900">
                  Painel Administrativo
                </h1>
                <p className="text-sm text-gray-600">
                  {tenantInfo?.name || 'Carregando...'}
                </p>
              </div>
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
        {/* Informações da Tenant */}
        {tenantInfo && (
          <div className="bg-white p-6 rounded-lg shadow mb-8">
            <h2 className="text-lg font-medium mb-4 flex items-center">
              <Settings className="h-5 w-5 mr-2 text-blue-600" />
              Informações da Empresa
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Nome da Empresa</label>
                <p className="text-lg font-semibold text-gray-900">{tenantInfo.name}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Domínio</label>
                <p className="text-lg text-gray-900">{tenantInfo.domain}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Status</label>
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  tenantInfo.status === 'active' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {tenantInfo.status === 'active' ? 'Ativa' : 'Inativa'}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Estatísticas */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Total de Usuários</h3>
                  <p className="text-3xl font-bold text-blue-600">{stats.users.total}</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Usuários Ativos</h3>
                  <p className="text-3xl font-bold text-green-600">{stats.users.active}</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center">
                <BarChart3 className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Logins Hoje</h3>
                  <p className="text-3xl font-bold text-purple-600">{stats.activity.logins_today}</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center">
                <BarChart3 className="h-8 w-8 text-indigo-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Logins Mês</h3>
                  <p className="text-3xl font-bold text-indigo-600">{stats.activity.logins_month}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Ações */}
        <div className="mb-6">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center"
          >
            <UserPlus className="h-4 w-4 mr-2" />
            {showCreateForm ? 'Cancelar' : 'Novo Usuário'}
          </button>
        </div>

        {/* Formulário de criação */}
        {showCreateForm && (
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <h2 className="text-lg font-medium mb-4">Criar Novo Usuário</h2>
            <form onSubmit={createUser} className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome Completo
                </label>
                <input
                  type="text"
                  value={newUser.name}
                  onChange={(e) => setNewUser({...newUser, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={newUser.email}
                  onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Senha Temporária
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={newUser.password}
                    onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 pr-20"
                    required
                  />
                  <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex space-x-1">
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                    <button
                      type="button"
                      onClick={generatePassword}
                      className="text-blue-600 hover:text-blue-800 text-xs"
                      title="Gerar senha"
                    >
                      🎲
                    </button>
                  </div>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Função
                </label>
                <select
                  value={newUser.role}
                  onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                >
                  <option value="user">Usuário</option>
                  <option value="manager">Gerente</option>
                  <option value="supervisor">Supervisor</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <button
                  type="submit"
                  className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
                >
                  Criar Usuário
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Lista de Usuários */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium">Usuários da Empresa</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Usuário
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Função
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Último Login
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{user.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{user.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900 capitalize">{user.role}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        user.status === 'active' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {user.status === 'active' ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">
                        {user.last_login ? new Date(user.last_login).toLocaleDateString('pt-BR') : 'Nunca'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      {user.status === 'active' ? (
                        <button
                          onClick={() => updateUserStatus(user.id, 'inactive')}
                          className="text-red-600 hover:text-red-900"
                        >
                          Desativar
                        </button>
                      ) : (
                        <button
                          onClick={() => updateUserStatus(user.id, 'active')}
                          className="text-green-600 hover:text-green-900"
                        >
                          Ativar
                        </button>
                      )}
                      <button
                        onClick={() => resetUserPassword(user.id)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Reset Senha
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Nota sobre Multi-Tenant */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <Shield className="h-5 w-5 text-blue-600 mr-2" />
            <div>
              <h3 className="text-sm font-medium text-blue-800">Sistema Multi-Tenant</h3>
              <p className="text-sm text-blue-700 mt-1">
                Você está gerenciando apenas os usuários da sua empresa. Os dados são completamente isolados de outras empresas no sistema.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

