import React, { useState, useEffect } from 'react'
import { 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Edit, 
  Trash2, 
  FileSignature, 
  Eye,
  Download,
  Copy,
  CheckCircle,
  XCircle,
  Clock,
  AlertTriangle,
  Calendar
} from 'lucide-react'
import { toast } from 'sonner'

// Dados mock para demonstração
const mockContracts = [
  {
    id: '1',
    title: 'Contrato de Prestação de Serviços - TechCorp',
    client: 'Ana Costa',
    clientEmail: 'ana@techcorp.com',
    value: 150000,
    status: 'ativo',
    startDate: '2023-06-15',
    endDate: '2024-06-14',
    signedDate: '2023-06-10',
    renewalDate: '2024-06-14',
    type: 'prestacao_servicos',
    paymentTerms: 'Mensal',
    description: 'Contrato para implementação e manutenção de sistema de telecomunicações',
    clauses: [
      'Prestação de serviços de telecomunicações',
      'Suporte técnico 24/7',
      'Garantia de 99.9% de uptime',
      'Renovação automática por igual período'
    ],
    attachments: ['contrato_techcorp_assinado.pdf'],
    notes: 'Cliente premium com histórico de pontualidade nos pagamentos'
  },
  {
    id: '2',
    title: 'Contrato de Upgrade - Indústria Silva',
    client: 'Carlos Silva',
    clientEmail: 'carlos@industria.com',
    value: 85000,
    status: 'pendente_assinatura',
    startDate: '2024-02-01',
    endDate: '2025-01-31',
    type: 'upgrade',
    paymentTerms: 'À vista',
    description: 'Contrato para upgrade do sistema de comunicação existente',
    clauses: [
      'Upgrade completo do sistema PABX',
      'Migração de dados sem interrupção',
      'Treinamento da equipe técnica',
      'Suporte por 12 meses'
    ],
    attachments: ['contrato_silva_minuta.pdf'],
    notes: 'Aguardando assinatura do diretor. Previsão para esta semana.'
  },
  {
    id: '3',
    title: 'Contrato de Manutenção - Comércio Santos',
    client: 'Maria Santos',
    clientEmail: 'maria@comercio.com',
    value: 24000,
    status: 'expirado',
    startDate: '2022-11-20',
    endDate: '2023-11-19',
    signedDate: '2022-11-15',
    type: 'manutencao',
    paymentTerms: 'Trimestral',
    description: 'Contrato de manutenção preventiva e corretiva',
    clauses: [
      'Manutenção preventiva mensal',
      'Suporte técnico em horário comercial',
      'Reposição de peças com defeito',
      'Relatórios mensais de performance'
    ],
    attachments: ['contrato_santos_assinado.pdf'],
    notes: 'Contrato expirado. Cliente não renovou devido a cortes de orçamento.'
  },
  {
    id: '4',
    title: 'Contrato de Locação - StartupTech',
    client: 'Pedro Oliveira',
    clientEmail: 'pedro@startuptech.com',
    value: 36000,
    status: 'suspenso',
    startDate: '2023-09-01',
    endDate: '2024-08-31',
    signedDate: '2023-08-25',
    suspendedDate: '2024-01-15',
    type: 'locacao',
    paymentTerms: 'Mensal',
    description: 'Contrato de locação de equipamentos de telecomunicações',
    clauses: [
      'Locação de equipamentos PABX',
      'Manutenção inclusa',
      'Possibilidade de upgrade',
      'Multa por rescisão antecipada'
    ],
    attachments: ['contrato_startuptech_assinado.pdf'],
    notes: 'Contrato suspenso por atraso nos pagamentos. Negociação em andamento.'
  }
]

const statusOptions = [
  { value: 'rascunho', label: 'Rascunho', color: 'bg-gray-100 text-gray-800', icon: Edit },
  { value: 'pendente_assinatura', label: 'Pendente Assinatura', color: 'bg-yellow-100 text-yellow-800', icon: FileSignature },
  { value: 'ativo', label: 'Ativo', color: 'bg-green-100 text-green-800', icon: CheckCircle },
  { value: 'suspenso', label: 'Suspenso', color: 'bg-orange-100 text-orange-800', icon: AlertTriangle },
  { value: 'expirado', label: 'Expirado', color: 'bg-red-100 text-red-800', icon: XCircle },
  { value: 'cancelado', label: 'Cancelado', color: 'bg-red-100 text-red-800', icon: XCircle }
]

const contractTypes = [
  { value: 'prestacao_servicos', label: 'Prestação de Serviços' },
  { value: 'locacao', label: 'Locação' },
  { value: 'manutencao', label: 'Manutenção' },
  { value: 'upgrade', label: 'Upgrade' },
  { value: 'consultoria', label: 'Consultoria' },
  { value: 'outros', label: 'Outros' }
]

const paymentTermsOptions = [
  'À vista',
  'Mensal',
  'Trimestral',
  'Semestral',
  'Anual'
]

function ContractCard({ contract, onEdit, onDelete, onView, onSign, onSuspend, onRenew }) {
  const [showMenu, setShowMenu] = useState(false)
  const status = statusOptions.find(s => s.value === contract.status)
  const StatusIcon = status?.icon
  const contractType = contractTypes.find(t => t.value === contract.type)

  const isNearExpiry = contract.endDate && contract.status === 'ativo' && 
    new Date(contract.endDate) <= new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
  
  const daysUntilExpiry = contract.endDate ? 
    Math.ceil((new Date(contract.endDate) - new Date()) / (1000 * 60 * 60 * 24)) : null

  const handleSign = () => {
    onSign(contract)
    setShowMenu(false)
  }

  const handleSuspend = () => {
    onSuspend(contract)
    setShowMenu(false)
  }

  const handleRenew = () => {
    onRenew(contract)
    setShowMenu(false)
  }

  const handleDownload = () => {
    toast.success('Download do contrato iniciado')
    setShowMenu(false)
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{contract.title}</h3>
            <div className="flex items-center">
              {StatusIcon && <StatusIcon className="h-4 w-4 mr-1" />}
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${status?.color}`}>
                {status?.label}
              </span>
            </div>
          </div>
          <p className="text-gray-600 mb-2">{contract.client}</p>
          <div className="space-y-1 text-sm text-gray-500 mb-3">
            <div>Tipo: <span className="font-medium">{contractType?.label}</span></div>
            <div>Valor: <span className="font-medium text-green-600">R$ {contract.value.toLocaleString()}</span></div>
            <div>Pagamento: {contract.paymentTerms}</div>
            {contract.startDate && (
              <div>Início: {new Date(contract.startDate).toLocaleDateString()}</div>
            )}
            {contract.endDate && (
              <div className="flex items-center">
                <Calendar className="h-3 w-3 mr-1" />
                Fim: {new Date(contract.endDate).toLocaleDateString()}
                {contract.status === 'ativo' && daysUntilExpiry !== null && (
                  <span className={`ml-2 ${isNearExpiry ? 'text-orange-600' : 'text-gray-500'}`}>
                    ({daysUntilExpiry > 0 ? `${daysUntilExpiry} dias` : 'Expirado'})
                  </span>
                )}
              </div>
            )}
          </div>
          {contract.signedDate && (
            <div className="text-xs text-gray-400">
              Assinado em: {new Date(contract.signedDate).toLocaleDateString()}
            </div>
          )}
          {isNearExpiry && (
            <div className="mt-2 p-2 bg-orange-50 border border-orange-200 rounded-lg">
              <div className="flex items-center text-orange-700">
                <AlertTriangle className="h-4 w-4 mr-1" />
                <span className="text-xs font-medium">Renovação necessária em breve</span>
              </div>
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
                  onView(contract)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Eye className="h-4 w-4 mr-2" />
                Visualizar
              </button>
              <button
                onClick={() => {
                  onEdit(contract)
                  setShowMenu(false)
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Edit className="h-4 w-4 mr-2" />
                Editar
              </button>
              {contract.status === 'pendente_assinatura' && (
                <button
                  onClick={handleSign}
                  className="flex items-center w-full px-4 py-2 text-sm text-green-600 hover:bg-gray-100"
                >
                  <FileSignature className="h-4 w-4 mr-2" />
                  Marcar como Assinado
                </button>
              )}
              {contract.status === 'ativo' && (
                <>
                  <button
                    onClick={handleSuspend}
                    className="flex items-center w-full px-4 py-2 text-sm text-orange-600 hover:bg-gray-100"
                  >
                    <AlertTriangle className="h-4 w-4 mr-2" />
                    Suspender
                  </button>
                  {isNearExpiry && (
                    <button
                      onClick={handleRenew}
                      className="flex items-center w-full px-4 py-2 text-sm text-blue-600 hover:bg-gray-100"
                    >
                      <Calendar className="h-4 w-4 mr-2" />
                      Renovar
                    </button>
                  )}
                </>
              )}
              <button
                onClick={handleDownload}
                className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <Download className="h-4 w-4 mr-2" />
                Download PDF
              </button>
              <button
                onClick={() => {
                  onDelete(contract.id)
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

      {contract.description && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">{contract.description}</p>
        </div>
      )}

      {contract.clauses && contract.clauses.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Principais Cláusulas:</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            {contract.clauses.slice(0, 2).map((clause, index) => (
              <li key={index} className="flex items-start">
                <span className="text-gray-400 mr-2">•</span>
                <span>{clause}</span>
              </li>
            ))}
            {contract.clauses.length > 2 && (
              <li className="text-gray-400 text-xs">
                +{contract.clauses.length - 2} cláusulas adicionais
              </li>
            )}
          </ul>
        </div>
      )}

      {contract.notes && (
        <div className="mt-3 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-700">{contract.notes}</p>
        </div>
      )}
    </div>
  )
}

function ContractModal({ contract, isOpen, onClose, onSave }) {
  const [formData, setFormData] = useState({
    title: '',
    client: '',
    clientEmail: '',
    value: 0,
    startDate: '',
    endDate: '',
    type: 'prestacao_servicos',
    paymentTerms: 'Mensal',
    description: '',
    clauses: [''],
    notes: ''
  })

  useEffect(() => {
    if (contract) {
      setFormData({
        ...contract,
        clauses: contract.clauses || ['']
      })
    } else {
      const today = new Date()
      const nextYear = new Date(today)
      nextYear.setFullYear(nextYear.getFullYear() + 1)
      
      setFormData({
        title: '',
        client: '',
        clientEmail: '',
        value: 0,
        startDate: today.toISOString().split('T')[0],
        endDate: nextYear.toISOString().split('T')[0],
        type: 'prestacao_servicos',
        paymentTerms: 'Mensal',
        description: '',
        clauses: [''],
        notes: ''
      })
    }
  }, [contract])

  const handleSubmit = (e) => {
    e.preventDefault()
    const cleanClauses = formData.clauses.filter(clause => clause.trim() !== '')
    onSave({ ...formData, clauses: cleanClauses })
    onClose()
  }

  const handleClauseChange = (index, value) => {
    const newClauses = [...formData.clauses]
    newClauses[index] = value
    setFormData({ ...formData, clauses: newClauses })
  }

  const addClause = () => {
    setFormData({
      ...formData,
      clauses: [...formData.clauses, '']
    })
  }

  const removeClause = (index) => {
    if (formData.clauses.length > 1) {
      const newClauses = formData.clauses.filter((_, i) => i !== index)
      setFormData({ ...formData, clauses: newClauses })
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            {contract ? 'Editar Contrato' : 'Novo Contrato'}
          </h2>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Informações Básicas */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Informações Básicas</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Título do Contrato *
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
                  Tipo de Contrato *
                </label>
                <select
                  required
                  value={formData.type}
                  onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {contractTypes.map(type => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Valor Total (R$) *
                </label>
                <input
                  type="number"
                  required
                  min="0"
                  step="0.01"
                  value={formData.value}
                  onChange={(e) => setFormData({ ...formData, value: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Data de Início *
                </label>
                <input
                  type="date"
                  required
                  value={formData.startDate}
                  onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Data de Término
                </label>
                <input
                  type="date"
                  value={formData.endDate}
                  onChange={(e) => setFormData({ ...formData, endDate: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Forma de Pagamento *
                </label>
                <select
                  required
                  value={formData.paymentTerms}
                  onChange={(e) => setFormData({ ...formData, paymentTerms: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {paymentTermsOptions.map(term => (
                    <option key={term} value={term}>
                      {term}
                    </option>
                  ))}
                </select>
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
                  placeholder="Descreva o objeto do contrato..."
                />
              </div>
            </div>
          </div>

          {/* Cláusulas */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Cláusulas Contratuais</h3>
              <button
                type="button"
                onClick={addClause}
                className="flex items-center px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
              >
                <Plus className="h-4 w-4 mr-1" />
                Adicionar Cláusula
              </button>
            </div>
            
            <div className="space-y-3">
              {formData.clauses.map((clause, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="flex-1">
                    <input
                      type="text"
                      value={clause}
                      onChange={(e) => handleClauseChange(index, e.target.value)}
                      placeholder={`Cláusula ${index + 1}`}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  {formData.clauses.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeClause(index)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Observações Internas
            </label>
            <textarea
              rows={3}
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Observações que não aparecerão no contrato..."
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
              {contract ? 'Salvar' : 'Criar Contrato'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function Contracts() {
  const [contracts, setContracts] = useState(mockContracts)
  const [filteredContracts, setFilteredContracts] = useState(mockContracts)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingContract, setEditingContract] = useState(null)

  useEffect(() => {
    let filtered = contracts

    if (searchTerm) {
      filtered = filtered.filter(contract =>
        contract.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        contract.client.toLowerCase().includes(searchTerm.toLowerCase()) ||
        contract.description.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (statusFilter) {
      filtered = filtered.filter(contract => contract.status === statusFilter)
    }

    if (typeFilter) {
      filtered = filtered.filter(contract => contract.type === typeFilter)
    }

    setFilteredContracts(filtered)
  }, [contracts, searchTerm, statusFilter, typeFilter])

  const handleSaveContract = (contractData) => {
    if (editingContract) {
      setContracts(contracts.map(contract => 
        contract.id === editingContract.id 
          ? { ...contractData, id: editingContract.id, signedDate: editingContract.signedDate }
          : contract
      ))
      toast.success('Contrato atualizado com sucesso!')
    } else {
      const newContract = {
        ...contractData,
        id: Date.now().toString(),
        status: 'rascunho'
      }
      setContracts([newContract, ...contracts])
      toast.success('Contrato criado com sucesso!')
    }
    setEditingContract(null)
  }

  const handleEditContract = (contract) => {
    setEditingContract(contract)
    setShowModal(true)
  }

  const handleDeleteContract = (contractId) => {
    if (window.confirm('Tem certeza que deseja excluir este contrato?')) {
      setContracts(contracts.filter(contract => contract.id !== contractId))
      toast.success('Contrato excluído com sucesso!')
    }
  }

  const handleViewContract = (contract) => {
    toast.info('Visualização detalhada em desenvolvimento')
  }

  const handleSignContract = (contract) => {
    setContracts(contracts.map(c => 
      c.id === contract.id 
        ? { ...c, status: 'ativo', signedDate: new Date().toISOString().split('T')[0] }
        : c
    ))
    toast.success(`Contrato de ${contract.client} marcado como assinado!`)
  }

  const handleSuspendContract = (contract) => {
    if (window.confirm('Tem certeza que deseja suspender este contrato?')) {
      setContracts(contracts.map(c => 
        c.id === contract.id 
          ? { ...c, status: 'suspenso', suspendedDate: new Date().toISOString().split('T')[0] }
          : c
      ))
      toast.success(`Contrato de ${contract.client} suspenso!`)
    }
  }

  const handleRenewContract = (contract) => {
    const renewedContract = {
      ...contract,
      id: Date.now().toString(),
      title: `${contract.title} (Renovação)`,
      status: 'rascunho',
      startDate: contract.endDate,
      endDate: new Date(new Date(contract.endDate).setFullYear(new Date(contract.endDate).getFullYear() + 1)).toISOString().split('T')[0],
      signedDate: null,
      renewalDate: null
    }
    setContracts([renewedContract, ...contracts])
    toast.success('Contrato de renovação criado!')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Contratos</h1>
          <p className="text-gray-600">Gerencie seus contratos e documentos</p>
        </div>
        <button
          onClick={() => {
            setEditingContract(null)
            setShowModal(true)
          }}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4 mr-2" />
          Novo Contrato
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar contratos..."
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
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos os tipos</option>
              {contractTypes.map(type => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
            <div className="text-sm text-gray-500 whitespace-nowrap">
              {filteredContracts.length} de {contracts.length} contratos
            </div>
          </div>
        </div>
      </div>

      {/* Contracts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredContracts.map(contract => (
          <ContractCard
            key={contract.id}
            contract={contract}
            onEdit={handleEditContract}
            onDelete={handleDeleteContract}
            onView={handleViewContract}
            onSign={handleSignContract}
            onSuspend={handleSuspendContract}
            onRenew={handleRenewContract}
          />
        ))}
      </div>

      {filteredContracts.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <FileSignature className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhum contrato encontrado</h3>
          <p className="text-gray-500 mb-4">
            {searchTerm || statusFilter || typeFilter
              ? 'Tente ajustar os filtros de busca'
              : 'Comece criando seu primeiro contrato'
            }
          </p>
          {!searchTerm && !statusFilter && !typeFilter && (
            <button
              onClick={() => {
                setEditingContract(null)
                setShowModal(true)
              }}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="h-4 w-4 mr-2" />
              Criar Primeiro Contrato
            </button>
          )}
        </div>
      )}

      {/* Modal */}
      <ContractModal
        contract={editingContract}
        isOpen={showModal}
        onClose={() => {
          setShowModal(false)
          setEditingContract(null)
        }}
        onSave={handleSaveContract}
      />
    </div>
  )
}

