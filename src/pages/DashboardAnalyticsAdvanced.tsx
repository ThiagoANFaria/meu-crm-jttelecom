import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  Users,
  Target,
  DollarSign,
  Activity,
  BarChart3,
  PieChart as PieChartIcon,
  Filter,
  Calendar,
  Download,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  Clock,
  Zap
} from 'lucide-react';
import { advancedAnalyticsService } from '@/services/analyticsAdvanced';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';

interface AnalyticsData {
  overview: {
    totalLeads: number;
    conversionRate: number;
    avgDealValue: number;
    revenue: number;
    growth: number;
  };
  leadMetrics: {
    conversionByFunnel: Array<{
      stage: string;
      leads: number;
      converted: number;
      rate: number;
    }>;
    successRateByUser: Array<{
      user: string;
      leads: number;
      converted: number;
      rate: number;
    }>;
  };
  volumeAnalysis: {
    byStage: Array<{
      stage: string;
      count: number;
      avgTime: number;
      bottleneck: boolean;
    }>;
    timeline: Array<{
      date: string;
      novo: number;
      contato: number;
      qualificado: number;
      proposta: number;
      fechado: number;
    }>;
  };
  revenueProjection: {
    monthly: Array<{
      month: string;
      actual: number;
      projected: number;
      target: number;
    }>;
    trends: Array<{
      period: string;
      value: number;
      growth: number;
    }>;
  };
}

