import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Workflow } from 'lucide-react';
import { useTenant } from '@/contexts/TenantContext';

const SalesFunnelManager: React.FC = () => {
  const { currentTenant } = useTenant();

  if (!currentTenant) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Funis de Vendas - {currentTenant.name}</h3>
          <p className="text-sm text-gray-600">
            Defina funis e etapas personalizadas para o processo de vendas da sua empresa
          </p>
        </div>
        <Button className="bg-green-600 hover:bg-green-700">
          <Plus className="w-4 h-4 mr-2" />
          Novo Funil
        </Button>
      </div>

      <Card>
        <CardContent className="p-8 text-center">
          <Workflow className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Funis de Vendas Personalizados</h3>
          <p className="text-gray-600 mb-4">
            Configure funis específicos para {currentTenant.name} com diferentes tipos de vendas e processos.
          </p>
          <Button className="bg-green-600 hover:bg-green-700">
            <Plus className="w-4 h-4 mr-2" />
            Criar Primeiro Funil para {currentTenant.name}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default SalesFunnelManager;

