from datetime import datetime
from app.extensions import db

TIPOS_MANEJO = [
    'Plantio de Mudas',
    'Retirada de Mudas',
    'Adubação',
    'Irrigação',
    'Desbrotar/Desbaste',
    'Desfolha',
    'Amarração/Escoramento',
    'Ensacamento',
    'Passar Herbicida',
    'Passar Inseticida',
    'Passar Fungicida',
    'Passar Nematicida',
    'Passar Adubo Líquido',
    'Tratamento Fitossanitário',
    'Outros',
]


class Manejo(db.Model):
    __tablename__ = 'manejos'

    id = db.Column(db.Integer, primary_key=True)
    talhao_id = db.Column(db.Integer, db.ForeignKey('talhoes.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    data_manejo = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text)
    responsavel = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Manejo {self.tipo} - {self.data_manejo}>'
