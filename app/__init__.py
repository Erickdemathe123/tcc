from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager, mail


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Registra modelos para o Migrate descobrir
    with app.app_context():
        from app.models import propriedade, talhao, talhao_variedade, manejo, ocorrencia, colheita, custo  # noqa
        from app.models import usuario  # noqa

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    # Filtro de moeda brasileira
    @app.template_filter('moeda')
    def moeda_filter(value):
        if value is None:
            return 'R$ 0,00'
        return 'R$ ' + f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    @app.template_filter('numero')
    def numero_filter(value, casas=2):
        if value is None:
            return '0'
        return f'{value:,.{casas}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    @app.template_filter('numero_input')
    def numero_input_filter(value):
        """Formata float para value= de input type=number (sem zeros desnecessários)."""
        if value is None:
            return ''
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        return str(value)

    from app.routes.auth import bp as auth_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.propriedades import bp as propriedades_bp
    from app.routes.talhoes import bp as talhoes_bp
    from app.routes.manejos import bp as manejos_bp
    from app.routes.ocorrencias import bp as ocorrencias_bp
    from app.routes.colheitas import bp as colheitas_bp
    from app.routes.custos import bp as custos_bp
    from app.routes.relatorios import bp as relatorios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(propriedades_bp)
    app.register_blueprint(talhoes_bp)
    app.register_blueprint(manejos_bp)
    app.register_blueprint(ocorrencias_bp)
    app.register_blueprint(colheitas_bp)
    app.register_blueprint(custos_bp)
    app.register_blueprint(relatorios_bp)

    from datetime import datetime

    @app.context_processor
    def injetar_variaveis():
        return {'now': datetime.now()}

    @app.errorhandler(404)
    def pagina_nao_encontrada(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    return app
