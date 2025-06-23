from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.telephony import Call, CallLog, db
from src.models.user import User
from src.models.lead import Lead
from src.models.pipeline import Opportunity
from src.services.telephony_service import JTTelecomPABXService
from datetime import datetime, timedelta
import logging
from flasgger import swag_from

telephony_bp = Blueprint("telephony", __name__)
logger = logging.getLogger(__name__)

# Inicializar serviço de telefonia
try:
    pabx_service = JTTelecomPABXService()
except Exception as e:
    logger.error(f"Erro ao inicializar serviço PABX: {e}")
    pabx_service = None

@telephony_bp.route("/test-connection", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Conexão com PABX testada com sucesso"},
        "500": {"description": "Erro ao testar conexão ou serviço PABX não configurado"}
    }
})
def test_pabx_connection():
    """Testa conectividade com a API do PABX JT Telecom"""
    if not pabx_service:
        return jsonify({
            "success": False,
            "message": "Serviço PABX não configurado. Verifique as variáveis de ambiente."
        }), 500
    
    try:
        result = pabx_service.test_connection()
        return jsonify(result), 200 if result["success"] else 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao testar conexão: {str(e)}"
        }), 500

@telephony_bp.route("/click-to-call", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "ClickToCall",
                "required": ["ramal_origem", "numero_destino"],
                "properties": {
                    "ramal_origem": {"type": "string", "description": "Ramal de origem da chamada"},
                    "numero_destino": {"type": "string", "description": "Número de destino da chamada"},
                    "lead_id": {"type": "string", "description": "ID do lead associado"},
                    "opportunity_id": {"type": "string", "description": "ID da oportunidade associada"},
                    "notes": {"type": "string", "description": "Notas sobre a chamada"},
                    "variaveis": {"type": "object", "description": "Variáveis adicionais para a chamada"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Chamada iniciada com sucesso"},
        "400": {"description": "Dados inválidos"},
        "500": {"description": "Erro ao realizar chamada ou serviço PABX não configurado"}
    }
})
def click_to_call():
    """Realiza uma chamada click-to-call"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validações
    required_fields = ["ramal_origem", "numero_destino"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo {field} é obrigatório"}), 400
    
    # Validar número de telefone
    if not pabx_service.validate_phone_number(data["numero_destino"]):
        return jsonify({"error": "Número de telefone inválido"}), 400
    
    try:
        # Realizar chamada via API do PABX
        pabx_response = pabx_service.click_to_call(
            numero_ramal_origem=data["ramal_origem"],
            numero_destino=data["numero_destino"],
            variaveis=data.get("variaveis", {})
        )
        
        # Registrar chamada no CRM
        call = Call(
            lead_id=data.get("lead_id"),
            opportunity_id=data.get("opportunity_id"),
            user_id=current_user_id,
            phone_number=data["numero_destino"],
            direction="outbound",
            status="in_progress",
            start_time=datetime.utcnow(),
            external_call_id=pabx_response.get("call_id"),
            notes=data.get("notes")
        )
        
        db.session.add(call)
        db.session.commit()
        
        # Log do evento
        call_log = CallLog(
            call_id=call.id,
            event_type="dialing",
            event_data=pabx_response,
            timestamp=datetime.utcnow()
        )
        db.session.add(call_log)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Chamada iniciada com sucesso",
            "call_id": call.id,
            "pabx_response": pabx_response
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao realizar click-to-call: {e}")
        return jsonify({"error": f"Erro ao realizar chamada: {str(e)}"}), 500

@telephony_bp.route("/calls", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "lead_id",
            "in": "query",
            "type": "integer",
            "description": "Filtrar por ID do lead"
        },
        {
            "name": "opportunity_id",
            "in": "query",
            "type": "integer",
            "description": "Filtrar por ID da oportunidade"
        },
        {
            "name": "direction",
            "in": "query",
            "type": "string",
            "enum": ["inbound", "outbound"],
            "description": "Filtrar por direção da chamada"
        },
        {
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "Filtrar por status da chamada"
        },
        {
            "name": "start_date",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data de início para filtro (YYYY-MM-DD)"
        },
        {
            "name": "end_date",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data de fim para filtro (YYYY-MM-DD)"
        },
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "description": "Número da página",
            "default": 1
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "description": "Itens por página",
            "default": 20
        }
    ],
    "responses": {
        "200": {"description": "Lista de chamadas com filtros e paginação"},
        "401": {"description": "Não autorizado"}
    }
})
def list_calls():
    """Lista chamadas com filtros"""
    current_user_id = get_jwt_identity()
    
    # Parâmetros de filtro
    lead_id = request.args.get("lead_id", type=int)
    opportunity_id = request.args.get("opportunity_id", type=int)
    direction = request.args.get("direction")  # "inbound" or "outbound"
    status = request.args.get("status")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    
    # Construir query
    query = Call.query
    
    # Filtros
    if lead_id:
        query = query.filter(Call.lead_id == lead_id)
    if opportunity_id:
        query = query.filter(Call.opportunity_id == opportunity_id)
    if direction:
        query = query.filter(Call.direction == direction)
    if status:
        query = query.filter(Call.status == status)
    if start_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Call.start_time >= start_dt)
    if end_date:
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Call.start_time < end_dt)
    
    # Ordenar por data mais recente
    query = query.order_by(Call.start_time.desc())
    
    # Paginação
    calls = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "calls": [call.to_dict() for call in calls.items],
        "total": calls.total,
        "pages": calls.pages,
        "current_page": page,
        "per_page": per_page
    }), 200

@telephony_bp.route("/calls/<int:call_id>", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "call_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID da chamada"
        }
    ],
    "responses": {
        "200": {"description": "Detalhes de uma chamada específica"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Chamada não encontrada"}
    }
})
def get_call_details(call_id):
    """Obtém detalhes de uma chamada específica"""
    call = Call.query.get_or_404(call_id)
    
    # Incluir logs da chamada
    call_data = call.to_dict()
    call_data["logs"] = [log.to_dict() for log in call.logs]
    
    return jsonify(call_data), 200

@telephony_bp.route("/calls/<int:call_id>/update", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "call_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID da chamada"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "CallUpdate",
                "properties": {
                    "status": {"type": "string", "description": "Status da chamada"},
                    "duration": {"type": "integer", "description": "Duração da chamada em segundos"},
                    "notes": {"type": "string", "description": "Notas sobre a chamada"},
                    "recording_url": {"type": "string", "description": "URL da gravação da chamada"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Informações de uma chamada atualizadas com sucesso"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Chamada não encontrada"}
    }
})
def update_call(call_id):
    """Atualiza informações de uma chamada"""
    call = Call.query.get_or_404(call_id)
    data = request.get_json()
    
    # Campos atualizáveis
    if "status" in data:
        call.status = data["status"]
        if data["status"] in ["completed", "failed", "missed"]:
            call.end_time = datetime.utcnow()
    
    if "duration" in data:
        call.duration = data["duration"]
    
    if "notes" in data:
        call.notes = data["notes"]
    
    if "recording_url" in data:
        call.recording_url = data["recording_url"]
    
    call.updated_at = datetime.utcnow()
    
    # Log da atualização
    call_log = CallLog(
        call_id=call.id,
        event_type="updated",
        event_data=data,
        timestamp=datetime.utcnow()
    )
    db.session.add(call_log)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Chamada atualizada com sucesso",
        "call": call.to_dict()
    }), 200

@telephony_bp.route("/pabx/history", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - PABX"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "data_inicial",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data inicial para o histórico (YYYY-MM-DD)"
        },
        {
            "name": "hora_inicial",
            "in": "query",
            "type": "string",
            "format": "time",
            "description": "Hora inicial para o histórico (HH:MM:SS)"
        },
        {
            "name": "data_final",
            "in": "query",
            "type": "string",
            "format": "date",
            "description": "Data final para o histórico (YYYY-MM-DD)"
        },
        {
            "name": "hora_final",
            "in": "query",
            "type": "string",
            "format": "time",
            "description": "Hora final para o histórico (HH:MM:SS)"
        },
        {
            "name": "filtro_status_chamada",
            "in": "query",
            "type": "string",
            "description": "Filtrar por status da chamada"
        },
        {
            "name": "ramal_origem",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ramal de origem"
        },
        {
            "name": "ramal_destino",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ramal de destino"
        },
        {
            "name": "numero_origem",
            "in": "query",
            "type": "string",
            "description": "Filtrar por número de origem"
        },
        {
            "name": "numero_destino",
            "in": "query",
            "type": "string",
            "description": "Filtrar por número de destino"
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "description": "Limite de resultados",
            "default": 50
        },
        {
            "name": "offset",
            "in": "query",
            "type": "integer",
            "description": "Offset para paginação",
            "default": 0
        }
    ],
    "responses": {
        "200": {"description": "Histórico de chamadas do PABX"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao buscar histórico ou serviço PABX não configurado"}
    }
})
def get_pabx_call_history():
    """Obtém histórico de chamadas diretamente do PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    # Parâmetros de filtro
    params = {
        "data_inicial": request.args.get("data_inicial"),
        "hora_inicial": request.args.get("hora_inicial"),
        "data_final": request.args.get("data_final"),
        "hora_final": request.args.get("hora_final"),
        "filtro_status_chamada": request.args.get("status"),
        "ramal_origem": request.args.get("ramal_origem"),
        "ramal_destino": request.args.get("ramal_destino"),
        "numero_origem": request.args.get("numero_origem"),
        "numero_destino": request.args.get("numero_destino"),
        "limit": request.args.get("limit", 50, type=int),
        "offset": request.args.get("offset", 0, type=int)
    }
    
    # Remove parâmetros None
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        history = pabx_service.list_call_history(**params)
        return jsonify(history), 200
    except Exception as e:
        logger.error(f"Erro ao buscar histórico do PABX: {e}")
        return jsonify({"error": f"Erro ao buscar histórico: {str(e)}"}), 500

