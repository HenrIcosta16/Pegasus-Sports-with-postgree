from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Importando db e migrate de helpers.database
from helpers.database import db, migrate

# Importando a Blueprint para os agendamentos
from resourcers.agendamentoR import agendamentos_blueprint

# Inicializando o app e extensões
app = Flask(__name__)
app.config.from_object(Config)

# Inicializando CORS, DB e Migrate
CORS(app)
db.init_app(app)
migrate.init_app(app, db)

# Registrar o Blueprint COM PREFIXO
app.register_blueprint(agendamentos_blueprint, url_prefix='/agendamentos')

# Criar as tabelas no banco de dados (caso não existam)
with app.app_context():
    try:
        db.create_all()
        print("✅ Banco de dados inicializado com sucesso!")
        
        # Verificar se a tabela agendamentos foi criada
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Tabelas no banco: {tables}")
        
        if 'agendamentos' in tables:
            print("✅ Tabela 'agendamentos' encontrada!")
        else:
            print("⚠️ Tabela 'agendamentos' NÃO encontrada!")
            
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")

# Rota de teste para verificar se a API está funcionando
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "API Pegasus está funcionando!",
        "endpoints": {
            "GET /agendamentos": "Listar todos os agendamentos",
            "GET /agendamentos/<id>": "Buscar agendamento por ID",
            "POST /agendamentos": "Criar novo agendamento",
            "PUT /agendamentos/<id>": "Atualizar agendamento",
            "DELETE /agendamentos/<id>": "Remover agendamento",
            "GET /agendamentos/horarios-disponiveis/<data>": "Ver horários disponíveis"
        }
    })

# Rota para verificar status do banco
@app.route('/health', methods=['GET'])
def health_check():
    try:
        from models.agendamento import Agendamento
        Agendamento.query.first()
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "message": "API está funcionando corretamente"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

# Configuração CORS
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Tratamento de erros 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "message": "Endpoint não encontrado",
        "available_endpoints": [
            "/",
            "/health",
            "/agendamentos",
            "/agendamentos/<id>",
            "/agendamentos/horarios-disponiveis/<data>"
        ]
    }), 404

# Tratamento de erros genérico
@app.errorhandler(Exception)
def handle_error(error):
    print(f"❌ Erro não tratado: {error}")
    return jsonify({
        "message": "Erro interno do servidor",
        "error": str(error)
    }), 500

if __name__ == "__main__":
    print("🚀 Iniciando servidor Pegasus...")
    print(f"🔧 Configuração: {Config.SQLALCHEMY_DATABASE_URI}")
    print("📡 Servidor rodando em http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)