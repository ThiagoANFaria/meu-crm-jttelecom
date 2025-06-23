import requests
import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class FlyERPService:
    """
    Serviço de integração com FlyERP
    Documentação: https://documenter.getpostman.com/view/24704188/2s8Yt1r8wu
    """
    
    def __init__(self):
        self.base_url = os.getenv("FLYERP_BASE_URL", "https://empresa.flyerp.com.br/apis")
        self.auth_token = os.getenv("FLYERP_AUTH_TOKEN")
        
        if not self.auth_token:
            raise ValueError("FLYERP_AUTH_TOKEN deve ser configurado nas variáveis de ambiente")
        
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Realiza requisições para a API do FlyERP"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data)
            else:
                response = requests.request(method, url, headers=self.headers, json=data)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição ao FlyERP: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            raise

    # ==================== CONTRATOS ====================
    
    def create_contract(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um contrato no FlyERP
        
        Args:
            contract_data: Dados do contrato
        
        Returns:
            Resposta da API do FlyERP
        """
        endpoint = "CadastrarContrato"
        
        # Estrutura básica do contrato para FlyERP
        flyerp_contract = {
            "id": 0,  # 0 para novo contrato
            "inicioRegistros": 0,
            "cnpj_cpf_cliente": contract_data.get("client_cnpj_cpf"),
            "referencia": contract_data.get("contract_number"),
            "id_pessoa": contract_data.get("client_id", 0)
        }
        
        return self._make_request(endpoint, method="POST", data=flyerp_contract)

    def get_contract(self, contract_id: Optional[int] = None, 
                    client_cnpj_cpf: Optional[str] = None,
                    reference: Optional[str] = None) -> Dict[str, Any]:
        """
        Busca contratos no FlyERP
        
        Args:
            contract_id: ID do contrato
            client_cnpj_cpf: CNPJ/CPF do cliente
            reference: Referência do contrato
        
        Returns:
            Lista de contratos encontrados
        """
        endpoint = "GetContrato"
        
        params = {}
        if contract_id:
            params["id"] = contract_id
        if client_cnpj_cpf:
            params["cnpj_cpf_cliente"] = client_cnpj_cpf
        if reference:
            params["referencia"] = reference
        
        return self._make_request(endpoint, params=params)

    # ==================== CLIENTES ====================
    
    def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um cliente no FlyERP
        
        Args:
            client_data: Dados do cliente do CRM
        
        Returns:
            Resposta da API do FlyERP
        """
        endpoint = "CadastrarCliente"
        
        # Mapear dados do CRM para estrutura do FlyERP
        flyerp_client = {
            "nome": client_data.get("name"),
            "email": client_data.get("email"),
            "cnpj_cpf": client_data.get("cnpj_cpf"),
            "telefone": client_data.get("phone"),
            "celular": client_data.get("whatsapp"),
            "endereco": {
                "cep": client_data.get("zipcode"),
                "logradouro": client_data.get("street"),
                "numero": client_data.get("number"),
                "complemento": client_data.get("complement"),
                "bairro": client_data.get("neighborhood"),
                "cidade": client_data.get("city"),
                "estado": client_data.get("state")
            }
        }
        
        # Remove campos vazios
        flyerp_client = {k: v for k, v in flyerp_client.items() if v}
        if "endereco" in flyerp_client:
            flyerp_client["endereco"] = {k: v for k, v in flyerp_client["endereco"].items() if v}
        
        return self._make_request(endpoint, method="POST", data=flyerp_client)

    def get_client(self, cnpj_cpf: str) -> Dict[str, Any]:
        """
        Busca cliente no FlyERP por CNPJ/CPF
        
        Args:
            cnpj_cpf: CNPJ ou CPF do cliente
        
        Returns:
            Dados do cliente
        """
        endpoint = "GetCliente"
        params = {"cnpj_cpf": cnpj_cpf}
        
        return self._make_request(endpoint, params=params)

    def update_client(self, client_id: int, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza dados do cliente no FlyERP
        
        Args:
            client_id: ID do cliente no FlyERP
            client_data: Novos dados do cliente
        
        Returns:
            Resposta da API
        """
        endpoint = "AtualizarCliente"
        
        flyerp_client = {
            "id": client_id,
            "nome": client_data.get("name"),
            "email": client_data.get("email"),
            "cnpj_cpf": client_data.get("cnpj_cpf"),
            "telefone": client_data.get("phone"),
            "celular": client_data.get("whatsapp")
        }
        
        # Remove campos vazios
        flyerp_client = {k: v for k, v in flyerp_client.items() if v}
        
        return self._make_request(endpoint, method="PUT", data=flyerp_client)

    # ==================== CARTÕES DE CRÉDITO ====================
    
    def register_credit_card(self, contract_id: int, card_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cadastra cartão de crédito no contrato
        
        Args:
            contract_id: ID do contrato no FlyERP
            card_data: Dados do cartão
        
        Returns:
            Resposta da API
        """
        endpoint = "CadastrarCartaoContrato"
        
        flyerp_card = {
            "id_contrato": contract_id,
            "cartao_principal": card_data.get("is_primary", True),
            "cartao_credito": {
                "nome_titular": card_data.get("holder_name"),
                "cnpj_cpf_titular": card_data.get("holder_document"),
                "numero_cartao": card_data.get("card_number"),
                "mes_validade": card_data.get("expiry_month"),
                "ano_validade": card_data.get("expiry_year"),
                "codigo_seguranca": card_data.get("security_code"),
                "ip_remoto": card_data.get("remote_ip", "127.0.0.1"),
                "titular": {
                    "nome": card_data.get("holder_name"),
                    "email": card_data.get("holder_email"),
                    "cnpj_cpf": card_data.get("holder_document"),
                    "cep": card_data.get("holder_zipcode"),
                    "numero": card_data.get("holder_number"),
                    "complemento": card_data.get("holder_complement"),
                    "telefone": card_data.get("holder_phone"),
                    "celular": card_data.get("holder_mobile")
                }
            }
        }
        
        return self._make_request(endpoint, method="POST", data=flyerp_card)

    def set_primary_card(self, contract_id: int, card_id: int) -> Dict[str, Any]:
        """
        Marca cartão como principal no contrato
        
        Args:
            contract_id: ID do contrato
            card_id: ID do cartão
        
        Returns:
            Resposta da API
        """
        endpoint = "MarcarCartaoPrincipal"
        
        data = {
            "id_contrato": contract_id,
            "id": card_id
        }
        
        return self._make_request(endpoint, method="POST", data=data)

    def get_contract_cards(self, contract_id: int) -> Dict[str, Any]:
        """
        Busca cartões de um contrato
        
        Args:
            contract_id: ID do contrato
        
        Returns:
            Lista de cartões
        """
        endpoint = "GetCartoesContrato"
        
        params = {
            "id": 0,
            "id_contrato": contract_id
        }
        
        return self._make_request(endpoint, params=params)

    # ==================== MÉTODOS AUXILIARES ====================
    
    def format_document(self, document: str) -> str:
        """
        Formata documento (CPF/CNPJ) para o padrão do FlyERP
        
        Args:
            document: Documento sem formatação
        
        Returns:
            Documento formatado
        """
        # Remove caracteres não numéricos
        clean_doc = ''.join(filter(str.isdigit, document))
        
        if len(clean_doc) == 11:  # CPF
            return f"{clean_doc[:3]}.{clean_doc[3:6]}.{clean_doc[6:9]}-{clean_doc[9:]}"
        elif len(clean_doc) == 14:  # CNPJ
            return f"{clean_doc[:2]}.{clean_doc[2:5]}.{clean_doc[5:8]}/{clean_doc[8:12]}-{clean_doc[12:]}"
        else:
            return document

    def validate_contract_data(self, contract_data: Dict[str, Any]) -> List[str]:
        """
        Valida dados do contrato antes do envio
        
        Args:
            contract_data: Dados do contrato
        
        Returns:
            Lista de erros encontrados
        """
        errors = []
        
        required_fields = ["client_cnpj_cpf", "contract_number"]
        for field in required_fields:
            if not contract_data.get(field):
                errors.append(f"Campo {field} é obrigatório")
        
        # Validar formato do documento
        cnpj_cpf = contract_data.get("client_cnpj_cpf", "")
        clean_doc = ''.join(filter(str.isdigit, cnpj_cpf))
        if len(clean_doc) not in [11, 14]:
            errors.append("CNPJ/CPF deve ter 11 ou 14 dígitos")
        
        return errors

    def test_connection(self) -> Dict[str, Any]:
        """
        Testa conectividade com a API do FlyERP
        
        Returns:
            Resultado do teste
        """
        try:
            # Tenta buscar contratos como teste de conectividade
            result = self.get_contract()
            return {
                "success": True,
                "message": "Conexão com FlyERP estabelecida com sucesso",
                "api_response": result
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao conectar com FlyERP: {str(e)}",
                "error": str(e)
            }

    def sync_contract_to_erp(self, crm_contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sincroniza contrato do CRM para o ERP
        
        Args:
            crm_contract_data: Dados completos do contrato do CRM
        
        Returns:
            Resultado da sincronização
        """
        try:
            # 1. Validar dados
            errors = self.validate_contract_data(crm_contract_data)
            if errors:
                return {
                    "success": False,
                    "message": "Dados inválidos",
                    "errors": errors
                }
            
            # 2. Verificar se cliente existe no ERP
            client_cnpj_cpf = self.format_document(crm_contract_data["client_cnpj_cpf"])
            
            try:
                client_result = self.get_client(client_cnpj_cpf)
                client_exists = client_result.get("Sucesso", False)
            except:
                client_exists = False
            
            # 3. Criar cliente se não existir
            if not client_exists:
                client_data = {
                    "name": crm_contract_data.get("client_name"),
                    "email": crm_contract_data.get("client_email"),
                    "cnpj_cpf": client_cnpj_cpf,
                    "phone": crm_contract_data.get("client_phone"),
                    "whatsapp": crm_contract_data.get("client_whatsapp"),
                    "zipcode": crm_contract_data.get("client_zipcode"),
                    "street": crm_contract_data.get("client_street"),
                    "number": crm_contract_data.get("client_number"),
                    "complement": crm_contract_data.get("client_complement"),
                    "neighborhood": crm_contract_data.get("client_neighborhood"),
                    "city": crm_contract_data.get("client_city"),
                    "state": crm_contract_data.get("client_state")
                }
                
                client_result = self.create_client(client_data)
                if not client_result.get("Sucesso", False):
                    return {
                        "success": False,
                        "message": "Erro ao criar cliente no ERP",
                        "error": client_result.get("Mensagem")
                    }
            
            # 4. Criar contrato
            contract_data = {
                "client_cnpj_cpf": client_cnpj_cpf,
                "contract_number": crm_contract_data["contract_number"],
                "client_id": crm_contract_data.get("client_id", 0)
            }
            
            contract_result = self.create_contract(contract_data)
            
            if not contract_result.get("Sucesso", False):
                return {
                    "success": False,
                    "message": "Erro ao criar contrato no ERP",
                    "error": contract_result.get("Mensagem")
                }
            
            # 5. Cadastrar cartão de crédito se fornecido
            if crm_contract_data.get("credit_card_data"):
                try:
                    contract_id = contract_result.get("NumeroPedido")
                    if contract_id:
                        card_result = self.register_credit_card(
                            contract_id, 
                            crm_contract_data["credit_card_data"]
                        )
                        
                        if not card_result.get("Sucesso", False):
                            logger.warning(f"Erro ao cadastrar cartão: {card_result.get('Mensagem')}")
                except Exception as e:
                    logger.warning(f"Erro ao cadastrar cartão de crédito: {e}")
            
            return {
                "success": True,
                "message": "Contrato sincronizado com sucesso no ERP",
                "erp_contract_id": contract_result.get("NumeroPedido"),
                "erp_response": contract_result
            }
            
        except Exception as e:
            logger.error(f"Erro na sincronização com ERP: {e}")
            return {
                "success": False,
                "message": f"Erro na sincronização: {str(e)}",
                "error": str(e)
            }

