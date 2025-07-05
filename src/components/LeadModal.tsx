import React, { useState, useEffect } from 'react';
import { Lead, Tag } from '@/types';
import { apiService } from '@/services/api';
import { cnpjService } from '@/services/cnpj';
import { smartbotService, SmartbotMessage } from '@/services/smartbot';
import { pabxService, PabxCall } from '@/services/pabx';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Loader2, 
  User, 
  Building, 
  MapPin, 
  Tag as TagIcon, 
  Settings, 
  Calculator, 
  Search,
  FileText,
  Phone,
  MessageSquare,
  Clock,
  Send,
  History,
  Bot
} from 'lucide-react';
import TagSystem from './TagSystem';
import LeadScoring from './LeadScoring';

interface LeadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  lead?: Lead | null;
}

const LeadModal: React.FC<LeadModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  lead,
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('basic');
  const { toast } = useToast();
  const { currentTenant } = useTenant();

  // Campos Padrão Obrigatórios
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    whatsapp: '',
    company: '',
    cnpj_cpf: '',
    ie_rg: '',
    address: '',
    number: '',
    neighborhood: '',
    city: '',
    state: '',
    cep: '',
    source: 'Website',
    status: 'Novo',
    responsible: '',
    notes: ''
  });

  // Campos Opcionais/Customizáveis
  const [customFields, setCustomFields] = useState<Record<string, any>>({});
  const [enabledOptionalFields, setEnabledOptionalFields] = useState<Record<string, boolean>>({
    website: false,
    linkedin: false,
    facebook: false,
    instagram: false,
    referral_source: false,
    budget: false,
    timeline: false,
    decision_maker: false,
    company_size: false,
    industry: false
  });

  // Tags e Scoring
  const [selectedTags, setSelectedTags] = useState<Tag[]>([]);
  const [availableTags] = useState<Tag[]>([
    { id: '1', name: 'VIP', color: '#FFD700', created_at: new Date().toISOString() },
    { id: '2', name: 'Urgente', color: '#FF4444', created_at: new Date().toISOString() },
    { id: '3', name: 'Qualificado', color: '#00AA00', created_at: new Date().toISOString() },
    { id: '4', name: 'Follow-up', color: '#4169E1', created_at: new Date().toISOString() },
    { id: '5', name: 'Orçamento Alto', color: '#8B5CF6', created_at: new Date().toISOString() }
  ]);

  const [calculatedScore, setCalculatedScore] = useState(0);

  // Estados para consulta de CNPJ
  const [isCNPJLoading, setIsCNPJLoading] = useState(false);
  const [cnpjData, setCnpjData] = useState<any>(null);
  const [showCNPJData, setShowCNPJData] = useState(false);

  // Opções para selects
  const sourceOptions = [
    'Website', 'Google Ads', 'Facebook', 'Instagram', 'Indicação',
    'Telefone', 'Email', 'Evento', 'LinkedIn', 'WhatsApp', 'Outros'
  ];

  const statusOptions = [
    'Novo', 'Em Contato', 'Qualificado', 'Proposta Enviada',
    'Em Negociação', 'Ganho', 'Perdido'
  ];

  const stateOptions = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
  ];

  const industryOptions = [
    'Tecnologia', 'Saúde', 'Educação', 'Varejo', 'Serviços',
    'Manufatura', 'Construção', 'Alimentação', 'Transporte', 'Outros'
  ];

  const companySizeOptions = [
    '1-10 funcionários', '11-50 funcionários', '51-200 funcionários',
    '201-500 funcionários', '500+ funcionários'
  ];

  // Campos opcionais disponíveis
  const optionalFieldsConfig = {
    website: { label: 'Website', type: 'url', placeholder: 'https://exemplo.com' },
    linkedin: { label: 'LinkedIn', type: 'url', placeholder: 'https://linkedin.com/in/perfil' },
    facebook: { label: 'Facebook', type: 'url', placeholder: 'https://facebook.com/perfil' },
    instagram: { label: 'Instagram', type: 'url', placeholder: '@usuario' },
    referral_source: { label: 'Fonte da Indicação', type: 'text', placeholder: 'Nome do indicador' },
    budget: { label: 'Orçamento Estimado', type: 'number', placeholder: '0' },
    timeline: { label: 'Prazo para Decisão', type: 'text', placeholder: 'Ex: 30 dias' },
    decision_maker: { label: 'Tomador de Decisão', type: 'text', placeholder: 'Nome e cargo' },
    company_size: { label: 'Tamanho da Empresa', type: 'select', options: companySizeOptions },
    industry: { label: 'Setor/Indústria', type: 'select', options: industryOptions }
  };

  useEffect(() => {
    if (lead) {
      setFormData({
        name: lead.name || '',
        email: lead.email || '',
        phone: lead.phone || '',
        whatsapp: lead.whatsapp || '',
        company: lead.company || '',
        cnpj_cpf: lead.cnpj_cpf || '',
        ie_rg: lead.ie_rg || '',
        address: lead.address || '',
        number: lead.number || '',
        neighborhood: lead.neighborhood || '',
        city: lead.city || '',
        state: lead.state || '',
        cep: lead.cep || '',
        source: lead.source || 'Website',
        status: lead.status || 'Novo',
        responsible: lead.responsible || '',
        notes: lead.notes || ''
      });
      
      setSelectedTags(lead.tags || []);
      setCustomFields(lead.custom_fields || {});
      setCalculatedScore(lead.score || 0);
      
      // Ativar campos opcionais que têm dados
      const enabledFields: Record<string, boolean> = {};
      Object.keys(optionalFieldsConfig).forEach(field => {
        enabledFields[field] = !!(lead.custom_fields?.[field]);
      });
      setEnabledOptionalFields(enabledFields);
    } else {
      // Reset para novo lead
      setFormData({
        name: '', email: '', phone: '', whatsapp: '', company: '',
        cnpj_cpf: '', ie_rg: '', address: '', number: '', neighborhood: '',
        city: '', state: '', cep: '', source: 'Website', status: 'Novo',
        responsible: '', notes: ''
      });
      setSelectedTags([]);
      setCustomFields({});
      setCalculatedScore(0);
      setEnabledOptionalFields({
        website: false, linkedin: false, facebook: false, instagram: false,
        referral_source: false, budget: false, timeline: false, decision_maker: false,
        company_size: false, industry: false
      });
    }
  }, [lead, isOpen]);

  // Calcular Lead Score automaticamente
  useEffect(() => {
    calculateLeadScore();
  }, [formData, selectedTags, customFields]);

  const calculateLeadScore = () => {
    let score = 0;

    // Completude dos dados (40 pontos)
    const requiredFields = ['name', 'email', 'phone', 'company'];
    const completedRequired = requiredFields.filter(field => formData[field as keyof typeof formData]).length;
    score += (completedRequired / requiredFields.length) * 40;

    // Dados adicionais (20 pontos)
    const optionalFieldsCount = Object.values(customFields).filter(value => value).length;
    score += Math.min(optionalFieldsCount * 2, 20);

    // Tags importantes (20 pontos)
    const importantTags = ['VIP', 'Qualificado', 'Orçamento Alto'];
    const hasImportantTags = selectedTags.some(tag => importantTags.includes(tag.name));
    if (hasImportantTags) score += 20;

    // Origem (10 pontos)
    const highValueSources = ['Indicação', 'LinkedIn', 'Evento'];
    if (highValueSources.includes(formData.source)) score += 10;

    // Empresa preenchida (10 pontos)
    if (formData.company && formData.cnpj_cpf) score += 10;

    setCalculatedScore(Math.min(Math.round(score), 100));
  };

  // ===== NOVOS ESTADOS PARA FUNCIONALIDADES AVANÇADAS =====
  
  // Estados para Registros e Notas
  const [leadNotes, setLeadNotes] = useState<any[]>([]);
  const [newNote, setNewNote] = useState('');
  const [isAddingNote, setIsAddingNote] = useState(false);

  // Estados para Histórico de Ligações
  const [callHistory, setCallHistory] = useState<PabxCall[]>([]);
  const [isLoadingCalls, setIsLoadingCalls] = useState(false);
  const [selectedExtension, setSelectedExtension] = useState('1001');
  const [availableExtensions, setAvailableExtensions] = useState<any[]>([]);

  // Estados para Smartbot
  const [smartbotMessages, setSmartbotMessages] = useState<SmartbotMessage[]>([]);
  const [newSmartbotMessage, setNewSmartbotMessage] = useState('');
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [selectedMessageTemplate, setSelectedMessageTemplate] = useState('');
  const [smartbotChannels, setSmartbotChannels] = useState<any[]>([]);

  // Estados para Automações
  const [automationTasks, setAutomationTasks] = useState<any[]>([]);
  const [isCreatingTask, setIsCreatingTask] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDate, setNewTaskDate] = useState('');
  const [newTaskType, setNewTaskType] = useState('call');

  // Carregar dados das novas funcionalidades quando o modal abrir
  useEffect(() => {
    if (isOpen && lead?.id) {
      loadLeadNotes();
      loadCallHistory();
      loadSmartbotMessages();
      loadAvailableExtensions();
      loadSmartbotChannels();
    }
  }, [isOpen, lead?.id]);

  // Funções para carregar dados específicos do tenant
  const loadLeadNotes = async () => {
    if (!lead?.id || !currentTenant) return;
    try {
      const notes = await apiService.getLeadNotes(lead.id, { tenantId: currentTenant.id });
      setLeadNotes(notes);
    } catch (error) {
      console.error('Erro ao carregar notas:', error);
    }
  };

  const loadCallHistory = async () => {
    if (!lead?.phone) return;
    setIsLoadingCalls(true);
    try {
      const calls = await pabxService.getLeadCallHistory(lead.phone);
      setCallHistory(calls);
    } catch (error) {
      console.error('Erro ao carregar histórico de ligações:', error);
    } finally {
      setIsLoadingCalls(false);
    }
  };

  const loadSmartbotMessages = async () => {
    if (!lead?.phone) return;
    try {
      const messages = await smartbotService.getMessages('default_token', lead.phone);
      setSmartbotMessages(messages);
    } catch (error) {
      console.error('Erro ao carregar mensagens Smartbot:', error);
    }
  };

  const loadAvailableExtensions = async () => {
    try {
      const extensions = await pabxService.getExtensions();
      setAvailableExtensions(extensions);
    } catch (error) {
      console.error('Erro ao carregar ramais:', error);
    }
  };

  const loadSmartbotChannels = async () => {
    try {
      const channels = await smartbotService.getChannels();
      setSmartbotChannels(channels);
    } catch (error) {
      console.error('Erro ao carregar canais Smartbot:', error);
    }
  };

  // ===== FUNÇÕES PARA NOVAS FUNCIONALIDADES =====

  // Adicionar nova nota
  const handleAddNote = async () => {
    if (!newNote.trim() || !lead?.id) return;
    
    setIsAddingNote(true);
    try {
      await apiService.addLeadNote(lead.id, newNote.trim());
      setNewNote('');
      await loadLeadNotes();
      toast({
        title: "Sucesso",
        description: "Nota adicionada com sucesso",
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro ao adicionar nota",
        variant: "destructive",
      });
    } finally {
      setIsAddingNote(false);
    }
  };

  // Fazer ligação via PABX
  const handleMakeCall = async () => {
    if (!lead?.phone || !selectedExtension) return;
    
    try {
      const result = await pabxService.makeCall(selectedExtension, lead.phone);
      toast({
        title: "Ligação Iniciada",
        description: `Chamada para ${lead.phone} iniciada no ramal ${selectedExtension}`,
      });
      
      // Recarregar histórico após alguns segundos
      setTimeout(() => {
        loadCallHistory();
      }, 3000);
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro ao iniciar ligação",
        variant: "destructive",
      });
    }
  };

  // Enviar mensagem via Smartbot
  const handleSendSmartbotMessage = async () => {
    if (!newSmartbotMessage.trim() || !lead?.phone) return;
    
    setIsSendingMessage(true);
    try {
      await smartbotService.sendLeadMessage(lead.phone, lead.name, newSmartbotMessage);
      setNewSmartbotMessage('');
      await loadSmartbotMessages();
      toast({
        title: "Sucesso",
        description: "Mensagem enviada via Smartbot",
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro ao enviar mensagem",
        variant: "destructive",
      });
    } finally {
      setIsSendingMessage(false);
    }
  };

  // Usar template de mensagem
  const handleUseMessageTemplate = (template: string) => {
    const templates = smartbotService.getMessageTemplates();
    const message = templates[template]?.replace('{nome}', lead?.name || 'Cliente');
    setNewSmartbotMessage(message || '');
  };

  // Criar tarefa de automação
  const handleCreateAutomationTask = async () => {
    if (!newTaskTitle.trim() || !newTaskDate || !lead?.id) return;
    
    setIsCreatingTask(true);
    try {
      const task = {
        lead_id: lead.id,
        title: newTaskTitle,
        type: newTaskType,
        scheduled_date: newTaskDate,
        status: 'pending'
      };
      
      // Simular criação de tarefa (implementar API real depois)
      const newTask = {
        ...task,
        id: Date.now().toString(),
        created_at: new Date().toISOString()
      };
      
      setAutomationTasks(prev => [...prev, newTask]);
      setNewTaskTitle('');
      setNewTaskDate('');
      setNewTaskType('call');
      
      toast({
        title: "Sucesso",
        description: "Tarefa de automação criada",
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro ao criar tarefa",
        variant: "destructive",
      });
    } finally {
      setIsCreatingTask(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleCustomFieldChange = (field: string, value: any) => {
    setCustomFields(prev => ({ ...prev, [field]: value }));
  };

  const toggleOptionalField = (field: string, enabled: boolean) => {
    setEnabledOptionalFields(prev => ({ ...prev, [field]: enabled }));
    if (!enabled) {
      // Remove o valor do campo se desabilitado
      setCustomFields(prev => {
        const newFields = { ...prev };
        delete newFields[field];
        return newFields;
      });
    }
  };

  // Funções para consulta de CNPJ
  const handleCNPJChange = (value: string) => {
    const maskedValue = cnpjService.applyCNPJMask(value);
    handleInputChange('cnpj_cpf', maskedValue);
    
    // Limpar dados anteriores se CNPJ foi alterado
    if (cnpjData) {
      setCnpjData(null);
      setShowCNPJData(false);
    }
  };

  const consultarCNPJ = async () => {
    if (!formData.cnpj_cpf) {
      toast({
        title: 'CNPJ obrigatório',
        description: 'Digite um CNPJ para consultar',
        variant: 'destructive',
      });
      return;
    }

    setIsCNPJLoading(true);
    
    try {
      // Usar proxy CORS para acessar a API ReceitaWS
      const cleanCNPJ = formData.cnpj_cpf.replace(/\D/g, '');
      const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(`https://receitaws.com.br/v1/cnpj/${cleanCNPJ}`)}`;
      
      console.log('Consultando CNPJ via proxy:', cleanCNPJ);
      
      const response = await fetch(proxyUrl);
      const proxyData = await response.json();
      
      if (proxyData.status.http_code === 200) {
        const cnpjData = JSON.parse(proxyData.contents);
        
        if (cnpjData.status === 'OK') {
          setCnpjData(cnpjData);
          setShowCNPJData(true);
          
          toast({
            title: 'CNPJ encontrado!',
            description: `Empresa: ${cnpjData.nome}`,
          });
        } else {
          toast({
            title: 'CNPJ não encontrado',
            description: 'Verifique o CNPJ digitado',
            variant: 'destructive',
          });
        }
      } else {
        toast({
          title: 'Erro na consulta',
          description: 'Serviço temporariamente indisponível',
          variant: 'destructive',
        });
      }
    } catch (error) {
      console.error('Erro ao consultar CNPJ:', error);
      toast({
        title: 'Erro na consulta',
        description: 'Erro ao consultar CNPJ. Verifique sua conexão.',
        variant: 'destructive',
      });
    } finally {
      setIsCNPJLoading(false);
    }
  };

  const preencherDadosCNPJ = () => {
    if (!cnpjData) return;

    // Preencher campos do formulário com dados reais da ReceitaWS
    setFormData(prev => ({
      ...prev,
      company: cnpjData.nome || '', // Razão Social
      address: cnpjData.logradouro || '',
      number: cnpjData.numero || '',
      complement: cnpjData.complemento || '',
      neighborhood: cnpjData.bairro || '',
      city: cnpjData.municipio || '',
      state: cnpjData.uf || '',
      cep: cnpjData.cep ? cnpjData.cep.replace(/(\d{5})(\d{3})/, '$1-$2') : '',
      phone: cnpjData.telefone || prev.phone,
      email: cnpjData.email || prev.email
    }));

    setShowCNPJData(false);
    
    toast({
      title: 'Dados preenchidos!',
      description: 'Informações da empresa foram preenchidas automaticamente.',
    });
  };

  const handlePhoneChange = (field: string, value: string) => {
    const maskedValue = cnpjService.applyPhoneMask(value);
    handleInputChange(field, maskedValue);
  };

  const handleCEPChange = (value: string) => {
    const maskedValue = cnpjService.applyCEPMask(value);
    handleInputChange('cep', maskedValue);
  };

  const validateForm = () => {
    const errors: string[] = [];

    if (!formData.name.trim()) errors.push('Nome é obrigatório');
    if (!formData.email.trim()) errors.push('Email é obrigatório');
    if (!formData.phone.trim()) errors.push('Telefone é obrigatório');

    // Validação de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (formData.email && !emailRegex.test(formData.email)) {
      errors.push('Email inválido');
    }

    // Validação de telefone (formato brasileiro)
    const phoneRegex = /^\(\d{2}\)\s\d{4,5}-\d{4}$|^\d{10,11}$/;
    if (formData.phone && !phoneRegex.test(formData.phone.replace(/\D/g, ''))) {
      errors.push('Telefone inválido');
    }

    // Validação de CNPJ/CPF
    if (formData.cnpj_cpf) {
      const numbers = formData.cnpj_cpf.replace(/\D/g, '');
      if (numbers.length !== 11 && numbers.length !== 14) {
        errors.push('CNPJ/CPF inválido');
      }
    }

    // Validação de CEP
    if (formData.cep) {
      const cepNumbers = formData.cep.replace(/\D/g, '');
      if (cepNumbers.length !== 8) {
        errors.push('CEP inválido');
      }
    }

    if (errors.length > 0) {
      toast({
        title: 'Erro de validação',
        description: errors.join(', '),
        variant: 'destructive',
      });
      return false;
    }

    return true;
  };

  const handleSubmit = async () => {
    if (!validateForm() || !currentTenant) return;

    setIsLoading(true);
    try {
      const leadData: Partial<Lead> = {
        ...formData,
        tags: selectedTags,
        custom_fields: customFields,
        score: calculatedScore,
        tenantId: currentTenant.id,
        updated_at: new Date().toISOString()
      };

      if (lead) {
        await apiService.updateLead(lead.id, leadData, { tenantId: currentTenant.id });
        toast({
          title: 'Lead atualizado',
          description: 'Lead atualizado com sucesso!',
        });
      } else {
        await apiService.createLead(leadData, { tenantId: currentTenant.id });
        toast({
          title: 'Lead criado',
          description: 'Lead criado com sucesso!',
        });
      }

      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error saving lead:', error);
      toast({
        title: 'Erro',
        description: 'Erro ao salvar lead. Tente novamente.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const renderOptionalField = (fieldKey: string) => {
    const config = optionalFieldsConfig[fieldKey as keyof typeof optionalFieldsConfig];
    const value = customFields[fieldKey] || '';

    if (config.type === 'select') {
      return (
        <Select
          value={value}
          onValueChange={(val) => handleCustomFieldChange(fieldKey, val)}
        >
          <SelectTrigger>
            <SelectValue placeholder={`Selecione ${config.label.toLowerCase()}`} />
          </SelectTrigger>
          <SelectContent>
            {config.options?.map((option) => (
              <SelectItem key={option} value={option}>
                {option}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      );
    }

    return (
      <Input
        type={config.type}
        placeholder={config.placeholder}
        value={value}
        onChange={(e) => handleCustomFieldChange(fieldKey, e.target.value)}
      />
    );
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <User className="w-5 h-5" />
            {lead ? 'Editar Lead' : 'Novo Lead'}
          </DialogTitle>
          <DialogDescription>
            Preencha as informações do lead. Campos marcados com * são obrigatórios.
          </DialogDescription>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-8">
            <TabsTrigger value="basic" className="flex items-center gap-1">
              <User className="w-4 h-4" />
              Básico
            </TabsTrigger>
            <TabsTrigger value="company" className="flex items-center gap-1">
              <Building className="w-4 h-4" />
              Empresa
            </TabsTrigger>
            <TabsTrigger value="location" className="flex items-center gap-1">
              <MapPin className="w-4 h-4" />
              Endereço
            </TabsTrigger>
            <TabsTrigger value="advanced" className="flex items-center gap-1">
              <Settings className="w-4 h-4" />
              Avançado
            </TabsTrigger>
            <TabsTrigger value="notes" className="flex items-center gap-1">
              <FileText className="w-4 h-4" />
              Registros
            </TabsTrigger>
            <TabsTrigger value="calls" className="flex items-center gap-1">
              <Phone className="w-4 h-4" />
              Ligações
            </TabsTrigger>
            <TabsTrigger value="smartbot" className="flex items-center gap-1">
              <Bot className="w-4 h-4" />
              Smartbot
            </TabsTrigger>
            <TabsTrigger value="automation" className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              Automação
            </TabsTrigger>
          </TabsList>

          {/* Aba Básico */}
          <TabsContent value="basic" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">Nome Completo *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="Nome completo"
                />
              </div>
              
              <div>
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  placeholder="email@exemplo.com"
                />
              </div>

              <div>
                <Label htmlFor="phone">Telefone *</Label>
                <Input
                  id="phone"
                  value={formData.phone}
                  onChange={(e) => handlePhoneChange('phone', e.target.value)}
                  placeholder="(11) 99999-9999"
                />
              </div>

              <div>
                <Label htmlFor="whatsapp">WhatsApp</Label>
                <Input
                  id="whatsapp"
                  value={formData.whatsapp}
                  onChange={(e) => handlePhoneChange('whatsapp', e.target.value)}
                  placeholder="(11) 99999-9999"
                />
              </div>

              <div>
                <Label htmlFor="source">Origem</Label>
                <Select
                  value={formData.source}
                  onValueChange={(value) => handleInputChange('source', value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {sourceOptions.map((option) => (
                      <SelectItem key={option} value={option}>
                        {option}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="status">Status</Label>
                <Select
                  value={formData.status}
                  onValueChange={(value) => handleInputChange('status', value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {statusOptions.map((option) => (
                      <SelectItem key={option} value={option}>
                        {option}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <Label htmlFor="notes">Observações</Label>
              <Textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="Observações sobre o lead..."
                rows={3}
              />
            </div>
          </TabsContent>

          {/* Aba Empresa */}
          <TabsContent value="company" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="company">Razão Social</Label>
                <Input
                  id="company"
                  value={formData.company}
                  onChange={(e) => handleInputChange('company', e.target.value)}
                  placeholder="Nome da empresa"
                />
              </div>

              <div>
                <Label htmlFor="cnpj_cpf">CNPJ/CPF</Label>
                <div className="relative">
                  <Input
                    id="cnpj_cpf"
                    value={formData.cnpj_cpf}
                    onChange={(e) => handleCNPJChange(e.target.value)}
                    placeholder="00.000.000/0000-00"
                    className="pr-10"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={consultarCNPJ}
                    disabled={isCNPJLoading || !formData.cnpj_cpf}
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 hover:bg-blue-50 hover:text-blue-600 text-gray-500 transition-colors"
                    title="Consultar CNPJ"
                  >
                    {isCNPJLoading ? (
                      <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                    ) : (
                      <Search className="w-5 h-5" />
                    )}
                  </Button>
                </div>
              </div>

              <div>
                <Label htmlFor="ie_rg">IE/RG</Label>
                <Input
                  id="ie_rg"
                  value={formData.ie_rg}
                  onChange={(e) => handleInputChange('ie_rg', e.target.value)}
                  placeholder="Inscrição Estadual ou RG"
                />
              </div>
            </div>

            {/* Dado            {/* Dados do CNPJ Consultado */}
            {showCNPJData && cnpjData && (
              <Card className="mt-4 border-green-200 bg-green-50">
                <CardHeader className="pb-3">
                  <CardTitle className="text-lg text-green-800 flex items-center gap-2">
                    <Building className="w-5 h-5" />
                    Dados da Empresa Encontrados
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div>
                      <strong>Razão Social:</strong> {cnpjData.nome}
                    </div>
                    {cnpjData.fantasia && (
                      <div>
                        <strong>Nome Fantasia:</strong> {cnpjData.fantasia}
                      </div>
                    )}
                    <div>
                      <strong>Situação:</strong> {cnpjData.situacao}
                    </div>
                    <div>
                      <strong>Porte:</strong> {cnpjData.porte}
                    </div>
                    <div className="md:col-span-2">
                      <strong>Atividade Principal:</strong> {cnpjData.atividade_principal[0]?.text}
                    </div>
                    <div className="md:col-span-2">
                      <strong>Endereço:</strong> {cnpjData.logradouro}, {cnpjData.numero} - {cnpjData.bairro}, {cnpjData.municipio}/{cnpjData.uf} - CEP: {cnpjData.cep}
                    </div>
                  </div>
                  <div className="flex gap-2 pt-2">
                    <Button
                      type="button"
                      onClick={preencherDadosCNPJ}
                      className="bg-green-600 hover:bg-green-700"
                    >
                      Preencher Dados Automaticamente
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setShowCNPJData(false)}
                    >
                      Fechar
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Aba Endereço */}
          <TabsContent value="location" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <Label htmlFor="address">Endereço</Label>
                <Input
                  id="address"
                  value={formData.address}
                  onChange={(e) => handleInputChange('address', e.target.value)}
                  placeholder="Rua, Avenida, etc."
                />
              </div>

              <div>
                <Label htmlFor="number">Número</Label>
                <Input
                  id="number"
                  value={formData.number}
                  onChange={(e) => handleInputChange('number', e.target.value)}
                  placeholder="123"
                />
              </div>

              <div>
                <Label htmlFor="neighborhood">Bairro</Label>
                <Input
                  id="neighborhood"
                  value={formData.neighborhood}
                  onChange={(e) => handleInputChange('neighborhood', e.target.value)}
                  placeholder="Nome do bairro"
                />
              </div>

              <div>
                <Label htmlFor="city">Cidade</Label>
                <Input
                  id="city"
                  value={formData.city}
                  onChange={(e) => handleInputChange('city', e.target.value)}
                  placeholder="Nome da cidade"
                />
              </div>

              <div>
                <Label htmlFor="state">Estado</Label>
                <Select
                  value={formData.state}
                  onValueChange={(value) => handleInputChange('state', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="UF" />
                  </SelectTrigger>
                  <SelectContent>
                    {stateOptions.map((option) => (
                      <SelectItem key={option} value={option}>
                        {option}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="cep">CEP</Label>
                <Input
                  id="cep"
                  value={formData.cep}
                  onChange={(e) => handleCEPChange(e.target.value)}
                  placeholder="00000-000"
                />
              </div>
            </div>
          </TabsContent>

          {/* Aba Avançado */}
          <TabsContent value="advanced" className="space-y-6">
            {/* Lead Scoring */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calculator className="w-5 h-5" />
                  Lead Scoring Automático
                </CardTitle>
              </CardHeader>
              <CardContent>
                <LeadScoring score={calculatedScore} showDetails={true} />
              </CardContent>
            </Card>

            {/* Sistema de Tags */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TagIcon className="w-5 h-5" />
                  Tags
                </CardTitle>
              </CardHeader>
              <CardContent>
                <TagSystem
                  tags={availableTags}
                  selectedTags={selectedTags}
                  onTagsChange={setSelectedTags}
                  editable={true}
                />
              </CardContent>
            </Card>

            {/* Campos Opcionais */}
            <Card>
              <CardHeader>
                <CardTitle>Campos Adicionais Opcionais</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(optionalFieldsConfig).map(([fieldKey, config]) => (
                  <div key={fieldKey} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label className="flex items-center gap-2">
                        <Switch
                          checked={enabledOptionalFields[fieldKey]}
                          onCheckedChange={(checked) => toggleOptionalField(fieldKey, checked)}
                        />
                        {config.label}
                      </Label>
                    </div>
                    {enabledOptionalFields[fieldKey] && (
                      <div className="ml-6">
                        {renderOptionalField(fieldKey)}
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* ===== NOVAS ABAS AVANÇADAS ===== */}

          {/* Aba Registros e Notas */}
          <TabsContent value="notes" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Registros e Notas
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Adicionar nova nota */}
                <div className="space-y-2">
                  <Label>Adicionar Nova Nota</Label>
                  <div className="flex gap-2">
                    <Textarea
                      placeholder="Digite sua nota aqui..."
                      value={newNote}
                      onChange={(e) => setNewNote(e.target.value)}
                      className="flex-1"
                    />
                    <Button 
                      onClick={handleAddNote}
                      disabled={isAddingNote || !newNote.trim()}
                      className="self-start"
                    >
                      {isAddingNote ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                    </Button>
                  </div>
                </div>

                {/* Lista de notas */}
                <div className="space-y-2">
                  <Label>Histórico de Notas</Label>
                  <ScrollArea className="h-64 border rounded-md p-4">
                    {leadNotes.length === 0 ? (
                      <p className="text-muted-foreground text-center py-8">
                        Nenhuma nota encontrada
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {leadNotes.map((note, index) => (
                          <div key={index} className="border-b pb-2 last:border-b-0">
                            <div className="flex justify-between items-start mb-1">
                              <span className="text-sm font-medium">{note.author || 'Usuário'}</span>
                              <span className="text-xs text-muted-foreground">
                                {new Date(note.created_at).toLocaleString('pt-BR')}
                              </span>
                            </div>
                            <p className="text-sm">{note.content}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </ScrollArea>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Aba Histórico de Ligações */}
          <TabsContent value="calls" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Phone className="w-5 h-5" />
                  Histórico de Ligações
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Fazer nova ligação */}
                <div className="flex gap-2 items-end">
                  <div className="flex-1">
                    <Label>Ramal</Label>
                    <Select value={selectedExtension} onValueChange={setSelectedExtension}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {availableExtensions.map((ext) => (
                          <SelectItem key={ext.id} value={ext.number}>
                            {ext.number} - {ext.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <Button 
                    onClick={handleMakeCall}
                    disabled={!lead?.phone || !selectedExtension}
                    className="flex items-center gap-2"
                  >
                    <Phone className="w-4 h-4" />
                    Ligar Agora
                  </Button>
                </div>

                {/* Histórico de chamadas */}
                <div className="space-y-2">
                  <Label>Histórico de Chamadas</Label>
                  <ScrollArea className="h-64 border rounded-md p-4">
                    {isLoadingCalls ? (
                      <div className="flex justify-center py-8">
                        <Loader2 className="w-6 h-6 animate-spin" />
                      </div>
                    ) : callHistory.length === 0 ? (
                      <p className="text-muted-foreground text-center py-8">
                        Nenhuma ligação encontrada
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {callHistory.map((call, index) => (
                          <div key={index} className="border-b pb-2 last:border-b-0">
                            <div className="flex justify-between items-start mb-1">
                              <div className="flex items-center gap-2">
                                <Badge variant={call.direction === 'outbound' ? 'default' : 'secondary'}>
                                  {call.direction === 'outbound' ? 'Saída' : 'Entrada'}
                                </Badge>
                                <span className="text-sm font-medium">
                                  {call.direction === 'outbound' ? call.called : call.caller}
                                </span>
                              </div>
                              <span className="text-xs text-muted-foreground">
                                {new Date(call.start_time).toLocaleString('pt-BR')}
                              </span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span>Status: {call.status}</span>
                              {call.duration && (
                                <span>Duração: {pabxService.formatCallDuration(call.duration)}</span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </ScrollArea>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Aba Smartbot */}
          <TabsContent value="smartbot" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bot className="w-5 h-5" />
                  Smartbot - Mensagens Automáticas
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Templates de mensagem */}
                <div className="space-y-2">
                  <Label>Templates de Mensagem</Label>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(smartbotService.getMessageTemplates()).map(([key, template]) => (
                      <Button
                        key={key}
                        variant="outline"
                        size="sm"
                        onClick={() => handleUseMessageTemplate(key)}
                        className="text-left justify-start"
                      >
                        {key.replace('_', ' ').toUpperCase()}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Enviar mensagem */}
                <div className="space-y-2">
                  <Label>Enviar Mensagem</Label>
                  <div className="flex gap-2">
                    <Textarea
                      placeholder="Digite sua mensagem aqui..."
                      value={newSmartbotMessage}
                      onChange={(e) => setNewSmartbotMessage(e.target.value)}
                      className="flex-1"
                    />
                    <Button 
                      onClick={handleSendSmartbotMessage}
                      disabled={isSendingMessage || !newSmartbotMessage.trim() || !lead?.phone}
                      className="self-start"
                    >
                      {isSendingMessage ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                    </Button>
                  </div>
                </div>

                {/* Histórico de mensagens */}
                <div className="space-y-2">
                  <Label>Histórico de Mensagens</Label>
                  <ScrollArea className="h-64 border rounded-md p-4">
                    {smartbotMessages.length === 0 ? (
                      <p className="text-muted-foreground text-center py-8">
                        Nenhuma mensagem encontrada
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {smartbotMessages.map((message, index) => (
                          <div key={index} className="border-b pb-2 last:border-b-0">
                            <div className="flex justify-between items-start mb-1">
                              <Badge variant={message.direction === 'outbound' ? 'default' : 'secondary'}>
                                {message.direction === 'outbound' ? 'Enviada' : 'Recebida'}
                              </Badge>
                              <span className="text-xs text-muted-foreground">
                                {new Date(message.timestamp).toLocaleString('pt-BR')}
                              </span>
                            </div>
                            <p className="text-sm">{message.message}</p>
                            <div className="flex justify-between text-xs text-muted-foreground mt-1">
                              <span>Status: {message.status}</span>
                              <span>Tipo: {message.type}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </ScrollArea>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Aba Automação */}
          <TabsContent value="automation" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  Automação de Tarefas
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Criar nova tarefa */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label>Título da Tarefa</Label>
                    <Input
                      placeholder="Ex: Ligar para follow-up"
                      value={newTaskTitle}
                      onChange={(e) => setNewTaskTitle(e.target.value)}
                    />
                  </div>
                  <div>
                    <Label>Tipo</Label>
                    <Select value={newTaskType} onValueChange={setNewTaskType}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="call">Ligação</SelectItem>
                        <SelectItem value="email">Email</SelectItem>
                        <SelectItem value="whatsapp">WhatsApp</SelectItem>
                        <SelectItem value="meeting">Reunião</SelectItem>
                        <SelectItem value="follow_up">Follow-up</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Data/Hora</Label>
                    <div className="flex gap-2">
                      <Input
                        type="datetime-local"
                        value={newTaskDate}
                        onChange={(e) => setNewTaskDate(e.target.value)}
                        className="flex-1"
                      />
                      <Button 
                        onClick={handleCreateAutomationTask}
                        disabled={isCreatingTask || !newTaskTitle.trim() || !newTaskDate}
                        size="sm"
                      >
                        {isCreatingTask ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Criar'}
                      </Button>
                    </div>
                  </div>
                </div>

                {/* Lista de tarefas */}
                <div className="space-y-2">
                  <Label>Tarefas Agendadas</Label>
                  <ScrollArea className="h-64 border rounded-md p-4">
                    {automationTasks.length === 0 ? (
                      <p className="text-muted-foreground text-center py-8">
                        Nenhuma tarefa agendada
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {automationTasks.map((task, index) => (
                          <div key={index} className="border-b pb-2 last:border-b-0">
                            <div className="flex justify-between items-start mb-1">
                              <span className="text-sm font-medium">{task.title}</span>
                              <Badge variant="outline">{task.type}</Badge>
                            </div>
                            <div className="flex justify-between text-sm text-muted-foreground">
                              <span>Agendado para: {new Date(task.scheduled_date).toLocaleString('pt-BR')}</span>
                              <span>Status: {task.status}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </ScrollArea>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isLoading}>
            Cancelar
          </Button>
          <Button onClick={handleSubmit} disabled={isLoading}>
            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            {lead ? 'Atualizar' : 'Criar'} Lead
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default LeadModal;

