import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Tags } from 'lucide-react';

const TagsManager: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Gestão de Tags</h3>
          <p className="text-sm text-gray-600">
            Crie e controle tags com cores personalizáveis
          </p>
        </div>
        <Button className="bg-purple-600 hover:bg-purple-700">
          <Plus className="w-4 h-4 mr-2" />
          Nova Tag
        </Button>
      </div>

      <Card>
        <CardContent className="p-8 text-center">
          <Tags className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Sistema de Tags</h3>
          <p className="text-gray-600 mb-4">
            Organize leads e clientes com tags coloridas e categorizadas.
          </p>
          <Button className="bg-purple-600 hover:bg-purple-700">
            <Plus className="w-4 h-4 mr-2" />
            Criar Primeira Tag
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default TagsManager;

