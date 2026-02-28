# import os

# class Config:
#     # Aqui você usa o banco PostgreSQL, substitua os valores conforme necessário
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://pegasus:pegasus123@localhost:5432/pegasusbase")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "your_secret_key"
import os

class Config:
    # Configuração do banco de dados PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost:5432/pegasus_db'
    
    # Desabilita notificações de modificações (recomendado)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chave secreta para segurança (use uma chave forte em produção)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-temporaria'