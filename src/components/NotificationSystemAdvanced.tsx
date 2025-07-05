import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Bell,
  BellRing,
  Check,
  X,
  Settings,
  UserPlus,
  Phone,
  MessageSquare,
  Calendar,
  DollarSign,
  AlertTriangle,
  Info,
  CheckCircle,
  Clock,
  Trash2,
  MarkAsUnread,
  Volume2,
  VolumeX
} from 'lucide-react';
import { notificationService, Notification, NotificationSettings } from '@/services/notificationsAdvanced';
import { useToast } from '@/hooks/use-toast';
import { useTenant } from '@/contexts/TenantContext';

interface NotificationSystemAdvancedProps {
  userId?: string;
}

const NotificationSystemAdvanced: React.FC<NotificationSystemAdvancedProps> = ({ userId }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [settings, setSettings] = useState<NotificationSettings | null>(null);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const { toast } = useToast();
  const { currentTenant } = useTenant();

  useEffect(() => {
    if (currentTenant) {
      loadNotifications();
      loadSettings();
      setupWebSocket();
      setupAudio();

      // Verificar novas notificações a cada 30 segundos
      const interval = setInterval(loadNotifications, 30000);

      return () => {
        clearInterval(interval);
        if (audioRef.current) {
          audioRef.current.remove();
        }
      };
    }
  }, [userId, currentTenant]);

  const setupAudio = () => {
    audioRef.current = new Audio('/notification-sound.mp3');
    audioRef.current.volume = 0.5;
  };

  const playNotificationSound = () => {
    if (soundEnabled && audioRef.current) {
      audioRef.current.play().catch(console.error);
    }
  };

  const setupWebSocket = () => {
    if (!currentTenant) return;

    // Implementar WebSocket para notificações em tempo real específicas do tenant
    try {
      const ws = new WebSocket(`ws://localhost:8080/ws/notifications/${userId}/${currentTenant.id}`);
      
      ws.onmessage = (event) => {
        const notification: Notification = JSON.parse(event.data);
        // Verificar se a notificação pertence ao tenant atual
        if (notification.tenantId === currentTenant.id) {
          handleNewNotification(notification);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      return () => ws.close();
    } catch (error) {
      console.error('Failed to setup WebSocket:', error);
    }
  };

  const loadNotifications = async () => {
    if (!currentTenant) return;

    try {
      const data = await notificationService.getNotifications({ tenantId: currentTenant.id });
      setNotifications(data);
      setUnreadCount(data.filter(n => !n.read).length);
    } catch (error) {
      console.error('Failed to load notifications:', error);
      // Usar dados mock específicos do tenant em caso de erro
      const mockNotifications = getMockNotifications();
      setNotifications(mockNotifications);
      setUnreadCount(mockNotifications.filter(n => !n.read).length);
    }
  };

  const loadSettings = async () => {
    try {
      const data = await notificationService.getSettings();
      setSettings(data);
      setSoundEnabled(data.soundEnabled);
    } catch (error) {
      console.error('Failed to load settings:', error);
      setSettings(getDefaultSettings());
    }
  };

  const handleNewNotification = (notification: Notification) => {
    setNotifications(prev => [notification, ...prev]);
    setUnreadCount(prev => prev + 1);
    
    // Tocar som se habilitado
    playNotificationSound();
    
    // Mostrar toast
    toast({
      title: notification.title,
      description: notification.message,
      variant: notification.type === 'error' ? 'destructive' : 'default',
    });

    // Notificação do browser se permitida
    if (Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/favicon.ico'
      });
    }
  };

  const markAsRead = async (notificationId: string) => {
    try {
      await notificationService.markAsRead(notificationId);
      setNotifications(prev => 
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
      console.error('Failed to mark as read:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await notificationService.markAllAsRead();
      setNotifications(prev => prev.map(n => ({ ...n, read: true })));
      setUnreadCount(0);
    } catch (error) {
      console.error('Failed to mark all as read:', error);
    }
  };

  const deleteNotification = async (notificationId: string) => {
    try {
      await notificationService.deleteNotification(notificationId);
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
      setUnreadCount(prev => {
        const notification = notifications.find(n => n.id === notificationId);
        return notification && !notification.read ? prev - 1 : prev;
      });
    } catch (error) {
      console.error('Failed to delete notification:', error);
    }
  };

  const updateSettings = async (newSettings: Partial<NotificationSettings>) => {
    try {
      const updated = await notificationService.updateSettings(newSettings);
      setSettings(updated);
      setSoundEnabled(updated.soundEnabled);
      toast({
        title: 'Configurações atualizadas',
        description: 'Suas preferências de notificação foram salvas.',
      });
    } catch (error) {
      console.error('Failed to update settings:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível salvar as configurações.',
        variant: 'destructive',
      });
    }
  };

  const requestNotificationPermission = async () => {
    if ('Notification' in window && Notification.permission === 'default') {
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        toast({
          title: 'Notificações habilitadas',
          description: 'Você receberá notificações do browser.',
        });
      }
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'lead': return <UserPlus className="w-4 h-4 text-blue-500" />;
      case 'call': return <Phone className="w-4 h-4 text-green-500" />;
      case 'message': return <MessageSquare className="w-4 h-4 text-purple-500" />;
      case 'task': return <Calendar className="w-4 h-4 text-orange-500" />;
      case 'sale': return <DollarSign className="w-4 h-4 text-emerald-500" />;
      case 'warning': return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      case 'error': return <X className="w-4 h-4 text-red-500" />;
      case 'success': return <CheckCircle className="w-4 h-4 text-green-500" />;
      default: return <Info className="w-4 h-4 text-gray-500" />;
    }
  };

  const getTimeAgo = (date: string) => {
    const now = new Date();
    const notificationDate = new Date(date);
    const diffInMinutes = Math.floor((now.getTime() - notificationDate.getTime()) / (1000 * 60));

    if (diffInMinutes < 1) return 'Agora';
    if (diffInMinutes < 60) return `${diffInMinutes}m`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h`;
    return `${Math.floor(diffInMinutes / 1440)}d`;
  };

  const getMockNotifications = (): Notification[] => [
    {
      id: '1',
      title: 'Novo Lead',
      message: 'João Silva se interessou pelos seus serviços',
      type: 'lead',
      read: false,
      createdAt: new Date().toISOString(),
      actionUrl: '/leads/1'
    },
    {
      id: '2',
      title: 'Ligação perdida',
      message: 'Maria Oliveira tentou ligar às 14:30',
      type: 'call',
      read: false,
      createdAt: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
      actionUrl: '/telephony'
    },
    {
      id: '3',
      title: 'Tarefa vencida',
      message: 'Follow-up com cliente ABC venceu ontem',
      type: 'warning',
      read: true,
      createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      actionUrl: '/tasks'
    }
  ];

  const getDefaultSettings = (): NotificationSettings => ({
    soundEnabled: true,
    browserNotifications: true,
    emailNotifications: true,
    leadNotifications: true,
    callNotifications: true,
    taskNotifications: true,
    saleNotifications: true,
    quietHours: {
      enabled: false,
      start: '22:00',
      end: '08:00'
    }
  });

  return (
    <>
      <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="sm" className="relative">
            {unreadCount > 0 ? (
              <BellRing className="h-5 w-5" />
            ) : (
              <Bell className="h-5 w-5" />
            )}
            {unreadCount > 0 && (
              <Badge 
                variant="destructive" 
                className="absolute -top-2 -right-2 h-5 w-5 flex items-center justify-center p-0 text-xs"
              >
                {unreadCount > 99 ? '99+' : unreadCount}
              </Badge>
            )}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-80">
          <DropdownMenuLabel className="flex items-center justify-between">
            <span>Notificações</span>
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSoundEnabled(!soundEnabled)}
                className="h-6 w-6 p-0"
              >
                {soundEnabled ? <Volume2 className="h-3 w-3" /> : <VolumeX className="h-3 w-3" />}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsSettingsOpen(true)}
                className="h-6 w-6 p-0"
              >
                <Settings className="h-3 w-3" />
              </Button>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          
          {unreadCount > 0 && (
            <>
              <DropdownMenuItem onClick={markAllAsRead} className="text-sm">
                <Check className="mr-2 h-4 w-4" />
                Marcar todas como lidas
              </DropdownMenuItem>
              <DropdownMenuSeparator />
            </>
          )}

          <ScrollArea className="h-96">
            {notifications.length === 0 ? (
              <div className="p-4 text-center text-sm text-gray-500">
                Nenhuma notificação
              </div>
            ) : (
              notifications.map((notification) => (
                <DropdownMenuItem
                  key={notification.id}
                  className={`p-3 cursor-pointer ${!notification.read ? 'bg-blue-50' : ''}`}
                  onClick={() => {
                    if (!notification.read) {
                      markAsRead(notification.id);
                    }
                    if (notification.actionUrl) {
                      window.location.href = notification.actionUrl;
                    }
                  }}
                >
                  <div className="flex items-start gap-3 w-full">
                    <div className="flex-shrink-0 mt-0.5">
                      {getNotificationIcon(notification.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium truncate">
                          {notification.title}
                        </p>
                        <div className="flex items-center gap-1">
                          <span className="text-xs text-gray-500">
                            {getTimeAgo(notification.createdAt)}
                          </span>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteNotification(notification.id);
                            }}
                            className="h-4 w-4 p-0 opacity-0 group-hover:opacity-100"
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                      <p className="text-xs text-gray-600 mt-1">
                        {notification.message}
                      </p>
                      {!notification.read && (
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-1"></div>
                      )}
                    </div>
                  </div>
                </DropdownMenuItem>
              ))
            )}
          </ScrollArea>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Settings Dialog */}
      <Dialog open={isSettingsOpen} onOpenChange={setIsSettingsOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Configurações de Notificação</DialogTitle>
            <DialogDescription>
              Personalize como você recebe notificações
            </DialogDescription>
          </DialogHeader>
          
          {settings && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Som</label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateSettings({ soundEnabled: !settings.soundEnabled })}
                >
                  {settings.soundEnabled ? 'Ligado' : 'Desligado'}
                </Button>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Notificações do Browser</label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    if (!settings.browserNotifications) {
                      requestNotificationPermission();
                    }
                    updateSettings({ browserNotifications: !settings.browserNotifications });
                  }}
                >
                  {settings.browserNotifications ? 'Ligado' : 'Desligado'}
                </Button>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Novos Leads</label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateSettings({ leadNotifications: !settings.leadNotifications })}
                >
                  {settings.leadNotifications ? 'Ligado' : 'Desligado'}
                </Button>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Ligações</label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateSettings({ callNotifications: !settings.callNotifications })}
                >
                  {settings.callNotifications ? 'Ligado' : 'Desligado'}
                </Button>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Tarefas</label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateSettings({ taskNotifications: !settings.taskNotifications })}
                >
                  {settings.taskNotifications ? 'Ligado' : 'Desligado'}
                </Button>
              </div>
            </div>
          )}
          
          <DialogFooter>
            <Button onClick={() => setIsSettingsOpen(false)}>
              Fechar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default NotificationSystemAdvanced;

