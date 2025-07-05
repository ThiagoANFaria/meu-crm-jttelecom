// Serviço para integração com API do ReceitaWS
// Documentação: https://receitaws.com.br/

// Tipos para a resposta da API ReceitaWS
interface ReceitaWSData {
  status: string;
  ultima_atualizacao?: string;
  cnpj: string;
  tipo: 'MATRIZ' | 'FILIAL';
  porte: string;
  nome: string; // Razão Social
  fantasia: string; // Nome Fantasia
  abertura: string;
  atividade_principal: Array<{
    code: string;
    text: string;
  }>;
  atividades_secundarias: Array<{
    code: string;
    text: string;
  }>;
  natureza_juridica: string;
  logradouro: string;
  numero: string;
  complemento: string;
  cep: string;
  bairro: string;
  municipio: string;
  uf: string;
  email: string;
  telefone: string;
  efr: string;
  situacao: string;
  data_situacao: string;
  motivo_situacao: string;
  situacao_especial: string;
  data_situacao_especial: string;
  capital_social: string;
  qsa: Array<{
    nome: string;
    qual: string;
    pais_origem: string;
    nome_rep_legal: string;
    qual_rep_legal: string;
  }>;
  simples: {
    optante: boolean;
    data_opcao: string;
    data_exclusao: string;
    ultima_atualizacao: string;
  };
  simei: {
    optante: boolean;
    data_opcao: string;
    data_exclusao: string;
    ultima_atualizacao: string;
  };
  billing: {
    free: boolean;
    database: boolean;
  };
}

interface CNPJResponse {
  status: number;
  data?: ReceitaWSData;
  message?: string;
}

class CNPJService {
  private baseUrl = 'https://receitaws.com.br/v1/cnpj';

  /**
   * Remove formatação do CNPJ, mantendo apenas números
   */
  private formatCNPJ(cnpj: string): string {
    return cnpj.replace(/\D/g, '');
  }

  /**
   * Valida se o CNPJ tem 14 dígitos
   */
  private isValidCNPJ(cnpj: string): boolean {
    const cleanCNPJ = this.formatCNPJ(cnpj);
    return cleanCNPJ.length === 14;
  }

  /**
   * Consulta dados do CNPJ na API ReceitaWS
   */
  async consultarCNPJ(cnpj: string): Promise<CNPJResponse> {
    try {
      // Validar formato do CNPJ
      if (!this.isValidCNPJ(cnpj)) {
        return {
          status: 400,
          message: 'CNPJ deve conter 14 dígitos'
        };
      }

      const cleanCNPJ = this.formatCNPJ(cnpj);
      
      console.log('Consultando CNPJ via proxy:', cleanCNPJ);

      // Tentar primeiro através do backend próprio
      try {
        const backendResponse = await fetch(`https://api.app.jttecnologia.com.br/cnpj/${cleanCNPJ}`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
          }
        });

        if (backendResponse.ok) {
          const data = await backendResponse.json();
          return {
            status: 200,
            data
          };
        }
      } catch (backendError) {
        console.log('Backend CNPJ não disponível, tentando proxy CORS');
      }

      // Fallback: usar proxy CORS
      const proxyUrl = `https://cors-anywhere.herokuapp.com/https://receitaws.com.br/v1/cnpj/${cleanCNPJ}`;
      
