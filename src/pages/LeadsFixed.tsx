import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lead } from '@/types';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Users, Plus, Search, Edit, Trash2, Mail, Phone, Building, 
  UserCheck, MoreHorizontal, ArrowUpDown, MessageSquare, 
  Calendar, FileText, Star, Target
} from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import LeadModal from '@/components/LeadModal';

const LeadsFixed: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [filteredLeads, setFilteredLeads] = useState<Lead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  
  const navigate = useNavigate();
  const { toast } = useToast();
  const { currentTenant } = useTenant();

  // Buscar leads específicos do tenant
  const fetchLeads = async () => {
    if (!currentTenant) return;

    try {
      setIsLoading(true);
      // Buscar leads específicos do tenant
      const response = await apiService.getLeads({ tenantId: currentTenant.id });
      setLeads(response || []);
      setFilteredLeads(response || []);
    } catch (error) {
      console.error('Failed to fetch leads:', error);
      // Usar dados mock específicos do tenant em caso de erro
      const mockLeads: Lead[] = [
        {
          id: `${currentTenant.id}-lead-1`,
          name: 'João Silva',
          email: 'joao@empresa.com',
          phone: '11999999999',
          whatsapp: '11999999999',
          company: 'Empresa XYZ',
          cnpj_cpf: '12.345.678/0001-90',
          ie_rg: '123456789',
          address: 'Rua das Flores, 123',
          number: '123',
          neighborhood: 'Centro',
          city: 'São Paulo',
          state: 'SP',
          cep: '01234-567',
          status: 'novo',
          source: 'website',
          notes: 'Lead interessado em nossos serviços',
          score: 85,
          tags: ['vip', 'urgente'],
          tenantId: currentTenant.id,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      ];
      setLeads(mockLeads);
      setFilteredLeads(mockLeads);
      
      toast({
        title: 'Aviso',
        description: 'Usando dados de exemplo. Verifique a conexão com a API.',
        variant: 'default',
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, [currentTenant]);

  // Filtrar leads
  useEffect(() => {
    let filtered = leads;

    // Filtro por status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(lead => lead.status === statusFilter);
    }

    // Filtro por busca
    if (searchTerm) {
      filtered = filtered.filter(lead =>
        lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.company?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lead.phone.includes(searchTerm)
      );
    }

    // Ordenação
    filtered.sort((a, b) => {
      let aValue: any = a[sortBy as keyof Lead];
      let bValue: any = b[sortBy as keyof Lead];

      if (sortBy === 'created_at' || sortBy === 'updated_at') {
        aValue = new Date(aValue).getTime();
        bValue = new Date(bValue).getTime();
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    setFilteredLeads(filtered);
  }, [leads, searchTerm, statusFilter, sortBy, sortOrder]);

  const handleCreateLead = () => {
    setSelectedLead(null);
    setIsModalOpen(true);
  };

  const handleEditLead = (lead: Lead) => {
    setSelectedLead(lead);
    setIsModalOpen(true);
  };

  const handleDeleteLead = async (leadId: string) => {
    if (!currentTenant || !confirm('Tem certeza que deseja excluir este lead?')) return;

    try {
      await apiService.deleteLead(leadId, { tenantId: currentTenant.id });
      setLeads(leads.filter(lead => lead.id !== leadId));
      toast({
        title: 'Sucesso',
        description: 'Lead excluído com sucesso.',
      });
    } catch (error) {
      console.error('Failed to delete lead:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível excluir o lead.',
        variant: 'destructive',
      });
    }
  };

  const handleConvertToClient = async (leadId: string) => {
    if (!currentTenant) return;

    try {
      await apiService.convertLeadToClient(leadId, { tenantId: currentTenant.id });
      setLeads(leads.filter(lead => lead.id !== leadId));
      toast({
        title: 'Sucesso',
        description: 'Lead convertido em cliente com sucesso.',
      });
    } catch (error) {
      console.error('Failed to convert lead:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível converter o lead.',
        variant: 'destructive',
      });
    }
  };

  const handleStatusChange = async (leadId: string, newStatus: string) => {
    if (!currentTenant) return;

    try {
      const updatedLead = await apiService.updateLeadStatus(leadId, newStatus, { tenantId: currentTenant.id });
      setLeads(leads.map(lead => 
        lead.id === leadId ? { ...lead, status: newStatus } : lead
      ));
      toast({
        title: 'Sucesso',
        description: 'Status do lead atualizado com sucesso.',
      });
    } catch (error) {
      console.error('Failed to update lead status:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível atualizar o status do lead.',
        variant: 'destructive',
      });
    }
  };

  const handleModalSuccess = (lead: Lead) => {
    if (selectedLead) {
      // Atualizar lead existente
      setLeads(leads.map(l => l.id === lead.id ? lead : l));
    } else {
      // Adicionar novo lead
      setLeads([lead, ...leads]);
    }
    setIsModalOpen(false);
    setSelectedLead(null);
  };

  const getStatusColor = (status: string) => {
    const colors = {
      'novo': 'bg-blue-100 text-blue-800',
      'contato': 'bg-yellow-100 text-yellow-800',
      'qualificado': 'bg-green-100 text-green-800',
      'proposta': 'bg-purple-100 text-purple-800',
      'negociacao': 'bg-orange-100 text-orange-800',
      'fechado': 'bg-emerald-100 text-emerald-800',
      'perdido': 'bg-red-100 text-red-800'
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-jt-blue">Leads</h1>
        </div>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jt-blue"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Users className="w-8 h-8 text-jt-blue" />
          <h1 className="text-3xl font-bold text-jt-blue">Leads</h1>
        </div>
        <Button onClick={handleCreateLead} className="bg-jt-blue hover:bg-jt-blue/90">
          <Plus className="w-4 h-4 mr-2" />
          Novo Lead
        </Button>
      </div>

      {/* Estatísticas */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{leads.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Novos</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {leads.filter(l => l.status === 'novo').length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Qualificados</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {leads.filter(l => l.status === 'qualificado').length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Conversão</CardTitle>
            <UserCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {leads.length > 0 ? Math.round((leads.filter(l => l.status === 'fechado').length / leads.length) * 100) : 0}%
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filtros */}
      <div className="flex gap-4 items-center">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Buscar leads..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Filtrar por status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos os status</SelectItem>
            <SelectItem value="novo">Novo</SelectItem>
            <SelectItem value="contato">Contato</SelectItem>
            <SelectItem value="qualificado">Qualificado</SelectItem>
            <SelectItem value="proposta">Proposta</SelectItem>
            <SelectItem value="negociacao">Negociação</SelectItem>
            <SelectItem value="fechado">Fechado</SelectItem>
            <SelectItem value="perdido">Perdido</SelectItem>
          </SelectContent>
        </Select>
        <Button
          variant="outline"
          onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
          className="flex items-center gap-2"
        >
          <ArrowUpDown className="w-4 h-4" />
          {sortOrder === 'asc' ? 'Crescente' : 'Decrescente'}
        </Button>
      </div>

      {/* Tabela de Leads */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nome</TableHead>
                <TableHead>Empresa</TableHead>
                <TableHead>Contato</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Score</TableHead>
                <TableHead>Criado em</TableHead>
                <TableHead className="text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLeads.map((lead) => (
                <TableRow key={lead.id} className="cursor-pointer hover:bg-gray-50">
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-jt-blue text-white rounded-full flex items-center justify-center text-sm font-medium">
                        {lead.name.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <div className="font-medium">{lead.name}</div>
                        <div className="text-sm text-gray-500">{lead.email}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Building className="w-4 h-4 text-gray-400" />
                      <span>{lead.company || 'N/A'}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 text-sm">
                        <Phone className="w-3 h-3 text-gray-400" />
                        <span>{lead.phone}</span>
                      </div>
                      {lead.whatsapp && (
                        <div className="flex items-center gap-2 text-sm">
                          <MessageSquare className="w-3 h-3 text-green-500" />
                          <span>{lead.whatsapp}</span>
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(lead.status)}>
                      {lead.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className={`font-medium ${getScoreColor(lead.score || 0)}`}>
                      {lead.score || 0}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="text-sm text-gray-500">
                      {new Date(lead.created_at).toLocaleDateString('pt-BR')}
                    </div>
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Ações</DropdownMenuLabel>
                        <DropdownMenuItem onClick={() => navigate(`/leads/${lead.id}`)}>
                          <FileText className="mr-2 h-4 w-4" />
                          Ver Detalhes
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleEditLead(lead)}>
                          <Edit className="mr-2 h-4 w-4" />
                          Editar
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem onClick={() => handleConvertToClient(lead.id)}>
                          <UserCheck className="mr-2 h-4 w-4" />
                          Converter em Cliente
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem 
                          onClick={() => handleDeleteLead(lead.id)}
                          className="text-red-600"
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Excluir
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          
          {filteredLeads.length === 0 && (
            <div className="text-center py-8">
              <Users className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum lead encontrado</h3>
              <p className="mt-1 text-sm text-gray-500">
                {searchTerm || statusFilter !== 'all' 
                  ? 'Tente ajustar os filtros de busca.'
                  : 'Comece criando um novo lead.'
                }
              </p>
              {!searchTerm && statusFilter === 'all' && (
                <div className="mt-6">
                  <Button onClick={handleCreateLead} className="bg-jt-blue hover:bg-jt-blue/90">
                    <Plus className="w-4 h-4 mr-2" />
                    Novo Lead
                  </Button>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Modal de Lead */}
      <LeadModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedLead(null);
        }}
        onSuccess={handleModalSuccess}
        lead={selectedLead}
      />
    </div>
  );
};

export default LeadsFixed;