const DashboardAnalyticsAdvanced: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('30d');
  const [selectedMetric, setSelectedMetric] = useState('conversion');
  const { toast } = useToast();
  const { currentTenant } = useTenant();

  useEffect(() => {
    fetchAnalyticsData();
  }, [selectedPeriod, currentTenant]);

  const fetchAnalyticsData = async () => {
    if (!currentTenant) return;

    try {
      setIsLoading(true);
      const analyticsData = await advancedAnalyticsService.getAdvancedMetrics(selectedPeriod, { tenantId: currentTenant.id });
      setData(analyticsData);
    } catch (error) {
      console.error('Failed to fetch analytics data:', error);
      // Usar dados mock específicos do tenant para demonstração
      setData(getMockAnalyticsData());
      toast({
        title: 'Modo Demonstração',
        description: `Exibindo dados de exemplo para ${currentTenant.name}. API em desenvolvimento.`,
        variant: 'default',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getMockAnalyticsData = (): AnalyticsData => {
    // Dados específicos por tenant
    const tenantMultiplier = currentTenant?.id === 'jt-telecom' ? 3 : 1;
    
    return {
      overview: {
        totalLeads: Math.floor(156 * tenantMultiplier),
        conversionRate: 24.5,
        avgDealValue: Math.floor(8500 * tenantMultiplier),
        revenue: Math.floor(125000 * tenantMultiplier),
        growth: 15.3
      },
      leadMetrics: {
        conversionByFunnel: [
          { stage: 'Novo', leads: Math.floor(156 * tenantMultiplier), converted: Math.floor(124 * tenantMultiplier), rate: 79.5 },
          { stage: 'Contato', leads: Math.floor(124 * tenantMultiplier), converted: Math.floor(89 * tenantMultiplier), rate: 71.8 },
          { stage: 'Qualificado', leads: Math.floor(89 * tenantMultiplier), converted: Math.floor(67 * tenantMultiplier), rate: 75.3 },
          { stage: 'Proposta', leads: Math.floor(67 * tenantMultiplier), converted: Math.floor(45 * tenantMultiplier), rate: 67.2 },
          { stage: 'Fechado', leads: Math.floor(45 * tenantMultiplier), converted: Math.floor(38 * tenantMultiplier), rate: 84.4 }
        ],
        successRateByUser: [
          { user: 'Ana Silva', leads: Math.floor(45 * tenantMultiplier), converted: Math.floor(18 * tenantMultiplier), rate: 40.0 },
          { user: 'Carlos Santos', leads: Math.floor(38 * tenantMultiplier), converted: Math.floor(12 * tenantMultiplier), rate: 31.6 },
          { user: 'Maria Oliveira', leads: Math.floor(42 * tenantMultiplier), converted: Math.floor(15 * tenantMultiplier), rate: 35.7 },
          { user: 'João Costa', leads: Math.floor(31 * tenantMultiplier), converted: Math.floor(8 * tenantMultiplier), rate: 25.8 }
        ]
      },
      volumeAnalysis: {
        byStage: [
          { stage: 'Novo', count: Math.floor(45 * tenantMultiplier), avgTime: 2.3, bottleneck: false },
          { stage: 'Contato', count: Math.floor(67 * tenantMultiplier), avgTime: 5.8, bottleneck: true },
          { stage: 'Qualificado', count: Math.floor(34 * tenantMultiplier), avgTime: 3.2, bottleneck: false },
          { stage: 'Proposta', count: Math.floor(23 * tenantMultiplier), avgTime: 7.1, bottleneck: true },
          { stage: 'Fechado', count: Math.floor(12 * tenantMultiplier), avgTime: 1.5, bottleneck: false }
        ],
        timeline: [
          { date: '2025-01', novo: Math.floor(45 * tenantMultiplier), contato: Math.floor(38 * tenantMultiplier), qualificado: Math.floor(29 * tenantMultiplier), proposta: Math.floor(18 * tenantMultiplier), fechado: Math.floor(12 * tenantMultiplier) },
          { date: '2025-02', novo: Math.floor(52 * tenantMultiplier), contato: Math.floor(42 * tenantMultiplier), qualificado: Math.floor(34 * tenantMultiplier), proposta: Math.floor(22 * tenantMultiplier), fechado: Math.floor(15 * tenantMultiplier) },
          { date: '2025-03', novo: Math.floor(48 * tenantMultiplier), contato: Math.floor(45 * tenantMultiplier), qualificado: Math.floor(38 * tenantMultiplier), proposta: Math.floor(25 * tenantMultiplier), fechado: Math.floor(18 * tenantMultiplier) },
          { date: '2025-04', novo: Math.floor(61 * tenantMultiplier), contato: Math.floor(51 * tenantMultiplier), qualificado: Math.floor(42 * tenantMultiplier), proposta: Math.floor(28 * tenantMultiplier), fechado: Math.floor(21 * tenantMultiplier) },
          { date: '2025-05', novo: Math.floor(58 * tenantMultiplier), contato: Math.floor(48 * tenantMultiplier), qualificado: Math.floor(39 * tenantMultiplier), proposta: Math.floor(31 * tenantMultiplier), fechado: Math.floor(24 * tenantMultiplier) },
          { date: '2025-06', novo: Math.floor(67 * tenantMultiplier), contato: Math.floor(55 * tenantMultiplier), qualificado: Math.floor(45 * tenantMultiplier), proposta: Math.floor(34 * tenantMultiplier), fechado: Math.floor(28 * tenantMultiplier) }
        ]
      },
      revenueProjection: {
        monthly: [
          { month: 'Jan', actual: Math.floor(85000 * tenantMultiplier), projected: Math.floor(90000 * tenantMultiplier), target: Math.floor(100000 * tenantMultiplier) },
          { month: 'Fev', actual: Math.floor(92000 * tenantMultiplier), projected: Math.floor(95000 * tenantMultiplier), target: Math.floor(100000 * tenantMultiplier) },
          { month: 'Mar', actual: Math.floor(88000 * tenantMultiplier), projected: Math.floor(98000 * tenantMultiplier), target: Math.floor(100000 * tenantMultiplier) },
          { month: 'Abr', actual: Math.floor(105000 * tenantMultiplier), projected: Math.floor(102000 * tenantMultiplier), target: Math.floor(100000 * tenantMultiplier) },
          { month: 'Mai', actual: Math.floor(98000 * tenantMultiplier), projected: Math.floor(105000 * tenantMultiplier), target: Math.floor(100000 * tenantMultiplier) },
          { month: 'Jun', actual: Math.floor(125000 * tenantMultiplier), projected: Math.floor(110000 * tenantMultiplier), target: Math.floor(100000 * tenantMultiplier) }
        ],
        trends: [
          { period: 'Q1 2025', value: Math.floor(265000 * tenantMultiplier), growth: 12.5 },
          { period: 'Q2 2025', value: Math.floor(328000 * tenantMultiplier), growth: 23.8 },
          { period: 'Q3 2025', value: Math.floor(385000 * tenantMultiplier), growth: 17.4 },
          { period: 'Q4 2025', value: Math.floor(420000 * tenantMultiplier), growth: 9.1 }
        ]
      }
    };
  };

  const COLORS = ['#4169E1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  if (isLoading || !data) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-blue-600">Analytics Avançado</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Card key={i}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="h-4 bg-gray-200 rounded w-24 animate-pulse"></div>
                <div className="h-4 w-4 bg-gray-200 rounded animate-pulse"></div>
              </CardHeader>
              <CardContent>
                <div className="h-8 bg-gray-200 rounded w-16 animate-pulse mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-32 animate-pulse"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-blue-600">Analytics Avançado</h1>
          <p className="text-gray-600 mt-1">Análise detalhada de performance - {currentTenant?.name}</p>
        </div>
        <div className="flex gap-2">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">7 dias</SelectItem>
              <SelectItem value="30d">30 dias</SelectItem>
              <SelectItem value="90d">90 dias</SelectItem>
              <SelectItem value="1y">1 ano</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" onClick={fetchAnalyticsData}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </div>
      </div>

      {/* Cards de Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.overview.totalLeads}</div>
            <p className="text-xs text-muted-foreground">
              +{data.overview.growth}% vs período anterior
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Conversão</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatPercentage(data.overview.conversionRate)}</div>
            <p className="text-xs text-muted-foreground">
              Meta: 25%
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ticket Médio</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(data.overview.avgDealValue)}</div>
            <p className="text-xs text-muted-foreground">
              Por lead convertido
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Receita Total</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(data.overview.revenue)}</div>
            <p className="text-xs text-muted-foreground">
              No período selecionado
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Crescimento</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">+{formatPercentage(data.overview.growth)}</div>
            <p className="text-xs text-muted-foreground">
              Vs período anterior
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs com Analytics Detalhados */}
      <Tabs defaultValue="conversion" className="space-y-4">
        <TabsList>
          <TabsTrigger value="conversion">Conversão</TabsTrigger>
          <TabsTrigger value="volume">Volume</TabsTrigger>
          <TabsTrigger value="revenue">Receita</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="conversion" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Conversão por Funil</CardTitle>
                <CardDescription>Taxa de conversão em cada etapa</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.leadMetrics.conversionByFunnel}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="stage" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="rate" fill="#4169E1" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Performance por Usuário</CardTitle>
                <CardDescription>Taxa de sucesso individual</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.leadMetrics.successRateByUser}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="user" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="rate" fill="#10B981" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="volume" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Volume por Etapa</CardTitle>
                <CardDescription>Distribuição de leads no funil</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={data.volumeAnalysis.byStage}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ stage, count }) => `${stage}: ${count}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="count"
                    >
                      {data.volumeAnalysis.byStage.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Evolução Temporal</CardTitle>
                <CardDescription>Leads por etapa ao longo do tempo</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={data.volumeAnalysis.timeline}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="novo" stackId="1" stroke="#4169E1" fill="#4169E1" />
                    <Area type="monotone" dataKey="contato" stackId="1" stroke="#10B981" fill="#10B981" />
                    <Area type="monotone" dataKey="qualificado" stackId="1" stroke="#F59E0B" fill="#F59E0B" />
                    <Area type="monotone" dataKey="proposta" stackId="1" stroke="#EF4444" fill="#EF4444" />
                    <Area type="monotone" dataKey="fechado" stackId="1" stroke="#8B5CF6" fill="#8B5CF6" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="revenue" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Receita Mensal</CardTitle>
                <CardDescription>Real vs Projetado vs Meta</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={data.revenueProjection.monthly}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => formatCurrency(Number(value))} />
                    <Legend />
                    <Line type="monotone" dataKey="actual" stroke="#4169E1" name="Real" />
                    <Line type="monotone" dataKey="projected" stroke="#10B981" name="Projetado" />
                    <Line type="monotone" dataKey="target" stroke="#EF4444" name="Meta" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Tendências Trimestrais</CardTitle>
                <CardDescription>Crescimento por trimestre</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.revenueProjection.trends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="period" />
                    <YAxis />
                    <Tooltip formatter={(value) => formatCurrency(Number(value))} />
                    <Bar dataKey="value" fill="#4169E1" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            {data.volumeAnalysis.byStage.map((stage, index) => (
              <Card key={stage.stage}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">{stage.stage}</CardTitle>
                  {stage.bottleneck ? (
                    <AlertTriangle className="h-4 w-4 text-red-500" />
                  ) : (
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  )}
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stage.count}</div>
                  <p className="text-xs text-muted-foreground">
                    Tempo médio: {stage.avgTime} dias
                  </p>
                  {stage.bottleneck && (
                    <Badge variant="destructive" className="mt-2">
                      Gargalo
                    </Badge>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DashboardAnalyticsAdvanced;

