"""
Testes para os modelos SQLAlchemy (requerem banco de dados via fixture db).
"""
from datetime import date
import pytest

from app.models.usuario import Usuario
from app.models.propriedade import Propriedade
from app.models.talhao import Talhao
from app.models.colheita import Colheita, ColheitaItem
from app.models.custo import Custo
from app.models.manejo import Manejo
from app.models.ocorrencia import Ocorrencia, PRAGAS_DOENCAS_COMUNS, RECOMENDACOES


# ---------- Modelo Usuario ----------

class TestUsuario:
    def test_cria_usuario(self, db):
        u = Usuario(nome='Maria', email='maria@teste.com')
        u.set_senha('Abc123!')
        db.session.add(u)
        db.session.commit()
        assert u.id is not None

    def test_senha_e_hash(self, db):
        u = Usuario(nome='Pedro', email='pedro@teste.com')
        u.set_senha('minha-senha')
        db.session.add(u)
        db.session.commit()
        assert u.senha_hash != 'minha-senha'

    def test_check_senha_correta(self, db):
        u = Usuario(nome='Ana', email='ana@teste.com')
        u.set_senha('correta')
        db.session.add(u)
        db.session.commit()
        assert u.check_senha('correta') is True

    def test_check_senha_errada(self, db):
        u = Usuario(nome='Carlos', email='carlos@teste.com')
        u.set_senha('certa')
        db.session.add(u)
        db.session.commit()
        assert u.check_senha('errada') is False

    def test_email_unico(self, db):
        u1 = Usuario(nome='A', email='dup@teste.com')
        u1.set_senha('123456')
        u2 = Usuario(nome='B', email='dup@teste.com')
        u2.set_senha('123456')
        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_gerar_e_verificar_token_reset(self, app, db):
        with app.app_context():
            u = Usuario(nome='Token', email='token@teste.com')
            u.set_senha('abc123')
            db.session.add(u)
            db.session.commit()
            token = u.gerar_token_reset()
            assert token is not None
            usuario_encontrado = Usuario.verificar_token_reset(token)
            assert usuario_encontrado is not None
            assert usuario_encontrado.email == 'token@teste.com'

    def test_token_invalido_retorna_none(self, app):
        with app.app_context():
            assert Usuario.verificar_token_reset('token-invalido') is None

    def test_repr_usuario(self, db):
        u = Usuario(nome='Repr', email='repr@teste.com')
        u.set_senha('123456')
        db.session.add(u)
        db.session.commit()
        assert 'repr@teste.com' in repr(u)


# ---------- Modelo Colheita e ColheitaItem ----------

class TestColheita:
    def test_quantidade_caixas_soma_itens(self, db, talhao):
        c = Colheita(talhao_id=talhao.id, data_colheita=date.today())
        db.session.add(c)
        db.session.flush()
        i1 = ColheitaItem(colheita_id=c.id, variedade='Nanica', quantidade_caixas=100)
        i2 = ColheitaItem(colheita_id=c.id, variedade='Prata', quantidade_caixas=50)
        db.session.add_all([i1, i2])
        db.session.commit()
        c = Colheita.query.get(c.id)
        assert c.quantidade_caixas == 150

    def test_peso_total_calculado(self, db, talhao):
        c = Colheita(talhao_id=talhao.id, data_colheita=date.today())
        db.session.add(c)
        db.session.flush()
        item = ColheitaItem(
            colheita_id=c.id,
            variedade='Nanica',
            quantidade_caixas=100,
            peso_por_caixa=20.0,
        )
        db.session.add(item)
        db.session.commit()
        c = Colheita.query.get(c.id)
        assert c.peso_total == 2000.0

    def test_receita_total_calculada(self, db, talhao):
        c = Colheita(talhao_id=talhao.id, data_colheita=date.today())
        db.session.add(c)
        db.session.flush()
        item = ColheitaItem(
            colheita_id=c.id,
            variedade='Nanica',
            quantidade_caixas=100,
            preco_por_caixa=15.0,
        )
        db.session.add(item)
        db.session.commit()
        c = Colheita.query.get(c.id)
        assert c.receita_total == 1500.0

    def test_colheita_sem_itens(self, db, talhao):
        c = Colheita(talhao_id=talhao.id, data_colheita=date.today())
        db.session.add(c)
        db.session.commit()
        c = Colheita.query.get(c.id)
        assert c.quantidade_caixas == 0
        assert c.peso_total == 0.0
        assert c.receita_total == 0.0

    def test_item_sem_preco_receita_zero(self, db, talhao):
        c = Colheita(talhao_id=talhao.id, data_colheita=date.today())
        db.session.add(c)
        db.session.flush()
        item = ColheitaItem(colheita_id=c.id, variedade='Prata', quantidade_caixas=50)
        db.session.add(item)
        db.session.commit()
        item = ColheitaItem.query.get(item.id)
        assert item.receita == 0.0

    def test_repr_colheita(self, db, talhao):
        c = Colheita(talhao_id=talhao.id, data_colheita=date.today())
        db.session.add(c)
        db.session.commit()
        assert 'Colheita' in repr(c)


