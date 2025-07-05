import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Shield } from 'lucide-react';

const PermissionsManager: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Permissões</h3>
          <p className="text-sm text-gray-600">
            Configure permissões por perfil de usuário
          </p>
        </div>
        <Button className="bg-orange-600 hover:bg-orange-700">
          <Plus className="w-4 h-4 mr-2" />
          Novo Perfil
        </Button>
      </div>

      <Card>
        <CardContent className="p-8 text-center">
          <Shield className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Sistema de Permissões</h3>
          <p className="text-gray-600 mb-4">
            Defina diferentes níveis de acesso e permissões para cada tipo de usuário.
          </p>
          <Button className="bg-orange-600 hover:bg-orange-700">
            <Plus className="w-4 h-4 mr-2" />
            Configurar Permissões
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default PermissionsManager;

