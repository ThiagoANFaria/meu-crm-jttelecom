import React, { useState, useEffect } from 'react';
import { Client } from '@/types';
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

interface ClientModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  client?: Client | null;
}

const ClientModal: React.FC<ClientModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  client,
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
    status: 'ativo',
    notes: '',
  });

  const { toast } = useToast();

  useEffect(() => {
    if (client) {
      setFormData({
        name: client.name || '',
        email: client.email || '',
        phone: client.phone || '',
        whatsapp: client.whatsapp || '',
        company: client.company || '',
        cnpj_cpf: client.cnpj_cpf || '',
        ie_rg: client.ie_rg || '',
        address: client.address || '',
        number: client.number || '',
        neighborhood: client.neighborhood || '',
        city: client.city || '',
        state: client.state || '',
        cep: client.cep || '',
        status: client.status || 'ativo',
        notes: client.notes || '',
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
        status: 'ativo',
        notes: '',
      });
    }
  }, [client, isOpen]);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.phone || !formData.company) {
      toast({
        title: 'Campos obrigatórios',
        description: 'Nome, email, telefone e empresa são obrigatórios.',
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);

    try {
      if (client) {
        await apiService.updateClient(client.id, formData);
        toast({
          title: 'Cliente atualizado',
          description: 'Cliente atualizado com sucesso.',
        });
      } else {
        await apiService.createClient(formData);
        toast({
          title: 'Cliente criado',
          description: 'Cliente criado com sucesso.',
        });
      }
      
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Failed to save client:', error);
      toast({
        title: 'Erro ao salvar',
        description: 'Não foi possível salvar o cliente.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const statusOptions = [
    { value: 'ativo', label: 'Ativo' },
    { value: 'inativo', label: 'Inativo' },
    { value: 'prospecto', label: 'Prospecto' },
    { value: 'suspenso', label: 'Suspenso' },
  ];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {client ? 'Editar Cliente' : 'Novo Cliente'}
          </DialogTitle>
          <DialogDescription>
            {client 
              ? 'Edite as informações do cliente abaixo.' 
              : 'Preencha as informações para criar um novo cliente.'
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
              <Label htmlFor="company">Empresa *</Label>
              <Input
                id="company"
                value={formData.company}
                onChange={(e) => handleInputChange('company', e.target.value)}
                placeholder="Nome da empresa"
                required
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
              placeholder="Observações adicionais sobre o cliente..."
              rows={3}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit" disabled={isLoading} className="bg-jt-blue hover:bg-blue-700">
              {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              {client ? 'Atualizar' : 'Criar'} Cliente
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default ClientModal;

