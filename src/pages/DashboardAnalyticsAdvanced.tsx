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
  Area,
  FunnelChart,
  Funnel,
  LabelList
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

  useEffect(() => {
    fetchAnalyticsData();
  }, [selectedPeriod]);

  const fetchAnalyticsData = async () => {
    try {
      setIsLoading(true);
      const analyticsData = await advancedAnalyticsService.getAdvancedMetrics(selectedPeriod);
      setData(analyticsData);
    } catch (error) {
      console.error('Failed to fetch analytics data:', error);
      // Usar dados mock para demonstração
      setData(getMockAnalyticsData());
      toast({
        title: 'Modo Demonstração',
        description: 'Exibindo dados de exemplo. API em desenvolvimento.',
        variant: 'default',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getMockAnalyticsData = (): AnalyticsData => ({
    overview: {
      totalLeads: 156,
      conversionRate: 24.5,
      avgDealValue: 8500,
      revenue: 125000,
      growth: 15.3
    },
    leadMetrics: {
      conversionByFunnel: [
        { stage: 'Novo', leads: 156, converted: 124, rate: 79.5 },
        { stage: 'Contato', leads: 124, converted: 89, rate: 71.8 },
        { stage: 'Qualificado', leads: 89, converted: 67, rate: 75.3 },
        { stage: 'Proposta', leads: 67, converted: 45, rate: 67.2 },
        { stage: 'Fechado', leads: 45, converted: 38, rate: 84.4 }
      ],
      successRateByUser: [
        { user: 'Ana Silva', leads: 45, converted: 18, rate: 40.0 },
        { user: 'Carlos Santos', leads: 38, converted: 12, rate: 31.6 },
        { user: 'Maria Oliveira', leads: 42, converted: 15, rate: 35.7 },
        { user: 'João Costa', leads: 31, converted: 8, rate: 25.8 }
      ]
    },
    volumeAnalysis: {
      byStage: [
        { stage: 'Novo', count: 45, avgTime: 2.3, bottleneck: false },
        { stage: 'Contato', count: 67, avgTime: 5.8, bottleneck: true },
        { stage: 'Qualificado', count: 34, avgTime: 3.2, bottleneck: false },
        { stage: 'Proposta', count: 23, avgTime: 7.1, bottleneck: true },
        { stage: 'Fechado', count: 12, avgTime: 1.5, bottleneck: false }
      ],
      timeline: [
        { date: '2025-01', novo: 45, contato: 38, qualificado: 29, proposta: 18, fechado: 12 },
        { date: '2025-02', novo: 52, contato: 42, qualificado: 34, proposta: 22, fechado: 15 },
        { date: '2025-03', novo: 48, contato: 45, qualificado: 38, proposta: 25, fechado: 18 },
        { date: '2025-04', novo: 61, contato: 51, qualificado: 42, proposta: 28, fechado: 21 },
        { date: '2025-05', novo: 58, contato: 48, qualificado: 39, proposta: 31, fechado: 24 },
        { date: '2025-06', novo: 67, contato: 55, qualificado: 45, proposta: 34, fechado: 28 }
      ]
    },
    revenueProjection: {
      monthly: [
        { month: 'Jan', actual: 85000, projected: 90000, target: 100000 },
        { month: 'Fev', actual: 92000, projected: 95000, target: 100000 },
        { month: 'Mar', actual: 88000, projected: 98000, target: 100000 },
        { month: 'Abr', actual: 105000, projected: 102000, target: 100000 },
        { month: 'Mai', actual: 98000, projected: 105000, target: 100000 },
        { month: 'Jun', actual: 125000, projected: 110000, target: 100000 }
      ],
      trends: [
        { period: 'Q1 2025', value: 265000, growth: 12.5 },
        { period: 'Q2 2025', value: 328000, growth: 23.8 },
        { period: 'Q3 2025', value: 385000, growth: 17.4 },
        { period: 'Q4 2025', value: 420000, growth: 9.1 }
      ]
    }
  });

  const COLORS = ['#4169E1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-jt-blue">Analytics Avançado</h1>
        </div>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jt-blue"></div>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <BarChart3 className="w-8 h-8 text-jt-blue" />
          <h1 className="text-3xl font-bold text-jt-blue">Analytics Avançado</h1>
        </div>
        <div className="flex items-center gap-4">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Período" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Últimos 7 dias</SelectItem>
              <SelectItem value="30d">Últimos 30 dias</SelectItem>
              <SelectItem value="90d">Últimos 90 dias</SelectItem>
              <SelectItem value="1y">Último ano</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={fetchAnalyticsData} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Exportar
          </Button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid gap-4 md:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.overview.totalLeads}</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +{data.overview.growth}% vs período anterior
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Conversão</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatPercentage(data.overview.conversionRate)}</div>
            <div className="text-xs text-muted-foreground">
              Meta: 30%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ticket Médio</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(data.overview.avgDealValue)}</div>
            <div className="text-xs text-muted-foreground">
              Por lead convertido
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Receita Total</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(data.overview.revenue)}</div>
            <div className="text-xs text-muted-foreground">
              No período selecionado
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Crescimento</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">+{formatPercentage(data.overview.growth)}</div>
            <div className="text-xs text-muted-foreground">
              Crescimento mensal
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Analytics Tabs */}
      <Tabs defaultValue="conversion" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="conversion">Conversão por Funil</TabsTrigger>
          <TabsTrigger value="volume">Volume por Etapa</TabsTrigger>
          <TabsTrigger value="revenue">Receita Prevista</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        {/* Conversão por Funil */}
        <TabsContent value="conversion" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Funil de Conversão</CardTitle>
                <CardDescription>Taxa de conversão por etapa do processo</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.leadMetrics.conversionByFunnel}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="stage" />
                    <YAxis />
                    <Tooltip formatter={(value, name) => [
                      name === 'rate' ? formatPercentage(value as number) : value,
                      name === 'rate' ? 'Taxa de Conversão' : name === 'leads' ? 'Leads' : 'Convertidos'
                    ]} />
                    <Legend />
                    <Bar dataKey="leads" fill="#4169E1" name="Leads" />
                    <Bar dataKey="converted" fill="#10B981" name="Convertidos" />
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
                <div className="space-y-4">
                  {data.leadMetrics.successRateByUser.map((user, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-jt-blue text-white rounded-full flex items-center justify-center text-sm font-medium">
                          {user.user.charAt(0)}
                        </div>
                        <div>
                          <div className="font-medium">{user.user}</div>
                          <div className="text-sm text-gray-500">{user.leads} leads</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-lg">{formatPercentage(user.rate)}</div>
                        <div className="text-sm text-gray-500">{user.converted} convertidos</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Volume por Etapa */}
        <TabsContent value="volume" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Análise de Gargalos</CardTitle>
                <CardDescription>Identificação de etapas com maior tempo de permanência</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {data.volumeAnalysis.byStage.map((stage, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center gap-3">
                        {stage.bottleneck ? (
                          <AlertTriangle className="w-5 h-5 text-orange-500" />
                        ) : (
                          <CheckCircle className="w-5 h-5 text-green-500" />
                        )}
                        <div>
                          <div className="font-medium">{stage.stage}</div>
                          <div className="text-sm text-gray-500">{stage.count} leads</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold">{stage.avgTime} dias</div>
                        <div className="text-sm text-gray-500">tempo médio</div>
                        {stage.bottleneck && (
                          <Badge variant="destructive" className="mt-1">Gargalo</Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Evolução Temporal</CardTitle>
                <CardDescription>Volume de leads por etapa ao longo do tempo</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={data.volumeAnalysis.timeline}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
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

        {/* Receita Prevista */}
        <TabsContent value="revenue" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Projeções Mensais</CardTitle>
                <CardDescription>Receita real vs projetada vs meta</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={data.revenueProjection.monthly}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis tickFormatter={(value) => formatCurrency(value)} />
                    <Tooltip formatter={(value) => formatCurrency(value as number)} />
                    <Legend />
                    <Line type="monotone" dataKey="actual" stroke="#4169E1" strokeWidth={3} name="Real" />
                    <Line type="monotone" dataKey="projected" stroke="#10B981" strokeWidth={2} strokeDasharray="5 5" name="Projetado" />
                    <Line type="monotone" dataKey="target" stroke="#EF4444" strokeWidth={2} strokeDasharray="10 5" name="Meta" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Tendências Trimestrais</CardTitle>
                <CardDescription>Crescimento da receita por trimestre</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {data.revenueProjection.trends.map((trend, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <div className="font-medium">{trend.period}</div>
                        <div className="text-sm text-gray-500">Receita trimestral</div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-lg">{formatCurrency(trend.value)}</div>
                        <div className={`text-sm flex items-center ${trend.growth > 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {trend.growth > 0 ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                          {formatPercentage(Math.abs(trend.growth))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Performance */}
        <TabsContent value="performance" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>Distribuição por Status</CardTitle>
                <CardDescription>Proporção de leads por etapa</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
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
                <CardTitle>Métricas de Velocidade</CardTitle>
                <CardDescription>Tempo médio por etapa</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.volumeAnalysis.byStage.map((stage, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">{stage.stage}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{stage.avgTime}d</span>
                        {stage.bottleneck && <Zap className="w-4 h-4 text-orange-500" />}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Indicadores Chave</CardTitle>
                <CardDescription>KPIs principais do período</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Leads/Dia</span>
                    <span className="font-bold">5.2</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Ciclo Médio</span>
                    <span className="font-bold">18.5d</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">LTV</span>
                    <span className="font-bold">{formatCurrency(25600)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">CAC</span>
                    <span className="font-bold">{formatCurrency(1200)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">ROI</span>
                    <span className="font-bold text-green-600">21.3x</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DashboardAnalyticsAdvanced;

