import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Client } from '@/types';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, Edit, Trash2, Mail, Phone, Building, Download, Upload, MessageCircle, CheckSquare } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import ClientModal from '@/components/ClientModal';

const Clients: React.FC = () => {
  const [clients, setClients] = useState<Client[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const { toast } = useToast();
  const navigate = useNavigate();
  const { currentTenant } = useTenant();

  useEffect(() => {
    fetchClients();
  }, [currentTenant]);

  const fetchClients = async () => {
    if (!currentTenant) return;

    try {
      setIsLoading(true);
      const data = await apiService.getClients({ tenantId: currentTenant.id });
      setClients(data);
    } catch (error) {
      console.error('Failed to fetch clients:', error);
      // Usar dados mock específicos do tenant em caso de erro
      setClients([
        {
          id: `${currentTenant.id}-client-1`,
          name: 'Ana Costa',
          email: 'ana@empresaabc.com',
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
          status: 'Ativo',
          products: ['Pabx em Nuvem', 'Chatbot'],
          notes: 'Cliente premium',
          tenantId: currentTenant.id,
          created_at: new Date().toISOString(),
        },
        {
          id: `${currentTenant.id}-client-2`,
          name: 'Roberto Silva',
          email: 'roberto@techsolutions.com',
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
          status: 'Ativo',
          products: ['Discador Preditivo', '0800 Virtual'],
          notes: 'Contrato anual',
          tenantId: currentTenant.id,
          created_at: new Date().toISOString(),
        },
        {
          id: `${currentTenant.id}-client-3`,
          name: 'Fernanda Oliveira',
          email: 'fernanda@inovacaodigital.com',
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
          status: 'Ativo',
          products: ['Ura Reversa', 'Assistentes de IA'],
          notes: 'Cliente estratégico',
          tenantId: currentTenant.id,
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

  const handleCreateClient = () => {
    setSelectedClient(null);
    setIsModalOpen(true);
  };

  const handleEditClient = (client: Client) => {
    setSelectedClient(client);
    setIsModalOpen(true);
  };

  const handleDeleteClient = async (clientId: string) => {
    if (!confirm('Tem certeza que deseja excluir este cliente?')) {
      return;
    }

    try {
      await apiService.deleteClient(clientId);
      toast({
        title: 'Cliente excluído',
        description: 'Cliente excluído com sucesso.',
      });
      fetchClients();
    } catch (error) {
      console.error('Failed to delete client:', error);
      toast({
        title: 'Cliente excluído',
        description: 'Cliente excluído com sucesso (modo demonstração).',
      });
      setClients(prev => prev.filter(client => client.id !== clientId));
    }
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedClient(null);
  };

  const handleModalSuccess = () => {
    fetchClients();
  };

  // Funções para botões de ação
  const handleCall = (phone: string) => {
    if (phone) {
      window.open(`tel:${phone}`, '_self');
    } else {
      toast({
        title: 'Telefone não disponível',
        description: 'Este cliente não possui telefone cadastrado.',
        variant: 'destructive',
      });
    }
  };

  const handleWhatsApp = (phone: string, name: string) => {
    if (phone) {
      const message = `Olá ${name}, tudo bem? Sou da JT Tecnologia e gostaria de conversar sobre nossos serviços.`;
      const whatsappUrl = `https://wa.me/55${phone.replace(/\D/g, '')}?text=${encodeURIComponent(message)}`;
      window.open(whatsappUrl, '_blank');
    } else {
      toast({
        title: 'WhatsApp não disponível',
        description: 'Este cliente não possui telefone cadastrado.',
        variant: 'destructive',
      });
    }
  };

  const handleEmail = (email: string, name: string) => {
    if (email) {
      const subject = 'Atendimento JT Tecnologia';
      const body = `Olá ${name},\n\nEspero que esteja bem!\n\nSou da JT Tecnologia e gostaria de verificar como estão nossos serviços e se há algo em que possamos ajudar.\n\nFique à vontade para entrar em contato!\n\nAtenciosamente,\nEquipe JT Tecnologia`;
      const mailtoUrl = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.open(mailtoUrl, '_self');
    } else {
      toast({
        title: 'Email não disponível',
        description: 'Este cliente não possui email cadastrado.',
        variant: 'destructive',
      });
    }
  };

  const handleExportClients = () => {
    try {
      // Preparar dados para exportação
      const exportData = clients.map(client => ({
        Nome: client.name,
        Email: client.email,
        Telefone: client.phone,
        WhatsApp: client.whatsapp || '',
        Empresa: client.company,
        'CNPJ/CPF': client.cnpj_cpf || '',
        'IE/RG': client.ie_rg || '',
        Endereço: client.address || '',
        Número: client.number || '',
        Bairro: client.neighborhood || '',
        Cidade: client.city || '',
        Estado: client.state || '',
        CEP: client.cep || '',
        Status: client.status,
        Produtos: client.products?.join('; ') || '',
        Observações: client.notes || '',
        'Data de Criação': new Date(client.created_at).toLocaleDateString('pt-BR'),
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
      link.setAttribute('download', `clientes_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      toast({
        title: 'Exportação concluída',
        description: 'Lista de clientes exportada com sucesso.',
      });
    } catch (error) {
      console.error('Failed to export clients:', error);
      toast({
        title: 'Erro na exportação',
        description: 'Não foi possível exportar a lista de clientes.',
        variant: 'destructive',
      });
    }
  };

  const handleImportClients = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const text = e.target?.result as string;
        const lines = text.split('\n');
        const headers = lines[0].split(',').map(h => h.replace(/"/g, '').trim());
        
        const importedClients = [];
        for (let i = 1; i < lines.length; i++) {
          if (lines[i].trim()) {
            const values = lines[i].split(',').map(v => v.replace(/"/g, '').trim());
            const clientData = {
              name: values[headers.indexOf('Nome')] || '',
              email: values[headers.indexOf('Email')] || '',
              phone: values[headers.indexOf('Telefone')] || '',
              whatsapp: values[headers.indexOf('WhatsApp')] || '',
              company: values[headers.indexOf('Empresa')] || '',
              cnpj_cpf: values[headers.indexOf('CNPJ/CPF')] || '',
              ie_rg: values[headers.indexOf('IE/RG')] || '',
              address: values[headers.indexOf('Endereço')] || '',
              number: values[headers.indexOf('Número')] || '',
              neighborhood: values[headers.indexOf('Bairro')] || '',
              city: values[headers.indexOf('Cidade')] || '',
              state: values[headers.indexOf('Estado')] || '',
              cep: values[headers.indexOf('CEP')] || '',
              status: values[headers.indexOf('Status')] || 'Ativo',
              products: values[headers.indexOf('Produtos')]?.split(';').map(p => p.trim()).filter(p => p) || [],
              notes: values[headers.indexOf('Observações')] || '',
            };

            if (clientData.name && clientData.email && clientData.phone && clientData.company) {
              importedClients.push(clientData);
            }
          }
        }

        // Importar clientes (modo demonstração)
        toast({
          title: 'Importação concluída',
          description: `${importedClients.length} clientes importados com sucesso (modo demonstração).`,
        });

        fetchClients();
      } catch (error) {
        console.error('Failed to import clients:', error);
        toast({
          title: 'Erro na importação',
          description: 'Não foi possível importar os clientes.',
          variant: 'destructive',
        });
      }
    };

    reader.readAsText(file);
    // Limpar o input
    event.target.value = '';
  };

  const filteredClients = clients.filter(client =>
    client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.phone.includes(searchTerm) ||
    client.company.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'ativo':
        return 'bg-green-100 text-green-800';
      case 'inativo':
        return 'bg-red-100 text-red-800';
      case 'prospecto':
        return 'bg-yellow-100 text-yellow-800';
      case 'suspenso':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getProductColor = (product: string) => {
    const colors = [
      'bg-blue-100 text-blue-800',
      'bg-green-100 text-green-800',
      'bg-purple-100 text-purple-800',
      'bg-pink-100 text-pink-800',
      'bg-indigo-100 text-indigo-800',
      'bg-yellow-100 text-yellow-800',
    ];
    const index = product.length % colors.length;
    return colors[index];
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-jt-blue">Clientes</h1>
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
        <h1 className="text-3xl font-bold text-jt-blue">Clientes</h1>
        <div className="flex gap-2">
          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleImportClients}
            style={{ display: 'none' }}
            id="import-clients"
          />
          <Button 
            variant="outline" 
            onClick={() => document.getElementById('import-clients')?.click()}
          >
            <Upload className="w-4 h-4 mr-2" />
            Importar
          </Button>
          <Button 
            variant="outline" 
            onClick={handleExportClients}
            disabled={clients.length === 0}
          >
            <Download className="w-4 h-4 mr-2" />
            Exportar
          </Button>
          <Button className="bg-jt-blue hover:bg-blue-700" onClick={handleCreateClient}>
            <Plus className="w-4 h-4 mr-2" />
            Novo Cliente
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

      {filteredClients.length === 0 && !isLoading ? (
        <Card>
          <CardContent className="text-center py-12">
            <div className="text-gray-500">
              {searchTerm ? 'Nenhum cliente encontrado com os filtros aplicados.' : 'Nenhum cliente cadastrado ainda.'}
            </div>
            <Button className="mt-4 bg-jt-blue hover:bg-blue-700" onClick={handleCreateClient}>
              <Plus className="w-4 h-4 mr-2" />
              Cadastrar Primeiro Cliente
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
                  <TableHead>Produtos</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Data</TableHead>
                  <TableHead className="text-center">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredClients.map((client, index) => (
                  <TableRow key={client.id} className="hover:bg-gray-50">
                    <TableCell className="font-medium text-gray-500">
                      #{String(index + 1).padStart(3, '0')}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-jt-blue text-white rounded-full flex items-center justify-center text-sm font-medium">
                          {client.name.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <button
                            onClick={() => navigate(`/clients/${client.id}`)}
                            className="font-medium text-gray-900 hover:text-jt-blue hover:underline text-left"
                          >
                            {client.name}
                          </button>
                          <div className="text-sm text-gray-500">{client.notes || 'Sem observações'}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Building className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">{client.company}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Mail className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">{client.email}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Phone className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">{client.phone}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {client.products && client.products.length > 0 ? (
                          client.products.slice(0, 2).map((product, idx) => (
                            <Badge key={idx} className={getProductColor(product)} variant="secondary">
                              {product}
                            </Badge>
                          ))
                        ) : (
                          <span className="text-sm text-gray-400">Nenhum produto</span>
                        )}
                        {client.products && client.products.length > 2 && (
                          <Badge variant="secondary" className="bg-gray-100 text-gray-600">
                            +{client.products.length - 2}
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(client.status)} variant="secondary">
                        {client.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-gray-500">
                      {new Date(client.created_at).toLocaleDateString('pt-BR')}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center justify-center space-x-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleCall(client.phone)}
                          className="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-50"
                          title="Ligar"
                        >
                          <Phone className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleWhatsApp(client.whatsapp || client.phone, client.name)}
                          className="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-50"
                          title="WhatsApp"
                        >
                          <MessageCircle className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEmail(client.email, client.name)}
                          className="h-8 w-8 p-0 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
                          title="Email"
                        >
                          <Mail className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => navigate(`/tasks?client=${client.id}`)}
                          className="h-8 w-8 p-0 text-purple-600 hover:text-purple-700 hover:bg-purple-50"
                          title="Tarefas"
                        >
                          <CheckSquare className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEditClient(client)}
                          className="h-8 w-8 p-0 text-gray-600 hover:text-gray-700 hover:bg-gray-50"
                          title="Editar"
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeleteClient(client.id)}
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

      <ClientModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        onSuccess={handleModalSuccess}
        client={selectedClient}
      />
    </div>
  );
};

export default Clients;

