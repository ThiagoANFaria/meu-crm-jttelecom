import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Download, 
  Calendar, 
  TrendingUp, 
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
  Mail
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
  PieChart as RechartsPieChart,
  Cell,
  Area,
  AreaChart
} from 'recharts';

interface ReportFilters {
  start_date: string;
  end_date: string;
  user_id?: string;
  stage?: string;
  source?: string;
  report_type: string;
}

interface PerformanceReport {
  summary: {
    total_leads: number;
    conversion_rate: number;
    avg_deal_size: number;
    revenue_growth: number;
    team_productivity: number;
  };
  trends: {
    leads_by_month: Array<{month: string, count: number, converted: number}>;
    revenue_by_month: Array<{month: string, amount: number}>;
    conversion_by_source: Array<{source: string, rate: number, count: number}>;
  };
  team_analysis: {
    top_performers: Array<{
      name: string;
      leads: number;
      conversions: number;
      revenue: number;
      score: number;
    }>;
    activity_metrics: Array<{
      user: string;
      calls: number;
      emails: number;
      meetings: number;
      notes: number;
    }>;
  };
  funnel_analysis: {
    stage_performance: Array<{
      stage: string;
      count: number;
      conversion_rate: number;
      avg_time: number;
      drop_rate: number;
    }>;
    bottlenecks: Array<{
      stage: string;
      issue: string;
      impact: number;
      recommendation: string;
    }>;
  };
  roi_analysis: {
    cost_per_lead: number;
    customer_lifetime_value: number;
    roi_percentage: number;
    payback_period: number;
    marketing_efficiency: Array<{
      channel: string;
      cost: number;
      leads: number;
      conversions: number;
      roi: number;
    }>;
  };
  predictions: {
    next_month_leads: number;
    next_month_revenue: number;
    quarterly_projection: number;
    growth_forecast: Array<{
      month: string;
      predicted_leads: number;
      predicted_revenue: number;
      confidence: number;
    }>;
  };
}

