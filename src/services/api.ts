
import { User, Lead, Client, Proposal, Contract, Task, Pipeline, DashboardSummary } from '@/types';

// Suporte para ambas as variáveis de ambiente (Vite e Next.js)
const API_BASE_URL = 
  import.meta.env.VITE_API_BASE_URL || 
  process.env.NEXT_PUBLIC_API_URL || 
  'https://api.app.jttecnologia.com.br';

class ApiService {
  private getHeaders(): HeadersInit {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('API Request:', url, options);
    
    const response = await fetch(url, {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    });

    console.log('API Response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', response.status, errorText);
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log('API Response data:', data);
    return data;
  }

  // Auth endpoints baseados na documentação
  async login(email: string, password: string): Promise<{ access_token: string; message: string; user: User }> {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // Dashboard
  async getDashboardSummary(): Promise<DashboardSummary> {
    return this.request('/dashboard/summary');
  }

  // Leads
  async getLeads(): Promise<Lead[]> {
    try {
      const response = await this.request<{leads: Lead[], total: number}>('/leads/');
      return response.leads || [];
    } catch (error) {
      console.log('API não disponível, usando localStorage para getLeads');
      const storedLeads = localStorage.getItem('jt-crm-leads');
      return storedLeads ? JSON.parse(storedLeads) : [];
    }
  }

  async createLead(lead: Omit<Lead, 'id' | 'created_at'>): Promise<Lead> {
    try {
      const response = await this.request<{lead: Lead, message: string}>('/leads/', {
        method: 'POST',
        body: JSON.stringify(lead),
      });
      
      // Sempre salvar no localStorage mesmo quando API funciona
      const newLead = response.lead;
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      const updatedLeads = [...existingLeads, newLead];
      localStorage.setItem('jt-crm-leads', JSON.stringify(updatedLeads));
      
      return newLead;
    } catch (error) {
      console.log('API não disponível, salvando no localStorage');
      
      // Criar lead localmente
      const newLead: Lead = {
        ...lead,
        id: Date.now().toString(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      // Buscar leads existentes
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      
      // Adicionar novo lead
      const updatedLeads = [...existingLeads, newLead];
      localStorage.setItem('jt-crm-leads', JSON.stringify(updatedLeads));
      
      return newLead;
    }
  }

  async updateLead(id: string, lead: Partial<Lead>): Promise<Lead> {
    try {
      return this.request(`/leads/${id}`, {
        method: 'PUT',
        body: JSON.stringify(lead),
      });
    } catch (error) {
      console.log('API não disponível, atualizando no localStorage');
      
      // Buscar leads existentes
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      
      // Encontrar e atualizar lead
      const leadIndex = existingLeads.findIndex(l => l.id === id);
      if (leadIndex !== -1) {
        const updatedLead = {
          ...existingLeads[leadIndex],
          ...lead,
          updated_at: new Date().toISOString()
        };
        existingLeads[leadIndex] = updatedLead;
        localStorage.setItem('jt-crm-leads', JSON.stringify(existingLeads));
        return updatedLead;
      }
      
      throw new Error('Lead não encontrado');
    }
  }

  async deleteLead(id: string): Promise<void> {
    try {
      return this.request(`/leads/${id}`, {
        method: 'DELETE',
      });
    } catch (error) {
      console.log('API não disponível, removendo do localStorage');
      
      // Buscar leads existentes
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      
      // Remover lead
      const updatedLeads = existingLeads.filter(l => l.id !== id);
      localStorage.setItem('jt-crm-leads', JSON.stringify(updatedLeads));
    }
  }

  // Clients
  async getClients(): Promise<Client[]> {
    return this.request('/clients');
  }

  async createClient(client: Omit<Client, 'id' | 'created_at'>): Promise<Client> {
    return this.request('/clients', {
      method: 'POST',
      body: JSON.stringify(client),
    });
  }

  async updateClient(id: string, client: Partial<Client>): Promise<Client> {
    return this.request(`/clients/${id}`, {
      method: 'PUT',
      body: JSON.stringify(client),
    });
  }

  async deleteClient(id: string): Promise<void> {
    return this.request(`/clients/${id}`, {
      method: 'DELETE',
    });
  }

  // Proposals
  async getProposals(): Promise<Proposal[]> {
    return this.request('/proposals');
  }

  async createProposal(proposal: Omit<Proposal, 'id' | 'created_at' | 'updated_at'>): Promise<Proposal> {
    return this.request('/proposals', {
      method: 'POST',
      body: JSON.stringify(proposal),
    });
  }

  async updateProposal(id: string, proposal: Partial<Proposal>): Promise<Proposal> {
    return this.request(`/proposals/${id}`, {
      method: 'PUT',
      body: JSON.stringify(proposal),
    });
  }

  async deleteProposal(id: string): Promise<void> {
    return this.request(`/proposals/${id}`, {
      method: 'DELETE',
    });
  }

  async sendProposalByEmail(id: string): Promise<void> {
    return this.request(`/proposals/${id}/send-email`, {
      method: 'POST',
    });
  }

  async sendProposalByWhatsApp(id: string): Promise<void> {
    return this.request(`/proposals/${id}/send-whatsapp`, {
      method: 'POST',
    });
  }

  // Contracts
  async getContracts(): Promise<Contract[]> {
    return this.request('/contracts');
  }

  async createContract(contract: Omit<Contract, 'id' | 'created_at'>): Promise<Contract> {
    return this.request('/contracts', {
      method: 'POST',
      body: JSON.stringify(contract),
    });
  }

  async updateContract(id: string, contract: Partial<Contract>): Promise<Contract> {
    return this.request(`/contracts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(contract),
    });
  }

  async deleteContract(id: string): Promise<void> {
    return this.request(`/contracts/${id}`, {
      method: 'DELETE',
    });
  }

  // Tasks
  async getTasks(): Promise<Task[]> {
    return this.request('/tasks');
  }

  async createTask(task: Omit<Task, 'id' | 'created_at'>): Promise<Task> {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async updateTask(id: string, task: Partial<Task>): Promise<Task> {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(task),
    });
  }

  async deleteTask(id: string): Promise<void> {
    return this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  // Pipelines
  async getPipelines(): Promise<Pipeline[]> {
    return this.request('/pipelines');
  }

  async createPipeline(pipeline: Omit<Pipeline, 'id' | 'created_at' | 'updated_at'>): Promise<Pipeline> {
    return this.request('/pipelines', {
      method: 'POST',
      body: JSON.stringify(pipeline),
    });
  }

  async updatePipeline(id: string, pipeline: Partial<Pipeline>): Promise<Pipeline> {
    return this.request(`/pipelines/${id}`, {
      method: 'PUT',
      body: JSON.stringify(pipeline),
    });
  }

  async deletePipeline(id: string): Promise<void> {
    return this.request(`/pipelines/${id}`, {
      method: 'DELETE',
    });
  }

  // Chatbot
  async sendChatbotMessage(message: string): Promise<{ response: string }> {
    return this.request('/chatbot/message', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  // Telephony
  async makeCall(phone: string): Promise<{ call_id: string; status: string }> {
    return this.request('/telephony/call', {
      method: 'POST',
      body: JSON.stringify({ phone }),
    });
  }

  // Automation
  async triggerAutomation(trigger: string, data: any): Promise<{ status: string }> {
    return this.request('/automation/trigger', {
      method: 'POST',
      body: JSON.stringify({ trigger, data }),
    });
  }

  // ===== NOVAS FUNCIONALIDADES AVANÇADAS DE LEADS =====
  
  // Converter Lead em Cliente
  async convertLeadToClient(leadId: string): Promise<{ client: any; message: string }> {
    try {
      return this.request(`/leads/${leadId}/convert-to-client`, {
        method: 'POST',
      });
    } catch (error) {
      console.log('API não disponível, simulando conversão no localStorage');
      
      // Buscar leads existentes
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      
      // Encontrar lead
      const leadIndex = existingLeads.findIndex(l => l.id === leadId);
      if (leadIndex !== -1) {
        const lead = existingLeads[leadIndex];
        
        // Simular criação do cliente
        const newClient = {
          id: Date.now().toString(),
          name: lead.name,
          email: lead.email,
          phone: lead.phone,
          company: lead.company,
          status: 'Ativo',
          created_at: new Date().toISOString(),
          converted_from_lead: leadId
        };
        
        // Salvar cliente no localStorage
        const storedClients = localStorage.getItem('jt-crm-clients');
        const existingClients = storedClients ? JSON.parse(storedClients) : [];
        existingClients.push(newClient);
        localStorage.setItem('jt-crm-clients', JSON.stringify(existingClients));
        
        // Atualizar status do lead para "Convertido"
        existingLeads[leadIndex] = {
          ...lead,
          status: 'Convertido',
          updated_at: new Date().toISOString()
        };
        localStorage.setItem('jt-crm-leads', JSON.stringify(existingLeads));
        
        return { client: newClient, message: 'Lead convertido com sucesso!' };
      }
      
      throw new Error('Lead não encontrado');
    }
  }

  // Atualizar Status do Lead
  async updateLeadStatus(leadId: string, newStatus: string): Promise<Lead> {
    try {
      return this.request(`/leads/${leadId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status: newStatus }),
      });
    } catch (error) {
      console.log('API não disponível, atualizando status no localStorage');
      
      // Buscar leads existentes
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      
      // Encontrar e atualizar lead
      const leadIndex = existingLeads.findIndex(l => l.id === leadId);
      if (leadIndex !== -1) {
        const updatedLead = {
          ...existingLeads[leadIndex],
          status: newStatus,
          updated_at: new Date().toISOString()
        };
        existingLeads[leadIndex] = updatedLead;
        localStorage.setItem('jt-crm-leads', JSON.stringify(existingLeads));
        return updatedLead;
      }
      
      throw new Error('Lead não encontrado');
    }
  }