@telephony_bp.route("/pabx/online-calls", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - PABX"],
    "security": [{
        "BearerAuth": []
    }],
    "responses": {
        "200": {"description": "Lista de chamadas online no PABX"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao buscar chamadas online ou serviço PABX não configurado"}
    }
})
def get_online_calls():
    """Lista chamadas online no PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    try:
        online_calls = pabx_service.list_online_calls()
        return jsonify(online_calls), 200
    except Exception as e:
        logger.error(f"Erro ao buscar chamadas online: {e}")
        return jsonify({"error": f"Erro ao buscar chamadas online: {str(e)}"}), 500

@telephony_bp.route("/extensions", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Ramais"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "ramal_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do ramal"
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "description": "Limite de resultados",
            "default": 100
        },
        {
            "name": "offset",
            "in": "query",
            "type": "integer",
            "description": "Offset para paginação",
            "default": 0
        }
    ],
    "responses": {
        "200": {"description": "Lista de ramais configurados no PABX"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao listar ramais ou serviço PABX não configurado"}
    }
})
def list_extensions():
    """Lista ramais configurados no PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    ramal_id = request.args.get("ramal_id")
    limit = request.args.get("limit", 100, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    try:
        extensions = pabx_service.list_extensions(
            ramal_id=ramal_id,
            limit=limit,
            offset=offset
        )
        return jsonify(extensions), 200
    except Exception as e:
        logger.error(f"Erro ao listar ramais: {e}")
        return jsonify({"error": f"Erro ao listar ramais: {str(e)}"}), 500

@telephony_bp.route("/extensions", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Ramais"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "CreateExtension",
                "properties": {
                    "ramal": {"type": "string", "description": "Número do ramal"},
                    "senha": {"type": "string", "description": "Senha do ramal"},
                    "nome": {"type": "string", "description": "Nome do usuário do ramal"}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Ramal criado com sucesso"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao criar ramal ou serviço PABX não configurado"}
    }
})
def create_extension():
    """Cria um novo ramal"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    data = request.get_json()
    
    try:
        result = pabx_service.create_extension(data)
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Erro ao criar ramal: {e}")
        return jsonify({"error": f"Erro ao criar ramal: {str(e)}"}), 500

@telephony_bp.route("/extensions/<ramal_id>", methods=["PUT"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Ramais"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "ramal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do ramal"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "UpdateExtension",
                "properties": {
                    "senha": {"type": "string", "description": "Nova senha do ramal"},
                    "nome": {"type": "string", "description": "Novo nome do usuário do ramal"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Ramal atualizado com sucesso"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Ramal não encontrado"},
        "500": {"description": "Erro ao atualizar ramal ou serviço PABX não configurado"}
    }
})
def update_extension(ramal_id):
    """Atualiza um ramal"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    data = request.get_json()
    
    try:
        result = pabx_service.update_extension(ramal_id, data)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar ramal: {e}")
        return jsonify({"error": f"Erro ao atualizar ramal: {str(e)}"}), 500

