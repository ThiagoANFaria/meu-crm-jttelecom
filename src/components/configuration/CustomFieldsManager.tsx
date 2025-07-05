import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { 
  Plus, 
  Edit, 
  Trash2, 
  Save, 
  X,
  Database,
  Type,
  Hash,
  Calendar,
  ToggleLeft,
  List,
  FileText,
  Mail,
  Phone,
  MapPin,
  DollarSign,
  Percent,
  Clock,
  Link,
  Image,
  CheckSquare
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';

interface CustomField {
  id: string;
  name: string;
  label: string;
  type: 'text' | 'number' | 'email' | 'phone' | 'date' | 'datetime' | 'boolean' | 'select' | 'textarea' | 'url' | 'currency' | 'percentage';
  module: 'leads' | 'clients';
  required: boolean;
  placeholder?: string;
  description?: string;
  options?: string[];
  defaultValue?: string;
  validation?: {
    minLength?: number;
    maxLength?: number;
    min?: number;
    max?: number;
    pattern?: string;
  };
  order: number;
  active: boolean;
  tenantId: string; // ID do tenant para isolamento multi-tenant
  createdAt: string;
  updatedAt: string;
}

const CustomFieldsManager: React.FC = () => {
  const [fields, setFields] = useState<CustomField[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editingField, setEditingField] = useState<Partial<CustomField> | null>(null);
  const [selectedModule, setSelectedModule] = useState<'leads' | 'clients' | 'all'>('all');
  const { toast } = useToast();
  const { currentTenant } = useTenant();

  useEffect(() => {
    if (currentTenant) {
      loadCustomFields();
    }
  }, [currentTenant]);

  const loadCustomFields = () => {
    if (!currentTenant) return;

    // Simular carregamento de campos personalizados específicos do tenant
    const mockFields: CustomField[] = [
      {
        id: `${currentTenant.id}-field-1`,
        name: 'lead_source_detail',
        label: 'Detalhes da Origem',
        type: 'textarea',
        module: 'leads',
        required: false,
        placeholder: 'Descreva como o lead chegou até nós...',
        description: 'Informações adicionais sobre a origem do lead',
        order: 1,
        active: true,
        tenantId: currentTenant.id,
        createdAt: '2025-01-01',
        updatedAt: '2025-01-01'
      },
      {
        id: `${currentTenant.id}-field-2`,
        name: 'budget_range',
        label: 'Faixa de Orçamento',
        type: 'select',
        module: 'leads',
        required: true,
        options: ['Até R$ 1.000', 'R$ 1.000 - R$ 5.000', 'R$ 5.000 - R$ 10.000', 'Acima de R$ 10.000'],
        description: 'Faixa de orçamento disponível do cliente',
        order: 2,
        active: true,
        tenantId: currentTenant.id,
        createdAt: '2025-01-01',
        updatedAt: '2025-01-01'
      },
      {
        id: `${currentTenant.id}-field-3`,
        name: 'client_priority',
        label: 'Prioridade do Cliente',
        type: 'select',
        module: 'clients',
        required: false,
        options: ['Baixa', 'Média', 'Alta', 'Crítica'],
        defaultValue: 'Média',
        description: 'Nível de prioridade para atendimento',
        order: 1,
        active: true,
        tenantId: currentTenant.id,
        createdAt: '2025-01-01',
        updatedAt: '2025-01-01'
      }
    ];
    setFields(mockFields);
  };

  const fieldTypes = [
    { value: 'text', label: 'Texto', icon: Type },
    { value: 'number', label: 'Número', icon: Hash },
    { value: 'email', label: 'E-mail', icon: Mail },
    { value: 'phone', label: 'Telefone', icon: Phone },
    { value: 'date', label: 'Data', icon: Calendar },
    { value: 'datetime', label: 'Data e Hora', icon: Clock },
    { value: 'boolean', label: 'Sim/Não', icon: ToggleLeft },
    { value: 'select', label: 'Lista de Opções', icon: List },
    { value: 'textarea', label: 'Texto Longo', icon: FileText },
    { value: 'url', label: 'URL/Link', icon: Link },
    { value: 'currency', label: 'Moeda', icon: DollarSign },
    { value: 'percentage', label: 'Porcentagem', icon: Percent }
  ];

  const getFieldIcon = (type: string) => {
    const fieldType = fieldTypes.find(ft => ft.value === type);
    return fieldType ? fieldType.icon : Type;
  };

  const filteredFields = fields.filter(field => 
    selectedModule === 'all' || field.module === selectedModule
  );

  const handleCreateField = () => {
    if (!currentTenant) return;

    setEditingField({
      name: '',
      label: '',
      type: 'text',
      module: 'leads',
      required: false,
      active: true,
      order: fields.length + 1,
      tenantId: currentTenant.id
    });
    setIsEditing(true);
  };

  const handleEditField = (field: CustomField) => {
    setEditingField(field);
    setIsEditing(true);
  };

  const handleSaveField = () => {
    if (!editingField?.name || !editingField?.label || !currentTenant) {
      toast({
        title: 'Erro',
        description: 'Nome e rótulo são obrigatórios.',
        variant: 'destructive',
      });
      return;
    }

    const now = new Date().toISOString().split('T')[0];
    
    if (editingField.id) {
      // Editar campo existente
      setFields(prev => prev.map(field => 
        field.id === editingField.id 
          ? { ...field, ...editingField, updatedAt: now } as CustomField
          : field
      ));
      toast({
        title: 'Campo atualizado',
        description: 'O campo personalizado foi atualizado com sucesso.',
      });
    } else {
      // Criar novo campo
      const newField: CustomField = {
        ...editingField,
        id: `${currentTenant.id}-field-${Date.now()}`,
        tenantId: currentTenant.id,
        createdAt: now,
        updatedAt: now
      } as CustomField;
      
      setFields(prev => [...prev, newField]);
      toast({
        title: 'Campo criado',
        description: 'O novo campo personalizado foi criado com sucesso.',
      });
    }

    setIsEditing(false);
    setEditingField(null);
  };

  const handleDeleteField = (fieldId: string) => {
    setFields(prev => prev.filter(field => field.id !== fieldId));
    toast({
      title: 'Campo removido',
      description: 'O campo personalizado foi removido com sucesso.',
    });
  };

  const handleToggleActive = (fieldId: string) => {
    setFields(prev => prev.map(field => 
      field.id === fieldId 
        ? { ...field, active: !field.active, updatedAt: new Date().toISOString().split('T')[0] }
        : field
    ));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Campos Personalizados</h3>
          <p className="text-sm text-gray-600">
            Gerencie campos adicionais para capturar informações específicas
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Select value={selectedModule} onValueChange={(value: any) => setSelectedModule(value)}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Filtrar por módulo" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos os Módulos</SelectItem>
              <SelectItem value="leads">Leads</SelectItem>
              <SelectItem value="clients">Clientes</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleCreateField} className="bg-blue-600 hover:bg-blue-700">
            <Plus className="w-4 h-4 mr-2" />
            Novo Campo
          </Button>
        </div>
      </div>

      {/* Fields List */}
      <div className="grid gap-4">
        {filteredFields.map((field) => {
          const IconComponent = getFieldIcon(field.type);
          return (
            <Card key={field.id} className={`${!field.active ? 'opacity-60' : ''}`}>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <IconComponent className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="font-medium">{field.label}</h4>
                        <Badge variant={field.module === 'leads' ? 'default' : 'secondary'}>
                          {field.module === 'leads' ? 'Leads' : 'Clientes'}
                        </Badge>
                        {field.required && (
                          <Badge variant="destructive" className="text-xs">Obrigatório</Badge>
                        )}
                        {!field.active && (
                          <Badge variant="outline" className="text-xs">Inativo</Badge>
                        )}
                      </div>
                      <div className="text-sm text-gray-600">
                        <span className="font-mono bg-gray-100 px-2 py-1 rounded text-xs mr-2">
                          {field.name}
                        </span>
                        <span>{fieldTypes.find(ft => ft.value === field.type)?.label}</span>
                      </div>
                      {field.description && (
                        <p className="text-xs text-gray-500 mt-1">{field.description}</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={field.active}
                      onCheckedChange={() => handleToggleActive(field.id)}
                    />
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEditField(field)}
                    >
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDeleteField(field.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}

        {filteredFields.length === 0 && (
          <Card>
            <CardContent className="p-8 text-center">
              <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhum campo encontrado</h3>
              <p className="text-gray-600 mb-4">
                {selectedModule === 'all' 
                  ? 'Não há campos personalizados criados ainda.'
                  : `Não há campos personalizados para ${selectedModule === 'leads' ? 'Leads' : 'Clientes'}.`
                }
              </p>
              <Button onClick={handleCreateField} className="bg-blue-600 hover:bg-blue-700">
                <Plus className="w-4 h-4 mr-2" />
                Criar Primeiro Campo
              </Button>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Edit/Create Modal */}
      {isEditing && editingField && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>
                    {editingField.id ? 'Editar Campo' : 'Novo Campo Personalizado'}
                  </CardTitle>
                  <CardDescription>
                    Configure as propriedades do campo personalizado
                  </CardDescription>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setIsEditing(false);
                    setEditingField(null);
                  }}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="field-name">Nome do Campo *</Label>
                  <Input
                    id="field-name"
                    value={editingField.name || ''}
                    onChange={(e) => setEditingField(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="ex: budget_range"
                    className="font-mono"
                  />
                  <p className="text-xs text-gray-500">Nome técnico (sem espaços ou caracteres especiais)</p>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="field-label">Rótulo do Campo *</Label>
                  <Input
                    id="field-label"
                    value={editingField.label || ''}
                    onChange={(e) => setEditingField(prev => ({ ...prev, label: e.target.value }))}
                    placeholder="ex: Faixa de Orçamento"
                  />
                  <p className="text-xs text-gray-500">Nome que aparecerá na interface</p>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="field-type">Tipo do Campo</Label>
                  <Select 
                    value={editingField.type} 
                    onValueChange={(value: any) => setEditingField(prev => ({ ...prev, type: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      {fieldTypes.map((type) => (
                        <SelectItem key={type.value} value={type.value}>
                          <div className="flex items-center gap-2">
                            <type.icon className="w-4 h-4" />
                            {type.label}
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="field-module">Módulo</Label>
                  <Select 
                    value={editingField.module} 
                    onValueChange={(value: any) => setEditingField(prev => ({ ...prev, module: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o módulo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="leads">Leads</SelectItem>
                      <SelectItem value="clients">Clientes</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="field-description">Descrição</Label>
                <Textarea
                  id="field-description"
                  value={editingField.description || ''}
                  onChange={(e) => setEditingField(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Descreva o propósito deste campo..."
                  rows={2}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="field-placeholder">Placeholder</Label>
                <Input
                  id="field-placeholder"
                  value={editingField.placeholder || ''}
                  onChange={(e) => setEditingField(prev => ({ ...prev, placeholder: e.target.value }))}
                  placeholder="Texto de exemplo que aparecerá no campo"
                />
              </div>

              {editingField.type === 'select' && (
                <div className="space-y-2">
                  <Label>Opções (uma por linha)</Label>
                  <Textarea
                    value={editingField.options?.join('\n') || ''}
                    onChange={(e) => setEditingField(prev => ({ 
                      ...prev, 
                      options: e.target.value.split('\n').filter(opt => opt.trim()) 
                    }))}
                    placeholder="Opção 1&#10;Opção 2&#10;Opção 3"
                    rows={4}
                  />
                </div>
              )}

              <div className="flex items-center space-x-2">
                <Switch
                  id="field-required"
                  checked={editingField.required || false}
                  onCheckedChange={(checked) => setEditingField(prev => ({ ...prev, required: checked }))}
                />
                <Label htmlFor="field-required">Campo obrigatório</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="field-active"
                  checked={editingField.active !== false}
                  onCheckedChange={(checked) => setEditingField(prev => ({ ...prev, active: checked }))}
                />
                <Label htmlFor="field-active">Campo ativo</Label>
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <Button
                  variant="outline"
                  onClick={() => {
                    setIsEditing(false);
                    setEditingField(null);
                  }}
                >
                  Cancelar
                </Button>
                <Button onClick={handleSaveField} className="bg-blue-600 hover:bg-blue-700">
                  <Save className="w-4 h-4 mr-2" />
                  {editingField.id ? 'Atualizar' : 'Criar'} Campo
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default CustomFieldsManager;

