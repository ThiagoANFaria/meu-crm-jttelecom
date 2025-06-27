import React, { useState, useEffect } from 'react';

const Leads = () => {
  const [leads, setLeads] = useState([]);
  const [filteredLeads, setFilteredLeads] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sourceFilter, setSourceFilter] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [editingLead, setEditingLead] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // grid ou list

  // Dados mock dos leads
  useEffect(() => {
    const mockLeads = [
      {
        id: 1,
        name: 'João Silva',
        email: 'joao@empresa.com',
        phone: '(11) 99999-9999',
        company: 'Tech Solutions Ltda',
        position: 'Diretor de TI',
        source: 'Website',
        status: 'new',
        score: 85,
        value: 15000,
        lastContact: '2024-01-15',
        notes: 'Interessado em soluções de telefonia IP',
        avatar: 'https://ui-avatars.com/api/?name=João+Silva&background=4169E1&color=fff'
      },
      {
        id: 2,
        name: 'Maria Santos',
        email: 'maria@comercio.com',
        phone: '(11) 88888-8888',
        company: 'Comércio & Cia',
        position: 'Gerente Comercial',
        source: 'LinkedIn',
        status: 'qualified',
        score: 92,
        value: 25000,
        lastContact: '2024-01-14',
        notes: 'Precisa de sistema completo de CRM',
        avatar: 'https://ui-avatars.com/api/?name=Maria+Santos&background=4169E1&color=fff'
      },
      {
        id: 3,
        name: 'Pedro Costa',
        email: 'pedro@startup.com',
        phone: '(11) 77777-7777',
        company: 'StartupTech',
        position: 'CEO',
        source: 'Indicação',
        status: 'proposal',
        score: 78,
        value: 8000,
        lastContact: '2024-01-13',
        notes: 'Startup em crescimento, orçamento limitado',
        avatar: 'https://ui-avatars.com/api/?name=Pedro+Costa&background=4169E1&color=fff'
      },
      {
        id: 4,
        name: 'Ana Oliveira',
        email: 'ana@consultoria.com',
        phone: '(11) 66666-6666',
        company: 'Consultoria Pro',
        position: 'Sócia',
        source: 'Google Ads',
        status: 'negotiation',
        score: 95,
        value: 35000,
        lastContact: '2024-01-12',
        notes: 'Pronta para fechar, aguardando aprovação final',
        avatar: 'https://ui-avatars.com/api/?name=Ana+Oliveira&background=4169E1&color=fff'
      },
      {
        id: 5,
        name: 'Carlos Mendes',
        email: 'carlos@industria.com',
        phone: '(11) 55555-5555',
        company: 'Indústria XYZ',
        position: 'Diretor Operacional',
        source: 'Evento',
        status: 'lost',
        score: 45,
        value: 12000,
        lastContact: '2024-01-10',
        notes: 'Optou por concorrente devido ao preço',
        avatar: 'https://ui-avatars.com/api/?name=Carlos+Mendes&background=4169E1&color=fff'
      }
    ];
    setLeads(mockLeads);
    setFilteredLeads(mockLeads);
  }, []);

  // Filtrar leads
  useEffect(() => {
    let filtered = leads;

    if (searchTerm) {
      filtered = filtered.filter(lead =>
        lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.company.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(lead => lead.status === statusFilter);
    }

    if (sourceFilter !== 'all') {
      filtered = filtered.filter(lead => lead.source === sourceFilter);
    }

    setFilteredLeads(filtered);
  }, [leads, searchTerm, statusFilter, sourceFilter]);

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800 border-blue-200',
      qualified: 'bg-green-100 text-green-800 border-green-200',
      proposal: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      negotiation: 'bg-purple-100 text-purple-800 border-purple-200',
      won: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      lost: 'bg-red-100 text-red-800 border-red-200'
    };
    return colors[status] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getStatusLabel = (status) => {
    const labels = {
      new: 'Novo',
      qualified: 'Qualificado',
      proposal: 'Proposta',
      negotiation: 'Negociação',
      won: 'Ganho',
      lost: 'Perdido'
    };
    return labels[status] || status;
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const renderStars = (score) => {
    const stars = Math.round(score / 20);
    return Array.from({ length: 5 }, (_, i) => (
      <i
        key={i}
        className={`fas fa-star text-sm ${
          i < stars ? 'text-yellow-400' : 'text-gray-300'
        }`}
      />
    ));
  };

  const handleAction = (action, leadId) => {
    console.log(`Ação ${action} para lead ${leadId}`);
    // Implementar ações específicas
  };

  const LeadCard = ({ lead }) => (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
      {/* Header do card */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <img
            src={lead.avatar}
            alt={lead.name}
            className="w-12 h-12 rounded-full border-2 border-blue-100"
          />
          <div>
            <h3 className="font-semibold text-gray-900 text-lg">{lead.name}</h3>
            <p className="text-sm text-gray-600">{lead.position}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(lead.status)}`}>
            {getStatusLabel(lead.status)}
          </span>
        </div>
      </div>

      {/* Informações da empresa */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <i className="fas fa-building text-gray-400 text-sm"></i>
          <span className="text-sm font-medium text-gray-700">{lead.company}</span>
        </div>
        <div className="flex items-center gap-2 mb-2">
          <i className="fas fa-envelope text-gray-400 text-sm"></i>
          <span className="text-sm text-gray-600">{lead.email}</span>
        </div>
        <div className="flex items-center gap-2">
          <i className="fas fa-phone text-gray-400 text-sm"></i>
          <span className="text-sm text-gray-600">{lead.phone}</span>
        </div>
      </div>

      {/* Score e valor */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="text-xs text-gray-500 mb-1">Score</p>
          <div className="flex items-center gap-2">
            <span className={`font-bold text-lg ${getScoreColor(lead.score)}`}>
              {lead.score}
            </span>
            <div className="flex gap-1">
              {renderStars(lead.score)}
            </div>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xs text-gray-500 mb-1">Valor Potencial</p>
          <p className="font-bold text-lg text-green-600">
            R$ {lead.value.toLocaleString('pt-BR')}
          </p>
        </div>
      </div>

      {/* Fonte e último contato */}
      <div className="flex items-center justify-between mb-4 text-sm">
        <div className="flex items-center gap-2">
          <i className="fas fa-tag text-gray-400"></i>
          <span className="text-gray-600">{lead.source}</span>
        </div>
        <div className="flex items-center gap-2">
          <i className="fas fa-clock text-gray-400"></i>
          <span className="text-gray-600">
            {new Date(lead.lastContact).toLocaleDateString('pt-BR')}
          </span>
        </div>
      </div>

      {/* Notas */}
      <div className="mb-4">
        <p className="text-sm text-gray-600 line-clamp-2">{lead.notes}</p>
      </div>

      {/* Ações */}
      <div className="flex gap-2">
        <button
          onClick={() => handleAction('call', lead.id)}
          className="flex-1 bg-blue-50 text-blue-600 py-2 px-3 rounded-lg text-sm font-medium hover:bg-blue-100 transition-colors flex items-center justify-center gap-2"
        >
          <i className="fas fa-phone"></i>
          Ligar
        </button>
        <button
          onClick={() => handleAction('email', lead.id)}
          className="flex-1 bg-green-50 text-green-600 py-2 px-3 rounded-lg text-sm font-medium hover:bg-green-100 transition-colors flex items-center justify-center gap-2"
        >
          <i className="fas fa-envelope"></i>
          Email
        </button>
        <button
          onClick={() => handleAction('whatsapp', lead.id)}
          className="flex-1 bg-emerald-50 text-emerald-600 py-2 px-3 rounded-lg text-sm font-medium hover:bg-emerald-100 transition-colors flex items-center justify-center gap-2"
        >
          <i className="fab fa-whatsapp"></i>
          WhatsApp
        </button>
      </div>
    </div>
  );

  const LeadListItem = ({ lead }) => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 hover:shadow-md transition-all duration-200">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 flex-1">
          <img
            src={lead.avatar}
            alt={lead.name}
            className="w-10 h-10 rounded-full border-2 border-blue-100"
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3 mb-1">
              <h3 className="font-semibold text-gray-900">{lead.name}</h3>
              <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(lead.status)}`}>
                {getStatusLabel(lead.status)}
              </span>
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <span>{lead.company}</span>
              <span>{lead.email}</span>
              <span>{lead.phone}</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-6">
          <div className="text-center">
            <p className="text-xs text-gray-500">Score</p>
            <div className="flex items-center gap-1">
              <span className={`font-bold ${getScoreColor(lead.score)}`}>
                {lead.score}
              </span>
              <div className="flex gap-0.5">
                {renderStars(lead.score)}
              </div>
            </div>
          </div>
          
          <div className="text-center">
            <p className="text-xs text-gray-500">Valor</p>
            <p className="font-bold text-green-600">
              R$ {lead.value.toLocaleString('pt-BR')}
            </p>
          </div>
          
          <div className="flex gap-1">
            <button
              onClick={() => handleAction('call', lead.id)}
              className="w-8 h-8 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors flex items-center justify-center"
            >
              <i className="fas fa-phone text-xs"></i>
            </button>
            <button
              onClick={() => handleAction('email', lead.id)}
              className="w-8 h-8 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition-colors flex items-center justify-center"
            >
              <i className="fas fa-envelope text-xs"></i>
            </button>
            <button
              onClick={() => handleAction('whatsapp', lead.id)}
              className="w-8 h-8 bg-emerald-50 text-emerald-600 rounded-lg hover:bg-emerald-100 transition-colors flex items-center justify-center"
            >
              <i className="fab fa-whatsapp text-xs"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Leads</h1>
            <p className="text-gray-600">Gerencie seus leads e oportunidades de vendas</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-blue-700 transition-colors flex items-center gap-2 shadow-lg hover:shadow-xl"
          >
            <i className="fas fa-plus"></i>
            Novo Lead
          </button>
        </div>

        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total de Leads</p>
                <p className="text-2xl font-bold text-gray-900">{leads.length}</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <i className="fas fa-users text-blue-600 text-xl"></i>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Qualificados</p>
                <p className="text-2xl font-bold text-green-600">
                  {leads.filter(l => l.status === 'qualified').length}
                </p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <i className="fas fa-check-circle text-green-600 text-xl"></i>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Em Negociação</p>
                <p className="text-2xl font-bold text-purple-600">
                  {leads.filter(l => l.status === 'negotiation').length}
                </p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                <i className="fas fa-handshake text-purple-600 text-xl"></i>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Valor Total</p>
                <p className="text-2xl font-bold text-emerald-600">
                  R$ {leads.reduce((sum, lead) => sum + lead.value, 0).toLocaleString('pt-BR')}
                </p>
              </div>
              <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
                <i className="fas fa-dollar-sign text-emerald-600 text-xl"></i>
              </div>
            </div>
          </div>
        </div>

        {/* Filtros e busca */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-6">
          <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
            <div className="flex flex-col sm:flex-row gap-4 flex-1">
              <div className="relative flex-1 max-w-md">
                <i className="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                <input
                  type="text"
                  placeholder="Buscar leads..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">Todos os Status</option>
                <option value="new">Novo</option>
                <option value="qualified">Qualificado</option>
                <option value="proposal">Proposta</option>
                <option value="negotiation">Negociação</option>
                <option value="won">Ganho</option>
                <option value="lost">Perdido</option>
              </select>
              
              <select
                value={sourceFilter}
                onChange={(e) => setSourceFilter(e.target.value)}
                className="px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">Todas as Fontes</option>
                <option value="Website">Website</option>
                <option value="LinkedIn">LinkedIn</option>
                <option value="Indicação">Indicação</option>
                <option value="Google Ads">Google Ads</option>
                <option value="Evento">Evento</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-3 rounded-xl transition-colors ${
                  viewMode === 'grid'
                    ? 'bg-blue-100 text-blue-600'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <i className="fas fa-th-large"></i>
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-3 rounded-xl transition-colors ${
                  viewMode === 'list'
                    ? 'bg-blue-100 text-blue-600'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <i className="fas fa-list"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Lista de leads */}
      {filteredLeads.length === 0 ? (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 text-center">
          <i className="fas fa-search text-4xl text-gray-300 mb-4"></i>
          <h3 className="text-xl font-semibold text-gray-600 mb-2">Nenhum lead encontrado</h3>
          <p className="text-gray-500">Tente ajustar os filtros ou adicionar um novo lead</p>
        </div>
      ) : (
        <div className={
          viewMode === 'grid'
            ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
            : 'space-y-4'
        }>
          {filteredLeads.map(lead => (
            viewMode === 'grid' ? (
              <LeadCard key={lead.id} lead={lead} />
            ) : (
              <LeadListItem key={lead.id} lead={lead} />
            )
          ))}
        </div>
      )}
    </div>
  );
};

export default Leads;

