import React, { useState, useEffect } from 'react'
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  DollarSign, 
  FileText, 
  Phone,
  Calendar,
  Clock,
  CheckCircle,
  AlertCircle,
  MoreVertical,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalLeads: 156,
    totalClients: 89,
    totalRevenue: 245000,
    totalProposals: 34,
    leadsGrowth: 12.5,
    clientsGrowth: 8.3,
    revenueGrowth: 15.2,
    proposalsGrowth: -2.1
  })

  const [recentActivities] = useState([
    {
      id: 1,
      type: 'lead',
      title: 'Novo lead cadastrado',
      description: 'Maria Silva - Empresa ABC Ltda',
      time: '5 min atrás',
      icon: Users,
      color: 'blue'
    },
    {
      id: 2,
      type: 'proposal',
      title: 'Proposta aprovada',
      description: 'Proposta #1234 - R$ 15.000',
      time: '1 hora atrás',
      icon: CheckCircle,
      color: 'green'
    },
    {
      id: 3,
      type: 'task',
      title: 'Tarefa pendente',
      description: 'Ligar para cliente João Santos',
      time: '2 horas atrás',
      icon: AlertCircle,
      color: 'yellow'
    },
    {
      id: 4,
      type: 'call',
      title: 'Chamada realizada',
      description: 'Contato com lead Pedro Costa',
      time: '3 horas atrás',
      icon: Phone,
      color: 'purple'
    }
  ])

  const StatCard = ({ title, value, growth, icon: Icon, prefix = '', suffix = '' }) => {
    const isPositive = growth > 0
    const GrowthIcon = isPositive ? ArrowUpRight : ArrowDownRight
    
    return (
      <div className="bg-white rounded-2xl p-6 border border-gray-200 hover:shadow-lg transition-all duration-200">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 bg-blue-50 rounded-xl">
            <Icon className="w-6 h-6 text-blue-600" />
          </div>
          <button className="p-1 hover:bg-gray-100 rounded-lg transition-colors">
            <MoreVertical className="w-4 h-4 text-gray-400" />
          </button>
        </div>
        
        <div className="space-y-2">
          <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
          <p className="text-2xl font-bold text-gray-900">
            {prefix}{typeof value === 'number' ? value.toLocaleString('pt-BR') : value}{suffix}
          </p>
          <div className="flex items-center space-x-1">
            <GrowthIcon className={`w-4 h-4 ${isPositive ? 'text-green-500' : 'text-red-500'}`} />
            <span className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {Math.abs(growth)}%
            </span>
            <span className="text-gray-500 text-sm">vs mês anterior</span>
          </div>
        </div>
      </div>
    )
  }

  const ActivityItem = ({ activity }) => {
    const Icon = activity.icon
    const colorClasses = {
      blue: 'bg-blue-100 text-blue-600',
      green: 'bg-green-100 text-green-600',
      yellow: 'bg-yellow-100 text-yellow-600',
      purple: 'bg-purple-100 text-purple-600'
    }

    return (
      <div className="flex items-start space-x-4 p-4 hover:bg-gray-50 rounded-xl transition-colors">
        <div className={`p-2 rounded-lg ${colorClasses[activity.color]}`}>
          <Icon className="w-4 h-4" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900">{activity.title}</p>
          <p className="text-sm text-gray-600 truncate">{activity.description}</p>
          <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total de Leads"
          value={stats.totalLeads}
          growth={stats.leadsGrowth}
          icon={Users}
        />
        <StatCard
          title="Clientes Ativos"
          value={stats.totalClients}
          growth={stats.clientsGrowth}
          icon={Users}
        />
        <StatCard
          title="Receita Total"
          value={stats.totalRevenue}
          growth={stats.revenueGrowth}
          icon={DollarSign}
          prefix="R$ "
        />
        <StatCard
          title="Propostas"
          value={stats.totalProposals}
          growth={stats.proposalsGrowth}
          icon={FileText}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart Section */}
        <div className="lg:col-span-2 space-y-6">
          {/* Revenue Chart */}
          <div className="bg-white rounded-2xl p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Receita Mensal</h3>
                <p className="text-gray-600 text-sm">Últimos 6 meses</p>
              </div>
              <button className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                Ver detalhes
              </button>
            </div>
            
            {/* Simplified Chart Placeholder */}
            <div className="h-64 bg-gradient-to-t from-blue-50 to-transparent rounded-xl flex items-end justify-center space-x-4 p-4">
              {[40, 65, 45, 80, 60, 90].map((height, index) => (
                <div
                  key={index}
                  className="bg-blue-600 rounded-t-lg w-12 transition-all duration-500 hover:bg-blue-700"
                  style={{ height: `${height}%` }}
                ></div>
              ))}
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="bg-white rounded-2xl p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Métricas de Performance</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <TrendingUp className="w-8 h-8 text-green-600" />
                </div>
                <p className="text-2xl font-bold text-gray-900">85%</p>
                <p className="text-sm text-gray-600">Taxa de Conversão</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Clock className="w-8 h-8 text-blue-600" />
                </div>
                <p className="text-2xl font-bold text-gray-900">2.5h</p>
                <p className="text-sm text-gray-600">Tempo Médio</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <CheckCircle className="w-8 h-8 text-purple-600" />
                </div>
                <p className="text-2xl font-bold text-gray-900">94%</p>
                <p className="text-sm text-gray-600">Satisfação</p>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Recent Activities */}
          <div className="bg-white rounded-2xl border border-gray-200">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">Atividades Recentes</h3>
                <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                  Ver todas
                </button>
              </div>
            </div>
            
            <div className="divide-y divide-gray-100">
              {recentActivities.map((activity) => (
                <ActivityItem key={activity.id} activity={activity} />
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-2xl p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Ações Rápidas</h3>
            
            <div className="space-y-3">
              <button className="w-full flex items-center space-x-3 p-3 text-left hover:bg-blue-50 rounded-xl transition-colors border border-gray-200 hover:border-blue-200">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Users className="w-4 h-4 text-blue-600" />
                </div>
                <span className="font-medium text-gray-900">Novo Lead</span>
              </button>
              
              <button className="w-full flex items-center space-x-3 p-3 text-left hover:bg-green-50 rounded-xl transition-colors border border-gray-200 hover:border-green-200">
                <div className="p-2 bg-green-100 rounded-lg">
                  <FileText className="w-4 h-4 text-green-600" />
                </div>
                <span className="font-medium text-gray-900">Nova Proposta</span>
              </button>
              
              <button className="w-full flex items-center space-x-3 p-3 text-left hover:bg-purple-50 rounded-xl transition-colors border border-gray-200 hover:border-purple-200">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Calendar className="w-4 h-4 text-purple-600" />
                </div>
                <span className="font-medium text-gray-900">Agendar Tarefa</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

