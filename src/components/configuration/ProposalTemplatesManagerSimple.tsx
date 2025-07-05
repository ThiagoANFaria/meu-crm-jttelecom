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
  FileText,
  Eye,
  Search,
  Filter,
  Star,
  StarOff,
  Copy,
  Download,
  Upload,
  Palette,
  Type,
  Bold,
  Italic,
  Underline,
  AlignLeft,
  AlignCenter,
  AlignRight,
  List,
  ListOrdered,
  Link,
  Image,
  Code,
  Undo,
  Redo
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/AuthContext';

interface ProposalTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  content: string;
  isDefault: boolean;
  isActive: boolean;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  variables?: string[];
  tags?: string[];
}

interface TemplateCategory {
  id: string;
  name: string;
  description: string;
  color: string;
}

const ProposalTemplatesManagerSimple: React.FC = () => {
  const [templates, setTemplates] = useState<ProposalTemplate[]>([]);
  const [categories, setCategories] = useState<TemplateCategory[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<ProposalTemplate | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showInactive, setShowInactive] = useState(false);
  const [previewMode, setPreviewMode] = useState(false);
  const { toast } = useToast();
  const { user } = useAuth();

  useEffect(() => {
    loadTemplates();
    loadCategories();
  }, []);

  const loadTemplates = () => {
    const defaultTemplates: ProposalTemplate[] = [
      {
        id: '1',
        name: 'Template Base',
        description: 'Template base personalizável para múltiplos segmentos',
        category: 'geral',
        content: `
          <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
              <h1 style="color: #4169E1; margin-bottom: 10px;">PROPOSTA COMERCIAL</h1>
              <p style="color: #666;">Número: {numeroproposta}</p>
              <p style="color: #666;">Data: {data}</p>
            </div>
            
            <div style="margin-bottom: 30px;">
              <h2 style="color: #333; border-bottom: 2px solid #4169E1; padding-bottom: 5px;">DADOS DO CLIENTE</h2>
              <p><strong>Empresa:</strong> {razaosocial}</p>
              <p><strong>CNPJ:</strong> {cnpj}</p>
              <p><strong>Contato:</strong> {username}</p>
              <p><strong>E-mail:</strong> {email}</p>
              <p><strong>Telefone:</strong> {telefone}</p>
              <p><strong>Endereço:</strong> {enderecocompleto}</p>
            </div>
            
            <div style="margin-bottom: 30px;">
              <h2 style="color: #333; border-bottom: 2px solid #4169E1; padding-bottom: 5px;">PROPOSTA</h2>
              <p>Produto/Serviço: {produto}</p>
              <p>Valor: {valortotal}</p>
              <p>Quantidade: {quantidade}</p>
            </div>
            
            <div style="margin-bottom: 30px;">
              <h2 style="color: #333; border-bottom: 2px solid #4169E1; padding-bottom: 5px;">OBSERVAÇÕES</h2>
              <p>[Inserir observações específicas do negócio]</p>
              <p>[Condições comerciais]</p>
              <p>[Prazo de ativação]</p>
            </div>
            
            <div style="margin-top: 40px; text-align: center; color: #666;">
              <p>Proposta válida até: {datavencimento}</p>
              <p>Responsável: {nomevendedor}</p>
              <p>E-mail: {emailvendedor}</p>
              <p>Telefone: {telefonevendedor}</p>
              <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;" />
              <p>{empresa} - {site} - {emailempresa}</p>
            </div>
          </div>
        `,
        isActive: true,
        isDefault: true,
        createdBy: 'system',
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        variables: [
          '{username}', '{email}', '{telefone}', '{whatsapp}',
          '{razaosocial}', '{cnpj}', '{cpf}', '{ie}', '{rg}',
          '{enderecocompleto}', '{endereco}', '{numero}', '{complemento}',
          '{bairro}', '{cidade}', '{estado}', '{cep}',
          '{produto}', '{valortotal}', '{valorunitario}', '{quantidade}',
          '{nomevendedor}', '{emailvendedor}', '{telefonevendedor}',
          '{data}', '{dataenvio}', '{datavencimento}', '{numeroproposta}',
          '{empresa}', '{logoempresa}', '{site}', '{emailempresa}'
        ],
        tags: ['base', 'generico', 'personalizavel']
      }
    ];
    setTemplates(defaultTemplates);
  };

  const loadCategories = () => {
    const defaultCategories: TemplateCategory[] = [
      { id: 'geral', name: 'Geral', description: 'Templates genéricos', color: '#6B7280' },
      { id: 'comunicacao', name: 'Comunicação', description: 'Soluções de comunicação', color: '#4169E1' },
      { id: 'telefonia', name: 'Telefonia', description: 'Serviços de telefonia', color: '#10B981' },
      { id: 'automacao', name: 'Automação', description: 'Soluções de automação', color: '#F59E0B' },
      { id: 'vendas', name: 'Vendas', description: 'Ferramentas de vendas', color: '#EF4444' },
      { id: 'servicos', name: 'Serviços', description: 'Serviços avulsos', color: '#8B5CF6' }
    ];
    setCategories(defaultCategories);
  };

  const availableVariables = [
    { group: 'Cliente', variables: ['{username}', '{email}', '{telefone}', '{whatsapp}'] },
    { group: 'Empresa', variables: ['{razaosocial}', '{cnpj}', '{cpf}', '{ie}', '{rg}'] },
    { group: 'Endereço', variables: ['{enderecocompleto}', '{endereco}', '{numero}', '{complemento}', '{bairro}', '{cidade}', '{estado}', '{cep}'] },
    { group: 'Produto', variables: ['{produto}', '{valortotal}', '{valorunitario}', '{quantidade}'] },
    { group: 'Vendedor', variables: ['{nomevendedor}', '{emailvendedor}', '{telefonevendedor}'] },
    { group: 'Datas', variables: ['{data}', '{dataenvio}', '{datavencimento}', '{numeroproposta}'] },
    { group: 'Sistema', variables: ['{empresa}', '{logoempresa}', '{site}', '{emailempresa}'] }
  ];

  const handleCreateTemplate = () => {
    const newTemplate: ProposalTemplate = {
      id: Date.now().toString(),
      name: '',
      description: '',
      category: 'geral',
      content: `
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
          <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #4169E1;">PROPOSTA COMERCIAL</h1>
            <p>Número: {numeroproposta} | Data: {data}</p>
          </div>
          
          <div style="margin-bottom: 30px;">
            <h2>DADOS DO CLIENTE</h2>
            <p>Empresa: {razaosocial}</p>
            <p>Contato: {username}</p>
            <p>E-mail: {email}</p>
          </div>
          
          <div style="margin-bottom: 30px;">
            <h2>PROPOSTA</h2>
            <p>[Inserir descrição da proposta]</p>
          </div>
          
          <div style="text-align: center; margin-top: 40px;">
            <p>Responsável: {nomevendedor}</p>
          </div>
        </div>
      `,
      isActive: true,
      isDefault: false,
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

  const handleSaveTemplate = () => {
    if (!selectedTemplate) return;

    if (!selectedTemplate.name.trim()) {
      toast({
        title: 'Erro',
        description: 'Nome do template é obrigatório.',
        variant: 'destructive'
      });
      return;
    }

    if (isCreating) {
      setTemplates(prev => [...prev, selectedTemplate]);
      toast({
        title: 'Template criado',
        description: 'Template criado com sucesso.',
      });
    } else {
      setTemplates(prev => prev.map(t => 
        t.id === selectedTemplate.id 
          ? { ...selectedTemplate, updatedAt: new Date().toISOString() }
          : t
      ));
      toast({
        title: 'Template atualizado',
        description: 'Template atualizado com sucesso.',
      });
    }

    setIsEditing(false);
    setIsCreating(false);
  };

  const handleDeleteTemplate = (templateId: string) => {
    const template = templates.find(t => t.id === templateId);
    if (template?.isDefault) {
      toast({
        title: 'Erro',
        description: 'Não é possível excluir o template padrão.',
        variant: 'destructive'
      });
      return;
    }

    setTemplates(prev => prev.filter(t => t.id !== templateId));
    if (selectedTemplate?.id === templateId) {
      setSelectedTemplate(null);
    }
    
    toast({
      title: 'Template excluído',
      description: 'Template excluído com sucesso.',
    });
  };

  const handleSetDefault = (templateId: string) => {
    setTemplates(prev => prev.map(t => ({
      ...t,
      isDefault: t.id === templateId,
      updatedAt: new Date().toISOString()
    })));
    
    toast({
      title: 'Template padrão definido',
      description: 'Template definido como padrão com sucesso.',
    });
  };

  const handleDuplicateTemplate = (template: ProposalTemplate) => {
    const duplicatedTemplate: ProposalTemplate = {
      ...template,
      id: Date.now().toString(),
      name: `${template.name} (Cópia)`,
      isDefault: false,
      createdBy: user?.name || 'admin',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    setTemplates(prev => [...prev, duplicatedTemplate]);
    toast({
      title: 'Template duplicado',
      description: 'Template duplicado com sucesso.',
    });
  };

  const insertVariable = (variable: string) => {
    if (!selectedTemplate || !isEditing) return;
    
    const textarea = document.getElementById('template-content') as HTMLTextAreaElement;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const content = selectedTemplate.content;
      const newContent = content.substring(0, start) + variable + content.substring(end);
      
      setSelectedTemplate({
        ...selectedTemplate,
        content: newContent
      });
      
      // Restore cursor position
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + variable.length;
        textarea.focus();
      }, 0);
    }
  };

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    const matchesActive = showInactive || template.isActive;
    return matchesSearch && matchesCategory && matchesActive;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Templates de Propostas</h3>
          <p className="text-sm text-gray-600">
            Estrutura base personalizável para múltiplos segmentos - sem exemplos específicos
          </p>
        </div>
        <Button onClick={handleCreateTemplate} className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />
          Novo Template
        </Button>
      </div>

      {/* Filters */}
      <div className="flex gap-4 items-center">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
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
        {/* Templates List */}
        <div className="lg:col-span-1 space-y-4">
          <h4 className="font-medium">Templates ({filteredTemplates.length})</h4>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {filteredTemplates.map((template) => (
              <Card 
                key={template.id} 
                className={`cursor-pointer transition-all ${
                  selectedTemplate?.id === template.id ? 'ring-2 ring-blue-500' : ''
                } ${!template.isActive ? 'opacity-60' : ''}`}
                onClick={() => setSelectedTemplate(template)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h5 className="font-medium">{template.name}</h5>
                        {template.isDefault && (
                          <Star className="w-4 h-4 text-yellow-500 fill-current" />
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">{template.description}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant="outline" style={{ 
                          borderColor: categories.find(c => c.id === template.category)?.color,
                          color: categories.find(c => c.id === template.category)?.color
                        }}>
                          {categories.find(c => c.id === template.category)?.name}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDuplicateTemplate(template);
                        }}
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedTemplate(template);
                          setIsEditing(true);
                        }}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      {!template.isDefault && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteTemplate(template.id);
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

        {/* Template Editor/Preview */}
        <div className="lg:col-span-2">
          {selectedTemplate ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      {selectedTemplate.name || 'Novo Template'}
                      {selectedTemplate.isDefault && (
                        <Star className="w-5 h-5 text-yellow-500 fill-current" />
                      )}
                    </CardTitle>
                    <CardDescription>
                      {isCreating ? 'Criando novo template' : 'Editando template existente'}
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    {!selectedTemplate.isDefault && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleSetDefault(selectedTemplate.id)}
                      >
                        <Star className="w-4 h-4" />
                      </Button>
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setPreviewMode(!previewMode)}
                    >
                      {previewMode ? <Edit className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
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
                  <div className="space-y-4">
                    {/* Template Info */}
                    <div className="grid gap-4 md:grid-cols-2">
                      <div>
                        <Label htmlFor="template-name">Nome do Template *</Label>
                        <Input
                          id="template-name"
                          value={selectedTemplate.name}
                          onChange={(e) => setSelectedTemplate({
                            ...selectedTemplate,
                            name: e.target.value
                          })}
                          placeholder="Ex: Template Base, Proposta Personalizada"
                        />
                      </div>
                      <div>
                        <Label htmlFor="template-category">Categoria</Label>
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
                      <Label htmlFor="template-description">Descrição</Label>
                      <Input
                        id="template-description"
                        value={selectedTemplate.description}
                        onChange={(e) => setSelectedTemplate({
                          ...selectedTemplate,
                          description: e.target.value
                        })}
                        placeholder="Descrição do template"
                      />
                    </div>

                    {/* Variables Panel */}
                    <div>
                      <Label>Variáveis Disponíveis</Label>
                      <div className="mt-2 p-4 border rounded-lg bg-gray-50 max-h-40 overflow-y-auto">
                        {availableVariables.map((group) => (
                          <div key={group.group} className="mb-3">
                            <h6 className="font-medium text-sm text-gray-700 mb-2">{group.group}</h6>
                            <div className="flex flex-wrap gap-1">
                              {group.variables.map((variable) => (
                                <Button
                                  key={variable}
                                  variant="outline"
                                  size="sm"
                                  className="text-xs h-6"
                                  onClick={() => insertVariable(variable)}
                                >
                                  {variable}
                                </Button>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Content Editor */}
                    <div>
                      <Label htmlFor="template-content">Conteúdo HTML</Label>
                      <Textarea
                        id="template-content"
                        value={selectedTemplate.content}
                        onChange={(e) => setSelectedTemplate({
                          ...selectedTemplate,
                          content: e.target.value
                        })}
                        placeholder="Conteúdo HTML do template..."
                        rows={15}
                        className="font-mono text-sm"
                      />
                    </div>

                    <div className="flex items-center space-x-2">
                      <Switch
                        id="template-active"
                        checked={selectedTemplate.isActive}
                        onCheckedChange={(checked) => setSelectedTemplate({
                          ...selectedTemplate,
                          isActive: checked
                        })}
                      />
                      <Label htmlFor="template-active">Template ativo</Label>
                    </div>

                    {/* Actions */}
                    <div className="flex justify-end gap-3 pt-4">
                      <Button
                        variant="outline"
                        onClick={() => {
                          setIsEditing(false);
                          setIsCreating(false);
                          if (isCreating) {
                            setSelectedTemplate(null);
                          }
                        }}
                      >
                        Cancelar
                      </Button>
                      <Button onClick={handleSaveTemplate} className="bg-blue-600 hover:bg-blue-700">
                        <Save className="w-4 h-4 mr-2" />
                        Salvar Template
                      </Button>
                    </div>
                  </div>
                ) : (
                  /* Template Preview */
                  <div className="space-y-4">
                    {previewMode ? (
                      <div className="border rounded-lg p-4 bg-white">
                        <div dangerouslySetInnerHTML={{ __html: selectedTemplate.content }} />
                      </div>
                    ) : (
                      <div className="space-y-4">
                        <div className="grid gap-4 md:grid-cols-2">
                          <div>
                            <span className="font-medium">Categoria:</span> {categories.find(c => c.id === selectedTemplate.category)?.name}
                          </div>
                          <div>
                            <span className="font-medium">Status:</span> 
                            <Badge variant={selectedTemplate.isActive ? "default" : "secondary"} className="ml-2">
                              {selectedTemplate.isActive ? "Ativo" : "Inativo"}
                            </Badge>
                          </div>
                          <div>
                            <span className="font-medium">Tipo:</span> 
                            <Badge variant={selectedTemplate.isDefault ? "default" : "outline"} className="ml-2">
                              {selectedTemplate.isDefault ? "Template Padrão" : "Template Personalizado"}
                            </Badge>
                          </div>
                        </div>

                        <div>
                          <span className="font-medium">Descrição:</span>
                          <p className="mt-1 text-gray-700">{selectedTemplate.description}</p>
                        </div>

                        <div>
                          <span className="font-medium">Variáveis utilizadas:</span>
                          <div className="mt-2 flex flex-wrap gap-1">
                            {availableVariables.flatMap(group => group.variables)
                              .filter(variable => selectedTemplate.content.includes(variable))
                              .map(variable => (
                                <Badge key={variable} variant="outline" className="text-xs">
                                  {variable}
                                </Badge>
                              ))}
                          </div>
                        </div>

                        <div className="grid gap-4 md:grid-cols-2 text-sm text-gray-600">
                          <div>
                            <span className="font-medium">Criado por:</span> {selectedTemplate.createdBy}
                          </div>
                          <div>
                            <span className="font-medium">Criado em:</span> {new Date(selectedTemplate.createdAt).toLocaleDateString('pt-BR')}
                          </div>
                          <div>
                            <span className="font-medium">Atualizado em:</span> {new Date(selectedTemplate.updatedAt).toLocaleDateString('pt-BR')}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-8 text-center">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Selecione um Template</h3>
                <p className="text-gray-600 mb-4">
                  Escolha um template da lista para visualizar ou editar seu conteúdo.
                </p>
                <Button onClick={handleCreateTemplate} className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Criar Novo Template
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Summary */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <FileText className="w-8 h-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold">{templates.length}</div>
                <div className="text-sm text-gray-600">Total de Templates</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Star className="w-8 h-8 text-yellow-500" />
              <div>
                <div className="text-2xl font-bold">{templates.filter(t => t.isDefault).length}</div>
                <div className="text-sm text-gray-600">Template Padrão</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Eye className="w-8 h-8 text-green-500" />
              <div>
                <div className="text-2xl font-bold">{templates.filter(t => t.isActive).length}</div>
                <div className="text-sm text-gray-600">Templates Ativos</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Code className="w-8 h-8 text-purple-500" />
              <div>
                <div className="text-2xl font-bold">{availableVariables.flatMap(g => g.variables).length}</div>
                <div className="text-sm text-gray-600">Variáveis Disponíveis</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProposalTemplatesManagerSimple;

