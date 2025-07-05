import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface Tenant {
  id: string;
  name: string;
  domain: string;
  subdomain: string;
  logo?: string;
  primaryColor: string;
  secondaryColor: string;
  isActive: boolean;
  plan: 'basic' | 'professional' | 'enterprise';
  maxUsers: number;
  features: string[];
  createdAt: string;
  updatedAt: string;
  settings: {
    allowCustomProducts: boolean;
    allowCustomTemplates: boolean;
    allowIntegrations: boolean;
    maxProducts: number;
    maxTemplates: number;
  };
}

interface TenantContextType {
  currentTenant: Tenant | null;
  setCurrentTenant: (tenant: Tenant | null) => void;
  isLoading: boolean;
  tenantProducts: any[];
  tenantTemplates: any[];
  tenantConfigurations: any[];
  loadTenantData: () => Promise<void>;
  updateTenantData: (data: any) => Promise<void>;
}

const TenantContext = createContext<TenantContextType | undefined>(undefined);

export const useTenant = () => {
  const context = useContext(TenantContext);
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider');
  }
  return context;
};

interface TenantProviderProps {
  children: ReactNode;
}

export const TenantProvider: React.FC<TenantProviderProps> = ({ children }) => {
  const [currentTenant, setCurrentTenant] = useState<Tenant | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [tenantProducts, setTenantProducts] = useState<any[]>([]);
  const [tenantTemplates, setTenantTemplates] = useState<any[]>([]);
  const [tenantConfigurations, setTenantConfigurations] = useState<any[]>([]);

  useEffect(() => {
    initializeTenant();
  }, []);

  const initializeTenant = async () => {
    try {
      setIsLoading(true);
      
      // Detectar tenant baseado no subdomínio ou domínio
      const hostname = window.location.hostname;
      const subdomain = hostname.split('.')[0];
      
      // Simular busca do tenant
      const tenant = await detectTenant(subdomain, hostname);
      
      if (tenant) {
        setCurrentTenant(tenant);
        await loadTenantData();
      } else {
        // Tenant padrão (JT Telecom)
        const defaultTenant: Tenant = {
          id: 'jt-telecom',
          name: 'JT Telecom',
          domain: 'jttecnologia.com.br',
          subdomain: 'app',
          logo: '/logo-jt.png',
          primaryColor: '#2563eb',
          secondaryColor: '#1e40af',
          isActive: true,
          plan: 'enterprise',
          maxUsers: -1, // Ilimitado
          features: ['all'],
          createdAt: '2025-01-01T00:00:00Z',
          updatedAt: '2025-07-05T19:30:00Z',
          settings: {
            allowCustomProducts: true,
            allowCustomTemplates: true,
            allowIntegrations: true,
            maxProducts: -1,
            maxTemplates: -1
          }
        };
        setCurrentTenant(defaultTenant);
        await loadTenantData();
      }
    } catch (error) {
      console.error('Erro ao inicializar tenant:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const detectTenant = async (subdomain: string, hostname: string): Promise<Tenant | null> => {
    // Simular API call para detectar tenant
    // Em produção, isso seria uma chamada real para a API
    
    const mockTenants: Tenant[] = [
      {
        id: 'empresa-exemplo',
        name: 'Empresa Exemplo Ltda',
        domain: 'empresaexemplo.com.br',
        subdomain: 'exemplo',
        logo: '/logo-exemplo.png',
        primaryColor: '#059669',
        secondaryColor: '#047857',
        isActive: true,
        plan: 'professional',
        maxUsers: 50,
        features: ['crm', 'proposals', 'analytics'],
        createdAt: '2025-06-01T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        settings: {
          allowCustomProducts: true,
          allowCustomTemplates: true,
          allowIntegrations: false,
          maxProducts: 20,
          maxTemplates: 10
        }
      },
      {
        id: 'tech-solutions',
        name: 'Tech Solutions Inc',
        domain: 'techsolutions.com',
        subdomain: 'tech',
        logo: '/logo-tech.png',
        primaryColor: '#7c3aed',
        secondaryColor: '#6d28d9',
        isActive: true,
        plan: 'basic',
        maxUsers: 10,
        features: ['crm', 'proposals'],
        createdAt: '2025-05-15T00:00:00Z',
        updatedAt: '2025-07-05T19:30:00Z',
        settings: {
          allowCustomProducts: false,
          allowCustomTemplates: true,
          allowIntegrations: false,
          maxProducts: 5,
          maxTemplates: 5
        }
      }
    ];

    // Buscar por subdomínio ou domínio
    return mockTenants.find(t => 
      t.subdomain === subdomain || 
      t.domain === hostname ||
      hostname.includes(t.domain)
    ) || null;
  };

  const loadTenantData = async () => {
    if (!currentTenant) return;

    try {
      // Carregar produtos específicos do tenant
      const products = await loadTenantProducts(currentTenant.id);
      setTenantProducts(products);

      // Carregar templates específicos do tenant
      const templates = await loadTenantTemplates(currentTenant.id);
      setTenantTemplates(templates);

      // Carregar configurações específicas do tenant
      const configurations = await loadTenantConfigurations(currentTenant.id);
      setTenantConfigurations(configurations);

    } catch (error) {
      console.error('Erro ao carregar dados do tenant:', error);
    }
  };

  const loadTenantProducts = async (tenantId: string) => {
    // Simular carregamento de produtos específicos do tenant
    // Em produção, seria uma chamada para API com filtro por tenant
    
    if (tenantId === 'jt-telecom') {
      // Produtos padrão da JT
      return [
        { id: '1', name: 'PABX em Nuvem', tenantId, isDefault: true },
        { id: '2', name: 'URA Reversa', tenantId, isDefault: true },
        { id: '3', name: 'Discador Preditivo', tenantId, isDefault: true },
        { id: '4', name: 'Smartbot (Chatbot)', tenantId, isDefault: true },
        { id: '5', name: '0800 Virtual', tenantId, isDefault: true },
        { id: '6', name: 'CRM', tenantId, isDefault: true },
        { id: '7', name: 'JT VOX', tenantId, isDefault: true },
        { id: '8', name: 'JT Mobi', tenantId, isDefault: true }
      ];
    } else {
      // Produtos personalizados do tenant + produtos base permitidos
      return [
        { id: `${tenantId}-1`, name: 'Produto Personalizado 1', tenantId, isDefault: false },
        { id: `${tenantId}-2`, name: 'Serviço Específico', tenantId, isDefault: false }
      ];
    }
  };

  const loadTenantTemplates = async (tenantId: string) => {
    // Simular carregamento de templates específicos do tenant
    return [
      { id: `${tenantId}-template-1`, name: 'Template Padrão', tenantId },
      { id: `${tenantId}-template-2`, name: 'Template Personalizado', tenantId }
    ];
  };

  const loadTenantConfigurations = async (tenantId: string) => {
    // Simular carregamento de configurações específicas do tenant
    return [
      { id: `${tenantId}-config-1`, key: 'email_smtp', value: '', tenantId },
      { id: `${tenantId}-config-2`, key: 'whatsapp_api', value: '', tenantId }
    ];
  };

  const updateTenantData = async (data: any) => {
    // Simular atualização de dados do tenant
    console.log('Atualizando dados do tenant:', data);
    await loadTenantData();
  };

  const value: TenantContextType = {
    currentTenant,
    setCurrentTenant,
    isLoading,
    tenantProducts,
    tenantTemplates,
    tenantConfigurations,
    loadTenantData,
    updateTenantData
  };

  return (
    <TenantContext.Provider value={value}>
      {children}
    </TenantContext.Provider>
  );
};

export default TenantProvider;

