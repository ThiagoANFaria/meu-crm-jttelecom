import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
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
  Copy,
  Eye,
  FileText,
  Star,
  StarOff,
  Tag,
  Code,
  Type,
  Bold,
  Italic,
  Underline,
  AlignLeft,
  AlignCenter,
  AlignRight,
  List,
  ListOrdered,
  Image,
  Link,
  Palette,
  Download,
  Upload,
  Search,
  Filter,
  MoreVertical,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/AuthContext';
import { useTenant } from '@/contexts/TenantContext';

interface ProposalTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  content: string;
  isDefault: boolean;
  isActive: boolean;
  tenantId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  variables: string[];
  tags: string[];
}

interface TemplateCategory {
  id: string;
  name: string;
  description: string;
  color: string;
}

const ProposalTemplatesManager: React.FC = () => {
  const [templates, setTemplates] = useState<ProposalTemplate[]>([]);
  const [categories, setCategories] = useState<TemplateCategory[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<ProposalTemplate | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showVariables, setShowVariables] = useState(false);
  const editorRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();
  const { user } = useAuth();
  const { currentTenant, tenantTemplates, loadTenantData } = useTenant();

  // Variáveis dinâmicas disponíveis
  const availableVariables = [
    { key: '{username}', description: 'Nome do usuário/cliente' },
    { key: '{email}', description: 'E-mail do cliente' },
    { key: '{telefone}', description: 'Telefone do cliente' },
    { key: '{whatsapp}', description: 'WhatsApp do cliente' },
    { key: '{razaosocial}', description: 'Razão social da empresa' },
    { key: '{cnpj}', description: 'CNPJ da empresa' },
    { key: '{cpf}', description: 'CPF do cliente' },
    { key: '{ie}', description: 'Inscrição Estadual' },
    { key: '{rg}', description: 'RG do cliente' },
    { key: '{enderecocompleto}', description: 'Endereço completo' },
    { key: '{endereco}', description: 'Endereço (rua)' },
    { key: '{numero}', description: 'Número do endereço' },
    { key: '{complemento}', description: 'Complemento do endereço' },
    { key: '{bairro}', description: 'Bairro' },
    { key: '{cidade}', description: 'Cidade' },
    { key: '{estado}', description: 'Estado' },
    { key: '{cep}', description: 'CEP' },
    { key: '{produto}', description: 'Nome do produto/serviço' },
    { key: '{valortotal}', description: 'Valor total da proposta' },
    { key: '{valorunitario}', description: 'Valor unitário do item' },
    { key: '{quantidade}', description: 'Quantidade do item' },
    { key: '{subtotal}', description: 'Subtotal do item' },
    { key: '{nomevendedor}', description: 'Nome do vendedor responsável' },
    { key: '{emailvendedor}', description: 'E-mail do vendedor' },
    { key: '{telefonevendedor}', description: 'Telefone do vendedor' },
    { key: '{data}', description: 'Data atual' },
    { key: '{dataenvio}', description: 'Data de envio da proposta' },
    { key: '{datavencimento}', description: 'Data de vencimento da proposta' },
    { key: '{numeroproposta}', description: 'Número da proposta' },
    { key: '{empresa}', description: 'Nome da empresa' },
    { key: '{logoempresa}', description: 'Logo da empresa' },
    { key: '{site}', description: 'Site da empresa' },
    { key: '{emailempresa}', description: 'E-mail da empresa' },
    { key: '{telefoneempresa}', description: 'Telefone da empresa' }
  ];

  useEffect(() => {
    loadTemplates();
    loadCategories();
  }, [currentTenant, tenantTemplates]);

  const loadTemplates = () => {
    if (!currentTenant) return;

    // Template base em branco para múltiplos segmentos
    const baseTemplates: ProposalTemplate[] = [
      {
        id: `${currentTenant.id}-template-base`,
        name: 'Template Padrão',
        description: 'Template base personalizável para propostas comerciais',
        category: 'geral',
        content: `<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
          <div style="text-align: center; margin-bottom: 30px;">
            <img src="{logoempresa}" alt="Logo da Empresa" style="max-width: 200px; margin-bottom: 20px;">
            <h1 style="color: #4169E1; margin: 0;">PROPOSTA COMERCIAL</h1>
            <p style="color: #666; margin: 5px 0;">Número: {numeroproposta}</p>
            <p style="color: #666; margin: 5px 0;">Data: {data}</p>
          </div>
          
          <div style="margin-bottom: 30px;">
            <h2 style="color: #333; border-bottom: 2px solid #4169E1; padding-bottom: 10px;">Dados do Cliente</h2>
            <p><strong>Cliente:</strong> {username}</p>
            <p><strong>Empresa:</strong> {razaosocial}</p>
            <p><strong>E-mail:</strong> {email}</p>
            <p><strong>Telefone:</strong> {telefone}</p>
            <p><strong>Endereço:</strong> {enderecocompleto}</p>
          </div>
          
          <div style="margin-bottom: 30px;">
            <h2 style="color: #333; border-bottom: 2px solid #4169E1; padding-bottom: 10px;">Produtos/Serviços</h2>
            <p><strong>Produto:</strong> {produto}</p>
            <p><strong>Valor Total:</strong> {valortotal}</p>
          </div>
          
          <div style="margin-bottom: 30px;">
            <h2 style="color: #333; border-bottom: 2px solid #4169E1; padding-bottom: 10px;">Observações</h2>
            <p>Insira aqui as condições comerciais, prazo de ativação e outras informações relevantes.</p>
          </div>
          
          <div style="text-align: center; margin-top: 40px;">
            <p style="color: #666;">Atenciosamente,</p>
            <p><strong>{nomevendedor}</strong></p>
            <p>{emailvendedor} | {telefonevendedor}</p>
          </div>
        </div>`,
        isDefault: true,
        isActive: true,
        tenantId: currentTenant.id,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        variables: ['{username}', '{razaosocial}', '{email}', '{telefone}', '{enderecocompleto}', '{produto}', '{valortotal}', '{nomevendedor}', '{emailvendedor}', '{telefonevendedor}', '{logoempresa}', '{numeroproposta}', '{data}'],
        tags: ['padrão', 'geral', 'comercial']
      }
    ];

    // Combinar templates base com templates personalizados do tenant
    const customTemplates = tenantTemplates.filter(t => !t.isDefault).map(t => ({
      ...t,
      tenantId: currentTenant.id
    }));

    setTemplates([...baseTemplates, ...customTemplates]);
  };

  const loadCategories = () => {
    const categories: TemplateCategory[] = [
      { id: 'geral', name: 'Geral', description: 'Templates gerais personalizáveis', color: '#6B7280' },
      { id: 'comunicacao', name: 'Comunicação', description: 'Templates para soluções de comunicação', color: '#4169E1' },
      { id: 'telefonia', name: 'Telefonia', description: 'Templates para telefonia', color: '#10B981' },
      { id: 'automacao', name: 'Automação', description: 'Templates para automação', color: '#F59E0B' },
      { id: 'vendas', name: 'Vendas', description: 'Templates para vendas', color: '#8B5CF6' },
      { id: 'gestao', name: 'Gestão', description: 'Templates para gestão', color: '#EF4444' }
    ];
    setCategories(categories);
  };

  const handleCreateTemplate = () => {
    if (!currentTenant) return;

    const newTemplate: ProposalTemplate = {
      id: `${currentTenant.id}-template-${Date.now()}`,
      name: '',
      description: '',
      category: 'geral',
      content: '',
      isDefault: false,
      isActive: true,
      tenantId: currentTenant.id,
      createdBy: user?.name || 'admin',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      variables: [],
      tags: []
    };
    
    setSelectedTemplate(newTemplate);
    setIsCreating(true);
    setIsEditing(true);
  };

  const handleEditTemplate = (template: ProposalTemplate) => {
    // Verificar se o usuário pode editar (apenas ADM ou criador)
    if (user?.role !== 'admin' && template.createdBy !== user?.name) {
      toast({
        title: 'Acesso Negado',
        description: 'Apenas administradores podem editar templates.',
        variant: 'destructive'
      });
      return;
    }

    setSelectedTemplate(template);
    setIsCreating(false);
    setIsEditing(true);
  };

  const handleSaveTemplate = () => {
    if (!selectedTemplate || !currentTenant) return;

    if (!selectedTemplate.name.trim()) {
      toast({
        title: 'Erro',
        description: 'Nome do template é obrigatório.',
        variant: 'destructive'
      });
      return;
    }

    if (!selectedTemplate.content.trim()) {
      toast({
        title: 'Erro',
        description: 'Conteúdo do template é obrigatório.',
        variant: 'destructive'
      });
      return;
    }

    const updatedTemplate = {
      ...selectedTemplate,
      updatedAt: new Date().toISOString(),
      tenantId: currentTenant.id
    };

    if (isCreating) {
      setTemplates(prev => [...prev, updatedTemplate]);
      toast({
        title: 'Sucesso',
        description: 'Template criado com sucesso!',
        variant: 'default'
      });
    } else {
      setTemplates(prev => prev.map(t => t.id === updatedTemplate.id ? updatedTemplate : t));
      toast({
        title: 'Sucesso',
        description: 'Template atualizado com sucesso!',
        variant: 'default'
      });
    }

    setSelectedTemplate(null);
    setIsEditing(false);
    setIsCreating(false);
  };

  const handleDeleteTemplate = (template: ProposalTemplate) => {
    // Verificar se o usuário pode excluir (apenas ADM)
    if (user?.role !== 'admin') {
      toast({
        title: 'Acesso Negado',
        description: 'Apenas administradores podem excluir templates.',
        variant: 'destructive'
      });
      return;
    }

    // Não permitir excluir templates padrão
    if (template.isDefault) {
      toast({
        title: 'Erro',
        description: 'Templates padrão não podem ser excluídos.',
        variant: 'destructive'
      });
      return;
    }

    setTemplates(prev => prev.filter(t => t.id !== template.id));
    toast({
      title: 'Sucesso',
      description: 'Template excluído com sucesso!',
      variant: 'default'
    });
  };

  const handleSetDefault = (template: ProposalTemplate) => {
    if (user?.role !== 'admin') {
      toast({
        title: 'Acesso Negado',
        description: 'Apenas administradores podem definir template padrão.',
        variant: 'destructive'
      });
      return;
    }

    setTemplates(prev => prev.map(t => ({
      ...t,
      isDefault: t.id === template.id
    })));

    toast({
      title: 'Sucesso',
      description: 'Template padrão definido com sucesso!',
      variant: 'default'
    });
  };

  const insertVariable = (variable: string) => {
    if (editorRef.current) {
      const selection = window.getSelection();
      if (selection && selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        range.deleteContents();
        range.insertNode(document.createTextNode(variable));
      }
    }
  };

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    const matchesTenant = template.tenantId === currentTenant?.id;
    
    return matchesSearch && matchesCategory && matchesTenant;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Templates de Propostas</h2>
          <p className="text-gray-600">Gerencie templates personalizáveis para propostas comerciais</p>
        </div>
        {user?.role === 'admin' && (
          <Button onClick={handleCreateTemplate} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Novo Template
          </Button>
        )}
      </div>

      {/* Filtros */}
      <div className="flex gap-4 items-center">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Buscar templates..."
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
            {categories.map(category => (
              <SelectItem key={category.id} value={category.id}>
                {category.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Lista de Templates */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTemplates.map(template => (
          <Card key={template.id} className="relative">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="flex items-center gap-2">
                    {template.name}
                    {template.isDefault && (
                      <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    )}
                  </CardTitle>
                  <CardDescription>{template.description}</CardDescription>
                </div>
                <div className="flex items-center gap-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleEditTemplate(template)}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  {user?.role === 'admin' && !template.isDefault && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteTemplate(template)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Badge 
                    variant="secondary"
                    style={{ 
                      backgroundColor: categories.find(c => c.id === template.category)?.color + '20',
                      color: categories.find(c => c.id === template.category)?.color 
                    }}
                  >
                    {categories.find(c => c.id === template.category)?.name || template.category}
                  </Badge>
                  <Badge variant={template.isActive ? 'default' : 'secondary'}>
                    {template.isActive ? 'Ativo' : 'Inativo'}
                  </Badge>
                </div>
                
                <div className="flex flex-wrap gap-1">
                  {template.tags.slice(0, 3).map(tag => (
                    <Badge key={tag} variant="outline" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                  {template.tags.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{template.tags.length - 3}
                    </Badge>
                  )}
                </div>

                <div className="text-sm text-gray-500">
                  <p>Criado por: {template.createdBy}</p>
                  <p>Atualizado: {new Date(template.updatedAt).toLocaleDateString('pt-BR')}</p>
                </div>

                {user?.role === 'admin' && !template.isDefault && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleSetDefault(template)}
                    className="w-full"
                  >
                    <Star className="h-4 w-4 mr-2" />
                    Definir como Padrão
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Dialog de Edição */}
      <Dialog open={isEditing} onOpenChange={setIsEditing}>
        <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {isCreating ? 'Criar Novo Template' : 'Editar Template'}
            </DialogTitle>
            <DialogDescription>
              Configure o template de proposta com variáveis dinâmicas
            </DialogDescription>
          </DialogHeader>

          {selectedTemplate && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="name">Nome do Template</Label>
                  <Input
                    id="name"
                    value={selectedTemplate.name}
                    onChange={(e) => setSelectedTemplate({
                      ...selectedTemplate,
                      name: e.target.value
                    })}
                    placeholder="Nome do template"
                  />
                </div>
                <div>
                  <Label htmlFor="category">Categoria</Label>
                  <Select
                    value={selectedTemplate.category}
                    onValueChange={(value) => setSelectedTemplate({
                      ...selectedTemplate,
                      category: value
                    })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map(category => (
                        <SelectItem key={category.id} value={category.id}>
                          {category.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="description">Descrição</Label>
                <Textarea
                  id="description"
                  value={selectedTemplate.description}
                  onChange={(e) => setSelectedTemplate({
                    ...selectedTemplate,
                    description: e.target.value
                  })}
                  placeholder="Descrição do template"
                  rows={2}
                />
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="active"
                  checked={selectedTemplate.isActive}
                  onCheckedChange={(checked) => setSelectedTemplate({
                    ...selectedTemplate,
                    isActive: checked
                  })}
                />
                <Label htmlFor="active">Template ativo</Label>
              </div>

              <Tabs defaultValue="editor" className="w-full">
                <TabsList>
                  <TabsTrigger value="editor">Editor</TabsTrigger>
                  <TabsTrigger value="variables">Variáveis</TabsTrigger>
                  <TabsTrigger value="preview">Preview</TabsTrigger>
                </TabsList>

                <TabsContent value="editor" className="space-y-4">
                  <div>
                    <Label>Conteúdo do Template</Label>
                    <div className="border rounded-md">
                      <div className="border-b p-2 flex gap-2 flex-wrap">
                        <Button variant="outline" size="sm" onClick={() => insertVariable('{username}')}>
                          <Type className="h-4 w-4 mr-1" />
                          Nome
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => insertVariable('{email}')}>
                          <Type className="h-4 w-4 mr-1" />
                          Email
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => insertVariable('{telefone}')}>
                          <Type className="h-4 w-4 mr-1" />
                          Telefone
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => insertVariable('{razaosocial}')}>
                          <Type className="h-4 w-4 mr-1" />
                          Empresa
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => insertVariable('{produto}')}>
                          <Type className="h-4 w-4 mr-1" />
                          Produto
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => insertVariable('{valortotal}')}>
                          <Type className="h-4 w-4 mr-1" />
                          Valor
                        </Button>
                      </div>
                      <Textarea
                        ref={editorRef}
                        value={selectedTemplate.content}
                        onChange={(e) => setSelectedTemplate({
                          ...selectedTemplate,
                          content: e.target.value
                        })}
                        placeholder="Conteúdo do template (HTML suportado)"
                        rows={15}
                        className="border-0 resize-none"
                      />
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="variables" className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Variáveis Disponíveis</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {availableVariables.map(variable => (
                        <div key={variable.key} className="border rounded-lg p-3">
                          <div className="flex items-center justify-between">
                            <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                              {variable.key}
                            </code>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => insertVariable(variable.key)}
                            >
                              Inserir
                            </Button>
                          </div>
                          <p className="text-sm text-gray-600 mt-2">{variable.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="preview" className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Preview do Template</h3>
                    <div 
                      className="border rounded-lg p-6 bg-white"
                      dangerouslySetInnerHTML={{ __html: selectedTemplate.content }}
                    />
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditing(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSaveTemplate}>
              <Save className="h-4 w-4 mr-2" />
              Salvar Template
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ProposalTemplatesManager;

