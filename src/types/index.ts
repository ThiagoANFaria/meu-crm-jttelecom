export interface User {
  id: string;
  name: string;
  email: string;
  company_name?: string;
  user_level: 'master' | 'admin' | 'user';
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
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Proposal {
  id: string;
  title: string;
  client_id: string;
  client_name?: string;
  client_email?: string;
  client_phone?: string;
  description: string;
  amount: number;
  discount?: number;
  total_amount: number;
  status: string;
  valid_until: string;
  template_id?: string;
  template_content?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Contract {
  id: string;
  title: string;
  client_id: string;
  amount: number;
  status: string;
  start_date: string;
  end_date: string;
  created_at: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  assigned_to: string;
  due_date: string;
  created_at: string;
}

export interface Pipeline {
  id: string;
  name: string;
  stages: string[];
  created_at: string;
  updated_at: string;
}

export interface DashboardSummary {
  total_leads: number;
  total_clients: number;
  total_proposals: number;
  total_contracts: number;
  revenue_this_month: number;
  conversion_rate: number;
}
