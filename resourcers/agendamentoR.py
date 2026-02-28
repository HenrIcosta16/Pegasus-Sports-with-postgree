from flask import Blueprint, request, jsonify
from models.agendamento import Agendamento
from helpers.database import db
from datetime import datetime
import traceback

agendamentos_blueprint = Blueprint('agendamentos', __name__)

# ========== ROTAS PRINCIPAIS ==========

@agendamentos_blueprint.route('/', methods=['GET', 'POST'])
def handle_agendamentos():
    """Endpoint: /agendamentos/ """
    if request.method == 'GET':
        return get_agendamentos()
    elif request.method == 'POST':
        return create_agendamento()

@agendamentos_blueprint.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_agendamento(id):
    """Endpoint: /agendamentos/1 """
    if request.method == 'GET':
        return get_agendamento(id)
    elif request.method == 'PUT':
        return update_agendamento(id)
    elif request.method == 'DELETE':
        return delete_agendamento(id)

@agendamentos_blueprint.route('/horarios-disponiveis/<data>', methods=['GET'])
def get_horarios_disponiveis(data):
    """Endpoint: /agendamentos/horarios-disponiveis/2025-04-15 """
    try:
        print(f"📥 GET /horarios-disponiveis/{data}")
        
        # Validar formato da data
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400
        
        todos_horarios = ['08:00', '09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00']
        limite_por_horario = 3
        
        horarios_disponiveis = []
        
        for horario in todos_horarios:
            agendamentos_no_horario = Agendamento.query.filter_by(
                dataPreferencial=data, 
                horarioPreferencial=horario
            ).count()
            
            disponivel = agendamentos_no_horario < limite_por_horario
            
            horarios_disponiveis.append({
                'horario': horario,
                'disponivel': disponivel,
                'vagas_restantes': max(0, limite_por_horario - agendamentos_no_horario)
            })
        
        return jsonify(horarios_disponiveis), 200
        
    except Exception as e:
        print(f"❌ Erro em GET /horarios-disponiveis: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ========== FUNÇÃO AUXILIAR PARA FORMATAR AGENDAMENTO ==========

def formatar_agendamento(agendamento):
    """Formata um objeto Agendamento para dicionário com todos os campos"""
    # Formatar data para exibição (dd/mm/aaaa)
    data_formatada = ""
    try:
        if agendamento.dataPreferencial:
            data_obj = datetime.strptime(agendamento.dataPreferencial, '%Y-%m-%d')
            data_formatada = data_obj.strftime('%d/%m/%Y')
    except:
        data_formatada = agendamento.dataPreferencial
    
    return {
        'id': agendamento.id,
        'nome': agendamento.nome,
        'telefone': agendamento.telefone,
        'email': agendamento.email,
        'veiculo': agendamento.veiculo,
        'servico': agendamento.servico,
        'dataPreferencial': agendamento.dataPreferencial,
        'dataFormatada': data_formatada,
        'horarioPreferencial': agendamento.horarioPreferencial,
        'mensagem': agendamento.mensagem or '',
        'status': agendamento.status
    }

# ========== FUNÇÕES CRUD ==========

def get_agendamentos():
    try:
        print("📥 GET /agendamentos/ - Buscando todos agendamentos")
        agendamentos = Agendamento.query.all()
        print(f"📊 Encontrados {len(agendamentos)} agendamentos")
        
        agendamentos_data = [formatar_agendamento(ag) for ag in agendamentos]
        return jsonify(agendamentos_data), 200
        
    except Exception as e:
        print(f"❌ Erro em GET /agendamentos: {str(e)}")
        traceback.print_exc()
        return jsonify({"message": f"Erro ao obter os agendamentos: {str(e)}"}), 500

def get_agendamento(id):
    try:
        print(f"📥 GET /agendamentos/{id}")
        agendamento = Agendamento.query.get(id)
        
        if not agendamento:
            return jsonify({"message": "Agendamento não encontrado"}), 404
        
        return jsonify(formatar_agendamento(agendamento)), 200
        
    except Exception as e:
        print(f"❌ Erro em GET /agendamentos/{id}: {str(e)}")
        return jsonify({"message": f"Erro ao obter o agendamento: {str(e)}"}), 500

def create_agendamento():
    try:
        print("📥 POST /agendamentos/ - Recebendo dados")
        data = request.get_json()
        print(f"📦 Dados recebidos: {data}")
        
        if not data:
            return jsonify({"message": "Dados não fornecidos"}), 400
        
        # Validar campos obrigatórios
        required_fields = ['nome', 'telefone', 'email', 'veiculo', 'servico', 'dataPreferencial', 'horarioPreferencial']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            print(f"❌ Campos faltando: {missing_fields}")
            return jsonify({
                "message": f"Dados incompletos. Campos faltando: {', '.join(missing_fields)}"
            }), 400
        
        # Verificar disponibilidade
        print(f"🔍 Verificando disponibilidade para {data['dataPreferencial']} às {data['horarioPreferencial']}")
        limite_por_horario = 3
        
        agendamentos_no_horario = Agendamento.query.filter_by(
            dataPreferencial=data['dataPreferencial'],
            horarioPreferencial=data['horarioPreferencial']
        ).count()
        
        if agendamentos_no_horario >= limite_por_horario:
            print(f"❌ Horário lotado: {agendamentos_no_horario}/{limite_por_horario}")
            return jsonify({
                "message": f"Horário {data['horarioPreferencial']} não está mais disponível. Limite de {limite_por_horario} agendamentos atingido."
            }), 400
        
        # Criar novo agendamento
        print("📝 Criando novo agendamento...")
        new_agendamento = Agendamento(
            nome=data['nome'],
            telefone=data['telefone'],
            email=data['email'],
            veiculo=data['veiculo'],
            servico=data['servico'],
            dataPreferencial=data['dataPreferencial'],
            horarioPreferencial=data['horarioPreferencial'],
            mensagem=data.get('mensagem', ''),
            status='pendente'
        )
        
        # Salvar no banco
        db.session.add(new_agendamento)
        db.session.commit()
        print(f"✅ Agendamento salvo com ID: {new_agendamento.id}")
        
        return jsonify({
            "message": "Agendamento criado com sucesso!",
            "agendamento": formatar_agendamento(new_agendamento)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro em POST /agendamentos: {str(e)}")
        traceback.print_exc()
        return jsonify({"message": f"Erro ao salvar o agendamento: {str(e)}"}), 500

def update_agendamento(id):
    try:
        print(f"📥 PUT /agendamentos/{id}")
        data = request.get_json()
        
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({"message": "Agendamento não encontrado"}), 404
        
        # Atualizar campos se fornecidos
        if 'nome' in data:
            agendamento.nome = data['nome']
        if 'telefone' in data:
            agendamento.telefone = data['telefone']
        if 'email' in data:
            agendamento.email = data['email']
        if 'veiculo' in data:
            agendamento.veiculo = data['veiculo']
        if 'servico' in data:
            agendamento.servico = data['servico']
        if 'dataPreferencial' in data:
            agendamento.dataPreferencial = data['dataPreferencial']
        if 'horarioPreferencial' in data:
            agendamento.horarioPreferencial = data['horarioPreferencial']
        if 'status' in data:
            agendamento.status = data['status']
        if 'mensagem' in data:
            agendamento.mensagem = data['mensagem']
        
        db.session.commit()
        print(f"✅ Agendamento {id} atualizado")
        
        return jsonify({
            "message": "Agendamento atualizado com sucesso!",
            "agendamento": formatar_agendamento(agendamento)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro em PUT /agendamentos/{id}: {str(e)}")
        return jsonify({"message": f"Erro ao atualizar: {str(e)}"}), 500

def delete_agendamento(id):
    try:
        print(f"📥 DELETE /agendamentos/{id}")
        
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({"message": "Agendamento não encontrado"}), 404
        
        agendamento_info = formatar_agendamento(agendamento)
        
        db.session.delete(agendamento)
        db.session.commit()
        print(f"✅ Agendamento {id} deletado")
        
        return jsonify({
            "message": "Agendamento deletado com sucesso!",
            "agendamento": agendamento_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro em DELETE /agendamentos/{id}: {str(e)}")
        return jsonify({"message": f"Erro ao deletar: {str(e)}"}), 500