  // Adicionar Nota ao Lead
  async addLeadNote(leadId: string, note: string): Promise<{ message: string }> {
    try {
      return this.request(`/leads/${leadId}/notes`, {
        method: 'POST',
        body: JSON.stringify({ note }),
      });
    } catch (error) {
      console.log('API não disponível, adicionando nota no localStorage');
      
      // Buscar leads existentes
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      
      // Encontrar lead
      const leadIndex = existingLeads.findIndex(l => l.id === leadId);
      if (leadIndex !== -1) {
        const lead = existingLeads[leadIndex];
        
        // Adicionar nota
        const newNote = {
          id: Date.now().toString(),
          content: note,
          created_at: new Date().toISOString(),
          author: 'Usuário Atual'
        };
        
        const updatedLead = {
          ...lead,
          notes: [...(lead.notes || []), newNote],
          updated_at: new Date().toISOString()
        };
        
        existingLeads[leadIndex] = updatedLead;
        localStorage.setItem('jt-crm-leads', JSON.stringify(existingLeads));
        
        return { message: 'Nota adicionada com sucesso!' };
      }
      
      throw new Error('Lead não encontrado');
    }
  }

  // Obter Notas do Lead
  async getLeadNotes(leadId: string): Promise<any[]> {
    try {
      return this.request(`/leads/${leadId}/notes`);
    } catch (error) {
      console.log('API não disponível, buscando notas no localStorage');
      
      // Buscar leads existentes
      const storedLeads = localStorage.getItem('jt-crm-leads');
      const existingLeads: Lead[] = storedLeads ? JSON.parse(storedLeads) : [];
      
      // Encontrar lead
      const lead = existingLeads.find(l => l.id === leadId);
      return lead?.notes || [];
    }
  }

  // Obter Histórico de Atividades do Lead
  async getLeadActivity(leadId: string): Promise<any[]> {
    try {
      return this.request(`/leads/${leadId}/activity`);
    } catch (error) {
      console.log('API não disponível, retornando histórico vazio');
      return [];
    }
  }
}

export const apiService = new ApiService();
