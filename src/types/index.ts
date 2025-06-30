
export interface User {
  id: string;
  name: string;
  email: string;
  company_name?: string;
}

export interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string;
  source: string;
  status: string;
  created_at: string;
}

export interface Client {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  status: string;
  created_at: string;
}

export interface Proposal {
  id: string;
  title: string;
  client_id: string;
  amount: number;
  status: string;
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
