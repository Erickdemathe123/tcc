"""
Testes unitários para app/services/alertas.py — todas as 8 regras.
"""
from datetime import date, timedelta
from types import SimpleNamespace

from app.services.alertas import gerar_alertas_talhao, gerar_todos_alertas


def _manejo(dias_atras=0):
    return SimpleNamespace(data_manejo=date.today() - timedelta(days=dias_atras))


def _ocorrencia(nome='Sigatoka-negra', severidade='Leve', dias_atras=0):
    return SimpleNamespace(
        nome=nome,
        severidade=severidade,
        data_ocorrencia=date.today() - timedelta(days=dias_atras),
    )


def _colheita(caixas=100, receita=1500.0, dias_atras=0):
    return SimpleNamespace(
        quantidade_caixas=caixas,
        receita_total=receita,
        data_colheita=date.today() - timedelta(days=dias_atras),
    )


def _custo(valor=100.0):
    return SimpleNamespace(valor=valor)


def _talhao(nome='T', manejos=None, ocorrencias=None, colheitas=None, custos=None):
    return SimpleNamespace(
        nome=nome,
        manejos=manejos or [],
        ocorrencias=ocorrencias or [],
        colheitas=colheitas or [],
        custos=custos or [],
    )


def _titulos(alertas):
    return [a['titulo'] for a in alertas]


# ---------- Regra 1 e 2: Manejo atrasado ----------

class TestAlertaManejo:
    def test_sem_nenhum_manejo_gera_alerta_warning(self):
        alertas = gerar_alertas_talhao(_talhao())
        assert any('manejo' in t.lower() for t in _titulos(alertas))

    def test_manejo_recente_sem_alerta(self):
        alertas = gerar_alertas_talhao(_talhao(manejos=[_manejo(dias_atras=5)]))
        titulos = _titulos(alertas)
        assert not any('manejo' in t.lower() and 'atrasado' in t.lower() for t in titulos)

    def test_manejo_31_dias_warning(self):
        alertas = gerar_alertas_talhao(_talhao(manejos=[_manejo(dias_atras=31)]))
        tipos = [a['tipo'] for a in alertas]
        titulos = _titulos(alertas)
        assert any('manejo' in t.lower() for t in titulos)
        assert 'warning' in tipos

    def test_manejo_61_dias_danger(self):
        alertas = gerar_alertas_talhao(_talhao(manejos=[_manejo(dias_atras=61)]))
        tipos = [a['tipo'] for a in alertas if 'manejo' in a['titulo'].lower()]
        assert 'danger' in tipos


# ---------- Regra 3: Alta incidência de pragas ----------

class TestAlertaIncidenciaPragas:
    def test_tres_ocorrencias_em_30_dias_gera_danger(self):
        ocs = [_ocorrencia(dias_atras=i) for i in range(3)]
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=ocs))
        assert any(a['tipo'] == 'danger' and 'incidência' in a['titulo'].lower() for a in alertas)

    def test_duas_ocorrencias_sem_alerta_incidencia(self):
        ocs = [_ocorrencia('PragaA', dias_atras=0), _ocorrencia('PragaB', dias_atras=1)]
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=ocs))
        assert not any('alta incidência' in a['titulo'].lower() for a in alertas)

    def test_ocorrencias_antigas_nao_contam(self):
        ocs = [_ocorrencia('PragaX', dias_atras=45) for _ in range(5)]
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=ocs))
        assert not any('alta incidência' in a['titulo'].lower() for a in alertas)


# ---------- Regra 4: Ocorrência grave recente ----------

class TestAlertaOcorrenciaGrave:
    def test_grave_recente_gera_danger(self):
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=[_ocorrencia(severidade='Grave', dias_atras=10)]))
        assert any('grave' in a['titulo'].lower() for a in alertas)
        assert any(a['tipo'] == 'danger' for a in alertas if 'grave' in a['titulo'].lower())

    def test_grave_antiga_nao_gera_alerta(self):
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=[_ocorrencia(severidade='Grave', dias_atras=61)]))
        assert not any('grave recente' in a['titulo'].lower() for a in alertas)

    def test_leve_nao_gera_alerta_grave(self):
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=[_ocorrencia(severidade='Leve')]))
        assert not any('grave' in a['titulo'].lower() for a in alertas)


# ---------- Regra 5: Custo elevado ----------

