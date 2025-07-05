import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { 
  Download, 
  Calendar, 
  TrendingUp, 
  TrendingDown,
  Users, 
  DollarSign, 
  Phone,
  MessageSquare,
  Target,
  Clock,
  BarChart3,
  PieChart,
  LineChart,
  Filter,
  RefreshCw,
  FileText,
  Mail,
  Award,
  AlertTriangle,
  CheckCircle,
  Star,
  Zap,
  Activity,
  Eye,
  ThumbsUp,
  ThumbsDown
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart as RechartsLineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart as RechartsPieChart,
  Cell,
  Area,
  AreaChart,
  ComposedChart,
  Scatter,
  ScatterChart,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { useToast } from '@/hooks/use-toast';

interface PerformanceMetrics {
  overview: {
    totalRevenue: number;
    revenueGrowth: number;
    totalLeads: number;
    leadsGrowth: number;
    conversionRate: number;
    conversionGrowth: number;
    avgDealSize: number;
    dealSizeGrowth: number;
  };
  salesInsights: {
    topPerformers: Array<{
      name: string;
      revenue: number;
      deals: number;
      conversionRate: number;
      rank: number;
    }>;
    productPerformance: Array<{
      product: string;
      revenue: number;
      units: number;
      growth: number;
    }>;
    salesTrends: Array<{
      month: string;
      revenue: number;
      deals: number;
      avgDealSize: number;
    }>;
  };
  customerAnalysis: {
    segmentation: Array<{
      segment: string;
      count: number;
      revenue: number;
      ltv: number;
    }>;
    retention: Array<{
      cohort: string;
      month1: number;
      month3: number;
      month6: number;
      month12: number;
    }>;
    satisfaction: Array<{
      category: string;
      score: number;
      responses: number;
    }>;
  };
  operationalMetrics: {
    efficiency: Array<{
      metric: string;
      current: number;
      target: number;
      trend: 'up' | 'down' | 'stable';
    }>;
    bottlenecks: Array<{
      process: string;
      avgTime: number;
      impact: 'high' | 'medium' | 'low';
      recommendations: string[];
    }>;
    productivity: Array<{
      user: string;
      tasksCompleted: number;
      avgResponseTime: number;
      qualityScore: number;
    }>;
  };
}

const AdvancedReportsEnhanced: React.FC = () => {
  const [data, setData] = useState<PerformanceMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('30d');
  const [selectedReport, setSelectedReport] = useState('performance');
  const { toast } = useToast();

  useEffect(() => {
    fetchReportData();
  }, [selectedPeriod, selectedReport]);

  const fetchReportData = async () => {
    try {
      setIsLoading(true);
      // Simular chamada de API
      await new Promise(resolve => setTimeout(resolve, 1000));
      setData(getMockReportData());
    } catch (error) {
      console.error('Failed to fetch report data:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível carregar os dados do relatório.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getMockReportData = (): PerformanceMetrics => ({
    overview: {
      totalRevenue: 485000,
      revenueGrowth: 18.5,
      totalLeads: 1247,
      leadsGrowth: 12.3,
      conversionRate: 24.8,
      conversionGrowth: 3.2,
      avgDealSize: 8500,
      dealSizeGrowth: 5.7
    },
    salesInsights: {
      topPerformers: [
        { name: 'Ana Silva', revenue: 125000, deals: 18, conversionRate: 32.5, rank: 1 },
        { name: 'Carlos Santos', revenue: 98000, deals: 15, conversionRate: 28.1, rank: 2 },
        { name: 'Maria Oliveira', revenue: 87000, deals: 12, conversionRate: 25.8, rank: 3 },
        { name: 'João Costa', revenue: 76000, deals: 11, conversionRate: 22.4, rank: 4 }
      ],
      productPerformance: [
        { product: 'PABX em Nuvem', revenue: 185000, units: 45, growth: 22.1 },
        { product: 'Chatbot IA', revenue: 142000, units: 38, growth: 18.7 },
        { product: 'Discador Preditivo', revenue: 98000, units: 28, growth: 15.3 },
        { product: '0800 Virtual', revenue: 76000, units: 22, growth: 12.8 }
      ],
      salesTrends: [
        { month: 'Jan', revenue: 65000, deals: 8, avgDealSize: 8125 },
        { month: 'Fev', revenue: 72000, deals: 9, avgDealSize: 8000 },
        { month: 'Mar', revenue: 68000, deals: 8, avgDealSize: 8500 },
        { month: 'Abr', revenue: 85000, deals: 10, avgDealSize: 8500 },
        { month: 'Mai', revenue: 92000, deals: 11, avgDealSize: 8364 },
        { month: 'Jun', revenue: 103000, deals: 12, avgDealSize: 8583 }
      ]
    },
    customerAnalysis: {
      segmentation: [
        { segment: 'Enterprise', count: 45, revenue: 285000, ltv: 45000 },
        { segment: 'SMB', count: 128, revenue: 156000, ltv: 18000 },
        { segment: 'Startup', count: 89, revenue: 44000, ltv: 8500 }
      ],
      retention: [
        { cohort: 'Jan 2025', month1: 95, month3: 87, month6: 78, month12: 72 },
        { cohort: 'Fev 2025', month1: 92, month3: 85, month6: 76, month12: 0 },
        { cohort: 'Mar 2025', month1: 94, month3: 88, month6: 0, month12: 0 },
        { cohort: 'Abr 2025', month1: 96, month3: 0, month6: 0, month12: 0 }
      ],
      satisfaction: [
        { category: 'Atendimento', score: 4.2, responses: 156 },
        { category: 'Produto', score: 4.5, responses: 142 },
        { category: 'Suporte', score: 3.8, responses: 98 },
        { category: 'Preço', score: 3.9, responses: 134 }
      ]
    },
    operationalMetrics: {
      efficiency: [
        { metric: 'Tempo de Resposta', current: 2.3, target: 2.0, trend: 'down' },
        { metric: 'Taxa de Resolução', current: 87, target: 90, trend: 'up' },
        { metric: 'Satisfação Cliente', current: 4.2, target: 4.5, trend: 'up' },
        { metric: 'Produtividade', current: 92, target: 95, trend: 'stable' }
      ],
      bottlenecks: [
        {
          process: 'Qualificação de Leads',
          avgTime: 5.2,
          impact: 'high',
          recommendations: ['Automatizar triagem inicial', 'Criar formulários inteligentes']
        },
        {
          process: 'Aprovação de Propostas',
          avgTime: 3.8,
          impact: 'medium',
          recommendations: ['Implementar aprovação digital', 'Definir alçadas claras']
        }
      ],
      productivity: [
        { user: 'Ana Silva', tasksCompleted: 45, avgResponseTime: 1.8, qualityScore: 4.6 },
        { user: 'Carlos Santos', tasksCompleted: 38, avgResponseTime: 2.1, qualityScore: 4.3 },
        { user: 'Maria Oliveira', tasksCompleted: 42, avgResponseTime: 1.9, qualityScore: 4.4 },
        { user: 'João Costa', tasksCompleted: 35, avgResponseTime: 2.5, qualityScore: 4.1 }
      ]
    }
  });

  const COLORS = ['#4169E1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down': return <TrendingDown className="w-4 h-4 text-red-500" />;
      default: return <Activity className="w-4 h-4 text-gray-500" />;
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-600 bg-red-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const exportReport = async (format: 'pdf' | 'excel' | 'csv') => {
    toast({
      title: 'Exportando relatório',
      description: `Gerando arquivo ${format.toUpperCase()}...`,
    });
    
    // Simular exportação
    setTimeout(() => {
      toast({
        title: 'Relatório exportado',
        description: `Arquivo ${format.toUpperCase()} baixado com sucesso.`,
      });
    }, 2000);
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-jt-blue">Relatórios Avançados</h1>
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
          <FileText className="w-8 h-8 text-jt-blue" />
          <h1 className="text-3xl font-bold text-jt-blue">Relatórios Avançados</h1>
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
          <Button onClick={fetchReportData} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
          <Select onValueChange={(value) => exportReport(value as any)}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder="Exportar" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="pdf">PDF</SelectItem>
              <SelectItem value="excel">Excel</SelectItem>
              <SelectItem value="csv">CSV</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Receita Total</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(data.overview.totalRevenue)}</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +{formatPercentage(data.overview.revenueGrowth)} vs período anterior
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.overview.totalLeads}</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +{formatPercentage(data.overview.leadsGrowth)} vs período anterior
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Conversão</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatPercentage(data.overview.conversionRate)}</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +{formatPercentage(data.overview.conversionGrowth)} vs período anterior
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ticket Médio</CardTitle>
            <Award className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(data.overview.avgDealSize)}</div>
            <div className="flex items-center text-xs text-green-600">
              <TrendingUp className="w-3 h-3 mr-1" />
              +{formatPercentage(data.overview.dealSizeGrowth)} vs período anterior
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Report Tabs */}
      <Tabs defaultValue="performance" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="performance">Performance de Vendas</TabsTrigger>
          <TabsTrigger value="customers">Análise de Clientes</TabsTrigger>
          <TabsTrigger value="operations">Métricas Operacionais</TabsTrigger>
          <TabsTrigger value="insights">Insights Estratégicos</TabsTrigger>
        </TabsList>

        {/* Performance de Vendas */}
        <TabsContent value="performance" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Top Performers</CardTitle>
                <CardDescription>Ranking de vendedores por performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {data.salesInsights.topPerformers.map((performer, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-jt-blue text-white rounded-full flex items-center justify-center text-sm font-bold">
                          {performer.rank}
                        </div>
                        <div>
                          <div className="font-medium">{performer.name}</div>
                          <div className="text-sm text-gray-500">{performer.deals} deals fechados</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold">{formatCurrency(performer.revenue)}</div>
                        <div className="text-sm text-gray-500">{formatPercentage(performer.conversionRate)} conversão</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Performance por Produto</CardTitle>
                <CardDescription>Receita e crescimento por linha de produto</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.salesInsights.productPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="product" />
                    <YAxis tickFormatter={(value) => formatCurrency(value)} />
                    <Tooltip formatter={(value) => formatCurrency(value as number)} />
                    <Bar dataKey="revenue" fill="#4169E1" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Tendências de Vendas</CardTitle>
              <CardDescription>Evolução da receita e ticket médio</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <ComposedChart data={data.salesInsights.salesTrends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis yAxisId="left" tickFormatter={(value) => formatCurrency(value)} />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Bar yAxisId="left" dataKey="revenue" fill="#4169E1" name="Receita" />
                  <Line yAxisId="right" type="monotone" dataKey="avgDealSize" stroke="#10B981" strokeWidth={3} name="Ticket Médio" />
                </ComposedChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Análise de Clientes */}
        <TabsContent value="customers" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Segmentação de Clientes</CardTitle>
                <CardDescription>Distribuição por segmento e LTV</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RechartsPieChart>
                    <Pie
                      data={data.customerAnalysis.segmentation}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ segment, count }) => `${segment}: ${count}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="count"
                    >
                      {data.customerAnalysis.segmentation.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Retenção de Clientes</CardTitle>
                <CardDescription>Taxa de retenção por coorte</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RechartsLineChart data={data.customerAnalysis.retention}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="cohort" />
                    <YAxis />
                    <Tooltip formatter={(value) => `${value}%`} />
                    <Legend />
                    <Line type="monotone" dataKey="month1" stroke="#4169E1" name="1 mês" />
                    <Line type="monotone" dataKey="month3" stroke="#10B981" name="3 meses" />
                    <Line type="monotone" dataKey="month6" stroke="#F59E0B" name="6 meses" />
                    <Line type="monotone" dataKey="month12" stroke="#EF4444" name="12 meses" />
                  </RechartsLineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Satisfação do Cliente</CardTitle>
              <CardDescription>Scores de satisfação por categoria</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {data.customerAnalysis.satisfaction.map((item, index) => (
                  <div key={index} className="space-y-2">
                    <div className="flex justify-between">
                      <span className="font-medium">{item.category}</span>
                      <span className="text-sm text-gray-500">{item.responses} respostas</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Progress value={(item.score / 5) * 100} className="flex-1" />
                      <span className="font-bold">{item.score.toFixed(1)}/5</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Métricas Operacionais */}
        <TabsContent value="operations" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Eficiência Operacional</CardTitle>
                <CardDescription>Métricas vs metas estabelecidas</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {data.operationalMetrics.efficiency.map((metric, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center gap-3">
                        {getTrendIcon(metric.trend)}
                        <div>
                          <div className="font-medium">{metric.metric}</div>
                          <div className="text-sm text-gray-500">Meta: {metric.target}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold">{metric.current}</div>
                        <div className="text-sm text-gray-500">
                          {metric.current >= metric.target ? 'Atingida' : 'Abaixo da meta'}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Produtividade da Equipe</CardTitle>
                <CardDescription>Performance individual dos colaboradores</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {data.operationalMetrics.productivity.map((user, index) => (
                    <div key={index} className="p-3 border rounded-lg">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">{user.user}</span>
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4 text-yellow-500" />
                          <span className="text-sm">{user.qualityScore}</span>
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-gray-500">Tarefas: </span>
                          <span className="font-medium">{user.tasksCompleted}</span>
                        </div>
                        <div>
                          <span className="text-gray-500">Resp. Média: </span>
                          <span className="font-medium">{user.avgResponseTime}h</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Gargalos Identificados</CardTitle>
              <CardDescription>Processos que precisam de atenção</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {data.operationalMetrics.bottlenecks.map((bottleneck, index) => (
                  <div key={index} className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <AlertTriangle className="w-5 h-5 text-orange-500" />
                        <div>
                          <div className="font-medium">{bottleneck.process}</div>
                          <div className="text-sm text-gray-500">Tempo médio: {bottleneck.avgTime} dias</div>
                        </div>
                      </div>
                      <Badge className={getImpactColor(bottleneck.impact)}>
                        {bottleneck.impact === 'high' ? 'Alto Impacto' : 
                         bottleneck.impact === 'medium' ? 'Médio Impacto' : 'Baixo Impacto'}
                      </Badge>
                    </div>
                    <div className="space-y-1">
                      <div className="text-sm font-medium text-gray-700">Recomendações:</div>
                      {bottleneck.recommendations.map((rec, recIndex) => (
                        <div key={recIndex} className="text-sm text-gray-600 flex items-center gap-2">
                          <CheckCircle className="w-3 h-3 text-green-500" />
                          {rec}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Insights Estratégicos */}
        <TabsContent value="insights" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Oportunidades de Crescimento</CardTitle>
                <CardDescription>Áreas com maior potencial</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Zap className="w-4 h-4 text-green-600" />
                      <span className="font-medium text-green-800">Upsell Enterprise</span>
                    </div>
                    <p className="text-sm text-green-700">
                      Clientes Enterprise têm LTV 2.5x maior. Foco em expansão deste segmento.
                    </p>
                  </div>
                  
                  <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Target className="w-4 h-4 text-blue-600" />
                      <span className="font-medium text-blue-800">Automação de Processos</span>
                    </div>
                    <p className="text-sm text-blue-700">
                      Reduzir tempo de qualificação em 40% com automação inteligente.
                    </p>
                  </div>
                  
                  <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Star className="w-4 h-4 text-purple-600" />
                      <span className="font-medium text-purple-800">Programa de Fidelidade</span>
                    </div>
                    <p className="text-sm text-purple-700">
                      Implementar programa para aumentar retenção em 15%.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Alertas e Riscos</CardTitle>
                <CardDescription>Pontos que requerem atenção imediata</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle className="w-4 h-4 text-red-600" />
                      <span className="font-medium text-red-800">Churn Rate Elevado</span>
                    </div>
                    <p className="text-sm text-red-700">
                      Segmento Startup com churn 23% acima da média. Ação imediata necessária.
                    </p>
                  </div>
                  
                  <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Clock className="w-4 h-4 text-yellow-600" />
                      <span className="font-medium text-yellow-800">Tempo de Resposta</span>
                    </div>
                    <p className="text-sm text-yellow-700">
                      Tempo médio de resposta 15% acima da meta. Revisar processos.
                    </p>
                  </div>
                  
                  <div className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingDown className="w-4 h-4 text-orange-600" />
                      <span className="font-medium text-orange-800">Conversão Q2</span>
                    </div>
                    <p className="text-sm text-orange-700">
                      Taxa de conversão em queda. Revisar estratégia de qualificação.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Recomendações Estratégicas</CardTitle>
              <CardDescription>Ações prioritárias para os próximos 90 dias</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold">1</div>
                    <span className="font-medium">Curto Prazo (30 dias)</span>
                  </div>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-center gap-2">
                      <CheckCircle className="w-3 h-3 text-green-500" />
                      Implementar chatbot para triagem
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="w-3 h-3 text-green-500" />
                      Treinar equipe em objeções
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="w-3 h-3 text-green-500" />
                      Revisar processo de follow-up
                    </li>
                  </ul>
                </div>

                <div className="p-4 border rounded-lg">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center font-bold">2</div>
                    <span className="font-medium">Médio Prazo (60 dias)</span>
                  </div>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-center gap-2">
                      <Clock className="w-3 h-3 text-yellow-500" />
                      Automatizar aprovações
                    </li>
                    <li className="flex items-center gap-2">
                      <Clock className="w-3 h-3 text-yellow-500" />
                      Implementar scoring de leads
                    </li>
                    <li className="flex items-center gap-2">
                      <Clock className="w-3 h-3 text-yellow-500" />
                      Dashboard executivo
                    </li>
                  </ul>
                </div>

                <div className="p-4 border rounded-lg">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold">3</div>
                    <span className="font-medium">Longo Prazo (90 dias)</span>
                  </div>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-center gap-2">
                      <Eye className="w-3 h-3 text-blue-500" />
                      IA para previsão de churn
                    </li>
                    <li className="flex items-center gap-2">
                      <Eye className="w-3 h-3 text-blue-500" />
                      Programa de fidelidade
                    </li>
                    <li className="flex items-center gap-2">
                      <Eye className="w-3 h-3 text-blue-500" />
                      Expansão para novos mercados
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdvancedReportsEnhanced;

