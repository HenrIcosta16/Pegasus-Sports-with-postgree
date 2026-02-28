from helpers.database import db
from datetime import datetime

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    veiculo = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    dataPreferencial = db.Column(db.String(20), nullable=False)
    horarioPreferencial = db.Column(db.String(10), nullable=True)
    mensagem = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='pendente')

    def to_dict(self):
        """Converte o objeto para dicionário"""
        data_formatada = ""
        try:
            data_obj = datetime.strptime(self.dataPreferencial, '%Y-%m-%d')
            data_formatada = data_obj.strftime('%d/%m/%Y')
        except:
            data_formatada = self.dataPreferencial
            
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'veiculo': self.veiculo,
            'servico': self.servico,
            'dataPreferencial': self.dataPreferencial,
            'dataFormatada': data_formatada,
            'horarioPreferencial': self.horarioPreferencial,
            'mensagem': self.mensagem,
            'timestamp': datetime.now().isoformat(),
            'status': self.status
        }

    def save(self):
        """Salva o agendamento no banco"""
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Agendamento {self.id} - {self.nome}>"