class TestAlertaCustoElevado:
    def test_custo_acima_5000_gera_warning(self):
        alertas = gerar_alertas_talhao(_talhao(custos=[_custo(6000.0)]))
        assert any('custo' in a['titulo'].lower() for a in alertas)

    def test_custo_abaixo_limite_sem_alerta(self):
        alertas = gerar_alertas_talhao(_talhao(custos=[_custo(3000.0)]))
        assert not any('custo total elevado' in a['titulo'].lower() for a in alertas)


# ---------- Regra 6: Reincidência ----------

class TestAlertaReincidencia:
    def test_reincidencia_detectada(self):
        ocs = [_ocorrencia('Moko'), _ocorrencia('Moko')]
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=ocs))
        assert any('reincidência' in a['titulo'].lower() for a in alertas)

    def test_sem_reincidencia_sem_alerta(self):
        ocs = [_ocorrencia('Moko'), _ocorrencia('Sigatoka-negra')]
        alertas = gerar_alertas_talhao(_talhao(ocorrencias=ocs))
        assert not any('reincidência' in a['titulo'].lower() for a in alertas)


# ---------- Regra 7: Previsão de colheita ----------

class TestAlertaPrevisaoColheita:
    def test_colheita_prevista_apos_270_dias(self):
        alertas = gerar_alertas_talhao(_talhao(colheitas=[_colheita(dias_atras=271)]))
        assert any('colheita' in a['titulo'].lower() and 'prevista' in a['titulo'].lower() for a in alertas)

    def test_colheita_recente_sem_alerta(self):
        alertas = gerar_alertas_talhao(_talhao(colheitas=[_colheita(dias_atras=100)]))
        assert not any('colheita prevista' in a['titulo'].lower() for a in alertas)


# ---------- Regra 8: Prejuízo estimado ----------

class TestAlertaPrejuizo:
    def test_receita_menor_que_custo_gera_danger(self):
        alertas = gerar_alertas_talhao(_talhao(
            colheitas=[_colheita(receita=500.0)],
            custos=[_custo(1000.0)],
        ))
        assert any('prejuízo' in a['titulo'].lower() for a in alertas)

    def test_receita_maior_sem_alerta_prejuizo(self):
        alertas = gerar_alertas_talhao(_talhao(
            colheitas=[_colheita(receita=2000.0)],
            custos=[_custo(1000.0)],
        ))
        assert not any('prejuízo' in a['titulo'].lower() for a in alertas)


# ---------- Regra 9: Queda de produtividade ----------

class TestAlertaQuedaProdutividade:
    def test_queda_acima_20_pct_gera_warning(self):
        colheitas = [
            _colheita(caixas=100, dias_atras=60),
            _colheita(caixas=100, dias_atras=30),
            _colheita(caixas=50, dias_atras=0),  # 50% da média (100)
        ]
        alertas = gerar_alertas_talhao(_talhao(colheitas=colheitas))
        assert any('produtividade' in a['titulo'].lower() for a in alertas)

    def test_producao_estavel_sem_alerta_queda(self):
        colheitas = [
            _colheita(caixas=100, dias_atras=60),
            _colheita(caixas=100, dias_atras=30),
            _colheita(caixas=95, dias_atras=0),  # só 5% abaixo
        ]
        alertas = gerar_alertas_talhao(_talhao(colheitas=colheitas))
        assert not any('queda de produtividade' in a['titulo'].lower() for a in alertas)

    def test_uma_colheita_sem_alerta_queda(self):
        alertas = gerar_alertas_talhao(_talhao(colheitas=[_colheita(caixas=100)]))
        assert not any('queda de produtividade' in a['titulo'].lower() for a in alertas)


# ---------- gerar_todos_alertas ----------

class TestTodosAlertas:
    def test_consolida_multiplos_talhoes(self):
        t1 = _talhao(nome='A', custos=[_custo(6000.0)])
        t2 = _talhao(nome='B', colheitas=[_colheita(receita=100.0)], custos=[_custo(1000.0)])
        prop = SimpleNamespace(talhoes=[t1, t2])
        alertas = gerar_todos_alertas(prop)
        talhoes_nos_alertas = {a['talhao'].nome for a in alertas}
        assert 'A' in talhoes_nos_alertas
        assert 'B' in talhoes_nos_alertas

    def test_sem_talhoes_retorna_lista_vazia(self):
        assert gerar_todos_alertas(SimpleNamespace(talhoes=[])) == []
