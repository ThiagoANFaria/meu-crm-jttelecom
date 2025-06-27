import React, { useState, useEffect } from 'react'
import { 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Edit, 
  Trash2, 
  Phone, 
  Mail,
  MessageCircle,
  Building,
  Calendar,
  DollarSign,
  FileText
} from 'lucide-react'
import { toast } from 'sonner'

// Dados mock para demonstração
const mockClients = [
  {
    id: '1',
    name: 'Ana Costa',
    email: 'ana@techcorp.com',
    phone: '(11) 99999-9999',
    whatsapp: '(11) 99999-9999',
    company: 'TechCorp Solutions',
    cnpj: '12.345.678/0001-90',
    ie: '123.456.789.123',
    address: {
      street: 'Rua das Flores, 123',
      neighborhood: 'Centro',
      city: 'São Paulo',
      state: 'SP',
      zipCode: '01234-567'
    },
    status: 'ativo',
    segment: 'Tecnologia',
    revenue: 150000,
    contractDate: '2023-06-15',
    lastInteraction: '2024-01-20',
    notes: 'Cliente premium com potencial de expansão'
  },
  {
    id: '2',
    name: 'Carlos Silva',
    email: 'carlos@industria.com',
    phone: '(11) 88888-8888',
    whatsapp: '(11) 88888-8888',
    company: 'Indústria Silva & Cia',
    cnpj: '98.765.432/0001-10',
    ie: '987.654.321.098',
    address: {
      street: 'Av. Industrial, 456',
      neighborhood: 'Distrito Industrial',
      city: 'São Bernardo',
      state: 'SP',
      zipCode: '09876-543'
    },
    status: 'ativo',
    segment: 'Indústria',
    revenue: 280000,
    contractDate: '2023-03-10',
    lastInteraction: '2024-01-18',
    notes: 'Renovação de contrato em março'
  },
  {
    id: '3',
    name: 'Maria Santos',
    email: 'maria@comercio.com',
    phone: '(11) 77777-7777',
    whatsapp: '(11) 77777-7777',
    company: 'Comércio Santos Ltda',
    cnpj: '11.222.333/0001-44',
    ie: '111.222.333.444',
    address: {
      street: 'Rua do Comércio, 789',
      neighborhood: 'Vila Comercial',
      city: 'Santo André',
      state: 'SP',
      zipCode: '09123-456'
    },
    status: 'inativo',
    segment: 'Comércio',
    revenue: 85000,
    contractDate: '2022-11-20',
    lastInteraction: '2023-12-15',
    notes: 'Contrato suspenso temporariamente'
  }
]

const statusOptions = [
  { value: 'ativo', label: 'Ativo', color: 'bg-green-100 text-green-800' },
  { value: 'inativo', label: 'Inativo', color: 'bg-red-100 text-red-800' },
  { value: 'suspenso', label: 'Suspenso', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'prospecto', label: 'Prospecto', color: 'bg-blue-100 text-blue-800' }
]

const segmentOptions = [
  'Tecnologia',
  'Indústria',
  'Comércio',
  'Serviços',
  'Saúde',
  'Educação',
  'Financeiro',
  'Outros'
]

