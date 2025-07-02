import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, Users, FileText, FileCheck, DollarSign, Target } from 'lucide-react';

const DashboardSimple: React.FC = () => {
  // Dados mockados para teste
  const mockSummary = {
    totalLeads: 25,
    totalClients: 12,
    totalProposals: 8,
    totalContracts: 5,
    monthlyRevenue: 15000,
    conversionRate: 48
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-jt-blue">Dashboard</h1>
        <p className="text-gray-600">Bem-vindo ao CRM JT Telecom</p>
      </div>

      {/* Mensagem de Status */}
      <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
        <h2 className="font-bold">✅ Dashboard Funcionando!</h2>
        <p>Sistema carregado com dados de exemplo. API será conectada em breve.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockSummary.totalLeads}</div>
            <p className="text-xs text-muted-foreground">Leads ativos no sistema</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Clientes</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockSummary.totalClients}</div>
            <p className="text-xs text-muted-foreground">Clientes cadastrados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Propostas</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockSummary.totalProposals}</div>
            <p className="text-xs text-muted-foreground">Propostas em andamento</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Contratos</CardTitle>
            <FileCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockSummary.totalContracts}</div>
            <p className="text-xs text-muted-foreground">Contratos ativos</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Receita do Mês</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              R$ {mockSummary.monthlyRevenue.toLocaleString('pt-BR')}
            </div>
            <p className="text-xs text-muted-foreground">Faturamento atual</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Conversão</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{mockSummary.conversionRate}%</div>
            <p className="text-xs text-muted-foreground">Leads para clientes</p>
          </CardContent>
        </Card>
      </div>

      {/* Resumo Geral */}
      <Card>
        <CardHeader>
          <CardTitle>Resumo Geral</CardTitle>
          <CardDescription>Visão geral do desempenho do seu CRM</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-medium text-blue-900">Performance Geral</h3>
              <p className="text-blue-700 mt-1">
                Seu CRM está funcionando bem! Continue acompanhando os indicadores para manter o
                crescimento.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border border-gray-200 p-4 rounded-lg">
                <h4 className="font-medium text-gray-900">📈 Próximas Ações</h4>
                <ul className="text-sm text-gray-600 mt-2 space-y-1">
                  <li>• Conectar com API real</li>
                  <li>• Implementar gráficos dinâmicos</li>
                  <li>• Adicionar filtros por período</li>
                </ul>
              </div>
              
              <div className="border border-gray-200 p-4 rounded-lg">
                <h4 className="font-medium text-gray-900">🎯 Metas</h4>
                <ul className="text-sm text-gray-600 mt-2 space-y-1">
                  <li>• Aumentar conversão para 60%</li>
                  <li>• Alcançar 50 leads/mês</li>
                  <li>• Faturar R$ 25.000/mês</li>
                </ul>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardSimple;

