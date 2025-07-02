// Serviço para integração com API do CNPJ.ws
// Documentação: https://docs.cnpj.ws/referencia-de-api/api-publica/consultando-cnpj

export interface CNPJData {
  cnpj: string;
  razao_social: string;
  nome_fantasia?: string;
  logradouro: string;
  numero: string;
  complemento?: string;
  bairro: string;
  municipio: string;
  uf: string;
  cep: string;
  telefone?: string;
  email?: string;
  situacao_cadastral: string;
  data_situacao_cadastral: string;
  atividade_principal: {
    codigo: string;
    descricao: string;
  };
  atividades_secundarias?: Array<{
    codigo: string;
    descricao: string;
  }>;
  natureza_juridica: {
    codigo: string;
    descricao: string;
  };
  porte: {
    codigo: string;
    descricao: string;
  };
  capital_social: number;
  socios?: Array<{
    nome: string;
    qualificacao: string;
  }>;
}

export interface CNPJResponse {
  status: number;
  message?: string;
  data?: CNPJData;
}

class CNPJService {
  private readonly baseUrl = 'https://publica.cnpj.ws/cnpj';

  /**
   * Formata CNPJ removendo caracteres especiais
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
   * Consulta dados do CNPJ na API pública do CNPJ.ws
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
      const url = `${this.baseUrl}/${cleanCNPJ}`;

      console.log('Consultando CNPJ:', cleanCNPJ);

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        if (response.status === 404) {
          return {
            status: 404,
            message: 'CNPJ não encontrado'
          };
        }
        
        if (response.status === 429) {
          return {
            status: 429,
            message: 'Muitas consultas. Tente novamente em alguns segundos.'
          };
        }

        return {
          status: response.status,
          message: `Erro na consulta: ${response.statusText}`
        };
      }

      const data: CNPJData = await response.json();

      // Verificar se a empresa está ativa
      if (data.situacao_cadastral !== 'ATIVA') {
        return {
          status: 200,
          message: `Empresa com situação: ${data.situacao_cadastral}`,
          data
        };
      }

      return {
        status: 200,
        data
      };

    } catch (error) {
      console.error('Erro ao consultar CNPJ:', error);
      return {
        status: 500,
        message: 'Erro interno na consulta do CNPJ'
      };
    }
  }

  /**
   * Formata os dados do CNPJ para uso no formulário de Lead
   */
  formatDataForLead(cnpjData: CNPJData) {
    return {
      company: cnpjData.nome_fantasia || cnpjData.razao_social,
      cnpj_cpf: this.formatCNPJDisplay(cnpjData.cnpj),
      address: cnpjData.logradouro,
      number: cnpjData.numero,
      neighborhood: cnpjData.bairro,
      city: cnpjData.municipio,
      state: cnpjData.uf,
      cep: this.formatCEPDisplay(cnpjData.cep),
      phone: cnpjData.telefone || '',
      email: cnpjData.email || '',
      custom_fields: {
        razao_social: cnpjData.razao_social,
        nome_fantasia: cnpjData.nome_fantasia,
        atividade_principal: cnpjData.atividade_principal.descricao,
        natureza_juridica: cnpjData.natureza_juridica.descricao,
        porte: cnpjData.porte.descricao,
        capital_social: cnpjData.capital_social,
        situacao_cadastral: cnpjData.situacao_cadastral,
        complemento: cnpjData.complemento
      }
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
  private formatCEPDisplay(cep: string): string {
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

