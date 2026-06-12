from datetime import datetime
from app.extensions import db

VARIEDADES = [
    'Prata',
    'Prata-Anã',
    'Pacovan',
    'Nanica',
    'Nanicão',
    'Grand Naine',
    'Cavendish',
    'Banana Maçã',
    'Banana Figo',
    'Banana D\'Angola',
    'Banana Terra',
    'BRS Platina',
    'FHIA-18',
    'Tropical',
    'Garantida',
    'Outras',
]


class Talhao(db.Model):
    __tablename__ = 'talhoes'

    id = db.Column(db.Integer, primary_key=True)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedades.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    area_ha = db.Column(db.Float, nullable=False)
    data_plantio = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    variedades_list = db.relationship('TalhaoVariedade', backref='talhao', lazy=True, cascade='all, delete-orphan')
    manejos = db.relationship('Manejo', backref='talhao', lazy=True, cascade='all, delete-orphan')
    ocorrencias = db.relationship('Ocorrencia', backref='talhao', lazy=True, cascade='all, delete-orphan')
    colheitas = db.relationship('Colheita', backref='talhao', lazy=True, cascade='all, delete-orphan')
    custos = db.relationship('Custo', backref='talhao', lazy=True, cascade='all, delete-orphan')

    @property
    def variedade(self):
        """Retorna as variedades separadas por vírgula (compat. com templates antigos)."""
        nomes = [v.variedade for v in self.variedades_list]
        return ', '.join(nomes) if nomes else None

    def __repr__(self):
        return f'<Talhao {self.nome}>'
