import React, { useState, useEffect } from 'react'
import { 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Edit, 
  Trash2, 
  Send, 
  Eye,
  Download,
  Copy,
  CheckCircle,
  XCircle,
  Clock,
  FileText
} from 'lucide-react'
import { toast } from 'sonner'

// Dados mock para demonstração
const mockProposals = [
  {
    id: '1',
    title: 'Proposta Comercial - TechCorp Solutions',
    client: 'Ana Costa',
    clientEmail: 'ana@techcorp.com',
    value: 150000,
    status: 'enviada',
    validUntil: '2024-02-15',
    createdAt: '2024-01-15',
    sentAt: '2024-01-16',
    description: 'Implementação de sistema de telecomunicações completo',
    items: [
      { description: 'Instalação de PABX', quantity: 1, unitPrice: 50000, total: 50000 },
      { description: 'Configuração de ramais', quantity: 50, unitPrice: 500, total: 25000 },
      { description: 'Treinamento da equipe', quantity: 8, unitPrice: 1000, total: 8000 },
      { description: 'Suporte técnico (12 meses)', quantity: 12, unitPrice: 5000, total: 60000 }
    ],
    terms: 'Pagamento em 3x sem juros. Garantia de 12 meses.',
    notes: 'Cliente demonstrou interesse em expansão futura'
  },
  {
    id: '2',
    title: 'Proposta de Upgrade - Indústria Silva',
    client: 'Carlos Silva',
    clientEmail: 'carlos@industria.com',
    value: 85000,
    status: 'aprovada',
    validUntil: '2024-02-20',
    createdAt: '2024-01-10',
    sentAt: '2024-01-12',
    approvedAt: '2024-01-18',
    description: 'Upgrade do sistema de comunicação existente',
    items: [
      { description: 'Upgrade de PABX', quantity: 1, unitPrice: 30000, total: 30000 },
      { description: 'Novos ramais IP', quantity: 25, unitPrice: 800, total: 20000 },
      { description: 'Software de gestão', quantity: 1, unitPrice: 15000, total: 15000 },
      { description: 'Migração de dados', quantity: 1, unitPrice: 20000, total: 20000 }
    ],
    terms: 'Pagamento à vista com 10% de desconto.',
    notes: 'Aprovada pelo diretor. Iniciar implementação em fevereiro.'
  },
  {
    id: '3',
    title: 'Proposta Básica - Comércio Santos',
    client: 'Maria Santos',
    clientEmail: 'maria@comercio.com',
    value: 45000,
    status: 'rejeitada',
    validUntil: '2024-01-25',
    createdAt: '2024-01-05',
    sentAt: '2024-01-08',
    rejectedAt: '2024-01-20',
    description: 'Sistema básico de telecomunicações',
    items: [
      { description: 'PABX básico', quantity: 1, unitPrice: 25000, total: 25000 },
      { description: 'Ramais analógicos', quantity: 15, unitPrice: 300, total: 4500 },
      { description: 'Instalação', quantity: 1, unitPrice: 5000, total: 5000 },
      { description: 'Suporte (6 meses)', quantity: 6, unitPrice: 1750, total: 10500 }
    ],
    terms: 'Pagamento em 2x.',
    notes: 'Cliente optou por solução mais econômica de outro fornecedor.'
  }
]

const statusOptions = [
  { value: 'rascunho', label: 'Rascunho', color: 'bg-gray-100 text-gray-800', icon: FileText },
  { value: 'enviada', label: 'Enviada', color: 'bg-blue-100 text-blue-800', icon: Send },
  { value: 'aprovada', label: 'Aprovada', color: 'bg-green-100 text-green-800', icon: CheckCircle },
  { value: 'rejeitada', label: 'Rejeitada', color: 'bg-red-100 text-red-800', icon: XCircle },
  { value: 'expirada', label: 'Expirada', color: 'bg-yellow-100 text-yellow-800', icon: Clock }
]

