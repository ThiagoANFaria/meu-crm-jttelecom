import API_CONFIG, { API_ENDPOINTS } from '../config/api.js'

class ApiService {
  constructor() {
    this.baseURL = API_CONFIG.baseURL
    this.timeout = API_CONFIG.timeout
    this.headers = API_CONFIG.headers
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      timeout: this.timeout,
      headers: {
        ...this.headers,
        ...options.headers
      },
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('API Request Error:', error)
      return { success: false, error: error.message }
    }
  }

  // Métodos de autenticação
  async login(email, password) {
    return this.request(API_ENDPOINTS.login, {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })
  }

  async register(userData) {
    return this.request(API_ENDPOINTS.register, {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  }

  // Métodos de leads
  async getLeads() {
    return this.request(API_ENDPOINTS.leads)
  }

  async createLead(leadData) {
    return this.request(API_ENDPOINTS.leads, {
      method: 'POST',
      body: JSON.stringify(leadData)
    })
  }

  // Métodos de clientes
  async getClients() {
    return this.request(API_ENDPOINTS.clients)
  }

  async createClient(clientData) {
    return this.request(API_ENDPOINTS.clients, {
      method: 'POST',
      body: JSON.stringify(clientData)
    })
  }

  async getClient(id) {
    return this.request(`${API_ENDPOINTS.clients}/${id}`)
  }

  async updateClient(id, clientData) {
    return this.request(`${API_ENDPOINTS.clients}/${id}`, {
      method: 'PUT',
      body: JSON.stringify(clientData)
    })
  }

  async deleteClient(id) {
    return this.request(`${API_ENDPOINTS.clients}/${id}`, {
      method: 'DELETE'
    })
  }

  // Métodos de propostas
  async getProposals() {
    return this.request(API_ENDPOINTS.proposals)
  }

  async createProposal(proposalData) {
    return this.request(API_ENDPOINTS.proposals, {
      method: 'POST',
      body: JSON.stringify(proposalData)
    })
  }

  async approveProposal(id) {
    return this.request(API_ENDPOINTS.proposalApprove(id), {
      method: 'POST'
    })
  }

  async rejectProposal(id) {
    return this.request(API_ENDPOINTS.proposalReject(id), {
      method: 'POST'
    })
  }

  // Métodos de contratos
  async getContracts() {
    return this.request(API_ENDPOINTS.contracts)
  }

  async createContract(contractData) {
    return this.request(API_ENDPOINTS.contracts, {
      method: 'POST',
      body: JSON.stringify(contractData)
    })
  }

  // Métodos de tarefas
  async getTasks() {
    return this.request(API_ENDPOINTS.tasks)
  }

  async createTask(taskData) {
    return this.request(API_ENDPOINTS.tasks, {
      method: 'POST',
      body: JSON.stringify(taskData)
    })
  }

  // Métodos de dashboard
  async getDashboardStats() {
    return this.request(API_ENDPOINTS.dashboardStats)
  }

  async getDashboardCharts() {
    return this.request(API_ENDPOINTS.dashboardCharts)
  }

  // Método de health check
  async healthCheck() {
    return this.request(API_ENDPOINTS.health)
  }
}

export default new ApiService()

