// Configuração da API
const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'https://api.app.jttecnologia.com.br',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
}

// URLs dos endpoints
export const API_ENDPOINTS = {
  // Sistema
  health: '/health',
  info: '/',
  
  // Autenticação
  login: '/auth/login',
  register: '/auth/register',
  
  // Leads
  leads: '/leads',
  
  // Clientes
  clients: '/clients',
  clientStats: (id) => `/clients/${id}/stats`,
  clientInteractions: (id) => `/clients/${id}/interactions`,
  
  // Propostas
  proposals: '/proposals',
  proposalApprove: (id) => `/proposals/${id}/approve`,
  proposalReject: (id) => `/proposals/${id}/reject`,
  proposalDuplicate: (id) => `/proposals/${id}/duplicate`,
  proposalSend: (id) => `/proposals/${id}/send`,
  
  // Contratos
  contracts: '/contracts',
  
  // Tarefas
  tasks: '/tasks',
  
  // Dashboard
  dashboardStats: '/dashboard/stats',
  dashboardCharts: '/dashboard/charts',
  
  // Pipelines
  pipelines: '/pipelines',
  
  // Chatbot
  chatbotConversations: '/chatbot/conversations',
  chatbotMessage: '/chatbot/message',
  
  // Telefonia
  telephonyCalls: '/telephony/calls',
  telephonyRecordings: '/telephony/recordings',
  
  // Automação
  automationWorkflows: '/automation/workflows',
  automationTrigger: '/automation/trigger',
  automationConditions: '/automation/conditions',
  automationActions: '/automation/actions'
}

export default API_CONFIG

