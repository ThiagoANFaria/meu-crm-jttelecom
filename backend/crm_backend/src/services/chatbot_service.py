import requests
import json
import openai
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from flask import current_app

class WhatsAppBusinessService:
    """Serviço para integração com WhatsApp Business API."""
    
    def __init__(self, access_token: str, phone_number_id: str, business_account_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.business_account_id = business_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """Envia mensagem de texto."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def send_interactive_message(self, to: str, message: str, buttons: List[Dict]) -> Dict[str, Any]:
        """Envia mensagem com botões interativos."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        interactive_buttons = []
        for i, button in enumerate(buttons[:3]):  # WhatsApp permite máximo 3 botões
            interactive_buttons.append({
                "type": "reply",
                "reply": {
                    "id": button.get("id", f"btn_{i}"),
                    "title": button.get("title", "")[:20]  # Máximo 20 caracteres
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": message},
                "action": {"buttons": interactive_buttons}
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def send_list_message(self, to: str, message: str, button_text: str, sections: List[Dict]) -> Dict[str, Any]:
        """Envia mensagem com lista de opções."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        list_sections = []
        for section in sections:
            rows = []
            for row in section.get("rows", [])[:10]:  # Máximo 10 itens por seção
                rows.append({
                    "id": row.get("id", ""),
                    "title": row.get("title", "")[:24],  # Máximo 24 caracteres
                    "description": row.get("description", "")[:72]  # Máximo 72 caracteres
                })
            
            list_sections.append({
                "title": section.get("title", "")[:24],
                "rows": rows
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": message},
                "action": {
                    "button": button_text[:20],
                    "sections": list_sections
                }
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """Marca mensagem como lida."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

class EvolutionAPIService:
    """Serviço para integração com Evolution API."""
    
    def __init__(self, api_url: str, api_key: str, instance_name: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.instance_name = instance_name
        
    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """Envia mensagem de texto via Evolution API."""
        url = f"{self.api_url}/message/sendText/{self.instance_name}"
        
        payload = {
            "number": to,
            "text": message
        }
        
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def send_buttons_message(self, to: str, message: str, buttons: List[Dict]) -> Dict[str, Any]:
        """Envia mensagem com botões via Evolution API."""
        url = f"{self.api_url}/message/sendButtons/{self.instance_name}"
        
        button_list = []
        for button in buttons:
            button_list.append({
                "buttonId": button.get("id", ""),
                "buttonText": {"displayText": button.get("title", "")}
            })
        
        payload = {
            "number": to,
            "text": message,
            "buttons": button_list
        }
        
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def get_instance_status(self) -> Dict[str, Any]:
        """Verifica status da instância."""
        url = f"{self.api_url}/instance/connectionState/{self.instance_name}"
        
        headers = {
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

class OpenAIService:
    """Serviço para integração com OpenAI GPT."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o", max_tokens: int = 1000, temperature: float = 0.7):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    def generate_response(self, messages: List[Dict], system_prompt: str = None) -> Dict[str, Any]:
        """Gera resposta usando OpenAI."""
        try:
            # Prepara as mensagens
            chat_messages = []
            
            if system_prompt:
                chat_messages.append({"role": "system", "content": system_prompt})
            
            # Adiciona mensagens da conversa
            for msg in messages:
                role = "user" if msg.get("direction") == "incoming" else "assistant"
                chat_messages.append({"role": role, "content": msg.get("content", "")})
            
            # Chama a API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def generate_response_async(self, messages: List[Dict], system_prompt: str = None) -> Dict[str, Any]:
        """Gera resposta de forma assíncrona."""
        try:
            # Simula processamento assíncrono
            await asyncio.sleep(0.1)
            return self.generate_response(messages, system_prompt)
        except Exception as e:
            return {"success": False, "error": str(e)}

class ChatFlowEngine:
    """Engine para processar fluxos de conversa."""
    
    def __init__(self):
        self.current_step = None
        self.variables = {}
    
    def process_flow_step(self, flow_data: Dict, current_step: str, user_input: str, variables: Dict) -> Dict[str, Any]:
        """Processa uma etapa do fluxo."""
        try:
            steps = flow_data.get("steps", {})
            step = steps.get(current_step)
            
            if not step:
                return {"error": "Etapa não encontrada"}
            
            step_type = step.get("type", "text")
            
            if step_type == "text":
                return self._process_text_step(step, variables)
            elif step_type == "input":
                return self._process_input_step(step, user_input, variables)
            elif step_type == "buttons":
                return self._process_buttons_step(step, user_input, variables)
            elif step_type == "condition":
                return self._process_condition_step(step, variables)
            elif step_type == "webhook":
                return self._process_webhook_step(step, variables)
            elif step_type == "ai":
                return self._process_ai_step(step, user_input, variables)
            else:
                return {"error": f"Tipo de etapa não suportado: {step_type}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _process_text_step(self, step: Dict, variables: Dict) -> Dict[str, Any]:
        """Processa etapa de texto."""
        message = self._replace_variables(step.get("message", ""), variables)
        next_step = step.get("next_step")
        
        return {
            "type": "text",
            "message": message,
            "next_step": next_step
        }
    
    def _process_input_step(self, step: Dict, user_input: str, variables: Dict) -> Dict[str, Any]:
        """Processa etapa de entrada de dados."""
        variable_name = step.get("variable_name")
        validation = step.get("validation", {})
        
        # Valida entrada
        if validation:
            validation_result = self._validate_input(user_input, validation)
            if not validation_result["valid"]:
                return {
                    "type": "validation_error",
                    "message": validation_result["message"],
                    "retry": True
                }
        
        # Salva variável
        if variable_name:
            variables[variable_name] = user_input
        
        next_step = step.get("next_step")
        
        return {
            "type": "input_saved",
            "variable_name": variable_name,
            "value": user_input,
            "next_step": next_step,
            "variables": variables
        }
    
    def _process_buttons_step(self, step: Dict, user_input: str, variables: Dict) -> Dict[str, Any]:
        """Processa etapa de botões."""
        buttons = step.get("buttons", [])
        
        # Encontra botão selecionado
        selected_button = None
        for button in buttons:
            if button.get("id") == user_input or button.get("title") == user_input:
                selected_button = button
                break
        
        if not selected_button:
            return {
                "type": "invalid_option",
                "message": "Opção inválida. Por favor, selecione uma das opções disponíveis.",
                "retry": True
            }
        
        # Salva variável se especificada
        variable_name = step.get("variable_name")
        if variable_name:
            variables[variable_name] = selected_button.get("value", selected_button.get("title"))
        
        next_step = selected_button.get("next_step", step.get("next_step"))
        
        return {
            "type": "button_selected",
            "selected": selected_button,
            "next_step": next_step,
            "variables": variables
        }
    
    def _process_condition_step(self, step: Dict, variables: Dict) -> Dict[str, Any]:
        """Processa etapa condicional."""
        conditions = step.get("conditions", [])
        
        for condition in conditions:
            if self._evaluate_condition(condition, variables):
                return {
                    "type": "condition_met",
                    "next_step": condition.get("next_step")
                }
        
        # Fallback
        return {
            "type": "condition_fallback",
            "next_step": step.get("fallback_step")
        }
    
    def _process_webhook_step(self, step: Dict, variables: Dict) -> Dict[str, Any]:
        """Processa etapa de webhook."""
        webhook_url = step.get("webhook_url")
        method = step.get("method", "POST")
        
        try:
            if method.upper() == "POST":
                response = requests.post(webhook_url, json=variables, timeout=10)
            else:
                response = requests.get(webhook_url, params=variables, timeout=10)
            
            response.raise_for_status()
            
            return {
                "type": "webhook_success",
                "response": response.json() if response.content else {},
                "next_step": step.get("next_step")
            }
            
        except Exception as e:
            return {
                "type": "webhook_error",
                "error": str(e),
                "next_step": step.get("error_step", step.get("next_step"))
            }
    
    def _process_ai_step(self, step: Dict, user_input: str, variables: Dict) -> Dict[str, Any]:
        """Processa etapa de IA."""
        return {
            "type": "ai_trigger",
            "context": step.get("context", ""),
            "user_input": user_input,
            "variables": variables,
            "next_step": step.get("next_step")
        }
    
    def _replace_variables(self, text: str, variables: Dict) -> str:
        """Substitui variáveis no texto."""
        for key, value in variables.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text
    
    def _validate_input(self, input_value: str, validation: Dict) -> Dict[str, Any]:
        """Valida entrada do usuário."""
        validation_type = validation.get("type")
        
        if validation_type == "email":
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, input_value):
                return {"valid": False, "message": "Por favor, digite um e-mail válido."}
        
        elif validation_type == "phone":
            import re
            phone_pattern = r'^\(?[1-9]{2}\)?\s?9?\d{4}-?\d{4}$'
            if not re.match(phone_pattern, input_value.replace(" ", "")):
                return {"valid": False, "message": "Por favor, digite um telefone válido."}
        
        elif validation_type == "cnpj":
            # Validação básica de CNPJ
            cnpj = ''.join(filter(str.isdigit, input_value))
            if len(cnpj) != 14:
                return {"valid": False, "message": "Por favor, digite um CNPJ válido."}
        
        elif validation_type == "required":
            if not input_value.strip():
                return {"valid": False, "message": "Este campo é obrigatório."}
        
        elif validation_type == "min_length":
            min_length = validation.get("value", 1)
            if len(input_value) < min_length:
                return {"valid": False, "message": f"Mínimo de {min_length} caracteres."}
        
        elif validation_type == "max_length":
            max_length = validation.get("value", 255)
            if len(input_value) > max_length:
                return {"valid": False, "message": f"Máximo de {max_length} caracteres."}
        
        return {"valid": True}
    
    def _evaluate_condition(self, condition: Dict, variables: Dict) -> bool:
        """Avalia condição."""
        variable = condition.get("variable")
        operator = condition.get("operator")
        value = condition.get("value")
        
        if variable not in variables:
            return False
        
        var_value = variables[variable]
        
        if operator == "equals":
            return str(var_value) == str(value)
        elif operator == "not_equals":
            return str(var_value) != str(value)
        elif operator == "contains":
            return str(value).lower() in str(var_value).lower()
        elif operator == "starts_with":
            return str(var_value).lower().startswith(str(value).lower())
        elif operator == "ends_with":
            return str(var_value).lower().endswith(str(value).lower())
        elif operator == "greater_than":
            try:
                return float(var_value) > float(value)
            except:
                return False
        elif operator == "less_than":
            try:
                return float(var_value) < float(value)
            except:
                return False
        
        return False

