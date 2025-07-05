import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Bell, 
  X, 
  Phone, 
  MessageSquare, 
  UserPlus, 
  DollarSign, 
  Calendar,
  AlertTriangle,
  CheckCircle,
  Info,
  Clock,
  Settings,
  Volume2,
  VolumeX
} from 'lucide-react';

export interface Notification {
  id: string;
  type: 'lead' | 'call' | 'message' | 'task' | 'system' | 'revenue' | 'alert';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  action?: {
    label: string;
    url?: string;
    callback?: () => void;
  };
  data?: any;
}

interface NotificationSystemProps {
  className?: string;
}

const NotificationSystem: React.FC<NotificationSystemProps> = ({ className }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [unreadCount, setUnreadCount] = useState(0);
  const audioRef = useRef<HTMLAudioElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Inicializar WebSocket para notificações em tempo real
    initializeWebSocket();
    
    // Carregar notificações existentes
    loadNotifications();

    // Solicitar permissão para notificações do navegador
    requestNotificationPermission();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    const unread = notifications.filter(n => !n.read).length;
    setUnreadCount(unread);
  }, [notifications]);

  const initializeWebSocket = () => {
    try {
      // Em produção, usar wss://api.jttecnologia.com.br/ws
      const wsUrl = process.env.NODE_ENV === 'production' 
        ? 'wss://api.jttecnologia.com.br/ws/notifications'
        : 'ws://localhost:3001/ws/notifications';
      
      wsRef.current = new WebSocket(wsUrl);
      
      wsRef.current.onopen = () => {
        console.log('WebSocket conectado para notificações');
      };
      
      wsRef.current.onmessage = (event) => {
        const notification: Notification = JSON.parse(event.data);
        addNotification(notification);
      };
      
      wsRef.current.onclose = () => {
        console.log('WebSocket desconectado. Tentando reconectar...');
        // Reconectar após 5 segundos
        setTimeout(initializeWebSocket, 5000);
      };
      
      wsRef.current.onerror = (error) => {
        console.error('Erro no WebSocket:', error);
      };
    } catch (error) {
      console.error('Erro ao inicializar WebSocket:', error);
      // Fallback para polling se WebSocket falhar
      startPolling();
    }
  };

  const startPolling = () => {
    // Polling como fallback (verificar a cada 30 segundos)
    setInterval(async () => {
      try {
        const response = await fetch('/api/notifications/recent');
        const newNotifications = await response.json();
        
        newNotifications.forEach((notification: Notification) => {
          if (!notifications.find(n => n.id === notification.id)) {
            addNotification(notification);
          }
        });
      } catch (error) {
        console.error('Erro no polling de notificações:', error);
      }
    }, 30000);
  };

  const loadNotifications = async () => {
    try {
      // Carregar notificações dos últimos 7 dias
      const response = await fetch('/api/notifications?days=7');
      const data = await response.json();
      setNotifications(data.map((n: any) => ({
        ...n,
        timestamp: new Date(n.timestamp)
      })));
    } catch (error) {
      console.error('Erro ao carregar notificações:', error);
      // Dados mock para desenvolvimento
      setNotifications([
        {
          id: '1',
          type: 'lead',
          title: 'Novo Lead',
          message: 'João Silva se interessou pelo produto Premium',
          timestamp: new Date(Date.now() - 5 * 60 * 1000),
          read: false,
          priority: 'high',
          action: {
            label: 'Ver Lead',
            url: '/leads/123'
          }
        },
        {
          id: '2',
          type: 'call',
          title: 'Ligação Perdida',
          message: 'Maria Santos tentou ligar mas não atendeu',
          timestamp: new Date(Date.now() - 15 * 60 * 1000),
          read: false,
          priority: 'medium',
          action: {
            label: 'Retornar Ligação',
            callback: () => console.log('Retornando ligação...')
          }
        },
        {
          id: '3',
          type: 'revenue',
          title: 'Meta Atingida!',
          message: 'Parabéns! Você atingiu 120% da meta mensal',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
          read: true,
          priority: 'high'
        }
      ]);
    }
  };

  const requestNotificationPermission = async () => {
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission();
    }
  };

  const addNotification = (notification: Notification) => {
    setNotifications(prev => [notification, ...prev]);
    
    // Tocar som se habilitado
    if (soundEnabled && audioRef.current) {
      audioRef.current.play().catch(console.error);
    }
    
    // Mostrar notificação do navegador
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/favicon.ico',
        tag: notification.id
      });
    }
  };

  const markAsRead = (id: string) => {
    setNotifications(prev => 
      prev.map(n => n.id === id ? { ...n, read: true } : n)
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(n => ({ ...n, read: true }))
    );
  };

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const clearAllNotifications = () => {
    setNotifications([]);
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'lead': return <UserPlus className="h-4 w-4" />;
      case 'call': return <Phone className="h-4 w-4" />;
      case 'message': return <MessageSquare className="h-4 w-4" />;
      case 'task': return <Calendar className="h-4 w-4" />;
      case 'revenue': return <DollarSign className="h-4 w-4" />;
      case 'alert': return <AlertTriangle className="h-4 w-4" />;
      case 'system': return <Info className="h-4 w-4" />;
      default: return <Bell className="h-4 w-4" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Agora';
    if (minutes < 60) return `${minutes}m atrás`;
    if (hours < 24) return `${hours}h atrás`;
    return `${days}d atrás`;
  };

  const handleNotificationAction = (notification: Notification) => {
    if (notification.action?.callback) {
      notification.action.callback();
    } else if (notification.action?.url) {
      window.location.href = notification.action.url;
    }
    markAsRead(notification.id);
  };

  return (
    <div className={`relative ${className}`}>
      {/* Botão de Notificações */}
      <Button
        variant="ghost"
        size="sm"
        className="relative"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Bell className="h-5 w-5" />
        {unreadCount > 0 && (
          <Badge 
            variant="destructive" 
            className="absolute -top-2 -right-2 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs"
          >
            {unreadCount > 99 ? '99+' : unreadCount}
          </Badge>
        )}
      </Button>

      {/* Painel de Notificações */}
      {isOpen && (
        <Card className="absolute right-0 top-12 w-96 max-h-96 shadow-lg z-50">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">Notificações</CardTitle>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSoundEnabled(!soundEnabled)}
                  title={soundEnabled ? 'Desativar som' : 'Ativar som'}
                >
                  {soundEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsOpen(false)}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>
            {unreadCount > 0 && (
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={markAllAsRead}>
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Marcar todas como lidas
                </Button>
                <Button variant="outline" size="sm" onClick={clearAllNotifications}>
                  <X className="h-3 w-3 mr-1" />
                  Limpar todas
                </Button>
              </div>
            )}
          </CardHeader>
          
          <CardContent className="p-0">
            <ScrollArea className="h-80">
              {notifications.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  <Bell className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>Nenhuma notificação</p>
                </div>
              ) : (
                <div className="space-y-1">
                  {notifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`p-3 border-b hover:bg-gray-50 cursor-pointer ${
                        !notification.read ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                      }`}
                      onClick={() => markAsRead(notification.id)}
                    >
                      <div className="flex items-start gap-3">
                        <div className={`p-1 rounded-full text-white ${getPriorityColor(notification.priority)}`}>
                          {getNotificationIcon(notification.type)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <h4 className="text-sm font-medium truncate">
                              {notification.title}
                            </h4>
                            <div className="flex items-center gap-1">
                              <span className="text-xs text-gray-500">
                                {formatTimestamp(notification.timestamp)}
                              </span>
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-6 w-6 p-0"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  removeNotification(notification.id);
                                }}
                              >
                                <X className="h-3 w-3" />
                              </Button>
                            </div>
                          </div>
                          <p className="text-xs text-gray-600 mt-1">
                            {notification.message}
                          </p>
                          {notification.action && (
                            <Button
                              variant="outline"
                              size="sm"
                              className="mt-2 h-6 text-xs"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleNotificationAction(notification);
                              }}
                            >
                              {notification.action.label}
                            </Button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>
          </CardContent>
        </Card>
      )}

      {/* Audio para notificações */}
      <audio ref={audioRef} preload="auto">
        <source src="/notification-sound.mp3" type="audio/mpeg" />
        <source src="/notification-sound.wav" type="audio/wav" />
      </audio>
    </div>
  );
};

export default NotificationSystem;

