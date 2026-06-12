from datetime import datetime
from app.extensions import db


class Propriedade(db.Model):
    __tablename__ = 'propriedades'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(200))
    area_total_ha = db.Column(db.Float)
    produtor_nome = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    talhoes = db.relationship('Talhao', backref='propriedade', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Propriedade {self.nome}>'
