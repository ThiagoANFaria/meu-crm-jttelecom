import React, { useState, useEffect } from 'react'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { 
  Users, 
  UserPlus, 
  FileText, 
  DollarSign,
  TrendingUp,
  TrendingDown,
  Activity
} from 'lucide-react'

// Dados mock para demonstração
const mockData = {
  stats: [
    {
      title: 'Total de Leads',
      value: '1,234',
      change: '+12%',
      trend: 'up',
      icon: UserPlus,
      color: 'blue'
    },
    {
      title: 'Clientes Ativos',
      value: '856',
      change: '+8%',
      trend: 'up',
      icon: Users,
      color: 'green'
    },
    {
      title: 'Propostas Enviadas',
      value: '342',
      change: '+15%',
      trend: 'up',
      icon: FileText,
      color: 'purple'
    },
    {
      title: 'Receita Mensal',
      value: 'R$ 125.430',
      change: '+23%',
      trend: 'up',
      icon: DollarSign,
      color: 'yellow'
    }
  ],
  leadsChart: [
    { name: 'Jan', leads: 65, conversoes: 12 },
    { name: 'Fev', leads: 78, conversoes: 18 },
    { name: 'Mar', leads: 90, conversoes: 25 },
    { name: 'Abr', leads: 81, conversoes: 22 },
    { name: 'Mai', leads: 95, conversoes: 28 },
    { name: 'Jun', leads: 110, conversoes: 35 }
  ],
  revenueChart: [
    { name: 'Jan', receita: 85000 },
    { name: 'Fev', receita: 92000 },
    { name: 'Mar', receita: 105000 },
    { name: 'Abr', receita: 98000 },
    { name: 'Mai', receita: 115000 },
    { name: 'Jun', receita: 125430 }
  ],
  statusDistribution: [
    { name: 'Novos', value: 35, color: '#3B82F6' },
    { name: 'Qualificados', value: 25, color: '#10B981' },
    { name: 'Propostas', value: 20, color: '#F59E0B' },
    { name: 'Fechados', value: 15, color: '#EF4444' },
    { name: 'Perdidos', value: 5, color: '#6B7280' }
  ]
}

function StatCard({ stat }) {
  const Icon = stat.icon
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    yellow: 'bg-yellow-500'
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{stat.title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
          <div className="flex items-center mt-2">
            {stat.trend === 'up' ? (
              <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-500 mr-1" />
            )}
            <span className={`text-sm font-medium ${
              stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
            }`}>
              {stat.change}
            </span>
            <span className="text-sm text-gray-500 ml-1">vs mês anterior</span>
          </div>
        </div>
        <div className={`p-3 rounded-full ${colorClasses[stat.color]}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(mockData)

  useEffect(() => {
    // Simular carregamento de dados
    const timer = setTimeout(() => {
      setLoading(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Visão geral do seu CRM</p>
        </div>
        <div className="flex items-center space-x-2">
          <Activity className="h-5 w-5 text-green-500" />
          <span className="text-sm text-gray-600">Atualizado agora</span>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {data.stats.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Leads e Conversões */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Leads e Conversões</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.leadsChart}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="leads" fill="#3B82F6" name="Leads" />
              <Bar dataKey="conversoes" fill="#10B981" name="Conversões" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Receita Mensal */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Receita Mensal</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.revenueChart}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value) => [`R$ ${value.toLocaleString()}`, 'Receita']} />
              <Line 
                type="monotone" 
                dataKey="receita" 
                stroke="#8B5CF6" 
                strokeWidth={3}
                dot={{ fill: '#8B5CF6', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Status Distribution e Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Status Distribution */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Distribuição de Status</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={data.statusDistribution}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {data.statusDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Recent Activity */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Atividades Recentes</h3>
          <div className="space-y-4">
            {[
              { action: 'Novo lead cadastrado', user: 'João Silva', time: '2 min atrás', type: 'lead' },
              { action: 'Proposta enviada', user: 'Maria Santos', time: '15 min atrás', type: 'proposal' },
              { action: 'Cliente convertido', user: 'Pedro Costa', time: '1 hora atrás', type: 'client' },
              { action: 'Contrato assinado', user: 'Ana Lima', time: '2 horas atrás', type: 'contract' },
              { action: 'Follow-up realizado', user: 'Carlos Oliveira', time: '3 horas atrás', type: 'activity' }
            ].map((activity, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
                <div className={`h-2 w-2 rounded-full ${
                  activity.type === 'lead' ? 'bg-blue-500' :
                  activity.type === 'proposal' ? 'bg-purple-500' :
                  activity.type === 'client' ? 'bg-green-500' :
                  activity.type === 'contract' ? 'bg-yellow-500' :
                  'bg-gray-500'
                }`}></div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                  <p className="text-xs text-gray-500">por {activity.user}</p>
                </div>
                <span className="text-xs text-gray-400">{activity.time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

