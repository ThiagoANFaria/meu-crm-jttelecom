export interface User {
  id: string;
  name: string;
  email: string;
  company_name?: string;
  user_level: 'master' | 'admin' | 'user';
}

export interface Tag {
  id: string;
  name: string;
  color: string;
  created_at: string;
}

export interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string;
  whatsapp?: string;
  company?: string;
  cnpj_cpf?: string;
  ie_rg?: string;
  address?: string;
  number?: string;
  neighborhood?: string;
  city?: string;
  state?: string;
  cep?: string;
  source: string;
  status: string;
  score?: number; // Lead scoring 0-100
  tags?: Tag[]; // Sistema de tags
  responsible?: string; // Responsável pelo lead
  last_contact?: string; // Data do último contato
  next_contact?: string; // Data do próximo contato
  custom_fields?: Record<string, any>; // Campos customizáveis
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Client {
  id: string;
  name: string;
  email: string;
  phone: string;
  whatsapp?: string;
  company: string;
  cnpj_cpf?: string;
  ie_rg?: string;
  address?: string;
  number?: string;
  neighborhood?: string;
  city?: string;
  state?: string;
  cep?: string;
  status: string;
  products?: string[];
  monthly_value?: number; // Valor mensal
  annual_value?: number; // Valor anual
  contract_start?: string; // Início do contrato
  contract_end?: string; // Fim do contrato
  payment_status?: string; // Status de pagamento
  tags?: Tag[]; // Sistema de tags
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  active: boolean;
}

export interface Opportunity {
  id: string;
  title: string;
  lead_id?: string;
  client_id?: string;
  pipeline_id: string;
  stage_id: string;
  products: Product[];
  value: number;
  probability: number; // 0-100%
  expected_close_date: string;
  responsible: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Pipeline {
  id: string;
  name: string;
  type: 'prospection' | 'sales'; // SDR ou Closer
  stages: PipelineStage[];
  created_at: string;
  updated_at: string;
}

export interface PipelineStage {
  id: string;
  name: string;
  order: number;
  color: string;
  pipeline_id: string;
}

export interface ProposalTemplate {
  id: string;
  name: string;
  content: string; // HTML com variáveis {name}, {company_name}, etc.
  variables: string[]; // Lista de variáveis disponíveis
  active: boolean;
  created_at: string;
}

export interface Proposal {
  id: string;
  number: string; // PROP-YYYYMM-NNNN
  title: string;
  client_id: string;
  client_name?: string;
  client_email?: string;
  client_phone?: string;
  template_id: string;
  content: string; // HTML renderizado
  description: string;
  amount: number;
  discount?: number;
  total_amount: number;
  status: 'draft' | 'sent' | 'viewed' | 'accepted' | 'rejected' | 'expired';
  valid_until: string;
  sent_at?: string;
  viewed_at?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface ContractTemplate {
  id: string;
  name: string;
  content: string; // HTML com variáveis
  variables: string[];
  active: boolean;
  created_at: string;
}

export interface Contract {
  id: string;
  number: string; // CONT-YYYY-NNNN
  title: string;
  client_id: string;
  template_id: string;
  content: string;
  amount: number;
  status: 'draft' | 'sent' | 'signed' | 'active' | 'expired' | 'cancelled';
  start_date: string;
  end_date: string;
  d4sign_document_id?: string; // ID do documento no D4Sign
  signed_document_url?: string;
  signers: ContractSigner[];
  created_at: string;
  updated_at: string;
}

export interface ContractSigner {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: 'client' | 'company' | 'witness';
  signed_at?: string;
}

export interface TaskType {
  id: string;
  name: string;
  icon: string;
  color: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  type: TaskType;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assigned_to: string;
  lead_id?: string;
  client_id?: string;
  due_date: string;
  completed_at?: string;
  is_recurring: boolean;
  recurrence_pattern?: string; // daily, weekly, monthly
  recurrence_end?: string;
  notifications: boolean;
  created_at: string;
  updated_at: string;
}

export interface Automation {
  id: string;
  name: string;
  description: string;
  trigger: AutomationTrigger;
  actions: AutomationAction[];
  active: boolean;
  created_at: string;
}

export interface AutomationTrigger {
  type: 'lead_created' | 'lead_status_changed' | 'task_completed' | 'date_reached';
  conditions: Record<string, any>;
}

export interface AutomationAction {
  type: 'send_email' | 'create_task' | 'update_lead' | 'send_whatsapp';
  parameters: Record<string, any>;
}

export interface EmailCampaign {
  id: string;
  name: string;
  subject: string;
  content: string;
  recipients: string[];
  status: 'draft' | 'scheduled' | 'sent' | 'cancelled';
  scheduled_at?: string;
  sent_at?: string;
  open_rate?: number;
  click_rate?: number;
  created_at: string;
}

export interface PhoneCall {
  id: string;
  lead_id?: string;
  client_id?: string;
  phone_number: string;
  direction: 'inbound' | 'outbound';
  duration: number; // em segundos
  status: 'completed' | 'missed' | 'busy' | 'failed';
  recording_url?: string;
  notes?: string;
  created_at: string;
}

export interface ChatbotFlow {
  id: string;
  name: string;
  description: string;
  nodes: ChatbotNode[];
  active: boolean;
  created_at: string;
}

export interface ChatbotNode {
  id: string;
  type: 'message' | 'question' | 'condition' | 'action';
  content: string;
  options?: string[];
  next_node_id?: string;
  conditions?: Record<string, any>;
}

export interface DashboardSummary {
  total_leads: number;
  total_clients: number;
  total_proposals: number;
  total_contracts: number;
  revenue_this_month: number;
  conversion_rate: number;
  // Métricas avançadas
  leads_by_source: Record<string, number>;
  leads_by_status: Record<string, number>;
  pipeline_metrics: {
    prospection: PipelineMetrics;
    sales: PipelineMetrics;
  };
  team_performance: UserPerformance[];
}

export interface PipelineMetrics {
  total_opportunities: number;
  total_value: number;
  conversion_rate: number;
  average_deal_size: number;
  opportunities_by_stage: Record<string, number>;
}

export interface UserPerformance {
  user_id: string;
  user_name: string;
  leads_created: number;
  opportunities_won: number;
  revenue_generated: number;
  conversion_rate: number;
}
