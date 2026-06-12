from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    propriedades = db.relationship('Propriedade', backref='usuario', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def gerar_token_reset(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.email, salt='reset-senha')

    @staticmethod
    def verificar_token_reset(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        expires = current_app.config.get('MAIL_RESET_TOKEN_EXPIRES', 3600)
        try:
            email = s.loads(token, salt='reset-senha', max_age=expires)
        except (SignatureExpired, BadSignature):
            return None
        return Usuario.query.filter_by(email=email).first()

    def __repr__(self):
        return f'<Usuario {self.email}>'
