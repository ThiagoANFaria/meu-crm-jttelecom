
import { User, Lead, Client, Proposal, Contract, Task, Pipeline, DashboardSummary } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://api.app.jttecnologia.com.br';

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
    const response = await fetch(url, {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Auth
  async login(email: string, password: string): Promise<{ token: string; user: User }> {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(data: { name: string; email: string; password: string; company_name?: string }): Promise<{ token: string; user: User }> {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
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
