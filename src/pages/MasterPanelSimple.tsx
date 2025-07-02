import { useAuth } from '../context/AuthContext';

export default function MasterPanelSimple() {
  const { user, logout } = useAuth();

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
                Olá, {user?.name || 'Admin Master'}
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
        {/* Mensagem de Sucesso */}
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
          <h2 className="font-bold">🎉 Painel Master Funcionando!</h2>
          <p>Você está logado como Admin Master e pode acessar este painel.</p>
        </div>

        {/* Informações do Usuário */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-lg font-medium mb-4">Informações do Usuário</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Nome:</label>
              <p className="text-gray-900">{user?.name || 'Admin Master JT Telecom'}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Email:</label>
              <p className="text-gray-900">{user?.email || 'master@jttecnologia.com.br'}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Nível:</label>
              <p className="text-gray-900">{user?.user_level || 'master'}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Status:</label>
              <p className="text-gray-900">{user?.status || 'active'}</p>
            </div>
          </div>
        </div>

        {/* Funcionalidades Disponíveis */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-4">Funcionalidades do Painel Master</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="border border-gray-200 p-4 rounded-lg">
              <h3 className="font-medium text-gray-900 mb-2">🏢 Gestão de Tenants</h3>
              <p className="text-sm text-gray-600">Criar, editar e gerenciar empresas no sistema</p>
              <button className="mt-2 text-blue-600 hover:text-blue-800 text-sm">
                Em desenvolvimento
              </button>
            </div>
            <div className="border border-gray-200 p-4 rounded-lg">
              <h3 className="font-medium text-gray-900 mb-2">👥 Gestão de Usuários</h3>
              <p className="text-sm text-gray-600">Visualizar e gerenciar usuários de todas as empresas</p>
              <button className="mt-2 text-blue-600 hover:text-blue-800 text-sm">
                Em desenvolvimento
              </button>
            </div>
            <div className="border border-gray-200 p-4 rounded-lg">
              <h3 className="font-medium text-gray-900 mb-2">📊 Relatórios Globais</h3>
              <p className="text-sm text-gray-600">Estatísticas e relatórios de todo o sistema</p>
              <button className="mt-2 text-blue-600 hover:text-blue-800 text-sm">
                Em desenvolvimento
              </button>
            </div>
          </div>
        </div>

        {/* Instruções */}
        <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded mt-6">
          <h3 className="font-bold">📋 Próximos Passos:</h3>
          <ul className="list-disc list-inside mt-2 space-y-1">
            <li>Implementar API endpoints para gestão de tenants</li>
            <li>Conectar com banco de dados</li>
            <li>Adicionar funcionalidades completas de CRUD</li>
            <li>Implementar relatórios e estatísticas</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

