import pytest
from datetime import date
from app import create_app
from app.extensions import db as _db
from app.models.usuario import Usuario
from app.models.propriedade import Propriedade
from app.models.talhao import Talhao
from app.models.manejo import Manejo
from app.models.ocorrencia import Ocorrencia
from app.models.colheita import Colheita, ColheitaItem
from app.models.custo import Custo
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key-agrobanana'
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope='session')
def app():
    """Cria o app e o schema do banco uma vez por sessão."""
    _app = create_app(TestConfig)
    with _app.app_context():
        _db.create_all()
    return _app


@pytest.fixture(autouse=True)
def app_ctx(app):
    """Cada teste recebe um app context fresco — evita vazamento do flask.g (Flask-Login)."""
    ctx = app.app_context()
    ctx.push()
    yield
    # Limpa todos os dados após cada teste
    try:
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
        _db.session.expunge_all()
    finally:
        ctx.pop()


@pytest.fixture
def db(app):
    yield _db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def usuario(db):
    u = Usuario(nome='João Teste', email='joao@teste.com')
    u.set_senha('Senha123!')
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def cliente_logado(client, usuario):
    client.post('/auth/login', data={
        'email': 'joao@teste.com',
        'senha': 'Senha123!'
    }, follow_redirects=True)
    return client


@pytest.fixture
def propriedade(db, usuario):
    p = Propriedade(
        usuario_id=usuario.id,
        nome='Fazenda Esperança',
        localizacao='Santa Catarina',
        area_total_ha=50.0,
        produtor_nome='João Teste',
    )
    db.session.add(p)
    db.session.commit()
    return p


@pytest.fixture
def talhao(db, propriedade):
    t = Talhao(
        propriedade_id=propriedade.id,
        nome='Talhão A',
        area_ha=10.0,
        data_plantio=date(2024, 1, 1),
    )
    db.session.add(t)
    db.session.commit()
    return t


@pytest.fixture
def talhao_com_dados(db, talhao):
    manejo = Manejo(talhao_id=talhao.id, tipo='Adubação', data_manejo=date.today())
    ocorrencia = Ocorrencia(
        talhao_id=talhao.id,
        tipo='Doença',
        nome='Sigatoka-negra',
        data_ocorrencia=date.today(),
        severidade='Leve',
    )
    colheita = Colheita(talhao_id=talhao.id, data_colheita=date.today())
    db.session.add_all([manejo, ocorrencia, colheita])
    db.session.flush()

    item = ColheitaItem(
        colheita_id=colheita.id,
        variedade='Nanica',
        quantidade_caixas=200,
        peso_por_caixa=20.0,
        preco_por_caixa=15.0,
    )
    custo = Custo(
        talhao_id=talhao.id,
        data_custo=date.today(),
        categoria='Insumos',
        descricao='Fertilizante',
        valor=1500.0,
    )
    db.session.add_all([item, custo])
    db.session.commit()
    return Talhao.query.get(talhao.id)