const AdvancedReports: React.FC = () => {
  const [reportData, setReportData] = useState<PerformanceReport | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState<ReportFilters>({
    start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end_date: new Date().toISOString().split('T')[0],
    report_type: 'performance'
  });

  const COLORS = ['#4169E1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  useEffect(() => {
    fetchReportData();
  }, [filters]);

  const fetchReportData = async () => {
    setIsLoading(true);
    try {
      // Simulando dados de relatório (em produção viria da API)
      const mockData: PerformanceReport = {
        summary: {
          total_leads: 342,
          conversion_rate: 23.4,
          avg_deal_size: 4500,
          revenue_growth: 18.7,
          team_productivity: 87.3
        },
        trends: {
          leads_by_month: [
            {month: 'Jan', count: 45, converted: 12},
            {month: 'Fev', count: 52, converted: 15},
            {month: 'Mar', count: 48, converted: 11},
            {month: 'Abr', count: 61, converted: 18},
            {month: 'Mai', count: 58, converted: 16},
            {month: 'Jun', count: 78, converted: 22}
          ],
          revenue_by_month: [
            {month: 'Jan', amount: 54000},
            {month: 'Fev', amount: 67500},
            {month: 'Mar', amount: 49500},
            {month: 'Abr', amount: 81000},
            {month: 'Mai', amount: 72000},
            {month: 'Jun', amount: 99000}
          ],
          conversion_by_source: [
            {source: 'Website', rate: 28.5, count: 89},
            {source: 'Indicação', rate: 45.2, count: 67},
            {source: 'Redes Sociais', rate: 15.8, count: 124},
            {source: 'Email Marketing', rate: 22.1, count: 62}
          ]
        },
        team_analysis: {
          top_performers: [
            {name: 'Maria Santos', leads: 45, conversions: 18, revenue: 81000, score: 95},
            {name: 'João Silva', leads: 38, conversions: 14, revenue: 63000, score: 88},
            {name: 'Ana Oliveira', leads: 42, conversions: 15, revenue: 67500, score: 85},
            {name: 'Pedro Costa', leads: 35, conversions: 11, revenue: 49500, score: 78},
            {name: 'Carlos Lima', leads: 29, conversions: 8, revenue: 36000, score: 72}
          ],
          activity_metrics: [
            {user: 'Maria Santos', calls: 156, emails: 89, meetings: 23, notes: 67},
            {user: 'João Silva', calls: 142, emails: 76, meetings: 19, notes: 54},
            {user: 'Ana Oliveira', calls: 138, emails: 82, meetings: 21, notes: 61},
            {user: 'Pedro Costa', calls: 124, emails: 68, meetings: 16, notes: 45},
            {user: 'Carlos Lima', calls: 98, emails: 52, meetings: 12, notes: 38}
          ]
        },
        funnel_analysis: {
          stage_performance: [
            {stage: 'Novo', count: 156, conversion_rate: 78.2, avg_time: 2.3, drop_rate: 21.8},
            {stage: 'Qualificado', count: 122, conversion_rate: 68.9, avg_time: 4.1, drop_rate: 31.1},
            {stage: 'Proposta', count: 84, conversion_rate: 59.5, avg_time: 6.7, drop_rate: 40.5},
            {stage: 'Negociação', count: 50, conversion_rate: 72.0, avg_time: 8.2, drop_rate: 28.0},
            {stage: 'Ganho', count: 36, conversion_rate: 100, avg_time: 0, drop_rate: 0}
          ],
          bottlenecks: [
            {
              stage: 'Qualificado → Proposta',
              issue: 'Alta taxa de abandono (31.1%)',
              impact: 38,
              recommendation: 'Melhorar processo de qualificação e timing de propostas'
            },
            {
              stage: 'Proposta → Negociação',
              issue: 'Propostas não competitivas',
              impact: 34,
              recommendation: 'Revisar estratégia de precificação e personalização'
            }
          ]
        },
        roi_analysis: {
          cost_per_lead: 125.50,
          customer_lifetime_value: 12500,
          roi_percentage: 340,
          payback_period: 3.2,
          marketing_efficiency: [
            {channel: 'Google Ads', cost: 8500, leads: 67, conversions: 19, roi: 285},
            {channel: 'Facebook Ads', cost: 4200, leads: 34, conversions: 8, roi: 190},
            {channel: 'LinkedIn', cost: 6800, leads: 28, conversions: 12, roi: 420},
            {channel: 'Email Marketing', cost: 1200, leads: 62, conversions: 14, roi: 580}
          ]
        },
        predictions: {
          next_month_leads: 85,
          next_month_revenue: 115000,
          quarterly_projection: 340000,
          growth_forecast: [
            {month: 'Jul', predicted_leads: 85, predicted_revenue: 115000, confidence: 87},
            {month: 'Ago', predicted_leads: 92, predicted_revenue: 125000, confidence: 82},
            {month: 'Set', predicted_leads: 88, predicted_revenue: 119000, confidence: 78}
          ]
        }
      };

      setReportData(mockData);
    } catch (error) {
      console.error('Erro ao buscar dados do relatório:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportReport = async (format: 'pdf' | 'excel') => {
    try {
      // Implementar exportação real
      console.log(`Exportando relatório em formato ${format}`);
      // await analyticsService.exportReport(format, filters);
    } catch (error) {
      console.error('Erro ao exportar relatório:', error);
    }
  };

  const handleFilterChange = (key: keyof ReportFilters, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="h-8 w-8 animate-spin text-jt-blue" />
        <span className="ml-2 text-lg">Gerando relatório...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-jt-blue">Relatórios Avançados</h1>
          <p className="text-gray-600">Análise detalhada de performance e insights</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => handleExportReport('pdf')} variant="outline">
            <FileText className="h-4 w-4 mr-2" />
            Exportar PDF
          </Button>
          <Button onClick={() => handleExportReport('excel')} variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Exportar Excel
          </Button>
          <Button onClick={fetchReportData}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Atualizar
          </Button>
        </div>
      </div>

      {/* Filtros */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filtros do Relatório
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-5">
            <div>
              <Label htmlFor="start_date">Data Início</Label>
              <Input
                id="start_date"
                type="date"
                value={filters.start_date}
                onChange={(e) => handleFilterChange('start_date', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="end_date">Data Fim</Label>
              <Input
                id="end_date"
                type="date"
                value={filters.end_date}
                onChange={(e) => handleFilterChange('end_date', e.target.value)}
              />
            </div>
            <div>
              <Label>Tipo de Relatório</Label>
              <Select value={filters.report_type} onValueChange={(value) => handleFilterChange('report_type', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="performance">Performance Geral</SelectItem>
                  <SelectItem value="sales">Vendas</SelectItem>
                  <SelectItem value="marketing">Marketing</SelectItem>
                  <SelectItem value="team">Equipe</SelectItem>
                  <SelectItem value="roi">ROI</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Usuário</Label>
              <Select value={filters.user_id || ''} onValueChange={(value) => handleFilterChange('user_id', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Todos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos</SelectItem>
                  <SelectItem value="1">Maria Santos</SelectItem>
                  <SelectItem value="2">João Silva</SelectItem>
                  <SelectItem value="3">Ana Oliveira</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Fonte</Label>
              <Select value={filters.source || ''} onValueChange={(value) => handleFilterChange('source', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Todas" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todas</SelectItem>
                  <SelectItem value="website">Website</SelectItem>
                  <SelectItem value="indicacao">Indicação</SelectItem>
                  <SelectItem value="social">Redes Sociais</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Resumo Executivo */}
      <div className="grid gap-4 md:grid-cols-5">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total de Leads</p>
                <p className="text-2xl font-bold text-jt-blue">{reportData?.summary.total_leads}</p>
              </div>
              <Users className="h-8 w-8 text-jt-blue" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Taxa de Conversão</p>
                <p className="text-2xl font-bold text-green-600">{reportData?.summary.conversion_rate}%</p>
              </div>
              <Target className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Ticket Médio</p>
                <p className="text-2xl font-bold text-blue-600">R$ {reportData?.summary.avg_deal_size.toLocaleString('pt-BR')}</p>
              </div>
              <DollarSign className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Crescimento</p>
                <p className="text-2xl font-bold text-purple-600">+{reportData?.summary.revenue_growth}%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Produtividade</p>
                <p className="text-2xl font-bold text-orange-600">{reportData?.summary.team_productivity}%</p>
              </div>
              <BarChart3 className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs de Relatórios */}
      <Tabs defaultValue="trends" className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="trends">Tendências</TabsTrigger>
          <TabsTrigger value="team">Equipe</TabsTrigger>
          <TabsTrigger value="funnel">Funil</TabsTrigger>
          <TabsTrigger value="roi">ROI</TabsTrigger>
          <TabsTrigger value="predictions">Previsões</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
        </TabsList>

        {/* Aba Tendências */}
        <TabsContent value="trends" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Leads por Mês</CardTitle>
                <CardDescription>Evolução de leads e conversões</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={reportData?.trends.leads_by_month}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="count" stackId="1" stroke="#4169E1" fill="#4169E1" name="Total" />
                    <Area type="monotone" dataKey="converted" stackId="2" stroke="#10B981" fill="#10B981" name="Convertidos" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Receita por Mês</CardTitle>
                <CardDescription>Evolução da receita mensal</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RechartsLineChart data={reportData?.trends.revenue_by_month}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="amount" stroke="#4169E1" strokeWidth={3} />
                  </RechartsLineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Conversão por Fonte</CardTitle>
              <CardDescription>Performance de cada canal de aquisição</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {reportData?.trends.conversion_by_source.map((source, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h4 className="font-medium">{source.source}</h4>
                      <p className="text-sm text-gray-600">{source.count} leads</p>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-jt-blue">{source.rate}%</div>
                      <div className="text-sm text-gray-600">conversão</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aba Equipe */}
        <TabsContent value="team" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Top Performers</CardTitle>
                <CardDescription>Ranking da equipe por performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reportData?.team_analysis.top_performers.map((performer, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-4">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                          index === 0 ? 'bg-yellow-500' : 
                          index === 1 ? 'bg-gray-400' : 
                          index === 2 ? 'bg-orange-600' : 'bg-blue-500'
                        }`}>
                          {index + 1}
                        </div>
                        <div>
                          <p className="font-medium">{performer.name}</p>
                          <p className="text-sm text-gray-600">
                            {performer.conversions}/{performer.leads} conversões
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-bold text-jt-blue">{performer.score}</div>
                        <div className="text-sm text-gray-600">
                          R$ {performer.revenue.toLocaleString('pt-BR')}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Atividades da Equipe</CardTitle>
                <CardDescription>Métricas de atividade por usuário</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={reportData?.team_analysis.activity_metrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="user" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="calls" fill="#4169E1" name="Ligações" />
                    <Bar dataKey="emails" fill="#10B981" name="Emails" />
                    <Bar dataKey="meetings" fill="#F59E0B" name="Reuniões" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba Funil */}
        <TabsContent value="funnel" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Performance por Etapa</CardTitle>
                <CardDescription>Análise detalhada do funil</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reportData?.funnel_analysis.stage_performance.map((stage, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium">{stage.stage}</span>
                        <div className="text-right">
                          <span className="text-sm font-bold">{stage.count}</span>
                          <span className="text-xs text-gray-500 ml-2">({stage.conversion_rate}%)</span>
                        </div>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full" 
                          style={{ width: `${stage.conversion_rate}%` }}
                        ></div>
                      </div>
                      <div className="flex justify-between text-xs text-gray-600">
                        <span>Tempo médio: {stage.avg_time} dias</span>
                        <span className="text-red-600">Perda: {stage.drop_rate}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Gargalos Identificados</CardTitle>
                <CardDescription>Pontos críticos do processo</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reportData?.funnel_analysis.bottlenecks.map((bottleneck, index) => (
                    <div key={index} className="p-4 border border-red-200 rounded-lg bg-red-50">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-red-800">{bottleneck.stage}</h4>
                        <Badge variant="destructive">{bottleneck.impact}% impacto</Badge>
                      </div>
                      <p className="text-sm text-red-700 mb-2">{bottleneck.issue}</p>
                      <p className="text-xs text-red-600">
                        <strong>Recomendação:</strong> {bottleneck.recommendation}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba ROI */}
        <TabsContent value="roi" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-jt-blue">
                    R$ {reportData?.roi_analysis.cost_per_lead.toFixed(2)}
                  </div>
                  <p className="text-sm text-gray-600">Custo por Lead</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    R$ {reportData?.roi_analysis.customer_lifetime_value.toLocaleString('pt-BR')}
                  </div>
                  <p className="text-sm text-gray-600">LTV</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {reportData?.roi_analysis.roi_percentage}%
                  </div>
                  <p className="text-sm text-gray-600">ROI</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {reportData?.roi_analysis.payback_period} meses
                  </div>
                  <p className="text-sm text-gray-600">Payback</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Eficiência por Canal</CardTitle>
              <CardDescription>ROI de cada canal de marketing</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {reportData?.roi_analysis.marketing_efficiency.map((channel, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h4 className="font-medium">{channel.channel}</h4>
                      <p className="text-sm text-gray-600">
                        {channel.conversions}/{channel.leads} conversões
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-jt-blue">{channel.roi}%</div>
                      <div className="text-sm text-gray-600">
                        R$ {channel.cost.toLocaleString('pt-BR')} investido
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aba Previsões */}
        <TabsContent value="predictions" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-jt-blue">
                    {reportData?.predictions.next_month_leads}
                  </div>
                  <p className="text-sm text-gray-600">Leads Próximo Mês</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    R$ {reportData?.predictions.next_month_revenue.toLocaleString('pt-BR')}
                  </div>
                  <p className="text-sm text-gray-600">Receita Próximo Mês</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    R$ {reportData?.predictions.quarterly_projection.toLocaleString('pt-BR')}
                  </div>
                  <p className="text-sm text-gray-600">Projeção Trimestral</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Previsão de Crescimento</CardTitle>
              <CardDescription>Projeções baseadas em IA e tendências históricas</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <RechartsLineChart data={reportData?.predictions.growth_forecast}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="predicted_leads" stroke="#4169E1" strokeWidth={2} name="Leads Previstos" />
                  <Line type="monotone" dataKey="predicted_revenue" stroke="#10B981" strokeWidth={2} name="Receita Prevista" />
                </RechartsLineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Confiança das Previsões</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {reportData?.predictions.growth_forecast.map((forecast, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm font-medium">{forecast.month}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-jt-blue h-2 rounded-full" 
                          style={{ width: `${forecast.confidence}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-600">{forecast.confidence}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aba Insights */}
        <TabsContent value="insights" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  Oportunidades Identificadas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                    <h4 className="font-medium text-green-800">LinkedIn tem maior ROI</h4>
                    <p className="text-sm text-green-700">
                      Canal com 420% de ROI. Considere aumentar investimento em 30%.
                    </p>
                  </div>
                  <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <h4 className="font-medium text-blue-800">Maria Santos é top performer</h4>
                    <p className="text-sm text-blue-700">
                      95% de score. Considere replicar suas estratégias para a equipe.
                    </p>
                  </div>
                  <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                    <h4 className="font-medium text-purple-800">Crescimento acelerado</h4>
                    <p className="text-sm text-purple-700">
                      18.7% de crescimento. Tendência positiva para próximos meses.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-red-600" />
                  Pontos de Atenção
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                    <h4 className="font-medium text-red-800">Gargalo na qualificação</h4>
                    <p className="text-sm text-red-700">
                      31.1% de perda entre qualificado e proposta. Revisar processo.
                    </p>
                  </div>
                  <div className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
                    <h4 className="font-medium text-orange-800">Facebook Ads com baixo ROI</h4>
                    <p className="text-sm text-orange-700">
                      Apenas 190% de ROI. Otimizar campanhas ou realocar budget.
                    </p>
                  </div>
                  <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <h4 className="font-medium text-yellow-800">Tempo longo na negociação</h4>
                    <p className="text-sm text-yellow-700">
                      8.2 dias médios. Acelerar processo de fechamento.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Recomendações Estratégicas</CardTitle>
              <CardDescription>Ações prioritárias baseadas nos dados</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-start gap-3 p-4 border rounded-lg">
                  <div className="w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                  <div>
                    <h4 className="font-medium">Otimizar processo de qualificação</h4>
                    <p className="text-sm text-gray-600">
                      Implementar checklist de qualificação mais rigoroso para reduzir perda de 31.1% entre qualificado e proposta.
                    </p>
                    <Badge variant="destructive" className="mt-2">Alta Prioridade</Badge>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-4 border rounded-lg">
                  <div className="w-6 h-6 bg-orange-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                  <div>
                    <h4 className="font-medium">Aumentar investimento em LinkedIn</h4>
                    <p className="text-sm text-gray-600">
                      Canal com melhor ROI (420%). Aumentar budget em 30% pode gerar 40% mais conversões.
                    </p>
                    <Badge variant="secondary" className="mt-2">Média Prioridade</Badge>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-4 border rounded-lg">
                  <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
                  <div>
                    <h4 className="font-medium">Treinamento da equipe</h4>
                    <p className="text-sm text-gray-600">
                      Replicar estratégias de Maria Santos (95% score) para melhorar performance geral da equipe.
                    </p>
                    <Badge variant="outline" className="mt-2">Baixa Prioridade</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdvancedReports;

