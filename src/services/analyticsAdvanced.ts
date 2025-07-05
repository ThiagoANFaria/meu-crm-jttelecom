import { apiService } from './api';

export interface AdvancedAnalyticsData {
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

export interface MetricFilter {
  period: string;
  startDate?: string;
  endDate?: string;
  userId?: string;
  stage?: string;
}

class AdvancedAnalyticsService {
  private baseUrl = '/api/analytics';

  async getAdvancedMetrics(period: string = '30d'): Promise<AdvancedAnalyticsData> {
    try {
      const response = await fetch(`${this.baseUrl}/advanced?period=${period}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch advanced analytics');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching advanced analytics:', error);
      throw error;
    }
  }

  async getOverviewMetrics(filter: MetricFilter): Promise<AdvancedAnalyticsData['overview']> {
    try {
      const queryParams = new URLSearchParams(filter as any).toString();
      const response = await fetch(`${this.baseUrl}/overview?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch overview metrics');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching overview metrics:', error);
      throw error;
    }
  }

  async getConversionMetrics(filter: MetricFilter): Promise<AdvancedAnalyticsData['leadMetrics']> {
    try {
      const queryParams = new URLSearchParams(filter as any).toString();
      const response = await fetch(`${this.baseUrl}/conversion?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch conversion metrics');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching conversion metrics:', error);
      throw error;
    }
  }

  async getVolumeAnalysis(filter: MetricFilter): Promise<AdvancedAnalyticsData['volumeAnalysis']> {
    try {
      const queryParams = new URLSearchParams(filter as any).toString();
      const response = await fetch(`${this.baseUrl}/volume?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch volume analysis');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching volume analysis:', error);
      throw error;
    }
  }

  async getRevenueProjection(filter: MetricFilter): Promise<AdvancedAnalyticsData['revenueProjection']> {
    try {
      const queryParams = new URLSearchParams(filter as any).toString();
      const response = await fetch(`${this.baseUrl}/revenue?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch revenue projection');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching revenue projection:', error);
      throw error;
    }
  }

  async exportAnalyticsData(filter: MetricFilter, format: 'csv' | 'xlsx' | 'pdf' = 'xlsx'): Promise<Blob> {
    try {
      const queryParams = new URLSearchParams({ ...filter, format } as any).toString();
      const response = await fetch(`${this.baseUrl}/export?${queryParams}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to export analytics data');
      }

      return await response.blob();
    } catch (error) {
      console.error('Error exporting analytics data:', error);
      throw error;
    }
  }

  async getBottleneckAnalysis(period: string = '30d'): Promise<Array<{
    stage: string;
    avgTime: number;
    bottleneckScore: number;
    recommendations: string[];
  }>> {
    try {
      const response = await fetch(`${this.baseUrl}/bottlenecks?period=${period}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch bottleneck analysis');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching bottleneck analysis:', error);
      throw error;
    }
  }

  async getUserPerformanceRanking(period: string = '30d'): Promise<Array<{
    userId: string;
    userName: string;
    leadsCount: number;
    conversionRate: number;
    revenue: number;
    rank: number;
    trend: 'up' | 'down' | 'stable';
  }>> {
    try {
      const response = await fetch(`${this.baseUrl}/user-performance?period=${period}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch user performance ranking');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching user performance ranking:', error);
      throw error;
    }
  }

  async getPredictiveAnalytics(period: string = '30d'): Promise<{
    nextMonthLeads: number;
    nextMonthRevenue: number;
    conversionTrend: 'increasing' | 'decreasing' | 'stable';
    recommendations: string[];
    confidence: number;
  }> {
    try {
      const response = await fetch(`${this.baseUrl}/predictive?period=${period}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch predictive analytics');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching predictive analytics:', error);
      throw error;
    }
  }

  // Métodos para cálculos locais quando a API não estiver disponível
  calculateConversionRate(leads: number, converted: number): number {
    return leads > 0 ? (converted / leads) * 100 : 0;
  }

  calculateGrowthRate(current: number, previous: number): number {
    return previous > 0 ? ((current - previous) / previous) * 100 : 0;
  }

  identifyBottlenecks(stageData: Array<{ stage: string; avgTime: number; count: number }>): Array<{ stage: string; bottleneck: boolean; severity: 'low' | 'medium' | 'high' }> {
    const avgTime = stageData.reduce((sum, stage) => sum + stage.avgTime, 0) / stageData.length;
    const threshold = avgTime * 1.5; // 50% acima da média

    return stageData.map(stage => ({
      stage: stage.stage,
      bottleneck: stage.avgTime > threshold,
      severity: stage.avgTime > threshold * 1.5 ? 'high' : stage.avgTime > threshold ? 'medium' : 'low'
    }));
  }

  formatMetricValue(value: number, type: 'currency' | 'percentage' | 'number'): string {
    switch (type) {
      case 'currency':
        return new Intl.NumberFormat('pt-BR', {
          style: 'currency',
          currency: 'BRL'
        }).format(value);
      case 'percentage':
        return `${value.toFixed(1)}%`;
      case 'number':
        return new Intl.NumberFormat('pt-BR').format(value);
      default:
        return value.toString();
    }
  }
}

export const advancedAnalyticsService = new AdvancedAnalyticsService();

