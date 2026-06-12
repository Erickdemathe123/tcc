from app.extensions import db


class TalhaoVariedade(db.Model):
    __tablename__ = 'talhao_variedades'

    id = db.Column(db.Integer, primary_key=True)
    talhao_id = db.Column(db.Integer, db.ForeignKey('talhoes.id'), nullable=False)
    variedade = db.Column(db.String(50), nullable=False)