@telephony_bp.route("/extensions/<ramal_id>", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Ramais"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "ramal_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do ramal"
        }
    ],
    "responses": {
        "200": {"description": "Ramal deletado com sucesso"},
        "401": {"description": "Não autorizado"},
        "404": {"description": "Ramal não encontrado"},
        "500": {"description": "Erro ao deletar ramal ou serviço PABX não configurado"}
    }
})
def delete_extension(ramal_id):
    """Deleta um ramal"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    try:
        result = pabx_service.delete_extension(ramal_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao deletar ramal: {e}")
        return jsonify({"error": f"Erro ao deletar ramal: {str(e)}"}), 500

@telephony_bp.route("/dids", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - DIDs"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "did_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID do DID"
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "description": "Limite de resultados",
            "default": 100
        },
        {
            "name": "offset",
            "in": "query",
            "type": "integer",
            "description": "Offset para paginação",
            "default": 0
        }
    ],
    "responses": {
        "200": {"description": "Lista de DIDs (números remotos)"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao listar DIDs ou serviço PABX não configurado"}
    }
})
def list_dids():
    """Lista DIDs (números remotos)"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    did_id = request.args.get("did_id")
    limit = request.args.get("limit", 100, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    try:
        dids = pabx_service.list_dids(
            did_id=did_id,
            limit=limit,
            offset=offset
        )
        return jsonify(dids), 200
    except Exception as e:
        logger.error(f"Erro ao listar DIDs: {e}")
        return jsonify({"error": f"Erro ao listar DIDs: {str(e)}"}), 500

@telephony_bp.route("/operators/<operador_id>/login", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Operadores"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "operador_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do operador"
        }
    ],
    "responses": {
        "200": {"description": "Login de operador realizado com sucesso"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao fazer login do operador ou serviço PABX não configurado"}
    }
})
def operator_login(operador_id):
    """Realiza login de operador no PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    try:
        result = pabx_service.operator_login(operador_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao fazer login do operador: {e}")
        return jsonify({"error": f"Erro ao fazer login: {str(e)}"}), 500

@telephony_bp.route("/operators/<operador_id>/logout", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Operadores"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "operador_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do operador"
        }
    ],
    "responses": {
        "200": {"description": "Logout de operador realizado com sucesso"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao fazer logout do operador ou serviço PABX não configurado"}
    }
})
def operator_logout(operador_id):
    """Realiza logout de operador no PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    try:
        result = pabx_service.operator_logout(operador_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao fazer logout do operador: {e}")
        return jsonify({"error": f"Erro ao fazer logout: {str(e)}"}), 500

@telephony_bp.route("/operators/<operador_id>/pause", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Operadores"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "operador_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do operador"
        },
        {
            "name": "body",
            "in": "body",
            "schema": {
                "id": "OperatorPause",
                "properties": {
                    "motivo_pausa": {"type": "string", "description": "Motivo da pausa"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Operador pausado com sucesso"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao pausar operador ou serviço PABX não configurado"}
    }
})
def operator_pause(operador_id):
    """Pausa operador no PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    data = request.get_json()
    motivo_pausa = data.get("motivo_pausa", "Pausa manual")
    
    try:
        result = pabx_service.operator_pause(operador_id, motivo_pausa)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao pausar operador: {e}")
        return jsonify({"error": f"Erro ao pausar operador: {str(e)}"}), 500

@telephony_bp.route("/operators/<operador_id>/unpause", methods=["POST"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Operadores"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "operador_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "ID do operador"
        }
    ],
    "responses": {
        "200": {"description": "Pausa do operador removida com sucesso"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao despausar operador ou serviço PABX não configurado"}
    }
})
def operator_unpause(operador_id):
    """Remove pausa do operador no PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    try:
        result = pabx_service.operator_unpause(operador_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao despausar operador: {e}")
        return jsonify({"error": f"Erro ao despausar operador: {str(e)}"}), 500

@telephony_bp.route("/campaigns", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Campanhas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "campanha_id",
            "in": "query",
            "type": "string",
            "description": "Filtrar por ID da campanha"
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "description": "Limite de resultados",
            "default": 100
        },
        {
            "name": "offset",
            "in": "query",
            "type": "integer",
            "description": "Offset para paginação",
            "default": 0
        }
    ],
    "responses": {
        "200": {"description": "Lista de campanhas do PABX"},
        "401": {"description": "Não autorizado"},
        "500": {"description": "Erro ao listar campanhas ou serviço PABX não configurado"}
    }
})
def list_campaigns():
    """Lista campanhas do PABX"""
    if not pabx_service:
        return jsonify({"error": "Serviço PABX não configurado"}), 500
    
    campanha_id = request.args.get("campanha_id")
    limit = request.args.get("limit", 100, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    try:
        campaigns = pabx_service.list_campaigns(
            campanha_id=campanha_id,
            limit=limit,
            offset=offset
        )
        return jsonify(campaigns), 200
    except Exception as e:
        logger.error(f"Erro ao listar campanhas: {e}")
        return jsonify({"error": f"Erro ao listar campanhas: {str(e)}"}), 500

@telephony_bp.route("/stats", methods=["GET"])
@jwt_required()
@swag_from({
    "tags": ["Telefonia - Estatísticas"],
    "security": [{
        "BearerAuth": []
    }],
    "parameters": [
        {
            "name": "days",
            "in": "query",
            "type": "integer",
            "description": "Número de dias para calcular as estatísticas",
            "default": 30
        }
    ],
    "responses": {
        "200": {"description": "Estatísticas de telefonia"},
        "401": {"description": "Não autorizado"}
    }
})
def get_telephony_stats():
    """Obtém estatísticas de telefonia"""
    current_user_id = get_jwt_identity()
    
    # Período para estatísticas (padrão: últimos 30 dias)
    days = request.args.get("days", 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Estatísticas básicas
    total_calls = Call.query.filter(Call.start_time >= start_date).count()
    completed_calls = Call.query.filter(
        Call.start_time >= start_date,
        Call.status == "completed"
    ).count()
    missed_calls = Call.query.filter(
        Call.start_time >= start_date,
        Call.status == "missed"
    ).count()
    failed_calls = Call.query.filter(
        Call.start_time >= start_date,
        Call.status == "failed"
    ).count()
    
    # Estatísticas por direção
    inbound_calls = Call.query.filter(
        Call.start_time >= start_date,
        Call.direction == "inbound"
    ).count()
    outbound_calls = Call.query.filter(
        Call.start_time >= start_date,
        Call.direction == "outbound"
    ).count()
    
    # Taxa de sucesso
    success_rate = (completed_calls / total_calls * 100) if total_calls > 0 else 0
    
    # Duração média das chamadas completadas
    avg_duration_result = db.session.query(
        db.func.avg(Call.duration)
    ).filter(
        Call.start_time >= start_date,
        Call.status == "completed",
        Call.duration.isnot(None)
    ).scalar()
    
    avg_duration = int(avg_duration_result) if avg_duration_result else 0
    
    return jsonify({
        "period_days": days,
        "total_calls": total_calls,
        "completed_calls": completed_calls,
        "missed_calls": missed_calls,
        "failed_calls": failed_calls,
        "inbound_calls": inbound_calls,
        "outbound_calls": outbound_calls,
        "success_rate": round(success_rate, 2),
        "average_duration_seconds": avg_duration
    }), 200


