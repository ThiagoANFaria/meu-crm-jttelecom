import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  TrendingUp, 
  Users, 
  FileText, 
  Phone, 
  Bot, 
  Clock, 
  Target, 
  Activity,
  MessageSquare,
  Calendar,
  BarChart3,
  PieChart,
  LineChart,
  RefreshCw,
  Download,
  Filter,
  Eye
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart as RechartsLineChart,
  Line,
  PieChart as RechartsPieChart,
  Cell,
  Area,
  AreaChart
} from 'recharts';

interface AnalyticsData {
  // Métricas gerais
  total_leads: number;
  total_clients: number;
  conversion_rate: number;
  
  // Métricas de Funil de Vendas
  funnel_metrics: {
    stages: Array<{
      name: string;
      count: number;
      conversion_rate: number;
      avg_time_in_stage: number; // em dias
    }>;
    bottlenecks: Array<{
      stage: string;
      drop_rate: number;
      suggestions: string[];
    }>;
  };
  
  // Métricas por Usuário
  user_performance: Array<{
    user_name: string;
    leads_assigned: number;
    leads_converted: number;
    success_rate: number;
    avg_response_time: number;
    revenue_generated: number;
  }>;
  
  // Receita e Projeções
  revenue_analytics: {
    current_month: number;
    previous_month: number;
    growth_rate: number;
    projected_next_month: number;
    quarterly_projection: number;
    revenue_by_month: Array<{
      month: string;
      actual: number;
      projected: number;
      target: number;
    }>;
    revenue_by_source: Array<{
      source: string;
      amount: number;
      percentage: number;
    }>;
  };
  
  // Volume por Etapa
  stage_analytics: {
    volume_by_stage: Array<{
      stage: string;
      current_count: number;
      previous_count: number;
      change_percentage: number;
      avg_time: number;
    }>;
    conversion_trends: Array<{
      date: string;
      novo: number;
      qualificado: number;
      proposta: number;
      negociacao: number;
      ganho: number;
      perdido: number;
    }>;
  };
  
  // Métricas das novas funcionalidades
  notes_analytics: {
    total_notes: number;
    notes_this_week: number;
    avg_notes_per_lead: number;
    most_active_users: Array<{name: string, count: number}>;
  };
  
  calls_analytics: {
    total_calls: number;
    calls_this_week: number;
    avg_call_duration: number;
    success_rate: number;
    calls_by_status: Array<{status: string, count: number}>;
    calls_by_hour: Array<{hour: number, count: number}>;
  };
  
  smartbot_analytics: {
    total_messages: number;
    messages_this_week: number;
    delivery_rate: number;
    response_rate: number;
    templates_usage: Array<{template: string, count: number}>;
    messages_by_day: Array<{day: string, sent: number, received: number}>;
  };
  
  automation_analytics: {
    total_tasks: number;
    completed_tasks: number;
    pending_tasks: number;
    completion_rate: number;
    tasks_by_type: Array<{type: string, count: number}>;
    tasks_by_status: Array<{status: string, count: number}>;
  };
  
  // Métricas de performance
  performance_metrics: {
    lead_response_time: number;
    customer_satisfaction: number;
    team_productivity: number;
    revenue_growth: number;
  };
}