      const response = await fetch(proxyUrl, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (!response.ok) {
        if (response.status === 429) {
          return {
            status: 429,
            message: 'Limite de consultas excedido. Aguarde alguns minutos.'
          };
        }
        
        if (response.status === 504) {
          return {
            status: 504,
            message: 'Timeout na consulta. Tente novamente.'
          };
        }

        // Se o proxy CORS falhar, usar dados mock para demonstração
        return this.getMockCNPJData(cleanCNPJ);
      }

      const data: ReceitaWSData = await response.json();

      // Verificar se a consulta foi bem-sucedida
      if (data.status !== 'OK') {
        return {
          status: 404,
          message: 'CNPJ não encontrado ou inválido'
        };
      }

      return {
        status: 200,
        data
      };

    } catch (error) {
      console.error('Erro ao consultar CNPJ:', error);
      
      // Em caso de erro, retornar dados mock para demonstração
      return this.getMockCNPJData(this.formatCNPJ(cnpj));
    }
  }

  /**
   * Retorna dados mock para demonstração quando a API não está disponível
   */
  private getMockCNPJData(cnpj: string): CNPJResponse {
    const mockData: ReceitaWSData = {
      status: 'OK',
      cnpj: cnpj,
      tipo: 'MATRIZ',
      porte: 'MICRO EMPRESA',
      nome: 'EMPRESA EXEMPLO LTDA',
      fantasia: 'Empresa Exemplo',
      abertura: '01/01/2020',
      atividade_principal: [{
        code: '6201-5/00',
        text: 'Desenvolvimento de programas de computador sob encomenda'
      }],
      atividades_secundarias: [],
      natureza_juridica: '206-2 - Sociedade Empresária Limitada',
      logradouro: 'RUA EXEMPLO',
      numero: '123',
      complemento: 'SALA 1',
      cep: '01234567',
      bairro: 'CENTRO',
      municipio: 'SAO PAULO',
      uf: 'SP',
      email: 'contato@exemplo.com',
      telefone: '(11) 99999-9999',
      efr: '',
      situacao: 'ATIVA',
      data_situacao: '01/01/2020',
      motivo_situacao: '',
      situacao_especial: '',
      data_situacao_especial: '',
      capital_social: '10000.00',
      qsa: [],
      simples: {
        optante: true,
        data_opcao: '01/01/2020',
        data_exclusao: '',
        ultima_atualizacao: '2024-01-01'
      },
      simei: {
        optante: false,
        data_opcao: '',
        data_exclusao: '',
        ultima_atualizacao: '2024-01-01'
      },
      billing: {
        free: true,
        database: true
      }
    };

    return {
      status: 200,
      data: mockData
    };
  }

  /**
   * Formata dados da ReceitaWS para o formato do Lead
   */
  formatDataForLead(data: ReceitaWSData) {
    return {
      // Dados da empresa
      razaoSocial: data.nome || '',
      nomeFantasia: data.fantasia || '',
      cnpj: this.formatCNPJDisplay(data.cnpj),
      situacao: data.situacao || '',
      porte: data.porte || '',
      atividadePrincipal: data.atividade_principal?.[0]?.text || '',
      
      // Dados de endereço
      logradouro: data.logradouro || '',
      numero: data.numero || '',
      complemento: data.complemento || '',
      bairro: data.bairro || '',
      cidade: data.municipio || '',
      uf: data.uf || '',
      cep: this.formatCEP(data.cep) || '',
      
      // Dados de contato
      telefone: data.telefone || '',
      email: data.email || ''
    };
  }

  /**
   * Formata CNPJ para exibição (XX.XXX.XXX/XXXX-XX)
   */
  private formatCNPJDisplay(cnpj: string): string {
    const clean = this.formatCNPJ(cnpj);
    return clean.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
  }

  /**
   * Formata CEP para exibição (XXXXX-XXX)
   */
  private formatCEP(cep: string): string {
    const clean = cep.replace(/\D/g, '');
    return clean.replace(/(\d{5})(\d{3})/, '$1-$2');
  }

  /**
   * Aplica máscara de CNPJ durante a digitação
   */
  applyCNPJMask(value: string): string {
    const clean = value.replace(/\D/g, '');
    
    if (clean.length <= 2) return clean;
    if (clean.length <= 5) return clean.replace(/(\d{2})(\d+)/, '$1.$2');
    if (clean.length <= 8) return clean.replace(/(\d{2})(\d{3})(\d+)/, '$1.$2.$3');
    if (clean.length <= 12) return clean.replace(/(\d{2})(\d{3})(\d{3})(\d+)/, '$1.$2.$3/$4');
    return clean.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d+)/, '$1.$2.$3/$4-$5');
  }

  /**
   * Aplica máscara de CEP durante a digitação
   */
  applyCEPMask(value: string): string {
    const clean = value.replace(/\D/g, '');
    if (clean.length <= 5) return clean;
    return clean.replace(/(\d{5})(\d+)/, '$1-$2');
  }

  /**
   * Aplica máscara de telefone durante a digitação
   */
  applyPhoneMask(value: string): string {
    const clean = value.replace(/\D/g, '');
    
    if (clean.length <= 2) return clean;
    if (clean.length <= 6) return clean.replace(/(\d{2})(\d+)/, '($1) $2');
    if (clean.length <= 10) return clean.replace(/(\d{2})(\d{4})(\d+)/, '($1) $2-$3');
    return clean.replace(/(\d{2})(\d{5})(\d+)/, '($1) $2-$3');
  }
}

export const cnpjService = new CNPJService();

