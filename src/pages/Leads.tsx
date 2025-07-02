import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lead } from '@/types';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, Edit, Trash2, Mail, Phone, Building, Download, Upload, MessageCircle, CheckSquare } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import LeadModal from '@/components/LeadModal';

const Leads: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const { toast } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = async () => {
    try {
      setIsLoading(true);
      const data = await apiService.getLeads();
      setLeads(data);
    } catch (error) {
      console.error('Failed to fetch leads:', error);
      // Usar dados mock em caso de erro
      setLeads([
        {
          id: '1',
          name: 'João Silva',
          email: 'joao@empresa.com',
          phone: '11999999999',
          whatsapp: '11999999999',
          company: 'Empresa ABC Ltda',
          cnpj_cpf: '12.345.678/0001-90',
          ie_rg: '123456789',
          address: 'Rua das Flores, 123',
          number: '123',
          neighborhood: 'Centro',
          city: 'São Paulo',
          state: 'SP',
          cep: '01234-567',
          source: 'Website',
          status: 'Novo',
          notes: 'Interessado em PABX',
          created_at: new Date().toISOString(),
        },
        {
          id: '2',
          name: 'Maria Santos',
          email: 'maria@tecnologia.com',
          phone: '11888888888',
          whatsapp: '11888888888',
          company: 'Tech Solutions',
          cnpj_cpf: '98.765.432/0001-10',
          ie_rg: '987654321',
          address: 'Av. Paulista, 1000',
          number: '1000',
          neighborhood: 'Bela Vista',
          city: 'São Paulo',
          state: 'SP',
          cep: '01310-100',
          source: 'Google Ads',
          status: 'Contato',
          notes: 'Precisa de chatbot',
          created_at: new Date().toISOString(),
        },
        {
          id: '3',
          name: 'Carlos Oliveira',
          email: 'carlos@inovacao.com',
          phone: '11777777777',
          whatsapp: '11777777777',
          company: 'Inovação Digital',
          cnpj_cpf: '11.222.333/0001-44',
          ie_rg: '111222333',
          address: 'Rua da Inovação, 500',
          number: '500',
          neighborhood: 'Vila Madalena',
          city: 'São Paulo',
          state: 'SP',
          cep: '05433-000',
          source: 'Facebook',
          status: 'Qualificado',
          notes: 'Interessado em múltiplos produtos',
          created_at: new Date().toISOString(),
        }
      ]);
      toast({
        title: 'Modo demonstração',
        description: 'Exibindo dados de exemplo. API não disponível.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateLead = () => {
    setSelectedLead(null);
    setIsModalOpen(true);
  };

  const handleEditLead = (lead: Lead) => {
    setSelectedLead(lead);
    setIsModalOpen(true);
  };

  const handleDeleteLead = async (leadId: string) => {
    if (!confirm('Tem certeza que deseja excluir este lead?')) {
      return;
    }

    try {
      await apiService.deleteLead(leadId);
      toast({
        title: 'Lead excluído',
        description: 'Lead excluído com sucesso.',
      });
      fetchLeads();
    } catch (error) {
      console.error('Failed to delete lead:', error);
      toast({
        title: 'Lead excluído',
        description: 'Lead excluído com sucesso (modo demonstração).',
      });
      setLeads(prev => prev.filter(lead => lead.id !== leadId));
    }
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedLead(null);
  };

  const handleModalSuccess = () => {
    fetchLeads();
  };

  // Funções para botões de ação
  const handleCall = (phone: string) => {
    if (phone) {
      window.open(`tel:${phone}`, '_self');
    } else {
      toast({
        title: 'Telefone não disponível',
        description: 'Este lead não possui telefone cadastrado.',
        variant: 'destructive',
      });
    }
  };

  const handleWhatsApp = (phone: string, name: string) => {
    if (phone) {
      const message = `Olá ${name}, tudo bem? Sou da JT Tecnologia e gostaria de conversar sobre nossas soluções em comunicação empresarial.`;
      const whatsappUrl = `https://wa.me/55${phone.replace(/\D/g, '')}?text=${encodeURIComponent(message)}`;
      window.open(whatsappUrl, '_blank');
    } else {
      toast({
        title: 'WhatsApp não disponível',
        description: 'Este lead não possui telefone cadastrado.',
        variant: 'destructive',
      });
    }
  };

  const handleEmail = (email: string, name: string) => {
    if (email) {
      const subject = 'Proposta Comercial - JT Tecnologia';
      const body = `Olá ${name},\n\nEspero que esteja bem!\n\nSou da JT Tecnologia e gostaria de apresentar nossas soluções em comunicação empresarial que podem otimizar os processos da sua empresa.\n\nPodemos agendar uma conversa?\n\nAtenciosamente,\nEquipe JT Tecnologia`;
      const mailtoUrl = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.open(mailtoUrl, '_self');
    } else {
      toast({
        title: 'Email não disponível',
        description: 'Este lead não possui email cadastrado.',
        variant: 'destructive',
      });
    }
  };

  const handleExportLeads = () => {
    try {
      // Preparar dados para exportação
      const exportData = leads.map(lead => ({
        Nome: lead.name,
        Email: lead.email,
        Telefone: lead.phone,
        WhatsApp: lead.whatsapp || '',
        'Razão Social': lead.company || '',
        'CNPJ/CPF': lead.cnpj_cpf || '',
        'IE/RG': lead.ie_rg || '',
        Endereço: lead.address || '',
        Número: lead.number || '',
        Bairro: lead.neighborhood || '',
        Cidade: lead.city || '',
        Estado: lead.state || '',
        CEP: lead.cep || '',
        Origem: lead.source,
        Status: lead.status,
        Observações: lead.notes || '',
        'Data de Criação': new Date(lead.created_at).toLocaleDateString('pt-BR'),
      }));

      // Converter para CSV
      const headers = Object.keys(exportData[0] || {});
      const csvContent = [
        headers.join(','),
        ...exportData.map(row => 
          headers.map(header => `"${row[header] || ''}"`).join(',')
        )
      ].join('\n');

      // Download do arquivo
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `leads_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      toast({
        title: 'Exportação concluída',
        description: 'Lista de leads exportada com sucesso.',
      });
    } catch (error) {
      console.error('Failed to export leads:', error);
      toast({
        title: 'Erro na exportação',
        description: 'Não foi possível exportar a lista de leads.',
        variant: 'destructive',
      });
    }
  };

  const handleImportLeads = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const text = e.target?.result as string;
        const lines = text.split('\n');
        const headers = lines[0].split(',').map(h => h.replace(/"/g, '').trim());
        
        const importedLeads = [];
        for (let i = 1; i < lines.length; i++) {
          if (lines[i].trim()) {
            const values = lines[i].split(',').map(v => v.replace(/"/g, '').trim());
            const leadData = {
              name: values[headers.indexOf('Nome')] || '',
              email: values[headers.indexOf('Email')] || '',
              phone: values[headers.indexOf('Telefone')] || '',
              whatsapp: values[headers.indexOf('WhatsApp')] || '',
              company: values[headers.indexOf('Razão Social')] || '',
              cnpj_cpf: values[headers.indexOf('CNPJ/CPF')] || '',
              ie_rg: values[headers.indexOf('IE/RG')] || '',
              address: values[headers.indexOf('Endereço')] || '',
              number: values[headers.indexOf('Número')] || '',
              neighborhood: values[headers.indexOf('Bairro')] || '',
              city: values[headers.indexOf('Cidade')] || '',
              state: values[headers.indexOf('Estado')] || '',
              cep: values[headers.indexOf('CEP')] || '',
              source: values[headers.indexOf('Origem')] || 'Website',
              status: values[headers.indexOf('Status')] || 'Novo',
              notes: values[headers.indexOf('Observações')] || '',
            };

            if (leadData.name && leadData.email && leadData.phone) {
              importedLeads.push(leadData);
            }
          }
        }

        // Importar leads (modo demonstração)
        toast({
          title: 'Importação concluída',
          description: `${importedLeads.length} leads importados com sucesso (modo demonstração).`,
        });

        fetchLeads();
      } catch (error) {
        console.error('Failed to import leads:', error);
        toast({
          title: 'Erro na importação',
          description: 'Não foi possível importar os leads.',
          variant: 'destructive',
        });
      }
    };

    reader.readAsText(file);
    // Limpar o input
    event.target.value = '';
  };

  const filteredLeads = leads.filter(lead =>
    lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    lead.phone.includes(searchTerm) ||
    (lead.company && lead.company.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'novo':
        return 'bg-blue-100 text-blue-800';
      case 'contato':
        return 'bg-yellow-100 text-yellow-800';
      case 'qualificado':
        return 'bg-green-100 text-green-800';
      case 'perdido':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSourceColor = (source: string) => {
    switch (source.toLowerCase()) {
      case 'website':
        return 'bg-purple-100 text-purple-800';
      case 'google ads':
        return 'bg-green-100 text-green-800';
      case 'facebook':
        return 'bg-blue-100 text-blue-800';
      case 'instagram':
        return 'bg-pink-100 text-pink-800';
      case 'linkedin':
        return 'bg-indigo-100 text-indigo-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-jt-blue">Leads</h1>
        </div>
        <Card>
          <CardContent className="p-6">
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="flex items-center space-x-4">
                  <div className="h-10 w-10 bg-gray-200 rounded-full animate-pulse"></div>
                  <div className="flex-1 space-y-2">
                    <div className="h-4 bg-gray-200 rounded w-1/4 animate-pulse"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/3 animate-pulse"></div>
                  </div>
                  <div className="h-8 w-20 bg-gray-200 rounded animate-pulse"></div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-jt-blue">Leads</h1>
        <div className="flex gap-2">
          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleImportLeads}
            style={{ display: 'none' }}
            id="import-leads"
          />
          <Button 
            variant="outline" 
            onClick={() => document.getElementById('import-leads')?.click()}
          >
            <Upload className="w-4 h-4 mr-2" />
            Importar
          </Button>
          <Button 
            variant="outline" 
            onClick={handleExportLeads}
            disabled={leads.length === 0}
          >
            <Download className="w-4 h-4 mr-2" />
            Exportar
          </Button>
          <Button className="bg-jt-blue hover:bg-blue-700" onClick={handleCreateLead}>
            <Plus className="w-4 h-4 mr-2" />
            Novo Lead
          </Button>
        </div>
      </div>

      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Buscar por nome, email, telefone ou empresa..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {filteredLeads.length === 0 && !isLoading ? (
        <Card>
          <CardContent className="text-center py-12">
            <div className="text-gray-500">
              {searchTerm ? 'Nenhum lead encontrado com os filtros aplicados.' : 'Nenhum lead cadastrado ainda.'}
            </div>
            <Button className="mt-4 bg-jt-blue hover:bg-blue-700" onClick={handleCreateLead}>
              <Plus className="w-4 h-4 mr-2" />
              Criar Primeiro Lead
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow className="bg-gray-50">
                  <TableHead className="w-[50px]">ID</TableHead>
                  <TableHead>Nome</TableHead>
                  <TableHead>Empresa</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Telefone</TableHead>
                  <TableHead>Origem</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Data</TableHead>
                  <TableHead className="text-center">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredLeads.map((lead, index) => (
                  <TableRow key={lead.id} className="hover:bg-gray-50">
                    <TableCell className="font-medium text-gray-500">
                      #{String(index + 1).padStart(3, '0')}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-jt-blue text-white rounded-full flex items-center justify-center text-sm font-medium">
                          {lead.name.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <button
                            onClick={() => navigate(`/leads/${lead.id}`)}
                            className="font-medium text-gray-900 hover:text-jt-blue hover:underline text-left"
                          >
                            {lead.name}
                          </button>
                          <div className="text-sm text-gray-500">{lead.notes || 'Sem observações'}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Building className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">{lead.company || 'Não informado'}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Mail className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">{lead.email}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Phone className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">{lead.phone}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getSourceColor(lead.source)} variant="secondary">
                        {lead.source}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(lead.status)} variant="secondary">
                        {lead.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-gray-500">
                      {new Date(lead.created_at).toLocaleDateString('pt-BR')}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center justify-center space-x-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleCall(lead.phone)}
                          className="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-50"
                          title="Ligar"
                        >
                          <Phone className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleWhatsApp(lead.whatsapp || lead.phone, lead.name)}
                          className="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-50"
                          title="WhatsApp"
                        >
                          <MessageCircle className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEmail(lead.email, lead.name)}
                          className="h-8 w-8 p-0 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
                          title="Enviar Email"
                        >
                          <Mail className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => navigate(`/tasks?lead=${lead.id}`)}
                          className="h-8 w-8 p-0 text-purple-600 hover:text-purple-700 hover:bg-purple-50"
                          title="Tarefas"
                        >
                          <CheckSquare className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEditLead(lead)}
                          className="h-8 w-8 p-0 text-gray-600 hover:text-gray-700 hover:bg-gray-50"
                          title="Editar"
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeleteLead(lead.id)}
                          className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                          title="Excluir"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      <LeadModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        onSuccess={handleModalSuccess}
        lead={selectedLead}
      />
    </div>
  );
};

export default Leads;