const DashboardAnalytics: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('7d');

  // Cores para gráficos
  const COLORS = ['#4169E1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setIsLoading(true);
        // Simulando dados de analytics (em produção viria da API)
        const mockData: AnalyticsData = {
          total_leads: 156,
          total_clients: 89,
          conversion_rate: 57.1,
          
          // Métricas de Funil
          funnel_metrics: {
            stages: [
              {name: 'Novo', count: 45, conversion_rate: 78.2, avg_time_in_stage: 2.3},
              {name: 'Qualificado', count: 35, conversion_rate: 68.5, avg_time_in_stage: 4.1},
              {name: 'Proposta', count: 24, conversion_rate: 58.3, avg_time_in_stage: 6.7},
              {name: 'Negociação', count: 14, conversion_rate: 71.4, avg_time_in_stage: 8.2},
              {name: 'Ganho', count: 10, conversion_rate: 100, avg_time_in_stage: 0},
              {name: 'Perdido', count: 4, conversion_rate: 0, avg_time_in_stage: 0}
            ],
            bottlenecks: [
              {
                stage: 'Proposta → Negociação',
                drop_rate: 41.7,
                suggestions: ['Melhorar qualidade das propostas', 'Follow-up mais frequente', 'Personalizar ofertas']
              },
              {
                stage: 'Qualificado → Proposta',
                drop_rate: 31.5,
                suggestions: ['Qualificação mais rigorosa', 'Identificar necessidades reais', 'Timing adequado']
              }
            ]
          },
          
          // Performance por Usuário
          user_performance: [
            {user_name: 'João Silva', leads_assigned: 23, leads_converted: 14, success_rate: 60.9, avg_response_time: 1.2, revenue_generated: 45000},
            {user_name: 'Maria Santos', leads_assigned: 19, leads_converted: 13, success_rate: 68.4, avg_response_time: 0.8, revenue_generated: 52000},
            {user_name: 'Pedro Costa', leads_assigned: 21, leads_converted: 11, success_rate: 52.4, avg_response_time: 2.1, revenue_generated: 38000},
            {user_name: 'Ana Oliveira', leads_assigned: 18, leads_converted: 12, success_rate: 66.7, avg_response_time: 1.5, revenue_generated: 48000},
            {user_name: 'Carlos Lima', leads_assigned: 16, leads_converted: 8, success_rate: 50.0, avg_response_time: 2.8, revenue_generated: 32000}
          ],
          
          // Receita e Projeções
          revenue_analytics: {
            current_month: 215000,
            previous_month: 189000,
            growth_rate: 13.8,
            projected_next_month: 245000,
            quarterly_projection: 720000,
            revenue_by_month: [
              {month: 'Jan', actual: 180000, projected: 175000, target: 200000},
              {month: 'Fev', actual: 195000, projected: 190000, target: 210000},
              {month: 'Mar', actual: 189000, projected: 185000, target: 205000},
              {month: 'Abr', actual: 215000, projected: 210000, target: 220000},
              {month: 'Mai', actual: 0, projected: 245000, target: 240000},
              {month: 'Jun', actual: 0, projected: 260000, target: 250000}
            ],
            revenue_by_source: [
              {source: 'Website', amount: 89000, percentage: 41.4},
              {source: 'Indicação', amount: 67000, percentage: 31.2},
              {source: 'Redes Sociais', amount: 34000, percentage: 15.8},
              {source: 'Email Marketing', amount: 25000, percentage: 11.6}
            ]
          },
          
          // Volume por Etapa
          stage_analytics: {
            volume_by_stage: [
              {stage: 'Novo', current_count: 45, previous_count: 38, change_percentage: 18.4, avg_time: 2.3},
              {stage: 'Qualificado', current_count: 35, previous_count: 42, change_percentage: -16.7, avg_time: 4.1},
              {stage: 'Proposta', current_count: 24, previous_count: 28, change_percentage: -14.3, avg_time: 6.7},
              {stage: 'Negociação', current_count: 14, previous_count: 16, change_percentage: -12.5, avg_time: 8.2},
              {stage: 'Ganho', current_count: 10, previous_count: 8, change_percentage: 25.0, avg_time: 0},
              {stage: 'Perdido', current_count: 4, previous_count: 6, change_percentage: -33.3, avg_time: 0}
            ],
            conversion_trends: [
              {date: '01/04', novo: 12, qualificado: 8, proposta: 6, negociacao: 4, ganho: 3, perdido: 1},
              {date: '08/04', novo: 15, qualificado: 10, proposta: 7, negociacao: 5, ganho: 2, perdido: 2},
              {date: '15/04', novo: 18, qualificado: 12, proposta: 8, negociacao: 6, ganho: 4, perdido: 1},
              {date: '22/04', novo: 14, qualificado: 9, proposta: 5, negociacao: 3, ganho: 2, perdido: 3},
              {date: '29/04', novo: 16, qualificado: 11, proposta: 8, negociacao: 5, ganho: 3, perdido: 2}
            ]
          },
          
          notes_analytics: {
            total_notes: 342,
            notes_this_week: 47,
            avg_notes_per_lead: 2.2,
            most_active_users: [
              {name: 'João Silva', count: 23},
              {name: 'Maria Santos', count: 18},
              {name: 'Pedro Costa', count: 15}
            ]
          },
          
          calls_analytics: {
            total_calls: 234,
            calls_this_week: 38,
            avg_call_duration: 4.5,
            success_rate: 78.2,
            calls_by_status: [
              {status: 'Atendida', count: 183},
              {status: 'Não Atendida', count: 34},
              {status: 'Ocupado', count: 17}
            ],
            calls_by_hour: [
              {hour: 8, count: 12}, {hour: 9, count: 18}, {hour: 10, count: 25},
              {hour: 11, count: 22}, {hour: 14, count: 28}, {hour: 15, count: 31},
              {hour: 16, count: 24}, {hour: 17, count: 19}
            ]
          },
          
          smartbot_analytics: {
            total_messages: 567,
            messages_this_week: 89,
            delivery_rate: 96.8,
            response_rate: 34.2,
            templates_usage: [
              {template: 'Welcome', count: 145},
              {template: 'Follow Up', count: 123},
              {template: 'Proposal Sent', count: 89},
              {template: 'Meeting Reminder', count: 67},
              {template: 'Thank You', count: 143}
            ],
            messages_by_day: [
              {day: 'Seg', sent: 45, received: 23},
              {day: 'Ter', sent: 52, received: 28},
              {day: 'Qua', sent: 38, received: 19},
              {day: 'Qui', sent: 61, received: 31},
              {day: 'Sex', sent: 48, received: 25},
              {day: 'Sáb', sent: 23, received: 12},
              {day: 'Dom', sent: 15, received: 8}
            ]
          },
          
          automation_analytics: {
            total_tasks: 128,
            completed_tasks: 89,
            pending_tasks: 39,
            completion_rate: 69.5,
            tasks_by_type: [
              {type: 'Ligação', count: 45},
              {type: 'Email', count: 32},
              {type: 'WhatsApp', count: 28},
              {type: 'Reunião', count: 15},
              {type: 'Follow-up', count: 8}
            ],
            tasks_by_status: [
              {status: 'Concluída', count: 89},
              {status: 'Pendente', count: 25},
              {status: 'Em Andamento', count: 14}
            ]
          },
          
          performance_metrics: {
            lead_response_time: 2.3,
            customer_satisfaction: 4.7,
            team_productivity: 87.5,
            revenue_growth: 23.8
          }
        };
        
        setAnalytics(mockData);
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalytics();
  }, [selectedPeriod]);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-jt-blue">Analytics Dashboard</h1>
          <div className="h-10 bg-gray-200 rounded w-32 animate-pulse"></div>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(8)].map((_, i) => (
            <Card key={i}>
              <CardHeader className="pb-2">
                <div className="h-4 bg-gray-200 rounded w-24 animate-pulse"></div>
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
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-jt-blue">Analytics Dashboard</h1>
          <p className="text-gray-600">Métricas avançadas e insights do CRM</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Filter className="w-4 h-4 mr-2" />
            Filtros
          </Button>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Exportar
          </Button>
          <Button variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </div>
      </div>

      {/* KPIs Principais */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="border-l-4 border-l-blue-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Leads</CardTitle>
            <Users className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-jt-blue">{analytics?.total_leads}</div>
            <p className="text-xs text-green-600">↗ +12% esta semana</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Conversão</CardTitle>
            <Target className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-jt-blue">{analytics?.conversion_rate}%</div>
            <p className="text-xs text-green-600">↗ +5.2% vs mês anterior</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-purple-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Notas Criadas</CardTitle>
            <FileText className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-jt-blue">{analytics?.notes_analytics.notes_this_week}</div>
            <p className="text-xs text-gray-600">Esta semana</p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-orange-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ligações Realizadas</CardTitle>
            <Phone className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-jt-blue">{analytics?.calls_analytics.calls_this_week}</div>
            <p className="text-xs text-gray-600">Esta semana</p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs de Analytics */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-9">
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="funnel">Funil</TabsTrigger>
          <TabsTrigger value="users">Usuários</TabsTrigger>
          <TabsTrigger value="revenue">Receita</TabsTrigger>
          <TabsTrigger value="stages">Etapas</TabsTrigger>
          <TabsTrigger value="notes">Registros</TabsTrigger>
          <TabsTrigger value="calls">Ligações</TabsTrigger>
          <TabsTrigger value="smartbot">Smartbot</TabsTrigger>
          <TabsTrigger value="automation">Automação</TabsTrigger>
        </TabsList>

        {/* Aba Visão Geral */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            {/* Performance Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="w-5 h-5" />
                  Métricas de Performance
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Tempo de Resposta</span>
                    <span>{analytics?.performance_metrics.lead_response_time}h</span>
                  </div>
                  <Progress value={85} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Satisfação do Cliente</span>
                    <span>{analytics?.performance_metrics.customer_satisfaction}/5</span>
                  </div>
                  <Progress value={94} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Produtividade da Equipe</span>
                    <span>{analytics?.performance_metrics.team_productivity}%</span>
                  </div>
                  <Progress value={analytics?.performance_metrics.team_productivity} className="h-2" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Crescimento da Receita</span>
                    <span>+{analytics?.performance_metrics.revenue_growth}%</span>
                  </div>
                  <Progress value={analytics?.performance_metrics.revenue_growth} className="h-2" />
                </div>
              </CardContent>
            </Card>

            {/* Resumo das Funcionalidades */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  Resumo das Funcionalidades
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-blue-500" />
                    <div>
                      <p className="font-medium">Registros</p>
                      <p className="text-sm text-gray-600">{analytics?.notes_analytics.total_notes} notas</p>
                    </div>
                  </div>
                  <Badge variant="secondary">{analytics?.notes_analytics.avg_notes_per_lead} por lead</Badge>
                </div>

                <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Phone className="w-5 h-5 text-green-500" />
                    <div>
                      <p className="font-medium">Ligações</p>
                      <p className="text-sm text-gray-600">{analytics?.calls_analytics.total_calls} chamadas</p>
                    </div>
                  </div>
                  <Badge variant="secondary">{analytics?.calls_analytics.success_rate}% sucesso</Badge>
                </div>

                <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Bot className="w-5 h-5 text-purple-500" />
                    <div>
                      <p className="font-medium">Smartbot</p>
                      <p className="text-sm text-gray-600">{analytics?.smartbot_analytics.total_messages} mensagens</p>
                    </div>
                  </div>
                  <Badge variant="secondary">{analytics?.smartbot_analytics.delivery_rate}% entrega</Badge>
                </div>

                <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Clock className="w-5 h-5 text-orange-500" />
                    <div>
                      <p className="font-medium">Automação</p>
                      <p className="text-sm text-gray-600">{analytics?.automation_analytics.total_tasks} tarefas</p>
                    </div>
                  </div>
                  <Badge variant="secondary">{analytics?.automation_analytics.completion_rate}% concluídas</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba Funil de Vendas */}
        <TabsContent value="funnel" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Funil de Conversão</CardTitle>
                <CardDescription>Análise de conversão por etapa</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analytics?.funnel_metrics.stages.map((stage, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium">{stage.name}</span>
                        <div className="text-right">
                          <span className="text-sm font-bold">{stage.count}</span>
                          <span className="text-xs text-gray-500 ml-2">({stage.conversion_rate}%)</span>
                        </div>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500" 
                          style={{ width: `${(stage.count / 45) * 100}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-gray-600">
                        Tempo médio: {stage.avg_time_in_stage} dias
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Gargalos Identificados</CardTitle>
                <CardDescription>Pontos de maior perda no funil</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analytics?.funnel_metrics.bottlenecks.map((bottleneck, index) => (
                    <div key={index} className="p-4 border border-red-200 rounded-lg bg-red-50">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-red-800">{bottleneck.stage}</h4>
                        <Badge variant="destructive">{bottleneck.drop_rate}% perda</Badge>
                      </div>
                      <div className="space-y-1">
                        <p className="text-sm text-red-700 font-medium">Sugestões de melhoria:</p>
                        {bottleneck.suggestions.map((suggestion, idx) => (
                          <p key={idx} className="text-xs text-red-600">• {suggestion}</p>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Tendências de Conversão</CardTitle>
              <CardDescription>Evolução do funil ao longo do tempo</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={analytics?.stage_analytics.conversion_trends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="novo" stackId="1" stroke="#4169E1" fill="#4169E1" />
                  <Area type="monotone" dataKey="qualificado" stackId="1" stroke="#10B981" fill="#10B981" />
                  <Area type="monotone" dataKey="proposta" stackId="1" stroke="#F59E0B" fill="#F59E0B" />
                  <Area type="monotone" dataKey="negociacao" stackId="1" stroke="#EF4444" fill="#EF4444" />
                  <Area type="monotone" dataKey="ganho" stackId="1" stroke="#8B5CF6" fill="#8B5CF6" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aba Performance por Usuário */}
        <TabsContent value="users" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Ranking de Performance</CardTitle>
              <CardDescription>Taxa de sucesso por usuário</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analytics?.user_performance
                  .sort((a, b) => b.success_rate - a.success_rate)
                  .map((user, index) => (
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
                        <p className="font-medium">{user.user_name}</p>
                        <p className="text-sm text-gray-600">
                          {user.leads_converted}/{user.leads_assigned} leads convertidos
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-jt-blue">{user.success_rate}%</div>
                      <div className="text-sm text-gray-600">
                        R$ {user.revenue_generated.toLocaleString('pt-BR')}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Tempo de Resposta Médio</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={analytics?.user_performance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="user_name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="avg_response_time" fill="#4169E1" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Receita Gerada por Usuário</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={analytics?.user_performance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="user_name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="revenue_generated" fill="#10B981" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba Receita e Projeções */}
        <TabsContent value="revenue" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-jt-blue">
                    R$ {analytics?.revenue_analytics.current_month.toLocaleString('pt-BR')}
                  </div>
                  <p className="text-sm text-gray-600">Receita Atual</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    +{analytics?.revenue_analytics.growth_rate}%
                  </div>
                  <p className="text-sm text-gray-600">Crescimento</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    R$ {analytics?.revenue_analytics.projected_next_month.toLocaleString('pt-BR')}
                  </div>
                  <p className="text-sm text-gray-600">Projeção Próximo Mês</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    R$ {analytics?.revenue_analytics.quarterly_projection.toLocaleString('pt-BR')}
                  </div>
                  <p className="text-sm text-gray-600">Projeção Trimestral</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Receita vs Projeção vs Meta</CardTitle>
                <CardDescription>Comparativo mensal</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RechartsLineChart data={analytics?.revenue_analytics.revenue_by_month}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="actual" stroke="#4169E1" strokeWidth={3} name="Real" />
                    <Line type="monotone" dataKey="projected" stroke="#10B981" strokeWidth={2} strokeDasharray="5 5" name="Projetado" />
                    <Line type="monotone" dataKey="target" stroke="#EF4444" strokeWidth={2} strokeDasharray="3 3" name="Meta" />
                  </RechartsLineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Receita por Fonte</CardTitle>
                <CardDescription>Distribuição de origem</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics?.revenue_analytics.revenue_by_source.map((source, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <span className="text-sm font-medium">{source.source}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-jt-blue h-2 rounded-full" 
                            style={{ width: `${source.percentage}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600">
                          R$ {source.amount.toLocaleString('pt-BR')}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba Volume por Etapa */}
        <TabsContent value="stages" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Volume por Etapa</CardTitle>
              <CardDescription>Comparativo com período anterior</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analytics?.stage_analytics.volume_by_stage.map((stage, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h4 className="font-medium">{stage.stage}</h4>
                      <p className="text-sm text-gray-600">
                        Tempo médio: {stage.avg_time} dias
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold">{stage.current_count}</div>
                      <div className={`text-sm ${
                        stage.change_percentage > 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {stage.change_percentage > 0 ? '↗' : '↘'} {Math.abs(stage.change_percentage)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Análise de Gargalos</CardTitle>
              <CardDescription>Identificação de pontos críticos</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics?.stage_analytics.volume_by_stage}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="stage" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="current_count" fill="#4169E1" name="Atual" />
                  <Bar dataKey="previous_count" fill="#94A3B8" name="Anterior" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aba Registros */}
        <TabsContent value="notes" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Usuários Mais Ativos</CardTitle>
                <CardDescription>Quem mais adiciona registros</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics?.notes_analytics.most_active_users.map((user, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <span className="text-sm font-medium">{user.name}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-jt-blue h-2 rounded-full" 
                            style={{ width: `${(user.count / 25) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600">{user.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Estatísticas de Registros</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-jt-blue">{analytics?.notes_analytics.total_notes}</div>
                  <p className="text-sm text-gray-600">Total de Notas</p>
                </div>
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <div className="text-xl font-bold text-green-600">{analytics?.notes_analytics.notes_this_week}</div>
                    <p className="text-xs text-gray-600">Esta Semana</p>
                  </div>
                  <div>
                    <div className="text-xl font-bold text-blue-600">{analytics?.notes_analytics.avg_notes_per_lead}</div>
                    <p className="text-xs text-gray-600">Média por Lead</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba Ligações */}
        <TabsContent value="calls" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Ligações por Horário</CardTitle>
                <CardDescription>Distribuição de chamadas ao longo do dia</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={analytics?.calls_analytics.calls_by_hour}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#4169E1" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Status das Ligações</CardTitle>
                <CardDescription>Distribuição por resultado</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <RechartsPieChart>
                    <Pie
                      data={analytics?.calls_analytics.calls_by_status}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="count"
                      nameKey="status"
                    >
                      {analytics?.calls_analytics.calls_by_status.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-jt-blue">{analytics?.calls_analytics.total_calls}</div>
                  <p className="text-sm text-gray-600">Total de Ligações</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{analytics?.calls_analytics.avg_call_duration}min</div>
                  <p className="text-sm text-gray-600">Duração Média</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{analytics?.calls_analytics.success_rate}%</div>
                  <p className="text-sm text-gray-600">Taxa de Sucesso</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba Smartbot */}
        <TabsContent value="smartbot" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Mensagens por Dia</CardTitle>
                <CardDescription>Enviadas vs Recebidas</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <AreaChart data={analytics?.smartbot_analytics.messages_by_day}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="sent" stackId="1" stroke="#4169E1" fill="#4169E1" />
                    <Area type="monotone" dataKey="received" stackId="1" stroke="#10B981" fill="#10B981" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Templates Mais Usados</CardTitle>
                <CardDescription>Distribuição de uso</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics?.smartbot_analytics.templates_usage.map((template, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <span className="text-sm font-medium">{template.template}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-purple-500 h-2 rounded-full" 
                            style={{ width: `${(template.count / 150) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600">{template.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-jt-blue">{analytics?.smartbot_analytics.total_messages}</div>
                  <p className="text-sm text-gray-600">Total de Mensagens</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{analytics?.smartbot_analytics.delivery_rate}%</div>
                  <p className="text-sm text-gray-600">Taxa de Entrega</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{analytics?.smartbot_analytics.response_rate}%</div>
                  <p className="text-sm text-gray-600">Taxa de Resposta</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{analytics?.smartbot_analytics.messages_this_week}</div>
                  <p className="text-sm text-gray-600">Esta Semana</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Aba Automação */}
        <TabsContent value="automation" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Tarefas por Tipo</CardTitle>
                <CardDescription>Distribuição de tipos de tarefa</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={analytics?.automation_analytics.tasks_by_type}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="type" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#F59E0B" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Status das Tarefas</CardTitle>
                <CardDescription>Progresso geral</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <RechartsPieChart>
                    <Pie
                      data={analytics?.automation_analytics.tasks_by_status}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="count"
                      nameKey="status"
                    >
                      {analytics?.automation_analytics.tasks_by_status.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-jt-blue">{analytics?.automation_analytics.total_tasks}</div>
                  <p className="text-sm text-gray-600">Total de Tarefas</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{analytics?.automation_analytics.completed_tasks}</div>
                  <p className="text-sm text-gray-600">Concluídas</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{analytics?.automation_analytics.pending_tasks}</div>
                  <p className="text-sm text-gray-600">Pendentes</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{analytics?.automation_analytics.completion_rate}%</div>
                  <p className="text-sm text-gray-600">Taxa de Conclusão</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DashboardAnalytics;

