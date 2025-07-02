
import { User, Lead, Client, Proposal, Contract, Task, Pipeline, DashboardSummary } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://www.api.app.jttecnologia.com.br';

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
    return this.request('/leads');
  }

  async createLead(lead: Omit<Lead, 'id' | 'created_at'>): Promise<Lead> {
    return this.request('/leads', {
      method: 'POST',
      body: JSON.stringify(lead),
    });
  }

  async updateLead(id: string, lead: Partial<Lead>): Promise<Lead> {
    return this.request(`/leads/${id}`, {
      method: 'PUT',
      body: JSON.stringify(lead),
    });
  }

  async deleteLead(id: string): Promise<void> {
    return this.request(`/leads/${id}`, {
      method: 'DELETE',
    });
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
}

export const apiService = new ApiService();
