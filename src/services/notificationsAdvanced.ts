export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'lead' | 'call' | 'message' | 'task' | 'sale' | 'warning' | 'error' | 'success' | 'info';
  read: boolean;
  createdAt: string;
  actionUrl?: string;
  metadata?: Record<string, any>;
}

export interface NotificationSettings {
  soundEnabled: boolean;
  browserNotifications: boolean;
  emailNotifications: boolean;
  leadNotifications: boolean;
  callNotifications: boolean;
  taskNotifications: boolean;
  saleNotifications: boolean;
  quietHours: {
    enabled: boolean;
    start: string;
    end: string;
  };
}

export interface NotificationTemplate {
  id: string;
  name: string;
  type: string;
  title: string;
  message: string;
  enabled: boolean;
}

class NotificationService {
  private baseUrl = '/api/notifications';
  private wsConnection: WebSocket | null = null;
  private eventListeners: Map<string, Function[]> = new Map();

  // Gerenciamento de notificações
  async getNotifications(limit: number = 50, offset: number = 0): Promise<Notification[]> {
    try {
      const response = await fetch(`${this.baseUrl}?limit=${limit}&offset=${offset}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch notifications');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching notifications:', error);
      throw error;
    }
  }

  async markAsRead(notificationId: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/${notificationId}/read`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to mark notification as read');
      }
    } catch (error) {
      console.error('Error marking notification as read:', error);
      throw error;
    }
  }

  async markAllAsRead(): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/read-all`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to mark all notifications as read');
      }
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
      throw error;
    }
  }

  async deleteNotification(notificationId: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/${notificationId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete notification');
      }
    } catch (error) {
      console.error('Error deleting notification:', error);
      throw error;
    }
  }

  async createNotification(notification: Omit<Notification, 'id' | 'createdAt' | 'read'>): Promise<Notification> {
    try {
      const response = await fetch(this.baseUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(notification)
      });

      if (!response.ok) {
        throw new Error('Failed to create notification');
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating notification:', error);
      throw error;
    }
  }

  // Configurações
  async getSettings(): Promise<NotificationSettings> {
    try {
      const response = await fetch(`${this.baseUrl}/settings`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch notification settings');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching notification settings:', error);
      throw error;
    }
  }

  async updateSettings(settings: Partial<NotificationSettings>): Promise<NotificationSettings> {
    try {
      const response = await fetch(`${this.baseUrl}/settings`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(settings)
      });

      if (!response.ok) {
        throw new Error('Failed to update notification settings');
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating notification settings:', error);
      throw error;
    }
  }

  // Templates de notificação
  async getTemplates(): Promise<NotificationTemplate[]> {
    try {
      const response = await fetch(`${this.baseUrl}/templates`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch notification templates');
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching notification templates:', error);
      throw error;
    }
  }

  async updateTemplate(templateId: string, template: Partial<NotificationTemplate>): Promise<NotificationTemplate> {
    try {
      const response = await fetch(`${this.baseUrl}/templates/${templateId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(template)
      });

      if (!response.ok) {
        throw new Error('Failed to update notification template');
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating notification template:', error);
      throw error;
    }
  }

  // WebSocket para notificações em tempo real
  connectWebSocket(userId: string): void {
    try {
      const wsUrl = `ws://localhost:8080/ws/notifications/${userId}`;
      this.wsConnection = new WebSocket(wsUrl);

      this.wsConnection.onopen = () => {
        console.log('WebSocket connected for notifications');
        this.emit('connected');
      };

      this.wsConnection.onmessage = (event) => {
        try {
          const notification: Notification = JSON.parse(event.data);
          this.emit('notification', notification);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.wsConnection.onclose = () => {
        console.log('WebSocket disconnected');
        this.emit('disconnected');
        
        // Tentar reconectar após 5 segundos
        setTimeout(() => {
          this.connectWebSocket(userId);
        }, 5000);
      };

      this.wsConnection.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.emit('error', error);
      };
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
    }
  }

  disconnectWebSocket(): void {
    if (this.wsConnection) {
      this.wsConnection.close();
      this.wsConnection = null;
    }
  }

  // Sistema de eventos
  on(event: string, callback: Function): void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event)!.push(callback);
  }

  off(event: string, callback: Function): void {
    const listeners = this.eventListeners.get(event);
    if (listeners) {
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  private emit(event: string, data?: any): void {
    const listeners = this.eventListeners.get(event);
    if (listeners) {
      listeners.forEach(callback => callback(data));
    }
  }

  // Notificações específicas do CRM
  async notifyNewLead(leadData: any): Promise<void> {
    const notification = {
      title: 'Novo Lead',
      message: `${leadData.name} demonstrou interesse em seus serviços`,
      type: 'lead' as const,
      actionUrl: `/leads/${leadData.id}`,
      metadata: { leadId: leadData.id }
    };

    await this.createNotification(notification);
  }

  async notifyMissedCall(callData: any): Promise<void> {
    const notification = {
      title: 'Ligação Perdida',
      message: `${callData.caller} tentou ligar às ${callData.time}`,
      type: 'call' as const,
      actionUrl: '/telephony',
      metadata: { callId: callData.id }
    };

    await this.createNotification(notification);
  }

  async notifyTaskDue(taskData: any): Promise<void> {
    const notification = {
      title: 'Tarefa Vencida',
      message: `${taskData.title} venceu em ${taskData.dueDate}`,
      type: 'warning' as const,
      actionUrl: `/tasks/${taskData.id}`,
      metadata: { taskId: taskData.id }
    };

    await this.createNotification(notification);
  }

  async notifyNewMessage(messageData: any): Promise<void> {
    const notification = {
      title: 'Nova Mensagem',
      message: `${messageData.sender}: ${messageData.preview}`,
      type: 'message' as const,
      actionUrl: `/messages/${messageData.id}`,
      metadata: { messageId: messageData.id }
    };

    await this.createNotification(notification);
  }

  async notifyStatusChange(entityType: string, entityData: any): Promise<void> {
    const notification = {
      title: 'Status Atualizado',
      message: `${entityType} ${entityData.name} mudou para ${entityData.status}`,
      type: 'info' as const,
      actionUrl: `/${entityType}s/${entityData.id}`,
      metadata: { entityType, entityId: entityData.id }
    };

    await this.createNotification(notification);
  }

  // Utilitários
  async getUnreadCount(): Promise<number> {
    try {
      const response = await fetch(`${this.baseUrl}/unread-count`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch unread count');
      }

      const data = await response.json();
      return data.count;
    } catch (error) {
      console.error('Error fetching unread count:', error);
      return 0;
    }
  }

  async requestBrowserPermission(): Promise<NotificationPermission> {
    if ('Notification' in window) {
      return await Notification.requestPermission();
    }
    return 'denied';
  }

  showBrowserNotification(title: string, options?: NotificationOptions): void {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, {
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        ...options
      });
    }
  }

  isQuietHours(settings: NotificationSettings): boolean {
    if (!settings.quietHours.enabled) return false;

    const now = new Date();
    const currentTime = now.getHours() * 60 + now.getMinutes();
    
    const [startHour, startMin] = settings.quietHours.start.split(':').map(Number);
    const [endHour, endMin] = settings.quietHours.end.split(':').map(Number);
    
    const startTime = startHour * 60 + startMin;
    const endTime = endHour * 60 + endMin;

    if (startTime <= endTime) {
      return currentTime >= startTime && currentTime <= endTime;
    } else {
      // Período que cruza meia-noite
      return currentTime >= startTime || currentTime <= endTime;
    }
  }
}

export const notificationService = new NotificationService();

