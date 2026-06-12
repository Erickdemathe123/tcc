from datetime import datetime
from app.extensions import db

CATEGORIAS_CUSTO = ['Mão de Obra', 'Insumos', 'Maquinário', 'Transporte', 'Outros']


class Custo(db.Model):
    __tablename__ = 'custos'

    id = db.Column(db.Integer, primary_key=True)
    talhao_id = db.Column(db.Integer, db.ForeignKey('talhoes.id'), nullable=False)
    data_custo = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200))
    valor = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Custo {self.categoria} - R${self.valor:.2f}>'
