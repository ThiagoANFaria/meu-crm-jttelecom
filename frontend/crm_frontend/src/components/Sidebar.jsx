import React from 'react'
import { 
  LayoutDashboard, 
  Users, 
  UserPlus, 
  FileText, 
  FileSignature,
  CheckSquare,
  MessageCircle,
  Phone,
  Settings,
  Zap,
  LogOut,
  ChevronRight
} from 'lucide-react'

const Sidebar = ({ activeModule, setActiveModule }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'leads', label: 'Leads', icon: UserPlus },
    { id: 'clients', label: 'Clientes', icon: Users },
    { id: 'proposals', label: 'Propostas', icon: FileText },
    { id: 'contracts', label: 'Contratos', icon: FileSignature },
    { id: 'tasks', label: 'Tarefas', icon: CheckSquare },
    { id: 'chatbot', label: 'Chatbot', icon: MessageCircle },
    { id: 'telephony', label: 'Telefonia', icon: Phone },
    { id: 'automation', label: 'Automação', icon: Zap },
  ]

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Logo Section */}
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-center space-x-3">
          <img
            src="https://crm.jttecnologia.com.br/media/JT-Telecom-LOGO1.jpg?_t=1727781649"
            alt="JT Telecom"
            className="h-10 w-auto"
          />
        </div>
        <p className="text-gray-400 text-xs mt-2">Sistema de Gestão</p>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = activeModule === item.id
          
          return (
            <button
              key={item.id}
              onClick={() => setActiveModule(item.id)}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-xl text-left transition-all duration-200 group ${
                isActive
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-gray-400 group-hover:text-white'}`} />
                <span className="font-medium">{item.label}</span>
              </div>
              {isActive && (
                <ChevronRight className="w-4 h-4 text-white" />
              )}
            </button>
          )
        })}
      </nav>

      {/* User Section */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold text-sm">JT</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-white font-medium text-sm truncate">Admin JT</p>
            <p className="text-gray-400 text-xs truncate">admin@jttelecom.com</p>
          </div>
        </div>

        {/* Settings & Logout */}
        <div className="space-y-1">
          <button className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors">
            <Settings className="w-4 h-4" />
            <span className="text-sm">Configurações</span>
          </button>
          <button className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-300 hover:bg-red-600 hover:text-white transition-colors">
            <LogOut className="w-4 h-4" />
            <span className="text-sm">Sair</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default Sidebar

