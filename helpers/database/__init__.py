from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializando db e migrate
db = SQLAlchemy()
migrate = Migrate()