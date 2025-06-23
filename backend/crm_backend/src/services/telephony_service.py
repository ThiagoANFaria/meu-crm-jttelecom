import requests
import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any

class JTTelecomPABXService:
    """
    Serviço integrado com a API oficial do PABX em Nuvem da JT Telecom
    Documentação: https://emnuvem.meupabxip.com.br/suite/api_doc.php
    """
    
    def __init__(self):
        self.base_url = "https://emnuvem.meupabxip.com.br/suite/api"
        self.auth_user = os.getenv("JTTELECOM_PABX_AUTH_USER")
        self.auth_token = os.getenv("JTTELECOM_PABX_AUTH_TOKEN")

        if not self.auth_user or not self.auth_token:
            raise ValueError("JTTELECOM_PABX_AUTH_USER and JTTELECOM_PABX_AUTH_TOKEN must be set as environment variables")

    def _make_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Realiza requisições para a API do PABX JT Telecom"""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        # Adiciona autenticação aos parâmetros da URL para GET ou ao corpo para POST/PUT
        if method == "GET":
            if params is None:
                params = {}
            params["autenticacao_usuario"] = self.auth_user
            params["autenticacao_token"] = self.auth_token
        else:
            if data is None:
                data = {}
            data["autenticacao_usuario"] = self.auth_user
            data["autenticacao_token"] = self.auth_token

        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            else:
                response = requests.request(method, url, json=data, headers=headers)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição à API do PABX: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            raise

    # ==================== DISCAGEM (CLICK-TO-CALL) ====================
    
    def click_to_call(self, numero_ramal_origem: str, numero_destino: str, variaveis: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza uma chamada click-to-call de um ramal específico para um número
        
        Args:
            numero_ramal_origem: Número do ramal que irá originar a chamada
            numero_destino: Número de destino da chamada
            variaveis: Variáveis adicionais para a chamada (opcional)
        
        Returns:
            Resposta da API com status da chamada
        """
        endpoint = "discar_numero"
        data = {
            "dados": {
                "numero_ramal_origem": numero_ramal_origem,
                "numero_destino": numero_destino,
                "variaveis": variaveis or {}
            }
        }
        return self._make_request(endpoint, method="POST", data=data)

    def discar_campanha_preview(self, operador_id: str, numero_destino: str, campanha_id: str, variaveis: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza uma chamada de um operador específico para um número em uma campanha do tipo Preview
        
        Args:
            operador_id: ID do operador
            numero_destino: Número de destino
            campanha_id: ID da campanha
            variaveis: Variáveis adicionais
        
        Returns:
            Resposta da API
        """
        endpoint = "discar_campanha"
        data = {
            "dados": {
                "operador_id": operador_id,
                "numero_destino": numero_destino,
                "campanha_id": campanha_id,
                "variaveis": variaveis or {}
            }
        }
        return self._make_request(endpoint, method="POST", data=data)

    # ==================== CHAMADAS ====================
    
    def list_online_calls(self) -> Dict[str, Any]:
        """Lista chamadas online (em andamento)"""
        endpoint = "listar_chamadas_online"
        return self._make_request(endpoint)

    def list_call_history(self, 
                         chamada_id: Optional[str] = None,
                         data_inicial: Optional[str] = None,
                         hora_inicial: Optional[str] = None,
                         data_final: Optional[str] = None,
                         hora_final: Optional[str] = None,
                         filtro_status_chamada: Optional[str] = None,
                         status_ocorrencia: Optional[str] = None,
                         ramal_origem: Optional[str] = None,
                         ramal_destino: Optional[str] = None,
                         numero_origem: Optional[str] = None,
                         numero_destino: Optional[str] = None,
                         duracao_minima: Optional[int] = None,
                         duracao_maxima: Optional[int] = None,
                         limit: int = 100,
                         offset: int = 0) -> Dict[str, Any]:
        """
        Lista histórico de chamadas com filtros avançados
        
        Args:
            chamada_id: ID específico da chamada
            data_inicial: Data inicial (DD/MM/YYYY)
            hora_inicial: Hora inicial (HH:MM)
            data_final: Data final (DD/MM/YYYY)
            hora_final: Hora final (HH:MM)
            filtro_status_chamada: 0=Não Atendido, 1=Atendido, 2=Falha, 486=Ocupado
            status_ocorrencia: 1=Produtiva, 2=Improdutiva, 3=Agendada
            ramal_origem: Ramal que originou a chamada
            ramal_destino: Ramal que recebeu a chamada
            numero_origem: Número que originou a chamada
            numero_destino: Número de destino
            duracao_minima: Duração mínima em segundos
            duracao_maxima: Duração máxima em segundos
            limit: Limite de registros
            offset: Offset para paginação
        
        Returns:
            Lista de chamadas com detalhes
        """
        endpoint = "listar_historico_chamada"
        params = {
            "limit": limit,
            "offset": offset
        }
        
        # Adiciona filtros opcionais
        if chamada_id:
            params["chamada_id"] = chamada_id
        if data_inicial:
            params["data_inicial"] = data_inicial
        if hora_inicial:
            params["hora_inicial"] = hora_inicial
        if data_final:
            params["data_final"] = data_final
        if hora_final:
            params["hora_final"] = hora_final
        if filtro_status_chamada:
            params["filtro_status_chamada"] = filtro_status_chamada
        if status_ocorrencia:
            params["status_ocorrencia"] = status_ocorrencia
        if ramal_origem:
            params["ramal_origem"] = ramal_origem
        if ramal_destino:
            params["ramal_destino"] = ramal_destino
        if numero_origem:
            params["numero_origem"] = numero_origem
        if numero_destino:
            params["numero_destino"] = numero_destino
        if duracao_minima:
            params["duracao_minima"] = duracao_minima
        if duracao_maxima:
            params["duracao_maxima"] = duracao_maxima
            
        return self._make_request(endpoint, params=params)

    # ==================== RAMAIS ====================
    
    def list_extensions(self, ramal_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Lista os ramais configurados
        
        Args:
            ramal_id: ID específico do ramal (opcional)
            limit: Limite de registros
            offset: Offset para paginação
        
        Returns:
            Lista de ramais
        """
        endpoint = "listar_ramais"
        params = {
            "limit": limit,
            "offset": offset
        }
        if ramal_id:
            params["ramal_id"] = ramal_id
            
        return self._make_request(endpoint, params=params)

    def create_extension(self, dados_ramal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo ramal
        
        Args:
            dados_ramal: Dados do ramal a ser criado
        
        Returns:
            Resposta da API
        """
        endpoint = "inserir_ramal"
        return self._make_request(endpoint, method="POST", data=dados_ramal)

    def update_extension(self, ramal_id: str, dados_ramal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza dados de um ramal
        
        Args:
            ramal_id: ID do ramal
            dados_ramal: Novos dados do ramal
        
        Returns:
            Resposta da API
        """
        endpoint = "alterar_ramal"
        data = {"ramal_id": ramal_id, **dados_ramal}
        return self._make_request(endpoint, method="PUT", data=data)

    def delete_extension(self, ramal_id: str) -> Dict[str, Any]:
        """
        Deleta um ramal
        
        Args:
            ramal_id: ID do ramal a ser deletado
        
        Returns:
            Resposta da API
        """
        endpoint = "deletar_ramal"
        data = {"ramal_id": ramal_id}
        return self._make_request(endpoint, method="DELETE", data=data)

    # ==================== DIDs (NÚMEROS REMOTOS) ====================
    
    def list_dids(self, did_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Lista DIDs (números remotos)
        
        Args:
            did_id: ID específico do DID (opcional)
            limit: Limite de registros
            offset: Offset para paginação
        
        Returns:
            Lista de DIDs
        """
        endpoint = "listar_dids"
        params = {
            "limit": limit,
            "offset": offset
        }
        if did_id:
            params["did_id"] = did_id
            
        return self._make_request(endpoint, params=params)

    def create_did(self, dados_did: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo DID
        
        Args:
            dados_did: Dados do DID a ser criado
        
        Returns:
            Resposta da API
        """
        endpoint = "inserir_did"
        return self._make_request(endpoint, method="POST", data=dados_did)

    def update_did(self, did_id: str, dados_did: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza informações de um DID
        
        Args:
            did_id: ID do DID
            dados_did: Novos dados do DID
        
        Returns:
            Resposta da API
        """
        endpoint = "alterar_did"
        data = {"did_id": did_id, **dados_did}
        return self._make_request(endpoint, method="PUT", data=data)

    def delete_did(self, did_id: str) -> Dict[str, Any]:
        """
        Deleta um DID
        
        Args:
            did_id: ID do DID a ser deletado
        
        Returns:
            Resposta da API
        """
        endpoint = "deletar_did"
        data = {"did_id": did_id}
        return self._make_request(endpoint, method="DELETE", data=data)

    # ==================== PESSOAS/OPERADORES ====================
    
    def list_people(self, pessoa_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Lista pessoas/operadores
        
        Args:
            pessoa_id: ID específico da pessoa (opcional)
            limit: Limite de registros
            offset: Offset para paginação
        
        Returns:
            Lista de pessoas
        """
        endpoint = "listar_pessoas"
        params = {
            "limit": limit,
            "offset": offset
        }
        if pessoa_id:
            params["pessoa_id"] = pessoa_id
            
        return self._make_request(endpoint, params=params)

    def operator_login(self, operador_id: str) -> Dict[str, Any]:
        """
        Realiza login de um operador, iniciando sua jornada de trabalho
        
        Args:
            operador_id: ID do operador
        
        Returns:
            Resposta da API
        """
        endpoint = "login_operador"
        data = {"operador_id": operador_id}
        return self._make_request(endpoint, method="PUT", data=data)

    def operator_logout(self, operador_id: str) -> Dict[str, Any]:
        """
        Realiza logout de um operador
        
        Args:
            operador_id: ID do operador
        
        Returns:
            Resposta da API
        """
        endpoint = "logout_operador"
        data = {"operador_id": operador_id}
        return self._make_request(endpoint, method="PUT", data=data)

    def operator_pause(self, operador_id: str, motivo_pausa: str) -> Dict[str, Any]:
        """
        Realiza pausa de um operador
        
        Args:
            operador_id: ID do operador
            motivo_pausa: Motivo da pausa
        
        Returns:
            Resposta da API
        """
        endpoint = "pausar_operador"
        data = {
            "operador_id": operador_id,
            "motivo_pausa": motivo_pausa
        }
        return self._make_request(endpoint, method="PUT", data=data)

    def operator_unpause(self, operador_id: str) -> Dict[str, Any]:
        """
        Remove pausa de um operador
        
        Args:
            operador_id: ID do operador
        
        Returns:
            Resposta da API
        """
        endpoint = "despausar_operador"
        data = {"operador_id": operador_id}
        return self._make_request(endpoint, method="PUT", data=data)

    # ==================== TRONCOS ====================
    
    def list_trunks(self, tronco_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Lista troncos
        
        Args:
            tronco_id: ID específico do tronco (opcional)
            limit: Limite de registros
            offset: Offset para paginação
        
        Returns:
            Lista de troncos
        """
        endpoint = "listar_troncos"
        params = {
            "limit": limit,
            "offset": offset
        }
        if tronco_id:
            params["tronco_id"] = tronco_id
            
        return self._make_request(endpoint, params=params)

    # ==================== CAMPANHAS ====================
    
    def list_campaigns(self, campanha_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Lista campanhas
        
        Args:
            campanha_id: ID específico da campanha (opcional)
            limit: Limite de registros
            offset: Offset para paginação
        
        Returns:
            Lista de campanhas
        """
        endpoint = "listar_campanhas"
        params = {
            "limit": limit,
            "offset": offset
        }
        if campanha_id:
            params["campanha_id"] = campanha_id
            
        return self._make_request(endpoint, params=params)

    def create_campaign(self, dados_campanha: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova campanha
        
        Args:
            dados_campanha: Dados da campanha
        
        Returns:
            Resposta da API
        """
        endpoint = "inserir_campanha"
        return self._make_request(endpoint, method="POST", data=dados_campanha)

    # ==================== MÉTODOS AUXILIARES ====================
    
    def get_call_status_description(self, status_code: str) -> str:
        """
        Retorna descrição do status da chamada
        
        Args:
            status_code: Código do status
        
        Returns:
            Descrição do status
        """
        status_map = {
            "0": "Não Atendido",
            "1": "Atendido",
            "2": "Falha",
            "486": "Ocupado"
        }
        return status_map.get(status_code, f"Status desconhecido: {status_code}")

    def get_occurrence_status_description(self, status_code: str) -> str:
        """
        Retorna descrição do status da ocorrência
        
        Args:
            status_code: Código do status
        
        Returns:
            Descrição do status
        """
        status_map = {
            "1": "Produtiva",
            "2": "Improdutiva", 
            "3": "Agendada"
        }
        return status_map.get(status_code, f"Status desconhecido: {status_code}")

    def format_call_duration(self, duration_seconds: int) -> str:
        """
        Formata duração da chamada em formato legível
        
        Args:
            duration_seconds: Duração em segundos
        
        Returns:
            Duração formatada (HH:MM:SS)
        """
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def validate_phone_number(self, phone_number: str) -> bool:
        """
        Valida formato do número de telefone
        
        Args:
            phone_number: Número a ser validado
        
        Returns:
            True se válido, False caso contrário
        """
        # Remove caracteres não numéricos
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Verifica se tem pelo menos 10 dígitos (telefone fixo) ou 11 (celular)
        return len(clean_number) >= 10

    def test_connection(self) -> Dict[str, Any]:
        """
        Testa conectividade com a API
        
        Returns:
            Resultado do teste
        """
        try:
            # Tenta listar ramais como teste de conectividade
            result = self.list_extensions(limit=1)
            return {
                "success": True,
                "message": "Conexão com API JT Telecom estabelecida com sucesso",
                "api_response": result
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao conectar com API JT Telecom: {str(e)}",
                "error": str(e)
            }

