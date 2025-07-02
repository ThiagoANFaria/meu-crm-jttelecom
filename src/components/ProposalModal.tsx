import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useToast } from '@/hooks/use-toast';
import { Proposal, Client } from '@/types';
import { apiService } from '@/services/api';

interface ProposalModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  proposal?: Proposal | null;
}

const ProposalModal: React.FC<ProposalModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  proposal,
}) => {
  const { toast } = useToast();
  const [clients, setClients] = useState<Client[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const [formData, setFormData] = useState({
    title: '',
    client_id: '',
    description: '',
    amount: '',
    discount: '',
    status: 'Rascunho',
    valid_until: '',
    template_id: '',
    notes: '',
  });

  useEffect(() => {
    if (proposal) {
      setFormData({
        title: proposal.title || '',
        client_id: proposal.client_id || '',
        description: proposal.description || '',
        amount: proposal.amount?.toString() || '',
        discount: proposal.discount?.toString() || '',
        status: proposal.status || 'Rascunho',
        valid_until: proposal.valid_until ? proposal.valid_until.split('T')[0] : '',
        template_id: proposal.template_id || '',
        notes: proposal.notes || '',
      });
    } else {
      setFormData({
        title: '',
        client_id: '',
        description: '',
        amount: '',
        discount: '',
        status: 'Rascunho',
        valid_until: '',
        template_id: '',
        notes: '',
      });
    }
  }, [proposal]);

  useEffect(() => {
    if (isOpen) {
      fetchClients();
    }
  }, [isOpen]);

  const fetchClients = async () => {
    try {
      const response = await apiService.getClients();
      setClients(response);
    } catch (error) {
      console.error('Failed to fetch clients:', error);
      // Usar dados mock em caso de erro
      setClients([
        { id: '1', name: 'Cliente Teste 1', email: 'cliente1@teste.com', phone: '11999999999', company: 'Empresa 1', status: 'Ativo', created_at: new Date().toISOString() },
        { id: '2', name: 'Cliente Teste 2', email: 'cliente2@teste.com', phone: '11888888888', company: 'Empresa 2', status: 'Ativo', created_at: new Date().toISOString() }
      ]);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const calculateTotal = () => {
    const amount = parseFloat(formData.amount) || 0;
    const discount = parseFloat(formData.discount) || 0;
    return amount - discount;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title || !formData.client_id || !formData.amount) {
      toast({
        title: 'Campos obrigatórios',
        description: 'Por favor, preencha todos os campos obrigatórios.',
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);

    try {
      const proposalData = {
        ...formData,
        amount: parseFloat(formData.amount),
        discount: parseFloat(formData.discount) || 0,
        total_amount: calculateTotal(),
      };

      if (proposal) {
        await apiService.updateProposal(proposal.id, proposalData);
        toast({
          title: 'Proposta atualizada',
          description: 'Proposta atualizada com sucesso.',
        });
      } else {
        await apiService.createProposal(proposalData);
        toast({
          title: 'Proposta criada',
          description: 'Proposta criada com sucesso.',
        });
      }

      onSuccess();
      onClose();
    } catch (error) {
      console.error('Failed to save proposal:', error);
      toast({
        title: 'Erro ao salvar',
        description: 'Não foi possível salvar a proposta.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const statusOptions = [
    'Rascunho',
    'Enviada',
    'Em Análise',
    'Aprovada',
    'Rejeitada',
    'Expirada',
  ];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {proposal ? 'Editar Proposta' : 'Nova Proposta'}
          </DialogTitle>
          <DialogDescription>
            Preencha as informações para {proposal ? 'atualizar' : 'criar'} uma proposta.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Título */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="title">Título *</Label>
              <Input
                id="title"
                placeholder="Título da proposta"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                required
              />
            </div>

            <div>
              <Label htmlFor="status">Status</Label>
              <Select value={formData.status} onValueChange={(value) => handleInputChange('status', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o status" />
                </SelectTrigger>
                <SelectContent>
                  {statusOptions.map((status) => (
                    <SelectItem key={status} value={status}>
                      {status}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Cliente */}
          <div>
            <Label htmlFor="client_id">Cliente *</Label>
            <Select value={formData.client_id} onValueChange={(value) => handleInputChange('client_id', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione um cliente" />
              </SelectTrigger>
              <SelectContent>
                {clients.map((client) => (
                  <SelectItem key={client.id} value={client.id}>
                    {client.name} - {client.email}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Descrição */}
          <div>
            <Label htmlFor="description">Descrição</Label>
            <Textarea
              id="description"
              placeholder="Descrição da proposta..."
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              rows={3}
            />
          </div>

          {/* Template */}
          <div>
            <Label htmlFor="template_id">Template</Label>
            <Select value={formData.template_id} onValueChange={(value) => handleInputChange('template_id', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione um template (opcional)" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Sem template</SelectItem>
                <SelectItem value="default">Template Padrão</SelectItem>
                <SelectItem value="pabx">Template PABX</SelectItem>
                <SelectItem value="chatbot">Template Chatbot</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Valores */}
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label htmlFor="amount">Valor *</Label>
              <Input
                id="amount"
                type="number"
                step="0.01"
                placeholder="0,00"
                value={formData.amount}
                onChange={(e) => handleInputChange('amount', e.target.value)}
                required
              />
            </div>

            <div>
              <Label htmlFor="discount">Desconto</Label>
              <Input
                id="discount"
                type="number"
                step="0.01"
                placeholder="0,00"
                value={formData.discount}
                onChange={(e) => handleInputChange('discount', e.target.value)}
              />
            </div>

            <div>
              <Label htmlFor="total">Total</Label>
              <Input
                id="total"
                value={`R$ ${calculateTotal().toFixed(2).replace('.', ',')}`}
                disabled
                className="bg-gray-50"
              />
            </div>
          </div>

          {/* Data de Validade */}
          <div>
            <Label htmlFor="valid_until">Válida até</Label>
            <Input
              id="valid_until"
              type="date"
              value={formData.valid_until}
              onChange={(e) => handleInputChange('valid_until', e.target.value)}
            />
          </div>

          {/* Observações */}
          <div>
            <Label htmlFor="notes">Observações</Label>
            <Textarea
              id="notes"
              placeholder="Observações adicionais..."
              value={formData.notes}
              onChange={(e) => handleInputChange('notes', e.target.value)}
              rows={2}
            />
          </div>
        </form>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancelar
          </Button>
          <Button type="submit" onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? 'Salvando...' : proposal ? 'Atualizar Proposta' : 'Criar Proposta'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ProposalModal;

