from datetime import datetime
from app.extensions import db

DESTINOS = ['Mercado Local', 'CEASA', 'Supermercado', 'Cooperativa', 'Exportação', 'Outros']


class ColheitaItem(db.Model):
    __tablename__ = 'colheita_itens'

    id = db.Column(db.Integer, primary_key=True)
    colheita_id = db.Column(db.Integer, db.ForeignKey('colheitas.id'), nullable=False)
    variedade = db.Column(db.String(50), nullable=False)
    quantidade_caixas = db.Column(db.Integer, default=0)
    peso_por_caixa = db.Column(db.Float)
    preco_por_caixa = db.Column(db.Float)

    @property
    def peso_total(self):
        if self.quantidade_caixas and self.peso_por_caixa:
            return round(self.quantidade_caixas * self.peso_por_caixa, 2)
        return 0.0

    @property
    def receita(self):
        if self.quantidade_caixas and self.preco_por_caixa:
            return round(self.quantidade_caixas * self.preco_por_caixa, 2)
        return 0.0


class Colheita(db.Model):
    __tablename__ = 'colheitas'

    id = db.Column(db.Integer, primary_key=True)
    talhao_id = db.Column(db.Integer, db.ForeignKey('talhoes.id'), nullable=False)
    data_colheita = db.Column(db.Date, nullable=False)
    destino = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship('ColheitaItem', backref='colheita', lazy=True, cascade='all, delete-orphan')

    @property
    def quantidade_caixas(self):
        return sum(i.quantidade_caixas or 0 for i in self.itens)

    @property
    def peso_total(self):
        return round(sum(i.peso_total for i in self.itens), 2)

    @property
    def receita_total(self):
        return round(sum(i.receita for i in self.itens), 2)

    def __repr__(self):
        return f'<Colheita {self.data_colheita} - {self.quantidade_caixas} cx>'
