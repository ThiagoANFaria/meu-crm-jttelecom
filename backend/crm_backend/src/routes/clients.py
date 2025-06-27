"""
Rotas para o módulo de Clientes
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import uuid

clients_bp = Blueprint('clients', __name__)

# Dados mock para demonstração
mock_clients = [
    {
        "id": "client_001",
        "name": "João Silva",
        "email": "joao.silva@empresa.com",
        "phone": "(11) 99999-9999",
        "company": "Empresa ABC Ltda",
        "document": "12.345.678/0001-90",
        "status": "ativo",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-20T14:45:00Z",
        "last_contact": "2024-01-20T14:45:00Z",
        "address": {
            "street": "Rua das Flores, 123",
            "city": "São Paulo",
            "state": "SP",
            "zip": "01234-567"
        },
        "notes": "Cliente interessado em planos corporativos",
        "contracts": ["contract_001", "contract_002"],
        "proposals": ["proposal_001"],
        "interactions": [
            {
                "id": "int_001",
                "type": "call",
                "description": "Ligação para apresentar nova proposta",
                "date": "2024-01-20T14:45:00Z",
                "duration": 300,
                "outcome": "interessado"
            }
        ]
    },
    {
        "id": "client_002",
        "name": "Maria Santos",
        "email": "maria@tecnologia.com",
        "phone": "(11) 88888-8888",
        "company": "Tech Solutions",
        "document": "98.765.432/0001-10",
        "status": "ativo",
        "created_at": "2024-01-10T09:15:00Z",
        "updated_at": "2024-01-18T16:20:00Z",
        "last_contact": "2024-01-18T16:20:00Z",
        "address": {
            "street": "Av. Paulista, 1000",
            "city": "São Paulo",
            "state": "SP",
            "zip": "01310-100"
        },
        "notes": "Cliente premium com múltiplos contratos",
        "contracts": ["contract_003"],
        "proposals": ["proposal_002", "proposal_003"],
        "interactions": []
    }
]

@clients_bp.route('/', methods=['GET'])
def list_clients():
    """Lista todos os clientes com paginação e busca"""
    try:
        # Parâmetros de query
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        search = request.args.get('search', '')
        
        # Filtrar clientes se houver busca
        filtered_clients = mock_clients
        if search:
            search_lower = search.lower()
            filtered_clients = [
                client for client in mock_clients
                if (search_lower in client['name'].lower() or
                    search_lower in client['email'].lower() or
                    search_lower in client['phone'] or
                    search_lower in client.get('company', '').lower())
            ]
        
        # Paginação
        total = len(filtered_clients)
        start = (page - 1) * limit
        end = start + limit
        clients_page = filtered_clients[start:end]
        
        # Remover dados sensíveis da listagem
        clients_summary = []
        for client in clients_page:
            clients_summary.append({
                "id": client["id"],
                "name": client["name"],
                "email": client["email"],
                "phone": client["phone"],
                "company": client.get("company", ""),
                "status": client["status"],
                "created_at": client["created_at"],
                "last_contact": client.get("last_contact", "")
            })
        
        return jsonify({
            "clients": clients_summary,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
            "limit": limit
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao listar clientes: {str(e)}"}), 500

@clients_bp.route('/', methods=['POST'])
def create_client():
    """Cria um novo cliente"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({"error": "Nome e email são obrigatórios"}), 400
        
        # Verificar se email já existe
        for client in mock_clients:
            if client['email'] == data['email']:
                return jsonify({"error": "Email já cadastrado"}), 400
        
        # Criar novo cliente
        new_client = {
            "id": f"client_{str(uuid.uuid4())[:8]}",
            "name": data['name'],
            "email": data['email'],
            "phone": data.get('phone', ''),
            "company": data.get('company', ''),
            "document": data.get('document', ''),
            "status": "ativo",
            "created_at": datetime.now().isoformat() + 'Z',
            "updated_at": datetime.now().isoformat() + 'Z',
            "last_contact": None,
            "address": data.get('address', {}),
            "notes": data.get('notes', ''),
            "contracts": [],
            "proposals": [],
            "interactions": []
        }
        
        mock_clients.append(new_client)
        
        return jsonify({
            "message": "Cliente criado com sucesso",
            "client": new_client
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Erro ao criar cliente: {str(e)}"}), 500

@clients_bp.route('/<client_id>', methods=['GET'])
def get_client(client_id):
    """Obtém detalhes de um cliente específico"""
    try:
        # Buscar cliente
        client = next((c for c in mock_clients if c['id'] == client_id), None)
        
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        return jsonify(client), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao obter cliente: {str(e)}"}), 500

@clients_bp.route('/<client_id>', methods=['PUT'])
def update_client(client_id):
    """Atualiza dados de um cliente"""
    try:
        data = request.get_json()
        
        # Buscar cliente
        client = next((c for c in mock_clients if c['id'] == client_id), None)
        
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        # Atualizar campos permitidos
        updatable_fields = ['name', 'email', 'phone', 'company', 'status', 'notes', 'address']
        for field in updatable_fields:
            if field in data:
                client[field] = data[field]
        
        client['updated_at'] = datetime.now().isoformat() + 'Z'
        
        return jsonify({
            "message": "Cliente atualizado com sucesso",
            "client": client
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar cliente: {str(e)}"}), 500

@clients_bp.route('/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Remove um cliente (soft delete)"""
    try:
        # Buscar cliente
        client = next((c for c in mock_clients if c['id'] == client_id), None)
        
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        # Soft delete - marcar como inativo
        client['status'] = 'inativo'
        client['updated_at'] = datetime.now().isoformat() + 'Z'
        
        return jsonify({"message": "Cliente removido com sucesso"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao remover cliente: {str(e)}"}), 500

@clients_bp.route('/<client_id>/interactions', methods=['GET'])
def get_client_interactions(client_id):
    """Obtém histórico de interações do cliente"""
    try:
        # Buscar cliente
        client = next((c for c in mock_clients if c['id'] == client_id), None)
        
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        return jsonify({
            "client_id": client_id,
            "interactions": client.get('interactions', [])
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao obter interações: {str(e)}"}), 500

@clients_bp.route('/<client_id>/interactions', methods=['POST'])
def create_client_interaction(client_id):
    """Registra uma nova interação com o cliente"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data or not data.get('type') or not data.get('description'):
            return jsonify({"error": "Tipo e descrição são obrigatórios"}), 400
        
        # Buscar cliente
        client = next((c for c in mock_clients if c['id'] == client_id), None)
        
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        # Criar nova interação
        new_interaction = {
            "id": f"int_{str(uuid.uuid4())[:8]}",
            "type": data['type'],
            "description": data['description'],
            "date": datetime.now().isoformat() + 'Z',
            "duration": data.get('duration'),
            "outcome": data.get('outcome', ''),
            "user_id": data.get('user_id', 'system')
        }
        
        # Adicionar à lista de interações
        if 'interactions' not in client:
            client['interactions'] = []
        
        client['interactions'].append(new_interaction)
        client['last_contact'] = new_interaction['date']
        client['updated_at'] = datetime.now().isoformat() + 'Z'
        
        return jsonify({
            "message": "Interação registrada com sucesso",
            "interaction": new_interaction
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Erro ao registrar interação: {str(e)}"}), 500

@clients_bp.route('/stats', methods=['GET'])
def get_clients_stats():
    """Obtém estatísticas dos clientes"""
    try:
        total_clients = len(mock_clients)
        active_clients = len([c for c in mock_clients if c['status'] == 'ativo'])
        inactive_clients = total_clients - active_clients
        
        # Clientes por mês (últimos 6 meses)
        clients_by_month = [
            {"month": "Jan", "count": 15},
            {"month": "Fev", "count": 23},
            {"month": "Mar", "count": 18},
            {"month": "Abr", "count": 31},
            {"month": "Mai", "count": 27},
            {"month": "Jun", "count": 19}
        ]
        
        return jsonify({
            "total_clients": total_clients,
            "active_clients": active_clients,
            "inactive_clients": inactive_clients,
            "clients_by_month": clients_by_month,
            "conversion_rate": 0.65,
            "avg_interactions_per_client": 3.2
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao obter estatísticas: {str(e)}"}), 500

