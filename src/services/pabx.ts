// Serviço de integração com PABX em Nuvem
// API: https://emnuvem.meupabxip.com.br/suite/api

interface PabxCall {
  id: string;
  caller: string;
  called: string;
  start_time: string;
  end_time?: string;
  duration?: number;
  status: 'ringing' | 'answered' | 'busy' | 'no_answer' | 'failed' | 'completed';
  direction: 'inbound' | 'outbound';
  recording_url?: string;
  cost?: number;
  extension?: string;
}

interface PabxExtension {
  id: string;
  number: string;
  name: string;
  status: 'online' | 'offline' | 'busy' | 'away';
  department?: string;
}

interface PabxCallRequest {
  extension: string;
  phone: string;
  caller_id?: string;
}

class PabxService {
  private baseUrl = 'https://emnuvem.meupabxip.com.br/suite/api';
  private authUser = 'jt_tecnologia'; // Configurar conforme necessário
  private authToken = 'your_auth_token'; // Configurar conforme necessário

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    // Adicionar autenticação via parâmetros URL conforme documentação
    const separator = endpoint.includes('?') ? '&' : '?';
    const authenticatedUrl = `${url}${separator}autenticacao_usuario=${this.authUser}&autenticacao_token=${this.authToken}`;
    
    const response = await fetch(authenticatedUrl, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`PABX API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Realizar chamada (Click2Call)
  async makeCall(extension: string, phone: string, callerId?: string): Promise<{ call_id: string; status: string }> {
    try {
      const response = await this.request<{ call_id: string; status: string }>('/discar_numero', {
        method: 'POST',
        body: JSON.stringify({
          ramal: extension,
          numero: phone,
          caller_id: callerId || 'JT Tecnologia'
        }),
      });

      return response;
    } catch (error) {
      console.log('PABX API não disponível, simulando chamada');
      
      // Simular chamada
      const simulatedCall = {
        call_id: Date.now().toString(),
        status: 'initiated'
      };

      // Salvar no localStorage para histórico
      const callRecord: PabxCall = {
        id: simulatedCall.call_id,
        caller: extension,
        called: phone,
        start_time: new Date().toISOString(),
        status: 'ringing',
        direction: 'outbound',
        extension: extension
      };

      const storedCalls = localStorage.getItem('jt-crm-pabx-calls');
      const existingCalls: PabxCall[] = storedCalls ? JSON.parse(storedCalls) : [];
      existingCalls.push(callRecord);
      localStorage.setItem('jt-crm-pabx-calls', JSON.stringify(existingCalls));

      return simulatedCall;
    }
  }

  // Obter histórico de chamadas
  async getCallHistory(startDate?: string, endDate?: string, phone?: string): Promise<PabxCall[]> {
    try {
      let endpoint = '/listar_historico_chamada';
      const params = new URLSearchParams();
      
      if (startDate) params.append('data_inicio', startDate);
      if (endDate) params.append('data_fim', endDate);
      if (phone) params.append('numero', phone);
      
      if (params.toString()) {
        endpoint += `?${params.toString()}`;
      }

      return await this.request<PabxCall[]>(endpoint);
    } catch (error) {
      console.log('PABX API não disponível, buscando no localStorage');
      
      const storedCalls = localStorage.getItem('jt-crm-pabx-calls');
      const existingCalls: PabxCall[] = storedCalls ? JSON.parse(storedCalls) : [];
      
      let filteredCalls = existingCalls;
      
      if (phone) {
        filteredCalls = filteredCalls.filter(call => 
          call.caller.includes(phone) || call.called.includes(phone)
        );
      }
      
      if (startDate) {
        filteredCalls = filteredCalls.filter(call => 
          new Date(call.start_time) >= new Date(startDate)
        );
      }
      
      if (endDate) {
        filteredCalls = filteredCalls.filter(call => 
          new Date(call.start_time) <= new Date(endDate)
        );
      }
      
      return filteredCalls.sort((a, b) => 
        new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
      );
    }
  }

  // Obter chamadas online (em andamento)
  async getOnlineCalls(): Promise<PabxCall[]> {
    try {
      return await this.request<PabxCall[]>('/listar_chamadas_online');
    } catch (error) {
      console.log('PABX API não disponível, retornando chamadas vazias');
      return [];
    }
  }

  // Obter ramais disponíveis
  async getExtensions(): Promise<PabxExtension[]> {
    try {
      return await this.request<PabxExtension[]>('/listar_ramais');
    } catch (error) {
      console.log('PABX API não disponível, retornando ramais simulados');
      
      return [
        {
          id: '1001',
          number: '1001',
          name: 'Vendas 1',
          status: 'online',
          department: 'Vendas'
        },
        {
          id: '1002',
          number: '1002',
          name: 'Vendas 2',
          status: 'online',
          department: 'Vendas'
        },
        {
          id: '2001',
          number: '2001',
          name: 'Suporte 1',
          status: 'offline',
          department: 'Suporte'
        }
      ];
    }
  }

  // Obter histórico de chamadas de um lead específico
  async getLeadCallHistory(leadPhone: string): Promise<PabxCall[]> {
    // Limpar formatação do telefone para busca
    const cleanPhone = leadPhone.replace(/\D/g, '');
    
    const allCalls = await this.getCallHistory();
    
    return allCalls.filter(call => {
      const cleanCaller = call.caller.replace(/\D/g, '');
      const cleanCalled = call.called.replace(/\D/g, '');
      
      return cleanCaller.includes(cleanPhone) || cleanCalled.includes(cleanPhone);
    });
  }

  // Formatar duração da chamada
  formatCallDuration(duration?: number): string {
    if (!duration) return '00:00';
    
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }

  // Obter estatísticas de chamadas
  async getCallStats(startDate?: string, endDate?: string): Promise<{
    total_calls: number;
    answered_calls: number;
    missed_calls: number;
    total_duration: number;
    average_duration: number;
  }> {
    const calls = await this.getCallHistory(startDate, endDate);
    
    const answeredCalls = calls.filter(call => call.status === 'completed' || call.status === 'answered');
    const missedCalls = calls.filter(call => call.status === 'no_answer' || call.status === 'busy');
    
    const totalDuration = answeredCalls.reduce((sum, call) => sum + (call.duration || 0), 0);
    const averageDuration = answeredCalls.length > 0 ? totalDuration / answeredCalls.length : 0;
    
    return {
      total_calls: calls.length,
      answered_calls: answeredCalls.length,
      missed_calls: missedCalls.length,
      total_duration: totalDuration,
      average_duration: Math.round(averageDuration)
    };
  }
}

export const pabxService = new PabxService();
export type { PabxCall, PabxExtension, PabxCallRequest };