# ---------- Modelo Talhao ----------

class TestTalhao:
    def test_variedade_property_vazia(self, talhao):
        assert talhao.variedade is None

    def test_repr_talhao(self, talhao):
        assert talhao.nome in repr(talhao)


# ---------- Modelo Custo ----------

class TestCusto:
    def test_cria_custo(self, db, talhao):
        c = Custo(
            talhao_id=talhao.id,
            data_custo=date.today(),
            categoria='Insumos',
            valor=500.0,
        )
        db.session.add(c)
        db.session.commit()
        assert c.id is not None

    def test_repr_custo(self, db, talhao):
        c = Custo(talhao_id=talhao.id, data_custo=date.today(), categoria='Mão de Obra', valor=200.0)
        db.session.add(c)
        db.session.commit()
        assert 'Mão de Obra' in repr(c)


# ---------- Modelo Manejo ----------

class TestManejo:
    def test_cria_manejo(self, db, talhao):
        m = Manejo(talhao_id=talhao.id, tipo='Adubação', data_manejo=date.today())
        db.session.add(m)
        db.session.commit()
        assert m.id is not None

    def test_repr_manejo(self, db, talhao):
        m = Manejo(talhao_id=talhao.id, tipo='Poda', data_manejo=date.today())
        db.session.add(m)
        db.session.commit()
        assert 'Poda' in repr(m)


# ---------- Modelo Ocorrencia ----------

class TestOcorrencia:
    def test_cria_ocorrencia(self, db, talhao):
        o = Ocorrencia(
            talhao_id=talhao.id,
            tipo='Doença',
            nome='Sigatoka-negra',
            data_ocorrencia=date.today(),
            severidade='Leve',
        )
        db.session.add(o)
        db.session.commit()
        assert o.id is not None

    def test_pragas_comuns_nao_vazio(self):
        assert len(PRAGAS_DOENCAS_COMUNS) > 0

    def test_recomendacoes_sigatoka_negra_tem_tres_niveis(self):
        rec = RECOMENDACOES['Sigatoka-negra']
        assert 'Leve' in rec
        assert 'Moderada' in rec
        assert 'Grave' in rec

    def test_recomendacoes_tem_prevencao(self):
        for nome, rec in RECOMENDACOES.items():
            if nome != 'Outros':
                assert 'prevencao' in rec, f'{nome} sem prevenção'

    def test_repr_ocorrencia(self, db, talhao):
        o = Ocorrencia(
            talhao_id=talhao.id,
            tipo='Praga',
            nome='Trips',
            data_ocorrencia=date.today(),
            severidade='Moderada',
        )
        db.session.add(o)
        db.session.commit()
        assert 'Trips' in repr(o)


# ---------- Modelo Propriedade ----------

class TestPropriedade:
    def test_cria_propriedade(self, db, usuario):
        p = Propriedade(
            usuario_id=usuario.id,
            nome='Fazenda Nova',
            produtor_nome='Fulano',
        )
        db.session.add(p)
        db.session.commit()
        assert p.id is not None

    def test_repr_propriedade(self, db, usuario):
        p = Propriedade(
            usuario_id=usuario.id,
            nome='Fazenda Repr',
            produtor_nome='Beltrano',
        )
        db.session.add(p)
        db.session.commit()
        assert 'Fazenda Repr' in repr(p)
