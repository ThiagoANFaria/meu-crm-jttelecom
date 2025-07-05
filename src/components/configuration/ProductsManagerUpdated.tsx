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
  Package,
  Search,
  Filter,
  Save,
  X,
  CheckCircle,
  AlertCircle,
  Star,
  Tag
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';

interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  price: number;
  unit: string;
  isActive: boolean;
  isDefault: boolean;
  tenantId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  tags: string[];
}

const ProductsManager: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [showProductDialog, setShowProductDialog] = useState(false);
  const { toast } = useToast();
  const { currentTenant, tenantProducts, loadTenantData } = useTenant();

  useEffect(() => {
    loadProducts();
  }, [currentTenant, tenantProducts]);

  const loadProducts = () => {
    if (!currentTenant) return;

    // Produtos base da JT (disponíveis para todos os tenants)
    const baseProducts: Product[] = [
      {
        id: `${currentTenant.id}-1`,
        name: 'PABX em Nuvem',
        description: 'Sistema de PABX completo em nuvem com ramais ilimitados',
        category: 'comunicacao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['pabx', 'nuvem', 'comunicacao']
      },
      {
        id: `${currentTenant.id}-2`,
        name: 'URA Reversa',
        description: 'Sistema de URA com tecnologia reversa e reconhecimento de voz',
        category: 'comunicacao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['ura', 'reversa', 'voz']
      },
      {
        id: `${currentTenant.id}-3`,
        name: 'Discador Preditivo',
        description: 'Sistema de discagem preditiva para telemarketing e vendas',
        category: 'vendas',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['discador', 'preditivo', 'telemarketing']
      },
      {
        id: `${currentTenant.id}-4`,
        name: 'Smartbot (Chatbot)',
        description: 'Chatbot inteligente para atendimento automatizado',
        category: 'automacao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['chatbot', 'smartbot', 'ia']
      },
      {
        id: `${currentTenant.id}-5`,
        name: '0800 Virtual',
        description: 'Número 0800 virtual para atendimento nacional gratuito',
        category: 'telefonia',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['0800', 'virtual', 'atendimento']
      },
      {
        id: `${currentTenant.id}-6`,
        name: 'CRM',
        description: 'Sistema de gestão de relacionamento com clientes',
        category: 'gestao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['crm', 'gestao', 'clientes']
      },
      {
        id: `${currentTenant.id}-7`,
        name: 'JT VOX',
        description: 'Solução completa de comunicação empresarial',
        category: 'comunicacao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['jt-vox', 'comunicacao', 'empresarial']
      },
      {
        id: `${currentTenant.id}-8`,
        name: 'JT Mobi',
        description: 'Telefonia móvel empresarial com gestão centralizada',
        category: 'telefonia',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['jt-mobi', 'movel', 'telefonia']
      }
    ];

    // Combinar produtos base com produtos personalizados do tenant
    const customProducts = tenantProducts.filter(p => !p.isDefault).map(p => ({
      ...p,
      tenantId: currentTenant.id
    }));

    setProducts([...baseProducts, ...customProducts]);
  };

  const handleCreateProduct = () => {
    if (!currentTenant) return;

    const newProduct: Product = {
      id: `${currentTenant.id}-${Date.now()}`,
      name: '',
      description: '',
      category: 'comunicacao',
      price: 0,
      unit: 'mensal',
      isActive: true,
      isDefault: false,
      tenantId: currentTenant.id,
      createdBy: 'admin',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: []
    };
    
    setSelectedProduct(newProduct);
    setIsCreating(true);
    setIsEditing(true);
    setShowProductDialog(true);
  };

  const handleEditProduct = (product: Product) => {
    setSelectedProduct(product);
    setIsCreating(false);
    setIsEditing(true);
    setShowProductDialog(true);
  };

  const handleSaveProduct = () => {
    if (!selectedProduct) return;

    if (!selectedProduct.name.trim()) {
      toast({
        title: 'Erro',
        description: 'Nome do produto é obrigatório.',
        variant: 'destructive'
      });
      return;
    }

    if (isCreating) {
      setProducts(prev => [...prev, selectedProduct]);
      toast({
        title: 'Produto criado',
        description: `Produto "${selectedProduct.name}" criado com sucesso.`,
      });
    } else {
      setProducts(prev => prev.map(p => 
        p.id === selectedProduct.id 
          ? { ...selectedProduct, updatedAt: new Date().toISOString() }
          : p
      ));
      toast({
        title: 'Produto atualizado',
        description: 'Produto atualizado com sucesso.',
      });
    }

    setShowProductDialog(false);
    setIsEditing(false);
    setIsCreating(false);
    setSelectedProduct(null);
  };

  const handleDeleteProduct = (productId: string) => {
    const product = products.find(p => p.id === productId);
    if (product?.createdBy === 'system') {
      toast({
        title: 'Erro',
        description: 'Produtos do sistema não podem ser excluídos.',
        variant: 'destructive'
      });
      return;
    }

    setProducts(prev => prev.filter(p => p.id !== productId));
    toast({
      title: 'Produto excluído',
      description: 'Produto excluído com sucesso.',
    });
  };

  const handleToggleActive = (productId: string) => {
    setProducts(prev => prev.map(p => 
      p.id === productId 
        ? { ...p, isActive: !p.isActive, updatedAt: new Date().toISOString() }
        : p
    ));
  };

  const getCategoryBadge = (category: string) => {
    const categoryConfig = {
      comunicacao: { label: 'Comunicação', color: 'bg-blue-500' },
      telefonia: { label: 'Telefonia', color: 'bg-green-500' },
      automacao: { label: 'Automação', color: 'bg-purple-500' },
      vendas: { label: 'Vendas', color: 'bg-orange-500' },
      gestao: { label: 'Gestão', color: 'bg-indigo-500' },
      servicos: { label: 'Serviços', color: 'bg-gray-500' }
    };
    
    const config = categoryConfig[category as keyof typeof categoryConfig] || categoryConfig.servicos;
    return (
      <Badge variant="secondary" className={`${config.color} text-white`}>
        {config.label}
      </Badge>
    );
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = categoryFilter === 'all' || product.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-xl font-semibold">Produtos e Serviços</h3>
          <p className="text-gray-600">
            Gerencie produtos da JT e crie novos produtos personalizados
          </p>
        </div>
        <Button onClick={handleCreateProduct} className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />
          Novo Produto
        </Button>
      </div>

      {/* Filters */}
      <div className="flex gap-4 items-center">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <Input
              placeholder="Buscar produtos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>
        <Select value={categoryFilter} onValueChange={setCategoryFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Categoria" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todas as categorias</SelectItem>
            <SelectItem value="comunicacao">Comunicação</SelectItem>
            <SelectItem value="telefonia">Telefonia</SelectItem>
            <SelectItem value="automacao">Automação</SelectItem>
            <SelectItem value="vendas">Vendas</SelectItem>
            <SelectItem value="gestao">Gestão</SelectItem>
            <SelectItem value="servicos">Serviços</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Products Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Package className="w-5 h-5" />
            Produtos ({filteredProducts.length})
          </CardTitle>
          <CardDescription>
            Lista de todos os produtos e serviços disponíveis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Produto</TableHead>
                <TableHead>Categoria</TableHead>
                <TableHead>Preço</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Origem</TableHead>
                <TableHead>Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredProducts.map((product) => (
                <TableRow key={product.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium flex items-center gap-2">
                        {product.name}
                        {product.isDefault && <Star className="w-4 h-4 text-yellow-500" />}
                      </div>
                      <div className="text-sm text-gray-600">{product.description}</div>
                      {product.tags.length > 0 && (
                        <div className="flex gap-1 mt-1">
                          {product.tags.slice(0, 3).map((tag, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {tag}
                            </Badge>
                          ))}
                          {product.tags.length > 3 && (
                            <Badge variant="outline" className="text-xs">
                              +{product.tags.length - 3}
                            </Badge>
                          )}
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    {getCategoryBadge(product.category)}
                  </TableCell>
                  <TableCell>
                    {product.price > 0 ? (
                      <span className="font-medium">
                        R$ {product.price.toFixed(2)}/{product.unit}
                      </span>
                    ) : (
                      <span className="text-gray-500 italic">A definir</span>
                    )}
                  </TableCell>
                  <TableCell>
                    <Badge 
                      variant={product.isActive ? "default" : "secondary"}
                      className={product.isActive ? "bg-green-500" : "bg-gray-500"}
                    >
                      {product.isActive ? 'Ativo' : 'Inativo'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">
                      {product.createdBy === 'system' ? 'JT' : 'Personalizado'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleToggleActive(product.id)}
                      >
                        {product.isActive ? (
                          <AlertCircle className="w-4 h-4 text-orange-600" />
                        ) : (
                          <CheckCircle className="w-4 h-4 text-green-600" />
                        )}
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleEditProduct(product)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      {product.createdBy !== 'system' && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeleteProduct(product.id)}
                          className="text-red-600 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Product Dialog */}
      <Dialog open={showProductDialog} onOpenChange={setShowProductDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {isCreating ? 'Criar Novo Produto' : 'Editar Produto'}
            </DialogTitle>
            <DialogDescription>
              Configure os detalhes do produto ou serviço.
            </DialogDescription>
          </DialogHeader>
          
          {selectedProduct && (
            <div className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <Label htmlFor="product-name">Nome do Produto *</Label>
                  <Input
                    id="product-name"
                    value={selectedProduct.name}
                    onChange={(e) => setSelectedProduct({
                      ...selectedProduct,
                      name: e.target.value
                    })}
                    placeholder="Nome do produto"
                  />
                </div>
                <div>
                  <Label htmlFor="product-category">Categoria</Label>
                  <Select 
                    value={selectedProduct.category}
                    onValueChange={(value) => setSelectedProduct({
                      ...selectedProduct,
                      category: value
                    })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione uma categoria" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="comunicacao">Comunicação</SelectItem>
                      <SelectItem value="telefonia">Telefonia</SelectItem>
                      <SelectItem value="automacao">Automação</SelectItem>
                      <SelectItem value="vendas">Vendas</SelectItem>
                      <SelectItem value="gestao">Gestão</SelectItem>
                      <SelectItem value="servicos">Serviços</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="product-description">Descrição</Label>
                <Textarea
                  id="product-description"
                  value={selectedProduct.description}
                  onChange={(e) => setSelectedProduct({
                    ...selectedProduct,
                    description: e.target.value
                  })}
                  placeholder="Descrição detalhada do produto"
                  rows={3}
                />
              </div>

              <div className="grid gap-4 md:grid-cols-3">
                <div>
                  <Label htmlFor="product-price">Preço Base</Label>
                  <Input
                    id="product-price"
                    type="number"
                    value={selectedProduct.price}
                    onChange={(e) => setSelectedProduct({
                      ...selectedProduct,
                      price: parseFloat(e.target.value) || 0
                    })}
                    step="0.01"
                    placeholder="0.00"
                  />
                </div>
                <div>
                  <Label htmlFor="product-unit">Unidade</Label>
                  <Select 
                    value={selectedProduct.unit}
                    onValueChange={(value) => setSelectedProduct({
                      ...selectedProduct,
                      unit: value
                    })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="mensal">Mensal</SelectItem>
                      <SelectItem value="anual">Anual</SelectItem>
                      <SelectItem value="unico">Único</SelectItem>
                      <SelectItem value="por-uso">Por uso</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex items-center space-x-2 pt-6">
                  <input
                    type="checkbox"
                    id="product-active"
                    checked={selectedProduct.isActive}
                    onChange={(e) => setSelectedProduct({
                      ...selectedProduct,
                      isActive: e.target.checked
                    })}
                    className="rounded"
                  />
                  <Label htmlFor="product-active">Produto ativo</Label>
                </div>
              </div>

              <div>
                <Label htmlFor="product-tags">Tags (separadas por vírgula)</Label>
                <Input
                  id="product-tags"
                  value={selectedProduct.tags.join(', ')}
                  onChange={(e) => setSelectedProduct({
                    ...selectedProduct,
                    tags: e.target.value.split(',').map(tag => tag.trim()).filter(tag => tag)
                  })}
                  placeholder="tag1, tag2, tag3"
                />
              </div>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowProductDialog(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSaveProduct}>
              <Save className="w-4 h-4 mr-2" />
              Salvar Produto
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Package className="w-8 h-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold">{products.length}</div>
                <div className="text-sm text-gray-600">Total de Produtos</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-8 h-8 text-green-500" />
              <div>
                <div className="text-2xl font-bold">{products.filter(p => p.isActive).length}</div>
                <div className="text-sm text-gray-600">Produtos Ativos</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Star className="w-8 h-8 text-yellow-500" />
              <div>
                <div className="text-2xl font-bold">{products.filter(p => p.createdBy === 'system').length}</div>
                <div className="text-sm text-gray-600">Produtos JT</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Tag className="w-8 h-8 text-purple-500" />
              <div>
                <div className="text-2xl font-bold">{products.filter(p => p.createdBy !== 'system').length}</div>
                <div className="text-sm text-gray-600">Personalizados</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProductsManager;

