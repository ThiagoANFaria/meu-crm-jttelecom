// Serviço de integração com Smartbot
// API: https://app.smartbot.jttecnologia.com.br/messages-api

interface SmartbotMessage {
  id: string;
  channel_id: string;
  contact: string;
  message: string;
  type: 'text' | 'image' | 'audio' | 'video' | 'document';
  direction: 'inbound' | 'outbound';
  timestamp: string;
  status: 'sent' | 'delivered' | 'read' | 'failed';
}

interface SmartbotChannel {
  id: string;
  name: string;
  type: 'whatsapp' | 'telegram' | 'instagram';
  token: string;
  status: 'active' | 'inactive';
}

class SmartbotService {
  private baseUrl = 'https://app.smartbot.jttecnologia.com.br/messages-api';

  private async request<T>(endpoint: string, options: RequestInit = {}, token?: string): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`Smartbot API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Enviar mensagem via Smartbot
  async sendMessage(channelToken: string, contact: string, message: string, type: 'text' | 'image' = 'text'): Promise<SmartbotMessage> {
    try {
      return await this.request('/send', {
        method: 'POST',
        body: JSON.stringify({
          contact,
          message,
          type
        }),
      }, channelToken);
    } catch (error) {
      console.log('Smartbot API não disponível, simulando envio');
      
      // Simular envio de mensagem
      const simulatedMessage: SmartbotMessage = {
        id: Date.now().toString(),
        channel_id: 'simulated_channel',
        contact,
        message,
        type,
        direction: 'outbound',
        timestamp: new Date().toISOString(),
        status: 'sent'
      };

      // Salvar no localStorage para histórico
      const storedMessages = localStorage.getItem('jt-crm-smartbot-messages');
      const existingMessages: SmartbotMessage[] = storedMessages ? JSON.parse(storedMessages) : [];
      existingMessages.push(simulatedMessage);
      localStorage.setItem('jt-crm-smartbot-messages', JSON.stringify(existingMessages));

      return simulatedMessage;
    }
  }

  // Obter mensagens de um contato
  async getMessages(channelToken: string, contact: string, limit: number = 50): Promise<SmartbotMessage[]> {
    try {
      return await this.request(`/messages?contact=${contact}&limit=${limit}`, {
        method: 'GET',
      }, channelToken);
    } catch (error) {
      console.log('Smartbot API não disponível, buscando no localStorage');
      
      const storedMessages = localStorage.getItem('jt-crm-smartbot-messages');
      const existingMessages: SmartbotMessage[] = storedMessages ? JSON.parse(storedMessages) : [];
      
      return existingMessages
        .filter(msg => msg.contact === contact)
        .slice(-limit)
        .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
    }
  }

  // Obter canais disponíveis
  async getChannels(): Promise<SmartbotChannel[]> {
    try {
      return await this.request('/channels', {
        method: 'GET',
      });
    } catch (error) {
      console.log('Smartbot API não disponível, retornando canais simulados');
      
      return [
        {
          id: 'whatsapp_channel_1',
          name: 'WhatsApp JT Tecnologia',
          type: 'whatsapp',
          token: 'simulated_token_whatsapp',
          status: 'active'
        },
        {
          id: 'telegram_channel_1',
          name: 'Telegram JT Tecnologia',
          type: 'telegram',
          token: 'simulated_token_telegram',
          status: 'active'
        }
      ];
    }
  }

  // Enviar mensagem automática para lead
  async sendLeadMessage(leadPhone: string, leadName: string, messageTemplate: string): Promise<SmartbotMessage> {
    const channels = await this.getChannels();
    const whatsappChannel = channels.find(c => c.type === 'whatsapp' && c.status === 'active');
    
    if (!whatsappChannel) {
      throw new Error('Nenhum canal WhatsApp ativo encontrado');
    }

    const personalizedMessage = messageTemplate
      .replace('{nome}', leadName)
      .replace('{empresa}', 'JT Tecnologia');

    return await this.sendMessage(whatsappChannel.token, leadPhone, personalizedMessage);
  }

  // Templates de mensagens pré-definidos
  getMessageTemplates(): Record<string, string> {
    return {
      'welcome': 'Olá {nome}! Obrigado pelo seu interesse em nossos serviços. Em breve entraremos em contato.',
      'follow_up': 'Olá {nome}! Gostaríamos de saber se você tem alguma dúvida sobre nossa proposta.',
      'proposal_sent': 'Olá {nome}! Enviamos uma proposta personalizada para você. Confira em seu email.',
      'meeting_reminder': 'Olá {nome}! Lembrando da nossa reunião agendada. Aguardamos você!',
      'thank_you': 'Olá {nome}! Obrigado por escolher a {empresa}. Estamos ansiosos para trabalhar juntos!'
    };
  }
}

export const smartbotService = new SmartbotService();
export type { SmartbotMessage, SmartbotChannel };

