import requests
import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any
from .flyerp_service import FlyERPService
import logging

logger = logging.getLogger(__name__)

class D4SignService:
    """Serviço de integração com D4Sign para assinatura digital de contratos."""
    
    def __init__(self, api_token: str = None, base_url: str = None):
        """
        Inicializa o serviço D4Sign.
        
        Args:
            api_token: Token de API do D4Sign
            base_url: URL base da API (padrão: https://secure.d4sign.com.br/api/v1)
        """
        self.api_token = api_token or os.getenv('D4SIGN_API_TOKEN')
        self.base_url = base_url or 'https://secure.d4sign.com.br/api/v1'
        self.headers = {
            'Content-Type': 'application/json',
            'tokenAPI': self.api_token
        }
        
        # Inicializar serviço FlyERP
        try:
            self.flyerp_service = FlyERPService()
        except Exception as e:
            logger.warning(f"FlyERP não configurado: {e}")
            self.flyerp_service = None
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, files: Dict = None) -> Dict:
        """
        Faz requisição para a API do D4Sign.
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API
            data: Dados para envio
            files: Arquivos para upload
            
        Returns:
            Resposta da API
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if files:
                # Para upload de arquivos, não usar Content-Type application/json
                headers = {'tokenAPI': self.api_token}
                response = requests.request(method, url, headers=headers, data=data, files=files)
            else:
                response = requests.request(method, url, headers=self.headers, json=data)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição D4Sign: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta D4Sign: {str(e)}")
    
    def upload_document(self, safe_id: str, file_path: str, file_name: str = None) -> Dict:
        """
        Faz upload de um documento para o D4Sign.
        
        Args:
            safe_id: ID do cofre
            file_path: Caminho do arquivo local
            file_name: Nome do arquivo (opcional)
            
        Returns:
            Dados do documento criado
        """
        if not os.path.exists(file_path):
            raise Exception(f"Arquivo não encontrado: {file_path}")
        
        file_name = file_name or os.path.basename(file_path)
        
        with open(file_path, 'rb') as file:
            files = {
                'file': (file_name, file, 'application/pdf')
            }
            data = {
                'safe_id': safe_id
            }
            
            return self._make_request('POST', 'documents', data, files)
    
    def add_signer(self, document_id: str, signer_data: Dict) -> Dict:
        """
        Adiciona um signatário ao documento.
        
        Args:
            document_id: ID do documento
            signer_data: Dados do signatário
                
        Returns:
            Dados do signatário adicionado
        """
        return self._make_request('POST', f'documents/{document_id}/createlist', signer_data)
    
    def send_document_for_signature(self, document_id: str, message: str = "", skip_email: bool = False) -> Dict:
        """
        Envia documento para assinatura.
        
        Args:
            document_id: ID do documento
            message: Mensagem personalizada para os signatários
            skip_email: Se True, não envia email automático
            
        Returns:
            Resultado do envio
        """
        data = {
            'message': message,
            'skip_email': '1' if skip_email else '0'
        }
        
        return self._make_request('POST', f'documents/{document_id}/sendtosigner', data)
    
    def get_document_status(self, document_id: str) -> Dict:
        """
        Obtém o status de um documento.
        
        Args:
            document_id: ID do documento
            
        Returns:
            Status do documento
        """
        return self._make_request('GET', f'documents/{document_id}')
    
    def download_signed_document(self, document_id: str) -> bytes:
        """
        Baixa o documento assinado.
        
        Args:
            document_id: ID do documento
            
        Returns:
            Conteúdo do documento em bytes
        """
        url = f"{self.base_url}/documents/{document_id}/download"
        headers = {'tokenAPI': self.api_token}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.content
    
    def process_signature_webhook(self, webhook_data: Dict, contract_id: int) -> Dict:
        """
        Processa webhook de assinatura e sincroniza com FlyERP.
        
        Args:
            webhook_data: Dados do webhook do D4Sign
            contract_id: ID do contrato no CRM
            
        Returns:
            Resultado do processamento
        """
        try:
            event_type = webhook_data.get('event')
            document_id = webhook_data.get('document_id')
            
            result = {
                'event_type': event_type,
                'document_id': document_id,
                'timestamp': datetime.utcnow(),
                'contract_id': contract_id,
                'flyerp_sync': False
            }
            
            # Se documento foi assinado completamente
            if event_type == 'document_signed':
                result['status'] = 'signed'
                result['signed_at'] = webhook_data.get('signed_at')
                
                # Sincronizar com FlyERP
                if self.flyerp_service:
                    try:
                        # Buscar dados do contrato no CRM
                        from src.models.contract import Contract
                        contract = Contract.query.get(contract_id)
                        
                        if contract and contract.lead:
                            # Preparar dados para sincronização
                            sync_data = self._prepare_contract_data_for_erp(contract)
                            
                            # Sincronizar com FlyERP
                            sync_result = self.flyerp_service.sync_contract_to_erp(sync_data)
                            
                            if sync_result.get('success'):
                                result['flyerp_sync'] = True
                                result['flyerp_contract_id'] = sync_result.get('erp_contract_id')
                                result['flyerp_message'] = sync_result.get('message')
                                
                                # Atualizar contrato no CRM com ID do ERP
                                contract.erp_contract_id = sync_result.get('erp_contract_id')
                                contract.erp_sync_status = 'synced'
                                contract.erp_sync_date = datetime.utcnow()
                                
                                from src.models.contract import db
                                db.session.commit()
                                
                                logger.info(f"Contrato {contract_id} sincronizado com FlyERP: {sync_result.get('erp_contract_id')}")
                            else:
                                result['flyerp_error'] = sync_result.get('message')
                                logger.error(f"Erro ao sincronizar contrato {contract_id} com FlyERP: {sync_result.get('message')}")
                                
                    except Exception as e:
                        result['flyerp_error'] = str(e)
                        logger.error(f"Erro na sincronização com FlyERP: {e}")
            
            elif event_type == 'document_refused':
                result['status'] = 'refused'
                result['refused_at'] = webhook_data.get('refused_at')
                result['refusal_reason'] = webhook_data.get('reason')
                
            elif event_type == 'document_cancelled':
                result['status'] = 'cancelled'
                result['cancelled_at'] = webhook_data.get('cancelled_at')
                result['cancellation_reason'] = webhook_data.get('reason')
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao processar webhook de assinatura: {e}")
            return {
                'error': str(e),
                'webhook_data': webhook_data
            }
    
    def _prepare_contract_data_for_erp(self, contract) -> Dict[str, Any]:
        """
        Prepara dados do contrato para sincronização com FlyERP.
        
        Args:
            contract: Instância do modelo Contract
            
        Returns:
            Dados formatados para o FlyERP
        """
        lead = contract.lead
        
        # Formatar documento (CPF/CNPJ)
        document = lead.cnpj if lead.cnpj else lead.cpf
        if not document:
            raise ValueError("Lead deve ter CPF ou CNPJ para sincronização com ERP")
        
        return {
            # Dados do contrato
            "contract_number": contract.contract_number,
            "contract_value": float(contract.total_value) if contract.total_value else 0,
            "contract_date": contract.created_at.strftime("%d/%m/%Y"),
            
            # Dados do cliente
            "client_name": lead.name,
            "client_email": lead.email,
            "client_cnpj_cpf": document,
            "client_phone": lead.phone,
            "client_whatsapp": lead.whatsapp,
            "client_zipcode": lead.zipcode,
            "client_street": lead.street,
            "client_number": lead.number,
            "client_complement": lead.complement,
            "client_neighborhood": lead.neighborhood,
            "client_city": lead.city,
            "client_state": lead.state,
            
            # Dados do cartão de crédito (se disponível)
            "credit_card_data": self._get_contract_credit_card_data(contract)
        }
    
    def _get_contract_credit_card_data(self, contract) -> Optional[Dict[str, Any]]:
        """
        Obtém dados do cartão de crédito do contrato, se disponível.
        
        Args:
            contract: Instância do modelo Contract
            
        Returns:
            Dados do cartão ou None
        """
        # Verificar se há dados de cartão no contrato
        if hasattr(contract, 'payment_method') and contract.payment_method == 'credit_card':
            # Buscar dados do cartão (implementar conforme estrutura do seu modelo)
            # Por enquanto, retorna None - implementar conforme necessário
            pass
        
        return None
    
    def sync_signed_contract_to_erp(self, contract_id: int) -> Dict[str, Any]:
        """
        Sincroniza contrato assinado com FlyERP manualmente.
        
        Args:
            contract_id: ID do contrato no CRM
            
        Returns:
            Resultado da sincronização
        """
        if not self.flyerp_service:
            return {
                'success': False,
                'message': 'Serviço FlyERP não configurado'
            }
        
        try:
            from src.models.contract import Contract
            contract = Contract.query.get(contract_id)
            
            if not contract:
                return {
                    'success': False,
                    'message': 'Contrato não encontrado'
                }
            
            if contract.status != 'signed':
                return {
                    'success': False,
                    'message': 'Contrato deve estar assinado para sincronização'
                }
            
            # Preparar dados
            sync_data = self._prepare_contract_data_for_erp(contract)
            
            # Sincronizar
            result = self.flyerp_service.sync_contract_to_erp(sync_data)
            
            if result.get('success'):
                # Atualizar contrato
                contract.erp_contract_id = result.get('erp_contract_id')
                contract.erp_sync_status = 'synced'
                contract.erp_sync_date = datetime.utcnow()
                
                from src.models.contract import db
                db.session.commit()
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na sincronização manual com FlyERP: {e}")
            return {
                'success': False,
                'message': f'Erro na sincronização: {str(e)}'
            }

