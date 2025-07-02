import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { Filter, X, Search } from 'lucide-react';
import { Tag } from '@/types';

interface FilterCriteria {
  status?: string[];
  source?: string[];
  responsible?: string[];
  scoreRange?: [number, number];
  city?: string;
  state?: string;
  tags?: string[];
  dateRange?: {
    start: string;
    end: string;
  };
}

interface AdvancedFiltersProps {
  onFiltersChange: (filters: FilterCriteria) => void;
  availableTags: Tag[];
  availableUsers: { id: string; name: string; }[];
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({
  onFiltersChange,
  availableTags,
  availableUsers
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filters, setFilters] = useState<FilterCriteria>({
    scoreRange: [0, 100]
  });
  const [activeFiltersCount, setActiveFiltersCount] = useState(0);

  const statusOptions = [
    'Novo',
    'Em Contato',
    'Qualificado',
    'Proposta Enviada',
    'Em Negociação',
    'Ganho',
    'Perdido'
  ];

  const sourceOptions = [
    'Website',
    'Google Ads',
    'Facebook',
    'Instagram',
    'Indicação',
    'Telefone',
    'Email',
    'Evento',
    'LinkedIn',
    'WhatsApp',
    'Outros'
  ];

  const stateOptions = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
  ];

  const updateFilters = (newFilters: Partial<FilterCriteria>) => {
    const updatedFilters = { ...filters, ...newFilters };
    setFilters(updatedFilters);
    
    // Contar filtros ativos
    let count = 0;
    if (updatedFilters.status?.length) count++;
    if (updatedFilters.source?.length) count++;
    if (updatedFilters.responsible?.length) count++;
    if (updatedFilters.scoreRange && (updatedFilters.scoreRange[0] > 0 || updatedFilters.scoreRange[1] < 100)) count++;
    if (updatedFilters.city) count++;
    if (updatedFilters.state) count++;
    if (updatedFilters.tags?.length) count++;
    if (updatedFilters.dateRange?.start || updatedFilters.dateRange?.end) count++;
    
    setActiveFiltersCount(count);
    onFiltersChange(updatedFilters);
  };

  const clearFilters = () => {
    const clearedFilters: FilterCriteria = { scoreRange: [0, 100] };
    setFilters(clearedFilters);
    setActiveFiltersCount(0);
    onFiltersChange(clearedFilters);
  };

  const handleMultiSelect = (field: keyof FilterCriteria, value: string) => {
    const currentValues = (filters[field] as string[]) || [];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];
    
    updateFilters({ [field]: newValues.length > 0 ? newValues : undefined });
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="relative">
          <Filter className="w-4 h-4 mr-2" />
          Filtros Avançados
          {activeFiltersCount > 0 && (
            <Badge className="ml-2 bg-jt-blue text-white text-xs px-1.5 py-0.5">
              {activeFiltersCount}
            </Badge>
          )}
        </Button>
      </DialogTrigger>
      
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center justify-between">
            <span>Filtros Avançados</span>
            <Button variant="ghost" size="sm" onClick={clearFilters}>
              <X className="w-4 h-4 mr-1" />
              Limpar Filtros
            </Button>
          </DialogTitle>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Status */}
          <div className="space-y-2">
            <Label>Status</Label>
            <div className="flex flex-wrap gap-2">
              {statusOptions.map((status) => (
                <Badge
                  key={status}
                  variant={filters.status?.includes(status) ? "default" : "outline"}
                  className="cursor-pointer"
                  onClick={() => handleMultiSelect('status', status)}
                >
                  {status}
                </Badge>
              ))}
            </div>
          </div>

          {/* Origem */}
          <div className="space-y-2">
            <Label>Origem</Label>
            <div className="flex flex-wrap gap-2">
              {sourceOptions.map((source) => (
                <Badge
                  key={source}
                  variant={filters.source?.includes(source) ? "default" : "outline"}
                  className="cursor-pointer"
                  onClick={() => handleMultiSelect('source', source)}
                >
                  {source}
                </Badge>
              ))}
            </div>
          </div>

          {/* Responsável */}
          <div className="space-y-2">
            <Label>Responsável</Label>
            <div className="flex flex-wrap gap-2">
              {availableUsers.map((user) => (
                <Badge
                  key={user.id}
                  variant={filters.responsible?.includes(user.id) ? "default" : "outline"}
                  className="cursor-pointer"
                  onClick={() => handleMultiSelect('responsible', user.id)}
                >
                  {user.name}
                </Badge>
              ))}
            </div>
          </div>

          {/* Lead Score */}
          <div className="space-y-2">
            <Label>Lead Score: {filters.scoreRange?.[0]} - {filters.scoreRange?.[1]}</Label>
            <Slider
              value={filters.scoreRange || [0, 100]}
              onValueChange={(value) => updateFilters({ scoreRange: value as [number, number] })}
              max={100}
              min={0}
              step={5}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>0 (Gelado)</span>
              <span>50 (Morno)</span>
              <span>100 (Quente)</span>
            </div>
          </div>

          {/* Localização */}
          <div className="space-y-2">
            <Label>Cidade</Label>
            <Input
              placeholder="Digite a cidade"
              value={filters.city || ''}
              onChange={(e) => updateFilters({ city: e.target.value || undefined })}
            />
          </div>

          <div className="space-y-2">
            <Label>Estado</Label>
            <Select
              value={filters.state || ''}
              onValueChange={(value) => updateFilters({ state: value || undefined })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecione o estado" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos os estados</SelectItem>
                {stateOptions.map((state) => (
                  <SelectItem key={state} value={state}>
                    {state}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Tags */}
          <div className="space-y-2 md:col-span-2">
            <Label>Tags</Label>
            <div className="flex flex-wrap gap-2">
              {availableTags.map((tag) => (
                <Badge
                  key={tag.id}
                  variant={filters.tags?.includes(tag.id) ? "default" : "outline"}
                  className="cursor-pointer"
                  style={filters.tags?.includes(tag.id) ? { backgroundColor: tag.color, color: 'white' } : { borderColor: tag.color, color: tag.color }}
                  onClick={() => handleMultiSelect('tags', tag.id)}
                >
                  {tag.name}
                </Badge>
              ))}
            </div>
          </div>

          {/* Período */}
          <div className="space-y-2">
            <Label>Data de Criação - Início</Label>
            <Input
              type="date"
              value={filters.dateRange?.start || ''}
              onChange={(e) => updateFilters({
                dateRange: {
                  ...filters.dateRange,
                  start: e.target.value
                }
              })}
            />
          </div>

          <div className="space-y-2">
            <Label>Data de Criação - Fim</Label>
            <Input
              type="date"
              value={filters.dateRange?.end || ''}
              onChange={(e) => updateFilters({
                dateRange: {
                  ...filters.dateRange,
                  end: e.target.value
                }
              })}
            />
          </div>
        </div>

        <div className="flex justify-end gap-2 mt-6">
          <Button variant="outline" onClick={() => setIsOpen(false)}>
            Fechar
          </Button>
          <Button onClick={() => setIsOpen(false)}>
            <Search className="w-4 h-4 mr-2" />
            Aplicar Filtros
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default AdvancedFilters;

