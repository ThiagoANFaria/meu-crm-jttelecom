// Serviço de Analytics para Dashboard
import { api } from './api';

export interface AnalyticsFilters {
  start_date?: string;
  end_date?: string;
  user_id?: number;
  stage?: string;
  source?: string;
}

export interface FunnelMetrics {
  stages: Array<{
    name: string;
    count: number;
    conversion_rate: number;
    avg_time_in_stage: number;
  }>;
  bottlenecks: Array<{
    stage: string;
    drop_rate: number;
    suggestions: string[];
  }>;
}

export interface UserPerformance {
  user_name: string;
  leads_assigned: number;
  leads_converted: number;
  success_rate: number;
  avg_response_time: number;
  revenue_generated: number;
}

export interface RevenueAnalytics {
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
}

export interface StageAnalytics {
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
}

export interface AnalyticsOverview {
  total_leads: number;
  total_clients: number;
  conversion_rate: number;
  funnel_metrics: FunnelMetrics;
  user_performance: UserPerformance[];
  revenue_analytics: RevenueAnalytics;
  stage_analytics: StageAnalytics;
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
  performance_metrics: {
    lead_response_time: number;
    customer_satisfaction: number;
    team_productivity: number;
    revenue_growth: number;
  };
}

class AnalyticsService {
  /**
   * Busca overview completo de analytics
   */
  async getOverview(filters?: AnalyticsFilters): Promise<AnalyticsOverview> {
    try {
      const response = await api.get('/analytics/overview', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar overview de analytics:', error);
      throw error;
    }
  }

  /**
   * Busca métricas específicas do funil de vendas
   */
  async getFunnelMetrics(filters?: AnalyticsFilters): Promise<FunnelMetrics> {
    try {
      const response = await api.get('/analytics/funnel', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar métricas do funil:', error);
      throw error;
    }
  }

  /**
   * Busca performance detalhada por usuário
   */
  async getUserPerformance(filters?: AnalyticsFilters): Promise<UserPerformance[]> {
    try {
      const response = await api.get('/analytics/users', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar performance de usuários:', error);
      throw error;
    }
  }

  /**
   * Busca analytics de receita e projeções
   */
  async getRevenueAnalytics(filters?: AnalyticsFilters): Promise<RevenueAnalytics> {
    try {
      const response = await api.get('/analytics/revenue', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar analytics de receita:', error);
      throw error;
    }
  }

  /**
   * Busca analytics de volume por etapa
   */
  async getStageAnalytics(filters?: AnalyticsFilters): Promise<StageAnalytics> {
    try {
      const response = await api.get('/analytics/stages', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar analytics de etapas:', error);
      throw error;
    }
  }

  /**
   * Busca métricas de conversão por período
   */
  async getConversionTrends(filters?: AnalyticsFilters) {
    try {
      const response = await api.get('/analytics/conversion-trends', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar tendências de conversão:', error);
      throw error;
    }
  }

  /**
   * Busca análise de gargalos no processo
   */
  async getBottleneckAnalysis(filters?: AnalyticsFilters) {
    try {
      const response = await api.get('/analytics/bottlenecks', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar análise de gargalos:', error);
      throw error;
    }
  }

  /**
   * Busca projeções de receita
   */
  async getRevenueProjections(months: number = 3) {
    try {
      const response = await api.get('/analytics/revenue-projections', { 
        params: { months } 
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar projeções de receita:', error);
      throw error;
    }
  }

  /**
   * Busca métricas de performance da equipe
   */
  async getTeamPerformance(filters?: AnalyticsFilters) {
    try {
      const response = await api.get('/analytics/team-performance', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar performance da equipe:', error);
      throw error;
    }
  }

  /**
   * Busca dados para gráficos específicos
   */
  async getChartData(chartType: string, filters?: AnalyticsFilters) {
    try {
      const response = await api.get(`/analytics/charts/${chartType}`, { params: filters });
      return response.data;
    } catch (error) {
      console.error(`Erro ao buscar dados do gráfico ${chartType}:`, error);
      throw error;
    }
  }

  /**
   * Exporta relatório de analytics
   */
  async exportReport(format: 'pdf' | 'excel', filters?: AnalyticsFilters) {
    try {
      const response = await api.get('/analytics/export', {
        params: { format, ...filters },
        responseType: 'blob'
      });
      
      // Criar download do arquivo
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `analytics-report.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return true;
    } catch (error) {
      console.error('Erro ao exportar relatório:', error);
      throw error;
    }
  }

  /**
   * Busca comparativo de períodos
   */
  async getPeriodComparison(
    currentPeriod: { start: string; end: string },
    previousPeriod: { start: string; end: string }
  ) {
    try {
      const response = await api.post('/analytics/period-comparison', {
        current_period: currentPeriod,
        previous_period: previousPeriod
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar comparativo de períodos:', error);
      throw error;
    }
  }

  /**
   * Busca insights automáticos baseados em IA
   */
  async getAIInsights(filters?: AnalyticsFilters) {
    try {
      const response = await api.get('/analytics/ai-insights', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar insights de IA:', error);
      throw error;
    }
  }
}

export const analyticsService = new AnalyticsService();
export default analyticsService;

