import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Filter } from 'lucide-react';
import { useTenant } from '@/contexts/TenantContext';

const OriginFieldsManager: React.FC = () => {
  const { currentTenant } = useTenant();

  if (!currentTenant) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Campos por Origem - {currentTenant.name}</h3>
          <p className="text-sm text-gray-600">
            Configure campos específicos por origem do Lead da sua empresa (Instagram, Site, etc.)
          </p>
        </div>
        <Button className="bg-pink-600 hover:bg-pink-700">
          <Plus className="w-4 h-4 mr-2" />
          Nova Origem
        </Button>
      </div>

      <Card>
        <CardContent className="p-8 text-center">
          <Filter className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Campos por Origem Personalizados</h3>
          <p className="text-gray-600 mb-4">
            Defina campos específicos da {currentTenant.name} que aparecem conforme a origem do lead (Instagram, Site, WhatsApp, etc.).
          </p>
          <Button className="bg-pink-600 hover:bg-pink-700">
            <Plus className="w-4 h-4 mr-2" />
            Configurar Primeira Origem para {currentTenant.name}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default OriginFieldsManager;