function ClientCard({ client, onEdit, onDelete, onViewDetails }) {
  const [showMenu, setShowMenu] = useState(false)
  const status = statusOptions.find(s => s.value === client.status)

  const handleCall = () => {
    window.open(`tel:${client.phone}`)
    toast.success('Iniciando ligação...')
  }

  const handleEmail = () => {
    window.open(`mailto:${client.email}`)
  }

  const handleWhatsApp = () => {
    const message = encodeURIComponent(`Olá ${client.name}, tudo bem?`)
    window.open(`https://wa.me/${client.whatsapp.replace(/\D/g, '')}?text=${message}`)
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{client.name}</h3>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${status?.color}`}>
              {status?.label}
            </span>
          </div>
          <div className="flex items-center text-gray-600 mb-2">
            <Building className="h-4 w-4 mr-1" />
            <span>{client.company}</span>
          </div>
          <div className="space-y-1 text-sm text-gray-500 mb-3">
            <div>{client.email}</div>
            <div>{client.phone}</div>
            <div>{client.segment}</div>
          </div>
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center text-green-600">
              <DollarSign className="h-4 w-4 mr-1" />
              <span>R$ {client.revenue.toLocaleString()}</span>
            </div>
            <div className="flex items-center text-gray-500">
              <Calendar className="h-4 w-4 mr-1" />
              <span>Cliente desde {new Date(client.contractDate).toLocaleDateString()}</span>
            </div>
          </div>
        </div>
        
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <MoreVertical className="h-4 w-4 text-gray-500" />
          </button>
          
          {showMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10">
              <button
                onClick={() => {
                  onViewDetails(client)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <FileText className="h-4 w-4 mr-2" />
                Ver Detalhes
              </button>
              <button
                onClick={() => {
                  onEdit(client)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Edit className="h-4 w-4 mr-2" />
                Editar
              </button>
              <button
                onClick={() => {
                  onDelete(client.id)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Excluir
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center space-x-2 pt-4 border-t border-gray-100">
        <button
          onClick={handleCall}
          className="flex items-center px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
        >
          <Phone className="h-4 w-4 mr-1" />
          Ligar
        </button>
        <button
          onClick={handleEmail}
          className="flex items-center px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <Mail className="h-4 w-4 mr-1" />
          Email
        </button>
        <button
          onClick={handleWhatsApp}
          className="flex items-center px-3 py-2 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors"
        >
          <MessageCircle className="h-4 w-4 mr-1" />
          WhatsApp
        </button>
      </div>

      {client.notes && (
        <div className="mt-3 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">{client.notes}</p>
        </div>
      )}
    </div>
  )
}

function ClientModal({ client, isOpen, onClose, onSave }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    whatsapp: '',
    company: '',
    cnpj: '',
    ie: '',
    address: {
      street: '',
      neighborhood: '',
      city: '',
      state: '',
      zipCode: ''
    },
    status: 'prospecto',
    segment: '',
    revenue: 0,
    notes: ''
  })

  useEffect(() => {
    if (client) {
      setFormData(client)
    } else {
      setFormData({
        name: '',
        email: '',
        phone: '',
        whatsapp: '',
        company: '',
        cnpj: '',
        ie: '',
        address: {
          street: '',
          neighborhood: '',
          city: '',
          state: '',
          zipCode: ''
        },
        status: 'prospecto',
        segment: '',
        revenue: 0,
        notes: ''
      })
    }
  }, [client])

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave(formData)
    onClose()
  }

  const handleAddressChange = (field, value) => {
    setFormData({
      ...formData,
      address: {
        ...formData.address,
        [field]: value
      }
    })
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            {client ? 'Editar Cliente' : 'Novo Cliente'}
          </h2>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Informações Básicas */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Informações Básicas</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email *
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Telefone *
                </label>
                <input
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  WhatsApp
                </label>
                <input
                  type="tel"
                  value={formData.whatsapp}
                  onChange={(e) => setFormData({ ...formData, whatsapp: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          {/* Informações da Empresa */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Informações da Empresa</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Razão Social *
                </label>
                <input
                  type="text"
                  required
                  value={formData.company}
                  onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CNPJ
                </label>
                <input
                  type="text"
                  value={formData.cnpj}
                  onChange={(e) => setFormData({ ...formData, cnpj: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Inscrição Estadual
                </label>
                <input
                  type="text"
                  value={formData.ie}
                  onChange={(e) => setFormData({ ...formData, ie: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Segmento
                </label>
                <select
                  value={formData.segment}
                  onChange={(e) => setFormData({ ...formData, segment: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Selecione...</option>
                  {segmentOptions.map(segment => (
                    <option key={segment} value={segment}>
                      {segment}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Endereço */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Endereço</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Logradouro
                </label>
                <input
                  type="text"
                  value={formData.address.street}
                  onChange={(e) => handleAddressChange('street', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CEP
                </label>
                <input
                  type="text"
                  value={formData.address.zipCode}
                  onChange={(e) => handleAddressChange('zipCode', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Bairro
                </label>
                <input
                  type="text"
                  value={formData.address.neighborhood}
                  onChange={(e) => handleAddressChange('neighborhood', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cidade
                </label>
                <input
                  type="text"
                  value={formData.address.city}
                  onChange={(e) => handleAddressChange('city', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Estado
                </label>
                <input
                  type="text"
                  value={formData.address.state}
                  onChange={(e) => handleAddressChange('state', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          {/* Informações Comerciais */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Informações Comerciais</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {statusOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Receita Mensal (R$)
                </label>
                <input
                  type="number"
                  value={formData.revenue}
                  onChange={(e) => setFormData({ ...formData, revenue: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Observações
            </label>
            <textarea
              rows={3}
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Adicione observações sobre este cliente..."
            />
          </div>
          
          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
            >
              {client ? 'Salvar' : 'Criar Cliente'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function Clients() {
  const [clients, setClients] = useState(mockClients)
  const [filteredClients, setFilteredClients] = useState(mockClients)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [segmentFilter, setSegmentFilter] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingClient, setEditingClient] = useState(null)

  useEffect(() => {
    let filtered = clients

    if (searchTerm) {
      filtered = filtered.filter(client =>
        client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        client.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        client.company.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (statusFilter) {
      filtered = filtered.filter(client => client.status === statusFilter)
    }

    if (segmentFilter) {
      filtered = filtered.filter(client => client.segment === segmentFilter)
    }

    setFilteredClients(filtered)
  }, [clients, searchTerm, statusFilter, segmentFilter])

  const handleSaveClient = (clientData) => {
    if (editingClient) {
      setClients(clients.map(client => 
        client.id === editingClient.id 
          ? { ...clientData, id: editingClient.id, contractDate: editingClient.contractDate, lastInteraction: new Date().toISOString().split('T')[0] }
          : client
      ))
      toast.success('Cliente atualizado com sucesso!')
    } else {
      const newClient = {
        ...clientData,
        id: Date.now().toString(),
        contractDate: new Date().toISOString().split('T')[0],
        lastInteraction: new Date().toISOString().split('T')[0]
      }
      setClients([newClient, ...clients])
      toast.success('Cliente criado com sucesso!')
    }
    setEditingClient(null)
  }

  const handleEditClient = (client) => {
    setEditingClient(client)
    setShowModal(true)
  }

  const handleDeleteClient = (clientId) => {
    if (window.confirm('Tem certeza que deseja excluir este cliente?')) {
      setClients(clients.filter(client => client.id !== clientId))
      toast.success('Cliente excluído com sucesso!')
    }
  }

  const handleViewDetails = (client) => {
    // Implementar modal de detalhes ou navegação para página de detalhes
    toast.info('Funcionalidade de detalhes em desenvolvimento')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clientes</h1>
          <p className="text-gray-600">Gerencie sua base de clientes</p>
        </div>
        <button
          onClick={() => {
            setEditingClient(null)
            setShowModal(true)
          }}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4 mr-2" />
          Novo Cliente
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar clientes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4 text-gray-400" />
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Todos os status</option>
                {statusOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            <select
              value={segmentFilter}
              onChange={(e) => setSegmentFilter(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos os segmentos</option>
              {segmentOptions.map(segment => (
                <option key={segment} value={segment}>
                  {segment}
                </option>
              ))}
            </select>
            <div className="text-sm text-gray-500 whitespace-nowrap">
              {filteredClients.length} de {clients.length} clientes
            </div>
          </div>
        </div>
      </div>

      {/* Clients Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredClients.map(client => (
          <ClientCard
            key={client.id}
            client={client}
            onEdit={handleEditClient}
            onDelete={handleDeleteClient}
            onViewDetails={handleViewDetails}
          />
        ))}
      </div>

      {filteredClients.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Building className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhum cliente encontrado</h3>
          <p className="text-gray-500 mb-4">
            {searchTerm || statusFilter || segmentFilter
              ? 'Tente ajustar os filtros de busca'
              : 'Comece criando seu primeiro cliente'
            }
          </p>
          {!searchTerm && !statusFilter && !segmentFilter && (
            <button
              onClick={() => {
                setEditingClient(null)
                setShowModal(true)
              }}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="h-4 w-4 mr-2" />
              Criar Primeiro Cliente
            </button>
          )}
        </div>
      )}

      {/* Modal */}
      <ClientModal
        client={editingClient}
        isOpen={showModal}
        onClose={() => {
          setShowModal(false)
          setEditingClient(null)
        }}
        onSave={handleSaveClient}
      />
    </div>
  )
}

