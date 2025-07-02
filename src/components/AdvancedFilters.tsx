import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { X, Filter } from 'lucide-react';

interface AdvancedFiltersProps {
  isOpen: boolean;
  onClose: () => void;
  onApplyFilters: (filters: any) => void;
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({ isOpen, onClose, onApplyFilters }) => {
  const [filters, setFilters] = useState({
    status: '',
    source: '',
    responsible: '',
    scoreRange: [0, 100],
    city: '',
    state: '',
    tags: [] as string[],
    dateFrom: '',
    dateTo: ''
  });

  const statusOptions = [
    'Novo', 'Em Contato', 'Qualificado', 'Proposta Enviada', 
    'Negociação', 'Fechado', 'Perdido'
  ];

  const sourceOptions = [
    'Website', 'Google Ads', 'Facebook', 'LinkedIn', 'Instagram',
    'Indicação', 'Telefone', 'Email', 'WhatsApp', 'Outros'
  ];

  const tagOptions = [
    'VIP', 'Urgente', 'Qualificado', 'Follow-up', 'Orçamento Alto'
  ];

  const handleApplyFilters = () => {
    onApplyFilters(filters);
    onClose();
  };

  const handleClearFilters = () => {
    setFilters({
      status: '',
      source: '',
      responsible: '',
      scoreRange: [0, 100],
      city: '',
      state: '',
      tags: [],
      dateFrom: '',
      dateTo: ''
    });
  };

  const handleTagToggle = (tag: string) => {
    setFilters(prev => ({
      ...prev,
      tags: prev.tags.includes(tag) 
        ? prev.tags.filter(t => t !== tag)
        : [...prev.tags, tag]
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Filter className="h-5 w-5 text-blue-600" />
            <h2 className="text-xl font-semibold">Filtros Avançados</h2>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Status */}
          <div className="space-y-2">
            <Label>Status</Label>
            <Select value={filters.status} onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione o status" />
              </SelectTrigger>
              <SelectContent>
                {statusOptions.map(status => (
                  <SelectItem key={status} value={status}>{status}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Origem */}
          <div className="space-y-2">
            <Label>Origem</Label>
            <Select value={filters.source} onValueChange={(value) => setFilters(prev => ({ ...prev, source: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione a origem" />
              </SelectTrigger>
              <SelectContent>
                {sourceOptions.map(source => (
                  <SelectItem key={source} value={source}>{source}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Responsável */}
          <div className="space-y-2">
            <Label>Responsável</Label>
            <Input
              placeholder="Nome do responsável"
              value={filters.responsible}
              onChange={(e) => setFilters(prev => ({ ...prev, responsible: e.target.value }))}
            />
          </div>

          {/* Cidade */}
          <div className="space-y-2">
            <Label>Cidade</Label>
            <Input
              placeholder="Nome da cidade"
              value={filters.city}
              onChange={(e) => setFilters(prev => ({ ...prev, city: e.target.value }))}
            />
          </div>

          {/* Estado */}
          <div className="space-y-2">
            <Label>Estado</Label>
            <Input
              placeholder="UF do estado"
              value={filters.state}
              onChange={(e) => setFilters(prev => ({ ...prev, state: e.target.value }))}
            />
          </div>

          {/* Data Inicial */}
          <div className="space-y-2">
            <Label>Data Inicial</Label>
            <Input
              type="date"
              value={filters.dateFrom}
              onChange={(e) => setFilters(prev => ({ ...prev, dateFrom: e.target.value }))}
            />
          </div>

          {/* Data Final */}
          <div className="space-y-2">
            <Label>Data Final</Label>
            <Input
              type="date"
              value={filters.dateTo}
              onChange={(e) => setFilters(prev => ({ ...prev, dateTo: e.target.value }))}
            />
          </div>
        </div>

        {/* Score Range */}
        <div className="mt-6 space-y-2">
          <Label>Faixa de Score: {filters.scoreRange[0]} - {filters.scoreRange[1]}</Label>
          <Slider
            value={filters.scoreRange}
            onValueChange={(value) => setFilters(prev => ({ ...prev, scoreRange: value }))}
            max={100}
            min={0}
            step={1}
            className="w-full"
          />
        </div>

        {/* Tags */}
        <div className="mt-6 space-y-2">
          <Label>Tags</Label>
          <div className="flex flex-wrap gap-2">
            {tagOptions.map(tag => (
              <Badge
                key={tag}
                variant={filters.tags.includes(tag) ? "default" : "outline"}
                className="cursor-pointer"
                onClick={() => handleTagToggle(tag)}
              >
                {tag}
              </Badge>
            ))}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-between mt-8">
          <Button variant="outline" onClick={handleClearFilters}>
            Limpar Filtros
          </Button>
          <div className="flex gap-2">
            <Button variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button onClick={handleApplyFilters}>
              Aplicar Filtros
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedFilters;

