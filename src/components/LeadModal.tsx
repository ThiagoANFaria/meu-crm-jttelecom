import React, { useState, useEffect } from 'react';
import { Lead } from '@/types';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
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
import { Loader2 } from 'lucide-react';

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
    source: '',
    status: 'novo',
    notes: '',
  });

  const { toast } = useToast();

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
        source: lead.source || '',
        status: lead.status || 'novo',
        notes: lead.notes || '',
      });
    } else {
      setFormData({
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
        source: '',
        status: 'novo',
        notes: '',
      });
    }
  }, [lead, isOpen]);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.phone) {
      toast({
        title: 'Campos obrigatórios',
        description: 'Nome, email e telefone são obrigatórios.',
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);

    try {
      if (lead) {
        await apiService.updateLead(lead.id, formData);
        toast({
          title: 'Lead atualizado',
          description: 'Lead atualizado com sucesso.',
        });
      } else {
        await apiService.createLead(formData);
        toast({
          title: 'Lead criado',
          description: 'Lead criado com sucesso.',
        });
      }
      
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Failed to save lead:', error);
      toast({
        title: 'Erro ao salvar',
        description: 'Não foi possível salvar o lead.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const statusOptions = [
    { value: 'novo', label: 'Novo' },
    { value: 'contato', label: 'Em Contato' },
    { value: 'qualificado', label: 'Qualificado' },
    { value: 'proposta', label: 'Proposta Enviada' },
    { value: 'negociacao', label: 'Em Negociação' },
    { value: 'ganho', label: 'Ganho' },
    { value: 'perdido', label: 'Perdido' },
  ];

  const sourceOptions = [
    { value: 'website', label: 'Website' },
    { value: 'google', label: 'Google Ads' },
    { value: 'facebook', label: 'Facebook' },
    { value: 'instagram', label: 'Instagram' },
    { value: 'indicacao', label: 'Indicação' },
    { value: 'telefone', label: 'Telefone' },
    { value: 'email', label: 'Email' },
    { value: 'evento', label: 'Evento' },
    { value: 'outros', label: 'Outros' },
  ];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {lead ? 'Editar Lead' : 'Novo Lead'}
          </DialogTitle>
          <DialogDescription>
            {lead 
              ? 'Edite as informações do lead abaixo.' 
              : 'Preencha as informações para criar um novo lead.'
            }
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Campos obrigatórios */}
            <div className="space-y-2">
              <Label htmlFor="name">Nome *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                placeholder="Nome completo"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email *</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="email@exemplo.com"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone">Telefone *</Label>
              <Input
                id="phone"
                value={formData.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                placeholder="(11) 99999-9999"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="whatsapp">WhatsApp</Label>
              <Input
                id="whatsapp"
                value={formData.whatsapp}
                onChange={(e) => handleInputChange('whatsapp', e.target.value)}
                placeholder="(11) 99999-9999"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="company">Razão Social</Label>
              <Input
                id="company"
                value={formData.company}
                onChange={(e) => handleInputChange('company', e.target.value)}
                placeholder="Nome da empresa"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="cnpj_cpf">CNPJ/CPF</Label>
              <Input
                id="cnpj_cpf"
                value={formData.cnpj_cpf}
                onChange={(e) => handleInputChange('cnpj_cpf', e.target.value)}
                placeholder="00.000.000/0000-00"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="ie_rg">IE/RG</Label>
              <Input
                id="ie_rg"
                value={formData.ie_rg}
                onChange={(e) => handleInputChange('ie_rg', e.target.value)}
                placeholder="Inscrição Estadual ou RG"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="source">Origem</Label>
              <Select value={formData.source} onValueChange={(value) => handleInputChange('source', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione a origem" />
                </SelectTrigger>
                <SelectContent>
                  {sourceOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select value={formData.status} onValueChange={(value) => handleInputChange('status', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o status" />
                </SelectTrigger>
                <SelectContent>
                  {statusOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Endereço */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Endereço</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="address">Endereço</Label>
                <Input
                  id="address"
                  value={formData.address}
                  onChange={(e) => handleInputChange('address', e.target.value)}
                  placeholder="Rua, Avenida, etc."
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="number">Número</Label>
                <Input
                  id="number"
                  value={formData.number}
                  onChange={(e) => handleInputChange('number', e.target.value)}
                  placeholder="123"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="neighborhood">Bairro</Label>
                <Input
                  id="neighborhood"
                  value={formData.neighborhood}
                  onChange={(e) => handleInputChange('neighborhood', e.target.value)}
                  placeholder="Nome do bairro"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="city">Cidade</Label>
                <Input
                  id="city"
                  value={formData.city}
                  onChange={(e) => handleInputChange('city', e.target.value)}
                  placeholder="Nome da cidade"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="state">Estado</Label>
                <Input
                  id="state"
                  value={formData.state}
                  onChange={(e) => handleInputChange('state', e.target.value)}
                  placeholder="SP"
                  maxLength={2}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="cep">CEP</Label>
                <Input
                  id="cep"
                  value={formData.cep}
                  onChange={(e) => handleInputChange('cep', e.target.value)}
                  placeholder="00000-000"
                />
              </div>
            </div>
          </div>

          {/* Observações */}
          <div className="space-y-2">
            <Label htmlFor="notes">Observações</Label>
            <Textarea
              id="notes"
              value={formData.notes}
              onChange={(e) => handleInputChange('notes', e.target.value)}
              placeholder="Observações adicionais sobre o lead..."
              rows={3}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit" disabled={isLoading} className="bg-jt-blue hover:bg-blue-700">
              {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              {lead ? 'Atualizar' : 'Criar'} Lead
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default LeadModal;

