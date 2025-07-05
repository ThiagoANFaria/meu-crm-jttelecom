// Serviço de Notificações em Tempo Real
import { api } from './api';

export interface NotificationPreferences {
  email_notifications: boolean;
  push_notifications: boolean;
  sound_enabled: boolean;
  lead_notifications: boolean;
  call_notifications: boolean;
  message_notifications: boolean;
  task_notifications: boolean;
  system_notifications: boolean;
  quiet_hours: {
    enabled: boolean;
    start_time: string;
    end_time: string;
  };
}

export interface NotificationTemplate {
  id: string;
  type: string;
  title_template: string;
  message_template: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  enabled: boolean;
  conditions: {
    field: string;
    operator: string;
    value: any;
  }[];
}

export interface NotificationRule {
  id: string;
  name: string;
  description: string;
  trigger: string;
  conditions: any[];
  actions: {
    type: 'notification' | 'email' | 'webhook';
    template_id?: string;
    recipients?: string[];
    webhook_url?: string;
  }[];
  enabled: boolean;
}

class NotificationService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private listeners: Map<string, Function[]> = new Map();

  /**
   * Inicializa conexão WebSocket para notificações em tempo real
   */
  initializeWebSocket(userId: string) {
    try {
      const wsUrl = process.env.NODE_ENV === 'production' 
        ? `wss://api.jttecnologia.com.br/ws/notifications?user_id=${userId}`
        : `ws://localhost:3001/ws/notifications?user_id=${userId}`;
      
      this.ws = new WebSocket(wsUrl);
      
      this.ws.onopen = () => {
        console.log('WebSocket conectado para notificações');
        this.reconnectAttempts = 0;
        this.emit('connected');
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleWebSocketMessage(data);
        } catch (error) {
          console.error('Erro ao processar mensagem WebSocket:', error);
        }
      };
      
      this.ws.onclose = () => {
        console.log('WebSocket desconectado');
        this.emit('disconnected');
        this.attemptReconnect(userId);
      };
      
      this.ws.onerror = (error) => {
        console.error('Erro no WebSocket:', error);
        this.emit('error', error);
      };
    } catch (error) {
      console.error('Erro ao inicializar WebSocket:', error);
    }
  }

  /**
   * Tenta reconectar WebSocket
   */
  private attemptReconnect(userId: string) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      setTimeout(() => {
        console.log(`Tentativa de reconexão ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
        this.initializeWebSocket(userId);
      }, delay);
    } else {
      console.error('Máximo de tentativas de reconexão atingido');
      this.emit('max_reconnect_attempts');
    }
  }

  /**
   * Processa mensagens do WebSocket
   */
  private handleWebSocketMessage(data: any) {
    switch (data.type) {
      case 'notification':
        this.emit('notification', data.payload);
        break;
      case 'lead_update':
        this.emit('lead_update', data.payload);
        break;
      case 'call_event':
        this.emit('call_event', data.payload);
        break;
      case 'message_received':
        this.emit('message_received', data.payload);
        break;
      case 'task_reminder':
        this.emit('task_reminder', data.payload);
        break;
      case 'system_alert':
        this.emit('system_alert', data.payload);
        break;
      default:
        console.log('Tipo de mensagem desconhecido:', data.type);
    }
  }

  /**
   * Adiciona listener para eventos
   */
  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
  }

  /**
   * Remove listener de evento
   */
  off(event: string, callback: Function) {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      const index = eventListeners.indexOf(callback);
      if (index > -1) {
        eventListeners.splice(index, 1);
      }
    }
  }

  /**
   * Emite evento para listeners
   */
  private emit(event: string, data?: any) {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(callback => callback(data));
    }
  }

  /**
   * Fecha conexão WebSocket
   */
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Busca notificações do usuário
   */
  async getNotifications(filters?: {
    page?: number;
    limit?: number;
    unread_only?: boolean;
    type?: string;
    days?: number;
  }) {
    try {
      const response = await api.get('/notifications', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar notificações:', error);
      throw error;
    }
  }

  /**
   * Marca notificação como lida
   */
  async markAsRead(notificationId: string) {
    try {
      await api.patch(`/notifications/${notificationId}/read`);
      return true;
    } catch (error) {
      console.error('Erro ao marcar notificação como lida:', error);
      throw error;
    }
  }

  /**
   * Marca todas as notificações como lidas
   */
  async markAllAsRead() {
    try {
      await api.patch('/notifications/mark-all-read');
      return true;
    } catch (error) {
      console.error('Erro ao marcar todas as notificações como lidas:', error);
      throw error;
    }
  }

  /**
   * Remove notificação
   */
  async deleteNotification(notificationId: string) {
    try {
      await api.delete(`/notifications/${notificationId}`);
      return true;
    } catch (error) {
      console.error('Erro ao remover notificação:', error);
      throw error;
    }
  }

  /**
   * Remove todas as notificações
   */
  async clearAllNotifications() {
    try {
      await api.delete('/notifications/clear-all');
      return true;
    } catch (error) {
      console.error('Erro ao limpar todas as notificações:', error);
      throw error;
    }
  }

  /**
   * Busca preferências de notificação do usuário
   */
  async getPreferences(): Promise<NotificationPreferences> {
    try {
      const response = await api.get('/notifications/preferences');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar preferências:', error);
      throw error;
    }
  }

  /**
   * Atualiza preferências de notificação
   */
  async updatePreferences(preferences: Partial<NotificationPreferences>) {
    try {
      const response = await api.patch('/notifications/preferences', preferences);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar preferências:', error);
      throw error;
    }
  }

  /**
   * Cria nova notificação manual
   */
  async createNotification(notification: {
    title: string;
    message: string;
    type: string;
    priority: 'low' | 'medium' | 'high' | 'urgent';
    recipients?: string[];
    action?: {
      label: string;
      url?: string;
    };
  }) {
    try {
      const response = await api.post('/notifications', notification);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar notificação:', error);
      throw error;
    }
  }

  /**
   * Busca templates de notificação
   */
  async getTemplates(): Promise<NotificationTemplate[]> {
    try {
      const response = await api.get('/notifications/templates');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar templates:', error);
      throw error;
    }
  }

  /**
   * Cria novo template de notificação
   */
  async createTemplate(template: Omit<NotificationTemplate, 'id'>) {
    try {
      const response = await api.post('/notifications/templates', template);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar template:', error);
      throw error;
    }
  }

  /**
   * Atualiza template de notificação
   */
  async updateTemplate(templateId: string, template: Partial<NotificationTemplate>) {
    try {
      const response = await api.patch(`/notifications/templates/${templateId}`, template);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar template:', error);
      throw error;
    }
  }

  /**
   * Remove template de notificação
   */
  async deleteTemplate(templateId: string) {
    try {
      await api.delete(`/notifications/templates/${templateId}`);
      return true;
    } catch (error) {
      console.error('Erro ao remover template:', error);
      throw error;
    }
  }

  /**
   * Busca regras de notificação
   */
  async getRules(): Promise<NotificationRule[]> {
    try {
      const response = await api.get('/notifications/rules');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar regras:', error);
      throw error;
    }
  }

  /**
   * Cria nova regra de notificação
   */
  async createRule(rule: Omit<NotificationRule, 'id'>) {
    try {
      const response = await api.post('/notifications/rules', rule);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar regra:', error);
      throw error;
    }
  }

  /**
   * Atualiza regra de notificação
   */
  async updateRule(ruleId: string, rule: Partial<NotificationRule>) {
    try {
      const response = await api.patch(`/notifications/rules/${ruleId}`, rule);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar regra:', error);
      throw error;
    }
  }

  /**
   * Remove regra de notificação
   */
  async deleteRule(ruleId: string) {
    try {
      await api.delete(`/notifications/rules/${ruleId}`);
      return true;
    } catch (error) {
      console.error('Erro ao remover regra:', error);
      throw error;
    }
  }

  /**
   * Testa regra de notificação
   */
  async testRule(ruleId: string, testData: any) {
    try {
      const response = await api.post(`/notifications/rules/${ruleId}/test`, testData);
      return response.data;
    } catch (error) {
      console.error('Erro ao testar regra:', error);
      throw error;
    }
  }

  /**
   * Busca estatísticas de notificações
   */
  async getStatistics(period: 'day' | 'week' | 'month' = 'week') {
    try {
      const response = await api.get('/notifications/statistics', { 
        params: { period } 
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error);
      throw error;
    }
  }

  /**
   * Registra token de push notification
   */
  async registerPushToken(token: string, device_type: 'web' | 'mobile') {
    try {
      const response = await api.post('/notifications/push-token', {
        token,
        device_type
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao registrar token push:', error);
      throw error;
    }
  }

  /**
   * Envia notificação push de teste
   */
  async sendTestPush() {
    try {
      const response = await api.post('/notifications/test-push');
      return response.data;
    } catch (error) {
      console.error('Erro ao enviar push de teste:', error);
      throw error;
    }
  }

  /**
   * Solicita permissão para notificações do navegador
   */
  async requestBrowserPermission(): Promise<boolean> {
    if (!('Notification' in window)) {
      console.warn('Este navegador não suporta notificações');
      return false;
    }

    if (Notification.permission === 'granted') {
      return true;
    }

    if (Notification.permission === 'denied') {
      return false;
    }

    const permission = await Notification.requestPermission();
    return permission === 'granted';
  }

  /**
   * Mostra notificação do navegador
   */
  showBrowserNotification(title: string, options?: NotificationOptions) {
    if ('Notification' in window && Notification.permission === 'granted') {
      return new Notification(title, {
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        ...options
      });
    }
    return null;
  }

  /**
   * Agenda notificação para o futuro
   */
  async scheduleNotification(notification: {
    title: string;
    message: string;
    type: string;
    priority: 'low' | 'medium' | 'high' | 'urgent';
    scheduled_for: string; // ISO date string
    recipients?: string[];
  }) {
    try {
      const response = await api.post('/notifications/schedule', notification);
      return response.data;
    } catch (error) {
      console.error('Erro ao agendar notificação:', error);
      throw error;
    }
  }

  /**
   * Cancela notificação agendada
   */
  async cancelScheduledNotification(notificationId: string) {
    try {
      await api.delete(`/notifications/scheduled/${notificationId}`);
      return true;
    } catch (error) {
      console.error('Erro ao cancelar notificação agendada:', error);
      throw error;
    }
  }

  /**
   * Busca notificações agendadas
   */
  async getScheduledNotifications() {
    try {
      const response = await api.get('/notifications/scheduled');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar notificações agendadas:', error);
      throw error;
    }
  }
}

export const notificationService = new NotificationService();
export default notificationService;

