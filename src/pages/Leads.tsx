
import React, { useEffect, useState } from 'react';
import { Lead } from '@/types';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, Edit, Trash2, Mail, Phone, Building, Download, Upload } from 'lucide-react';
import LeadModal from '@/components/LeadModal';

const Leads: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const { toast } = useToast();

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
      toast({
        title: 'Erro ao carregar leads',
        description: 'Não foi possível carregar a lista de leads.',
        variant: 'destructive',
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
        title: 'Erro ao excluir',
        description: 'Não foi possível excluir o lead.',
        variant: 'destructive',
      });
    }
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedLead(null);
  };

  const handleModalSuccess = () => {
    fetchLeads();
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

        // Importar leads
        for (const leadData of importedLeads) {
          try {
            await apiService.createLead(leadData);
          } catch (error) {
            console.error('Failed to import lead:', leadData.name, error);
          }
        }

        toast({
          title: 'Importação concluída',
          description: `${importedLeads.length} leads importados com sucesso.`,
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
    lead.phone.includes(searchTerm)
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

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-jt-blue">Leads</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <div className="h-4 bg-gray-200 rounded w-3/4 animate-pulse"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2 animate-pulse"></div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="h-3 bg-gray-200 rounded w-full animate-pulse"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3 animate-pulse"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
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
            placeholder="Buscar leads..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredLeads.map((lead) => (
          <Card key={lead.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg">{lead.name}</CardTitle>
                  <CardDescription className="text-sm">
                    {lead.source}
                  </CardDescription>
                </div>
                <Badge className={getStatusColor(lead.status)}>
                  {lead.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Mail className="w-4 h-4" />
                  <span>{lead.email}</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Phone className="w-4 h-4" />
                  <span>{lead.phone}</span>
                </div>
                <div className="text-xs text-gray-500">
                  Criado em: {new Date(lead.created_at).toLocaleDateString('pt-BR')}
                </div>
              </div>
              <div className="flex gap-2 mt-4">
                <Button variant="outline" size="sm" className="flex-1" onClick={() => handleEditLead(lead)}>
                  <Edit className="w-4 h-4 mr-1" />
                  Editar
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="text-red-600 hover:text-red-700"
                  onClick={() => handleDeleteLead(lead.id)}
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredLeads.length === 0 && !isLoading && (
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
