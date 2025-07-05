import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { 
  Plus,
  Edit,
  Trash2,
  FileText,
  Eye,
  Search,
  Filter,
  Send,
  Download,
  Calculator,
  Package,
  User,
  Calendar,
  DollarSign,
  Mail,
  MessageSquare,
  Save,
  Copy,
  CheckCircle,
  Clock,
  AlertCircle,
  X
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/AuthContext';
import { useTenant } from '@/contexts/TenantContext';

interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  basePrice: number;
  isActive: boolean;
}

interface ProposalItem {
  id: string;
  productId: string;
  productName: string;
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
}

interface Proposal {
  id: string;
  number: string;
  clientId: string;
  clientName: string;
  clientEmail: string;
  clientPhone: string;
  clientCompany: string;
  clientCnpj: string;
  responsibleId: string;
  responsibleName: string;
  items: ProposalItem[];
  subtotal: number;
  discount: number;
  total: number;
  observations: string;
  validUntil: string;
  paymentTerms: string;
  status: 'draft' | 'sent' | 'approved' | 'rejected' | 'expired';
  templateId: string;
  createdAt: string;
  updatedAt: string;
  sentAt?: string;
  approvedAt?: string;
}

interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  content: string;
  isDefault: boolean;
}

const Proposals: React.FC = () => {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedProposal, setSelectedProposal] = useState<Proposal | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [showItemDialog, setShowItemDialog] = useState(false);
  const [editingItem, setEditingItem] = useState<ProposalItem | null>(null);
  const { toast } = useToast();
  const { user } = useAuth();
  const { currentTenant, tenantProducts, tenantTemplates } = useTenant();

  useEffect(() => {
    loadProposals();
    loadProducts();
    loadTemplates();
  }, [currentTenant, tenantProducts, tenantTemplates]);

  const loadProposals = () => {
    const mockProposals: Proposal[] = [
      {
        id: '1',
        number: 'PROP-2025-001',
        clientId: '1',
        clientName: 'João Silva',
        clientEmail: 'joao@empresa.com',
        clientPhone: '(11) 99999-9999',
        clientCompany: 'Empresa ABC Ltda',
        clientCnpj: '12.345.678/0001-90',
        responsibleId: user?.id || '1',
        responsibleName: user?.name || 'Vendedor',
        items: [
          {
            id: '1',
            productId: '1',
            productName: 'JT VOX',
            description: 'PABX em Nuvem completo',
            quantity: 10,
            unitPrice: 89.90,
            total: 899.00
          }
        ],
        subtotal: 899.00,
        discount: 0,
        total: 899.00,
        observations: 'Proposta para implementação de PABX em nuvem',
        validUntil: '2025-08-05',
        paymentTerms: 'Mensal via boleto',
        status: 'draft',
        templateId: '1',
        createdAt: '2025-07-05T19:30:00Z',
        updatedAt: '2025-07-05T19:30:00Z'
      }
    ];
    setProposals(mockProposals);
  };

  const loadProducts = () => {
    if (!currentTenant) return;

    // Usar produtos do tenant (base + personalizados)
    const tenantProductsFormatted: Product[] = tenantProducts.map(p => ({
      id: p.id,
      name: p.name,
      description: p.description || '',
      category: p.category || 'geral',
      basePrice: p.price || 0,
      isActive: p.isActive !== false
    }));

    setProducts(tenantProductsFormatted);
  };

  const loadTemplates = () => {
    if (!currentTenant) return;

    // Usar templates do tenant
    const tenantTemplatesFormatted: Template[] = tenantTemplates.map(t => ({
      id: t.id,
      name: t.name,
      description: t.description || '',
      category: t.category || 'geral',
      content: t.content || '',
      isDefault: t.isDefault || false
    }));

    setTemplates(tenantTemplatesFormatted);
  };

  const handleCreateProposal = () => {
    const newProposal: Proposal = {
      id: Date.now().toString(),
      number: `PROP-${new Date().getFullYear()}-${String(proposals.length + 1).padStart(3, '0')}`,
      clientId: '',
      clientName: '',
      clientEmail: '',
      clientPhone: '',
      clientCompany: '',
      clientCnpj: '',
      responsibleId: user?.id || '',
      responsibleName: user?.name || '',
      items: [],
      subtotal: 0,
      discount: 0,
      total: 0,
      observations: '',
      validUntil: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      paymentTerms: 'Mensal via boleto',
      status: 'draft',
      templateId: templates.find(t => t.isDefault)?.id || '1',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    setSelectedProposal(newProposal);
    setIsCreating(true);
    setIsEditing(true);
  };

  const handleSaveProposal = () => {
    if (!selectedProposal) return;

    if (!selectedProposal.clientName.trim()) {
      toast({
        title: 'Erro',
        description: 'Nome do cliente é obrigatório.',
        variant: 'destructive'
      });
      return;
    }

    if (selectedProposal.items.length === 0) {
      toast({
        title: 'Erro',
        description: 'Adicione pelo menos um item à proposta.',
        variant: 'destructive'
      });
      return;
    }

    if (isCreating) {
      setProposals(prev => [...prev, selectedProposal]);
      toast({
        title: 'Proposta criada',
        description: `Proposta ${selectedProposal.number} criada com sucesso.`,
      });
    } else {
      setProposals(prev => prev.map(p => 
        p.id === selectedProposal.id 
          ? { ...selectedProposal, updatedAt: new Date().toISOString() }
          : p
      ));
      toast({
        title: 'Proposta atualizada',
        description: 'Proposta atualizada com sucesso.',
      });
    }

    setIsEditing(false);
    setIsCreating(false);
  };

  const handleDeleteProposal = (proposalId: string) => {
    setProposals(prev => prev.filter(p => p.id !== proposalId));
    if (selectedProposal?.id === proposalId) {
      setSelectedProposal(null);
    }
    
    toast({
      title: 'Proposta excluída',
      description: 'Proposta excluída com sucesso.',
    });
  };

  const handleAddItem = () => {
    setEditingItem({
      id: Date.now().toString(),
      productId: '',
      productName: '',
      description: '',
      quantity: 1,
      unitPrice: 0,
      total: 0
    });
    setShowItemDialog(true);
  };

  const handleEditItem = (item: ProposalItem) => {
    setEditingItem(item);
    setShowItemDialog(true);
  };

  const handleSaveItem = () => {
    if (!editingItem || !selectedProposal) return;

    if (!editingItem.productName.trim()) {
      toast({
        title: 'Erro',
        description: 'Nome do produto é obrigatório.',
        variant: 'destructive'
      });
      return;
    }

    const updatedItem = {
      ...editingItem,
      total: editingItem.quantity * editingItem.unitPrice
    };

    let updatedItems;
    const existingItemIndex = selectedProposal.items.findIndex(item => item.id === editingItem.id);
    
    if (existingItemIndex >= 0) {
      updatedItems = selectedProposal.items.map(item => 
        item.id === editingItem.id ? updatedItem : item
      );
    } else {
      updatedItems = [...selectedProposal.items, updatedItem];
    }

    const subtotal = updatedItems.reduce((sum, item) => sum + item.total, 0);
    const total = subtotal - selectedProposal.discount;

    setSelectedProposal({
      ...selectedProposal,
      items: updatedItems,
      subtotal,
      total
    });

    setShowItemDialog(false);
    setEditingItem(null);
  };

  const handleRemoveItem = (itemId: string) => {
    if (!selectedProposal) return;

    const updatedItems = selectedProposal.items.filter(item => item.id !== itemId);
    const subtotal = updatedItems.reduce((sum, item) => sum + item.total, 0);
    const total = subtotal - selectedProposal.discount;

    setSelectedProposal({
      ...selectedProposal,
      items: updatedItems,
      subtotal,
      total
    });
  };

  const handleProductSelect = (productId: string) => {
    const product = products.find(p => p.id === productId);
    if (product && editingItem) {
      setEditingItem({
        ...editingItem,
        productId: product.id,
        productName: product.name,
        description: product.description,
        unitPrice: product.basePrice,
        total: editingItem.quantity * product.basePrice
      });
    }
  };

  const handleSendProposal = (proposalId: string) => {
    setProposals(prev => prev.map(p => 
      p.id === proposalId 
        ? { 
            ...p, 
            status: 'sent', 
            sentAt: new Date().toISOString(),
            updatedAt: new Date().toISOString() 
          }
        : p
    ));
    
    toast({
      title: 'Proposta enviada',
      description: 'Proposta enviada por email com sucesso.',
    });
  };

  const handleGeneratePDF = (proposalId: string) => {
    toast({
      title: 'PDF gerado',
      description: 'PDF da proposta gerado com sucesso.',
    });
  };

  const handleDuplicateProposal = (proposal: Proposal) => {
    const duplicatedProposal: Proposal = {
      ...proposal,
      id: Date.now().toString(),
      number: `PROP-${new Date().getFullYear()}-${String(proposals.length + 1).padStart(3, '0')}`,
      status: 'draft',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      sentAt: undefined,
      approvedAt: undefined
    };
    
    setProposals(prev => [...prev, duplicatedProposal]);
    toast({
      title: 'Proposta duplicada',
      description: 'Proposta duplicada com sucesso.',
    });
  };

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      draft: { label: 'Rascunho', variant: 'secondary' as const, color: 'bg-gray-500' },
      sent: { label: 'Enviada', variant: 'default' as const, color: 'bg-blue-500' },
      approved: { label: 'Aprovada', variant: 'default' as const, color: 'bg-green-500' },
      rejected: { label: 'Rejeitada', variant: 'destructive' as const, color: 'bg-red-500' },
      expired: { label: 'Expirada', variant: 'outline' as const, color: 'bg-orange-500' }
    };
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.draft;
    return <Badge variant={config.variant}>{config.label}</Badge>;
  };

  const filteredProposals = proposals.filter(proposal => {
    const matchesSearch = proposal.number.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         proposal.clientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         proposal.clientCompany.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || proposal.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Propostas Comerciais</h2>
          <p className="text-gray-600">
            Gerencie propostas com produtos JT VOX, 0800 Virtual e serviços personalizados
          </p>
        </div>
        <Button onClick={handleCreateProposal} className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />
          Nova Proposta
        </Button>
      </div>

      {/* Filters */}
      <div className="flex gap-4 items-center">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              placeholder="Buscar propostas..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos os status</SelectItem>
            <SelectItem value="draft">Rascunho</SelectItem>
            <SelectItem value="sent">Enviada</SelectItem>
            <SelectItem value="approved">Aprovada</SelectItem>
            <SelectItem value="rejected">Rejeitada</SelectItem>
            <SelectItem value="expired">Expirada</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Proposals List */}
        <div className="lg:col-span-1 space-y-4">
          <h3 className="font-medium">Propostas ({filteredProposals.length})</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {filteredProposals.map((proposal) => (
              <Card 
                key={proposal.id} 
                className={`cursor-pointer transition-all ${
                  selectedProposal?.id === proposal.id ? 'ring-2 ring-blue-500' : ''
                }`}
                onClick={() => setSelectedProposal(proposal)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h5 className="font-medium">{proposal.number}</h5>
                        {getStatusBadge(proposal.status)}
                      </div>
                      <p className="text-sm text-gray-600 mt-1">{proposal.clientName}</p>
                      <p className="text-sm text-gray-500">{proposal.clientCompany}</p>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-sm font-medium text-green-600">
                          R$ {proposal.total.toFixed(2)}
                        </span>
                        <span className="text-xs text-gray-500">
                          {new Date(proposal.createdAt).toLocaleDateString('pt-BR')}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDuplicateProposal(proposal);
                        }}
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedProposal(proposal);
                          setIsEditing(true);
                        }}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteProposal(proposal.id);
                        }}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Proposal Details/Editor */}
        <div className="lg:col-span-2">
          {selectedProposal ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      {selectedProposal.number}
                      {getStatusBadge(selectedProposal.status)}
                    </CardTitle>
                    <CardDescription>
                      {isCreating ? 'Criando nova proposta' : 'Editando proposta existente'}
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    {!isEditing && selectedProposal.status === 'draft' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleSendProposal(selectedProposal.id)}
                      >
                        <Send className="w-4 h-4 mr-2" />
                        Enviar
                      </Button>
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleGeneratePDF(selectedProposal.id)}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      PDF
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setIsEditing(!isEditing)}
                    >
                      {isEditing ? <Eye className="w-4 h-4" /> : <Edit className="w-4 h-4" />}
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {isEditing ? (
                  <div className="space-y-6">
                    {/* Client Information */}
                    <div>
                      <h4 className="font-medium mb-3">Dados do Cliente</h4>
                      <div className="grid gap-4 md:grid-cols-2">
                        <div>
                          <Label htmlFor="client-name">Nome do Cliente *</Label>
                          <Input
                            id="client-name"
                            value={selectedProposal.clientName}
                            onChange={(e) => setSelectedProposal({
                              ...selectedProposal,
                              clientName: e.target.value
                            })}
                            placeholder="Nome completo"
                          />
                        </div>
                        <div>
                          <Label htmlFor="client-email">E-mail</Label>
                          <Input
                            id="client-email"
                            type="email"
                            value={selectedProposal.clientEmail}
                            onChange={(e) => setSelectedProposal({
                              ...selectedProposal,
                              clientEmail: e.target.value
                            })}
                            placeholder="email@empresa.com"
                          />
                        </div>
                        <div>
                          <Label htmlFor="client-phone">Telefone</Label>
                          <Input
                            id="client-phone"
                            value={selectedProposal.clientPhone}
                            onChange={(e) => setSelectedProposal({
                              ...selectedProposal,
                              clientPhone: e.target.value
                            })}
                            placeholder="(11) 99999-9999"
                          />
                        </div>
                        <div>
                          <Label htmlFor="client-company">Empresa</Label>
                          <Input
                            id="client-company"
                            value={selectedProposal.clientCompany}
                            onChange={(e) => setSelectedProposal({
                              ...selectedProposal,
                              clientCompany: e.target.value
                            })}
                            placeholder="Nome da empresa"
                          />
                        </div>
                        <div>
                          <Label htmlFor="client-cnpj">CNPJ</Label>
                          <Input
                            id="client-cnpj"
                            value={selectedProposal.clientCnpj}
                            onChange={(e) => setSelectedProposal({
                              ...selectedProposal,
                              clientCnpj: e.target.value
                            })}
                            placeholder="00.000.000/0000-00"
                          />
                        </div>
                      </div>
                    </div>

                    {/* Items */}
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-medium">Itens da Proposta</h4>
                        <Button onClick={handleAddItem} size="sm">
                          <Plus className="w-4 h-4 mr-2" />
                          Adicionar Item
                        </Button>
                      </div>
                      
                      {selectedProposal.items.length > 0 ? (
                        <Table>
                          <TableHeader>
                            <TableRow>
                              <TableHead>Produto/Serviço</TableHead>
                              <TableHead>Qtd</TableHead>
                              <TableHead>Valor Unit.</TableHead>
                              <TableHead>Total</TableHead>
                              <TableHead>Ações</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {selectedProposal.items.map((item) => (
                              <TableRow key={item.id}>
                                <TableCell>
                                  <div>
                                    <div className="font-medium">{item.productName}</div>
                                    <div className="text-sm text-gray-600">{item.description}</div>
                                  </div>
                                </TableCell>
                                <TableCell>{item.quantity}</TableCell>
                                <TableCell>R$ {item.unitPrice.toFixed(2)}</TableCell>
                                <TableCell>R$ {item.total.toFixed(2)}</TableCell>
                                <TableCell>
                                  <div className="flex items-center gap-1">
                                    <Button
                                      variant="ghost"
                                      size="sm"
                                      onClick={() => handleEditItem(item)}
                                    >
                                      <Edit className="w-4 h-4" />
                                    </Button>
                                    <Button
                                      variant="ghost"
                                      size="sm"
                                      onClick={() => handleRemoveItem(item.id)}
                                      className="text-red-600 hover:text-red-700"
                                    >
                                      <Trash2 className="w-4 h-4" />
                                    </Button>
                                  </div>
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      ) : (
                        <div className="text-center py-8 text-gray-500">
                          Nenhum item adicionado. Clique em "Adicionar Item" para começar.
                        </div>
                      )}
                    </div>

                    {/* Totals */}
                    <div className="border-t pt-4">
                      <div className="flex justify-end">
                        <div className="w-64 space-y-2">
                          <div className="flex justify-between">
                            <span>Subtotal:</span>
                            <span>R$ {selectedProposal.subtotal.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Desconto:</span>
                            <Input
                              type="number"
                              value={selectedProposal.discount}
                              onChange={(e) => {
                                const discount = parseFloat(e.target.value) || 0;
                                setSelectedProposal({
                                  ...selectedProposal,
                                  discount,
                                  total: selectedProposal.subtotal - discount
                                });
                              }}
                              className="w-24 text-right"
                              step="0.01"
                            />
                          </div>
                          <div className="flex justify-between font-bold text-lg border-t pt-2">
                            <span>Total:</span>
                            <span>R$ {selectedProposal.total.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Additional Information */}
                    <div className="grid gap-4 md:grid-cols-2">
                      <div>
                        <Label htmlFor="valid-until">Válida até</Label>
                        <Input
                          id="valid-until"
                          type="date"
                          value={selectedProposal.validUntil}
                          onChange={(e) => setSelectedProposal({
                            ...selectedProposal,
                            validUntil: e.target.value
                          })}
                        />
                      </div>
                      <div>
                        <Label htmlFor="payment-terms">Condições de Pagamento</Label>
                        <Input
                          id="payment-terms"
                          value={selectedProposal.paymentTerms}
                          onChange={(e) => setSelectedProposal({
                            ...selectedProposal,
                            paymentTerms: e.target.value
                          })}
                          placeholder="Ex: Mensal via boleto"
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="observations">Observações</Label>
                      <Textarea
                        id="observations"
                        value={selectedProposal.observations}
                        onChange={(e) => setSelectedProposal({
                          ...selectedProposal,
                          observations: e.target.value
                        })}
                        placeholder="Condições comerciais, prazo de ativação, etc."
                        rows={4}
                      />
                    </div>

                    {/* Actions */}
                    <div className="flex justify-end gap-3 pt-4">
                      <Button
                        variant="outline"
                        onClick={() => {
                          setIsEditing(false);
                          setIsCreating(false);
                          if (isCreating) {
                            setSelectedProposal(null);
                          }
                        }}
                      >
                        Cancelar
                      </Button>
                      <Button onClick={handleSaveProposal} className="bg-blue-600 hover:bg-blue-700">
                        <Save className="w-4 h-4 mr-2" />
                        Salvar Proposta
                      </Button>
                    </div>
                  </div>
                ) : (
                  /* Proposal View */
                  <div className="space-y-6">
                    {/* Client Info */}
                    <div>
                      <h4 className="font-medium mb-3">Dados do Cliente</h4>
                      <div className="grid gap-4 md:grid-cols-2">
                        <div>
                          <span className="font-medium">Nome:</span> {selectedProposal.clientName}
                        </div>
                        <div>
                          <span className="font-medium">E-mail:</span> {selectedProposal.clientEmail}
                        </div>
                        <div>
                          <span className="font-medium">Telefone:</span> {selectedProposal.clientPhone}
                        </div>
                        <div>
                          <span className="font-medium">Empresa:</span> {selectedProposal.clientCompany}
                        </div>
                        <div>
                          <span className="font-medium">CNPJ:</span> {selectedProposal.clientCnpj}
                        </div>
                      </div>
                    </div>

                    {/* Items */}
                    <div>
                      <h4 className="font-medium mb-3">Itens da Proposta</h4>
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Produto/Serviço</TableHead>
                            <TableHead>Qtd</TableHead>
                            <TableHead>Valor Unit.</TableHead>
                            <TableHead>Total</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {selectedProposal.items.map((item) => (
                            <TableRow key={item.id}>
                              <TableCell>
                                <div>
                                  <div className="font-medium">{item.productName}</div>
                                  <div className="text-sm text-gray-600">{item.description}</div>
                                </div>
                              </TableCell>
                              <TableCell>{item.quantity}</TableCell>
                              <TableCell>R$ {item.unitPrice.toFixed(2)}</TableCell>
                              <TableCell>R$ {item.total.toFixed(2)}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>

                    {/* Totals */}
                    <div className="border-t pt-4">
                      <div className="flex justify-end">
                        <div className="w-64 space-y-2">
                          <div className="flex justify-between">
                            <span>Subtotal:</span>
                            <span>R$ {selectedProposal.subtotal.toFixed(2)}</span>
                          </div>
                          {selectedProposal.discount > 0 && (
                            <div className="flex justify-between">
                              <span>Desconto:</span>
                              <span>- R$ {selectedProposal.discount.toFixed(2)}</span>
                            </div>
                          )}
                          <div className="flex justify-between font-bold text-lg border-t pt-2">
                            <span>Total:</span>
                            <span>R$ {selectedProposal.total.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Additional Info */}
                    <div className="grid gap-4 md:grid-cols-2">
                      <div>
                        <span className="font-medium">Válida até:</span> {new Date(selectedProposal.validUntil).toLocaleDateString('pt-BR')}
                      </div>
                      <div>
                        <span className="font-medium">Condições:</span> {selectedProposal.paymentTerms}
                      </div>
                    </div>

                    {selectedProposal.observations && (
                      <div>
                        <h4 className="font-medium mb-2">Observações</h4>
                        <p className="text-gray-700 whitespace-pre-wrap">{selectedProposal.observations}</p>
                      </div>
                    )}

                    <div className="grid gap-4 md:grid-cols-2 text-sm text-gray-600">
                      <div>
                        <span className="font-medium">Responsável:</span> {selectedProposal.responsibleName}
                      </div>
                      <div>
                        <span className="font-medium">Criada em:</span> {new Date(selectedProposal.createdAt).toLocaleDateString('pt-BR')}
                      </div>
                      {selectedProposal.sentAt && (
                        <div>
                          <span className="font-medium">Enviada em:</span> {new Date(selectedProposal.sentAt).toLocaleDateString('pt-BR')}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-8 text-center">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Selecione uma Proposta</h3>
                <p className="text-gray-600 mb-4">
                  Escolha uma proposta da lista para visualizar ou editar seus detalhes.
                </p>
                <Button onClick={handleCreateProposal} className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Criar Nova Proposta
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Item Dialog */}
      <Dialog open={showItemDialog} onOpenChange={setShowItemDialog}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>
              {editingItem?.productId ? 'Editar Item' : 'Adicionar Item'}
            </DialogTitle>
            <DialogDescription>
              Configure os detalhes do produto ou serviço.
            </DialogDescription>
          </DialogHeader>
          
          {editingItem && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="product-select">Produto/Serviço</Label>
                <Select 
                  value={editingItem.productId}
                  onValueChange={handleProductSelect}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um produto" />
                  </SelectTrigger>
                  <SelectContent>
                    {products.filter(p => p.isActive).map((product) => (
                      <SelectItem key={product.id} value={product.id}>
                        {product.name} - R$ {product.basePrice.toFixed(2)}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="product-name">Nome do Produto *</Label>
                <Input
                  id="product-name"
                  value={editingItem.productName}
                  onChange={(e) => setEditingItem({
                    ...editingItem,
                    productName: e.target.value
                  })}
                  placeholder="Nome do produto ou serviço"
                />
              </div>

              <div>
                <Label htmlFor="product-description">Descrição</Label>
                <Textarea
                  id="product-description"
                  value={editingItem.description}
                  onChange={(e) => setEditingItem({
                    ...editingItem,
                    description: e.target.value
                  })}
                  placeholder="Descrição detalhada"
                  rows={3}
                />
              </div>

              <div className="grid gap-4 grid-cols-2">
                <div>
                  <Label htmlFor="quantity">Quantidade</Label>
                  <Input
                    id="quantity"
                    type="number"
                    value={editingItem.quantity}
                    onChange={(e) => {
                      const quantity = parseInt(e.target.value) || 1;
                      setEditingItem({
                        ...editingItem,
                        quantity,
                        total: quantity * editingItem.unitPrice
                      });
                    }}
                    min="1"
                  />
                </div>
                <div>
                  <Label htmlFor="unit-price">Valor Unitário</Label>
                  <Input
                    id="unit-price"
                    type="number"
                    value={editingItem.unitPrice}
                    onChange={(e) => {
                      const unitPrice = parseFloat(e.target.value) || 0;
                      setEditingItem({
                        ...editingItem,
                        unitPrice,
                        total: editingItem.quantity * unitPrice
                      });
                    }}
                    step="0.01"
                  />
                </div>
              </div>

              <div>
                <Label>Total</Label>
                <div className="text-lg font-bold text-green-600">
                  R$ {editingItem.total.toFixed(2)}
                </div>
              </div>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowItemDialog(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSaveItem}>
              Salvar Item
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <FileText className="w-8 h-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold">{proposals.length}</div>
                <div className="text-sm text-gray-600">Total de Propostas</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-8 h-8 text-green-500" />
              <div>
                <div className="text-2xl font-bold">{proposals.filter(p => p.status === 'approved').length}</div>
                <div className="text-sm text-gray-600">Aprovadas</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Clock className="w-8 h-8 text-yellow-500" />
              <div>
                <div className="text-2xl font-bold">{proposals.filter(p => p.status === 'sent').length}</div>
                <div className="text-sm text-gray-600">Aguardando</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <DollarSign className="w-8 h-8 text-green-500" />
              <div>
                <div className="text-2xl font-bold">
                  R$ {proposals.filter(p => p.status === 'approved').reduce((sum, p) => sum + p.total, 0).toFixed(0)}
                </div>
                <div className="text-sm text-gray-600">Valor Aprovado</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Proposals;

