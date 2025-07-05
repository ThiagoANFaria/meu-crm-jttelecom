import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
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
  Save, 
  Plus,
  Edit,
  Trash2,
  Package,
  DollarSign,
  Search,
  Filter,
  Star,
  StarOff,
  CheckCircle,
  AlertCircle,
  Eye,
  EyeOff
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/AuthContext';

interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  price: number;
  unit: string;
  isActive: boolean;
  isDefault: boolean;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  tags: string[];
}

interface ProductCategory {
  id: string;
  name: string;
  description: string;
  color: string;
}

const ProductsManager: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<ProductCategory[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showInactive, setShowInactive] = useState(false);
  const { toast } = useToast();
  const { user } = useAuth();

  useEffect(() => {
    loadProducts();
    loadCategories();
  }, []);

  const loadProducts = () => {
    const defaultProducts: Product[] = [
      {
        id: '1',
        name: 'JT VOX',
        description: 'Sistema completo de comunicação empresarial com PABX em nuvem, URA inteligente e integração total',
        category: 'comunicacao',
        price: 0, // Valor em aberto para configuração
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['pabx', 'nuvem', 'ura', 'comunicacao']
      },
      {
        id: '2',
        name: '0800 Virtual',
        description: 'Número 0800 virtual para atendimento gratuito aos clientes com roteamento inteligente',
        category: 'telefonia',
        price: 0, // Valor em aberto para configuração
        unit: 'mensal',
        isActive: true,
        isDefault: true,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['0800', 'virtual', 'atendimento']
      },
      {
        id: '3',
        name: 'PABX em Nuvem',
        description: 'Central telefônica 100% em nuvem com ramais ilimitados e gravação de chamadas',
        category: 'comunicacao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: false,
        createdBy: 'admin',
        createdAt: '2025-02-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['pabx', 'nuvem', 'ramais']
      },
      {
        id: '4',
        name: 'URA Reversa',
        description: 'Sistema de URA inteligente com reconhecimento de voz e roteamento automático',
        category: 'automacao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: false,
        createdBy: 'admin',
        createdAt: '2025-02-15T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['ura', 'automacao', 'voz']
      },
      {
        id: '5',
        name: 'Discador Preditivo',
        description: 'Sistema de discagem automática para campanhas de telemarketing e vendas',
        category: 'vendas',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: false,
        createdBy: 'admin',
        createdAt: '2025-03-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['discador', 'telemarketing', 'vendas']
      },
      {
        id: '6',
        name: 'Chatbot',
        description: 'Chatbot inteligente para WhatsApp, Instagram e Site com IA integrada',
        category: 'automacao',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: false,
        createdBy: 'admin',
        createdAt: '2025-03-15T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['chatbot', 'whatsapp', 'ia']
      },
      {
        id: '7',
        name: 'Tronco SIP',
        description: 'Conexão SIP para integração com sistemas telefônicos existentes',
        category: 'telefonia',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: false,
        createdBy: 'admin',
        createdAt: '2025-04-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['sip', 'tronco', 'integracao']
      },
      {
        id: '8',
        name: 'Telefonia Móvel',
        description: 'Planos de telefonia móvel corporativa com gestão centralizada',
        category: 'telefonia',
        price: 0,
        unit: 'mensal',
        isActive: true,
        isDefault: false,
        createdBy: 'admin',
        createdAt: '2025-04-15T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        tags: ['movel', 'corporativo', 'planos']
      }
    ];
    setProducts(defaultProducts);
  };

  const loadCategories = () => {
    const defaultCategories: ProductCategory[] = [
      { id: 'comunicacao', name: 'Comunicação', description: 'Soluções de comunicação empresarial', color: '#4169E1' },
      { id: 'telefonia', name: 'Telefonia', description: 'Serviços de telefonia', color: '#10B981' },
      { id: 'automacao', name: 'Automação', description: 'Soluções de automação', color: '#F59E0B' },
      { id: 'vendas', name: 'Vendas', description: 'Ferramentas de vendas', color: '#EF4444' },
      { id: 'servicos', name: 'Serviços', description: 'Serviços avulsos', color: '#8B5CF6' },
      { id: 'consultoria', name: 'Consultoria', description: 'Serviços de consultoria', color: '#6B7280' }
    ];
    setCategories(defaultCategories);
  };

  const handleCreateProduct = () => {
    const newProduct: Product = {
      id: Date.now().toString(),
      name: '',
      description: '',
      category: 'servicos',
      price: 0,
      unit: 'mensal',
      isActive: true,
      isDefault: false,
      createdBy: user?.name || 'admin',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: []
    };
    
    setSelectedProduct(newProduct);
    setIsCreating(true);
    setIsEditing(true);
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
        description: 'Produto criado com sucesso.',
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

    setIsEditing(false);
    setIsCreating(false);
  };

  const handleDeleteProduct = (productId: string) => {
    const product = products.find(p => p.id === productId);
    if (product?.isDefault) {
      toast({
        title: 'Erro',
        description: 'Não é possível excluir produtos padrão do sistema.',
        variant: 'destructive'
      });
      return;
    }

    setProducts(prev => prev.filter(p => p.id !== productId));
    if (selectedProduct?.id === productId) {
      setSelectedProduct(null);
    }
    
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

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    const matchesActive = showInactive || product.isActive;
    return matchesSearch && matchesCategory && matchesActive;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Gestão de Produtos e Serviços</h3>
          <p className="text-sm text-gray-600">
            Gerencie produtos padrão (JT VOX, 0800 Virtual) e adicione novos produtos dinamicamente
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
        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Categoria" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todas as categorias</SelectItem>
            {categories.map((category) => (
              <SelectItem key={category.id} value={category.id}>
                {category.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <div className="flex items-center space-x-2">
          <Switch
            id="show-inactive"
            checked={showInactive}
            onCheckedChange={setShowInactive}
          />
          <Label htmlFor="show-inactive">Mostrar inativos</Label>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Products List */}
        <div className="lg:col-span-1 space-y-4">
          <h4 className="font-medium">Produtos ({filteredProducts.length})</h4>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {filteredProducts.map((product) => (
              <Card 
                key={product.id} 
                className={`cursor-pointer transition-all ${
                  selectedProduct?.id === product.id ? 'ring-2 ring-blue-500' : ''
                } ${!product.isActive ? 'opacity-60' : ''}`}
                onClick={() => setSelectedProduct(product)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h5 className="font-medium">{product.name}</h5>
                        {product.isDefault && (
                          <Star className="w-4 h-4 text-yellow-500 fill-current" />
                        )}
                        {!product.isActive && (
                          <EyeOff className="w-4 h-4 text-gray-400" />
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">{product.description}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant="outline" style={{ 
                          borderColor: categories.find(c => c.id === product.category)?.color,
                          color: categories.find(c => c.id === product.category)?.color
                        }}>
                          {categories.find(c => c.id === product.category)?.name}
                        </Badge>
                        {product.price > 0 && (
                          <Badge variant="secondary">
                            R$ {product.price.toFixed(2)}/{product.unit}
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleToggleActive(product.id);
                        }}
                      >
                        {product.isActive ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedProduct(product);
                          setIsEditing(true);
                        }}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      {!product.isDefault && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteProduct(product.id);
                          }}
                          className="text-red-600 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Product Editor/Details */}
        <div className="lg:col-span-2">
          {selectedProduct ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      {selectedProduct.name || 'Novo Produto'}
                      {selectedProduct.isDefault && (
                        <Star className="w-5 h-5 text-yellow-500 fill-current" />
                      )}
                    </CardTitle>
                    <CardDescription>
                      {isCreating ? 'Criando novo produto' : 'Editando produto existente'}
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
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
                  <div className="space-y-4">
                    {/* Product Info */}
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
                          placeholder="Ex: JT VOX, 0800 Virtual"
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
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            {categories.map((category) => (
                              <SelectItem key={category.id} value={category.id}>
                                {category.name}
                              </SelectItem>
                            ))}
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
                        placeholder="Descrição detalhada do produto ou serviço"
                        rows={3}
                      />
                    </div>

                    <div className="grid gap-4 md:grid-cols-3">
                      <div>
                        <Label htmlFor="product-price">Preço (R$)</Label>
                        <Input
                          id="product-price"
                          type="number"
                          step="0.01"
                          min="0"
                          value={selectedProduct.price}
                          onChange={(e) => setSelectedProduct({
                            ...selectedProduct,
                            price: parseFloat(e.target.value) || 0
                          })}
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
                            <SelectItem value="por_usuario">Por usuário</SelectItem>
                            <SelectItem value="por_ramal">Por ramal</SelectItem>
                            <SelectItem value="por_linha">Por linha</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="flex items-center space-x-2 pt-6">
                        <Switch
                          id="product-active"
                          checked={selectedProduct.isActive}
                          onCheckedChange={(checked) => setSelectedProduct({
                            ...selectedProduct,
                            isActive: checked
                          })}
                        />
                        <Label htmlFor="product-active">Produto ativo</Label>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex justify-end gap-3 pt-4">
                      <Button
                        variant="outline"
                        onClick={() => {
                          setIsEditing(false);
                          setIsCreating(false);
                          if (isCreating) {
                            setSelectedProduct(null);
                          }
                        }}
                      >
                        Cancelar
                      </Button>
                      <Button onClick={handleSaveProduct} className="bg-blue-600 hover:bg-blue-700">
                        <Save className="w-4 h-4 mr-2" />
                        Salvar Produto
                      </Button>
                    </div>
                  </div>
                ) : (
                  /* Product Details */
                  <div className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2">
                      <div>
                        <span className="font-medium">Categoria:</span> {categories.find(c => c.id === selectedProduct.category)?.name}
                      </div>
                      <div>
                        <span className="font-medium">Status:</span> 
                        <Badge variant={selectedProduct.isActive ? "default" : "secondary"} className="ml-2">
                          {selectedProduct.isActive ? "Ativo" : "Inativo"}
                        </Badge>
                      </div>
                      <div>
                        <span className="font-medium">Preço:</span> 
                        {selectedProduct.price > 0 ? (
                          <span className="ml-2">R$ {selectedProduct.price.toFixed(2)}/{selectedProduct.unit}</span>
                        ) : (
                          <span className="ml-2 text-gray-500">Valor em aberto</span>
                        )}
                      </div>
                      <div>
                        <span className="font-medium">Tipo:</span> 
                        <Badge variant={selectedProduct.isDefault ? "default" : "outline"} className="ml-2">
                          {selectedProduct.isDefault ? "Produto Padrão" : "Produto Personalizado"}
                        </Badge>
                      </div>
                    </div>

                    <div>
                      <span className="font-medium">Descrição:</span>
                      <p className="mt-1 text-gray-700">{selectedProduct.description}</p>
                    </div>

                    <div className="grid gap-4 md:grid-cols-2 text-sm text-gray-600">
                      <div>
                        <span className="font-medium">Criado por:</span> {selectedProduct.createdBy}
                      </div>
                      <div>
                        <span className="font-medium">Criado em:</span> {new Date(selectedProduct.createdAt).toLocaleDateString('pt-BR')}
                      </div>
                      <div>
                        <span className="font-medium">Atualizado em:</span> {new Date(selectedProduct.updatedAt).toLocaleDateString('pt-BR')}
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-8 text-center">
                <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Selecione um Produto</h3>
                <p className="text-gray-600 mb-4">
                  Escolha um produto da lista para visualizar ou editar suas informações.
                </p>
                <Button onClick={handleCreateProduct} className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Criar Novo Produto
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

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
                <div className="text-2xl font-bold">{products.filter(p => p.isDefault).length}</div>
                <div className="text-sm text-gray-600">Produtos Padrão</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <DollarSign className="w-8 h-8 text-green-600" />
              <div>
                <div className="text-2xl font-bold">{products.filter(p => p.price > 0).length}</div>
                <div className="text-sm text-gray-600">Com Preço Definido</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProductsManager;