function ProposalCard({ proposal, onEdit, onDelete, onView, onSend, onDuplicate }) {
  const [showMenu, setShowMenu] = useState(false)
  const status = statusOptions.find(s => s.value === proposal.status)
  const StatusIcon = status?.icon

  const isExpired = new Date(proposal.validUntil) < new Date() && proposal.status === 'enviada'
  const daysUntilExpiry = Math.ceil((new Date(proposal.validUntil) - new Date()) / (1000 * 60 * 60 * 24))

  const handleSend = () => {
    onSend(proposal)
    setShowMenu(false)
  }

  const handleDownload = () => {
    toast.success('Download da proposta iniciado')
    setShowMenu(false)
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{proposal.title}</h3>
            <div className="flex items-center">
              {StatusIcon && <StatusIcon className="h-4 w-4 mr-1" />}
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${status?.color}`}>
                {status?.label}
              </span>
            </div>
          </div>
          <p className="text-gray-600 mb-2">{proposal.client}</p>
          <div className="space-y-1 text-sm text-gray-500 mb-3">
            <div>Valor: <span className="font-medium text-green-600">R$ {proposal.value.toLocaleString()}</span></div>
            <div>Criada em: {new Date(proposal.createdAt).toLocaleDateString()}</div>
            <div>
              Válida até: {new Date(proposal.validUntil).toLocaleDateString()}
              {proposal.status === 'enviada' && (
                <span className={`ml-2 ${isExpired ? 'text-red-600' : daysUntilExpiry <= 3 ? 'text-yellow-600' : 'text-gray-500'}`}>
                  ({isExpired ? 'Expirada' : `${daysUntilExpiry} dias`})
                </span>
              )}
            </div>
          </div>
          {proposal.sentAt && (
            <div className="text-xs text-gray-400">
              Enviada em: {new Date(proposal.sentAt).toLocaleDateString()}
            </div>
          )}
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
                  onView(proposal)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Eye className="h-4 w-4 mr-2" />
                Visualizar
              </button>
              <button
                onClick={() => {
                  onEdit(proposal)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Edit className="h-4 w-4 mr-2" />
                Editar
              </button>
              {proposal.status === 'rascunho' && (
                <button
                  onClick={handleSend}
                  className="flex items-center w-full px-4 py-2 text-sm text-blue-600 hover:bg-gray-100"
                >
                  <Send className="h-4 w-4 mr-2" />
                  Enviar
                </button>
              )}
              <button
                onClick={() => {
                  onDuplicate(proposal)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Copy className="h-4 w-4 mr-2" />
                Duplicar
              </button>
              <button
                onClick={handleDownload}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Download className="h-4 w-4 mr-2" />
                Download PDF
              </button>
              <button
                onClick={() => {
                  onDelete(proposal.id)
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

      {proposal.description && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">{proposal.description}</p>
        </div>
      )}

      {proposal.notes && (
        <div className="mt-3 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-700">{proposal.notes}</p>
        </div>
      )}
    </div>
  )
}

function ProposalModal({ proposal, isOpen, onClose, onSave }) {
  const [formData, setFormData] = useState({
    title: '',
    client: '',
    clientEmail: '',
    value: 0,
    validUntil: '',
    description: '',
    items: [{ description: '', quantity: 1, unitPrice: 0, total: 0 }],
    terms: '',
    notes: ''
  })

  useEffect(() => {
    if (proposal) {
      setFormData(proposal)
    } else {
      const nextMonth = new Date()
      nextMonth.setMonth(nextMonth.getMonth() + 1)
      
      setFormData({
        title: '',
        client: '',
        clientEmail: '',
        value: 0,
        validUntil: nextMonth.toISOString().split('T')[0],
        description: '',
        items: [{ description: '', quantity: 1, unitPrice: 0, total: 0 }],
        terms: '',
        notes: ''
      })
    }
  }, [proposal])

  const handleSubmit = (e) => {
    e.preventDefault()
    const totalValue = formData.items.reduce((sum, item) => sum + item.total, 0)
    onSave({ ...formData, value: totalValue })
    onClose()
  }

  const handleItemChange = (index, field, value) => {
    const newItems = [...formData.items]
    newItems[index] = { ...newItems[index], [field]: value }
    
    if (field === 'quantity' || field === 'unitPrice') {
      newItems[index].total = newItems[index].quantity * newItems[index].unitPrice
    }
    
    setFormData({ ...formData, items: newItems })
  }

  const addItem = () => {
    setFormData({
      ...formData,
      items: [...formData.items, { description: '', quantity: 1, unitPrice: 0, total: 0 }]
    })
  }

  const removeItem = (index) => {
    if (formData.items.length > 1) {
      const newItems = formData.items.filter((_, i) => i !== index)
      setFormData({ ...formData, items: newItems })
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            {proposal ? 'Editar Proposta' : 'Nova Proposta'}
          </h2>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Informações Básicas */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Informações Básicas</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Título da Proposta *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cliente *
                </label>
                <input
                  type="text"
                  required
                  value={formData.client}
                  onChange={(e) => setFormData({ ...formData, client: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email do Cliente *
                </label>
                <input
                  type="email"
                  required
                  value={formData.clientEmail}
                  onChange={(e) => setFormData({ ...formData, clientEmail: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Válida até *
                </label>
                <input
                  type="date"
                  required
                  value={formData.validUntil}
                  onChange={(e) => setFormData({ ...formData, validUntil: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descrição
                </label>
                <textarea
                  rows={3}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Descreva brevemente o que está sendo proposto..."
                />
              </div>
            </div>
          </div>

          {/* Itens da Proposta */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Itens da Proposta</h3>
              <button
                type="button"
                onClick={addItem}
                className="flex items-center px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
              >
                <Plus className="h-4 w-4 mr-1" />
                Adicionar Item
              </button>
            </div>
            
            <div className="space-y-4">
              {formData.items.map((item, index) => (
                <div key={index} className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4 border border-gray-200 rounded-lg">
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Descrição
                    </label>
                    <input
                      type="text"
                      value={item.description}
                      onChange={(e) => handleItemChange(index, 'description', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Qtd
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={item.quantity}
                      onChange={(e) => handleItemChange(index, 'quantity', Number(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Valor Unit.
                    </label>
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={item.unitPrice}
                      onChange={(e) => handleItemChange(index, 'unitPrice', Number(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div className="flex items-end">
                    <div className="flex-1">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Total
                      </label>
                      <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-gray-900">
                        R$ {item.total.toLocaleString()}
                      </div>
                    </div>
                    {formData.items.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeItem(index)}
                        className="ml-2 p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex justify-between items-center">
                <span className="text-lg font-medium text-gray-900">Total Geral:</span>
                <span className="text-xl font-bold text-green-600">
                  R$ {formData.items.reduce((sum, item) => sum + item.total, 0).toLocaleString()}
                </span>
              </div>
            </div>
          </div>

          {/* Termos e Observações */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Termos e Condições
              </label>
              <textarea
                rows={4}
                value={formData.terms}
                onChange={(e) => setFormData({ ...formData, terms: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: Pagamento em 30 dias, garantia de 12 meses..."
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Observações Internas
              </label>
              <textarea
                rows={4}
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Observações que não aparecerão na proposta..."
              />
            </div>
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
              {proposal ? 'Salvar' : 'Criar Proposta'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function Proposals() {
  const [proposals, setProposals] = useState(mockProposals)
  const [filteredProposals, setFilteredProposals] = useState(mockProposals)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingProposal, setEditingProposal] = useState(null)

  useEffect(() => {
    let filtered = proposals

    if (searchTerm) {
      filtered = filtered.filter(proposal =>
        proposal.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        proposal.client.toLowerCase().includes(searchTerm.toLowerCase()) ||
        proposal.description.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (statusFilter) {
      filtered = filtered.filter(proposal => proposal.status === statusFilter)
    }

    setFilteredProposals(filtered)
  }, [proposals, searchTerm, statusFilter])

  const handleSaveProposal = (proposalData) => {
    if (editingProposal) {
      setProposals(proposals.map(proposal => 
        proposal.id === editingProposal.id 
          ? { ...proposalData, id: editingProposal.id, createdAt: editingProposal.createdAt, status: editingProposal.status }
          : proposal
      ))
      toast.success('Proposta atualizada com sucesso!')
    } else {
      const newProposal = {
        ...proposalData,
        id: Date.now().toString(),
        status: 'rascunho',
        createdAt: new Date().toISOString().split('T')[0]
      }
      setProposals([newProposal, ...proposals])
      toast.success('Proposta criada com sucesso!')
    }
    setEditingProposal(null)
  }

  const handleEditProposal = (proposal) => {
    setEditingProposal(proposal)
    setShowModal(true)
  }

  const handleDeleteProposal = (proposalId) => {
    if (window.confirm('Tem certeza que deseja excluir esta proposta?')) {
      setProposals(proposals.filter(proposal => proposal.id !== proposalId))
      toast.success('Proposta excluída com sucesso!')
    }
  }

  const handleViewProposal = (proposal) => {
    toast.info('Visualização detalhada em desenvolvimento')
  }

  const handleSendProposal = (proposal) => {
    setProposals(proposals.map(p => 
      p.id === proposal.id 
        ? { ...p, status: 'enviada', sentAt: new Date().toISOString().split('T')[0] }
        : p
    ))
    toast.success(`Proposta enviada para ${proposal.client}!`)
  }

  const handleDuplicateProposal = (proposal) => {
    const duplicated = {
      ...proposal,
      id: Date.now().toString(),
      title: `${proposal.title} (Cópia)`,
      status: 'rascunho',
      createdAt: new Date().toISOString().split('T')[0],
      sentAt: null,
      approvedAt: null,
      rejectedAt: null
    }
    setProposals([duplicated, ...proposals])
    toast.success('Proposta duplicada com sucesso!')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Propostas</h1>
          <p className="text-gray-600">Gerencie suas propostas comerciais</p>
        </div>
        <button
          onClick={() => {
            setEditingProposal(null)
            setShowModal(true)
          }}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4 mr-2" />
          Nova Proposta
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 md:space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar propostas..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex items-center space-x-4">
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
            <div className="text-sm text-gray-500">
              {filteredProposals.length} de {proposals.length} propostas
            </div>
          </div>
        </div>
      </div>

      {/* Proposals Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredProposals.map(proposal => (
          <ProposalCard
            key={proposal.id}
            proposal={proposal}
            onEdit={handleEditProposal}
            onDelete={handleDeleteProposal}
            onView={handleViewProposal}
            onSend={handleSendProposal}
            onDuplicate={handleDuplicateProposal}
          />
        ))}
      </div>

      {filteredProposals.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <FileText className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhuma proposta encontrada</h3>
          <p className="text-gray-500 mb-4">
            {searchTerm || statusFilter 
              ? 'Tente ajustar os filtros de busca'
              : 'Comece criando sua primeira proposta'
            }
          </p>
          {!searchTerm && !statusFilter && (
            <button
              onClick={() => {
                setEditingProposal(null)
                setShowModal(true)
              }}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="h-4 w-4 mr-2" />
              Criar Primeira Proposta
            </button>
          )}
        </div>
      )}

      {/* Modal */}
      <ProposalModal
        proposal={editingProposal}
        isOpen={showModal}
        onClose={() => {
          setShowModal(false)
          setEditingProposal(null)
        }}
        onSave={handleSaveProposal}
      />
    </div>
  )
}

