import React, { useState } from 'react'
import { Search, Bell, Settings, User, ChevronDown, Plus } from 'lucide-react'

const Header = ({ activeModule }) => {
  const [showNotifications, setShowNotifications] = useState(false)
  const [showUserMenu, setShowUserMenu] = useState(false)

  const getModuleTitle = () => {
    const titles = {
      dashboard: 'Dashboard',
      leads: 'Gestão de Leads',
      clients: 'Gestão de Clientes',
      proposals: 'Propostas Comerciais',
      contracts: 'Contratos',
      tasks: 'Tarefas',
      chatbot: 'Chatbot',
      telephony: 'Telefonia',
      automation: 'Automação'
    }
    return titles[activeModule] || 'CRM JT Telecom'
  }

  const getModuleDescription = () => {
    const descriptions = {
      dashboard: 'Visão geral do seu negócio',
      leads: 'Gerencie seus leads e oportunidades',
      clients: 'Cadastro e gestão de clientes',
      proposals: 'Crie e gerencie propostas comerciais',
      contracts: 'Contratos e documentos legais',
      tasks: 'Organize suas tarefas e atividades',
      chatbot: 'Automação de atendimento',
      telephony: 'Sistema de telefonia integrado',
      automation: 'Workflows e automações'
    }
    return descriptions[activeModule] || 'Sistema de gestão empresarial'
  }

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Left Section - Title */}
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-gray-900">{getModuleTitle()}</h1>
          <p className="text-gray-600 text-sm mt-1">{getModuleDescription()}</p>
        </div>

        {/* Center Section - Search */}
        <div className="flex-1 max-w-md mx-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar..."
              className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
          </div>
        </div>

        {/* Right Section - Actions */}
        <div className="flex items-center space-x-4">
          {/* Add Button */}
          <button className="flex items-center space-x-2 px-4 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors font-medium">
            <Plus className="w-4 h-4" />
            <span>Novo</span>
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-xl transition-colors"
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-3 h-3 bg-red-500 rounded-full"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <h3 className="font-semibold text-gray-900">Notificações</h3>
                </div>
                <div className="p-4 space-y-3">
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-sm text-gray-900">Nova proposta criada</p>
                      <p className="text-xs text-gray-500">Há 5 minutos</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-sm text-gray-900">Lead convertido</p>
                      <p className="text-xs text-gray-500">Há 1 hora</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-sm text-gray-900">Tarefa pendente</p>
                      <p className="text-xs text-gray-500">Há 2 horas</p>
                    </div>
                  </div>
                </div>
                <div className="p-3 border-t border-gray-200">
                  <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                    Ver todas as notificações
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-3 p-2 hover:bg-gray-100 rounded-xl transition-colors"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold text-sm">JT</span>
              </div>
              <div className="hidden md:block text-left">
                <p className="text-sm font-medium text-gray-900">Admin JT</p>
                <p className="text-xs text-gray-500">Administrador</p>
              </div>
              <ChevronDown className="w-4 h-4 text-gray-500" />
            </button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-semibold">JT</span>
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">Admin JT</p>
                      <p className="text-sm text-gray-500">admin@jttelecom.com</p>
                    </div>
                  </div>
                </div>
                <div className="p-2">
                  <button className="w-full flex items-center space-x-3 px-3 py-2 text-left hover:bg-gray-100 rounded-lg transition-colors">
                    <User className="w-4 h-4 text-gray-500" />
                    <span className="text-sm text-gray-700">Meu Perfil</span>
                  </button>
                  <button className="w-full flex items-center space-x-3 px-3 py-2 text-left hover:bg-gray-100 rounded-lg transition-colors">
                    <Settings className="w-4 h-4 text-gray-500" />
                    <span className="text-sm text-gray-700">Configurações</span>
                  </button>
                </div>
                <div className="p-2 border-t border-gray-200">
                  <button className="w-full flex items-center space-x-3 px-3 py-2 text-left hover:bg-red-50 rounded-lg transition-colors text-red-600">
                    <span className="text-sm">Sair</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header

