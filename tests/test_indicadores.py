"""
Testes unitários para app/services/indicadores.py.
Usa objetos SimpleNamespace para simular modelos sem banco de dados.
"""
from datetime import date, timedelta
from types import SimpleNamespace

from app.services.indicadores import (
    calcular_indicadores_talhao,
    calcular_indicadores_propriedade,
    historico_producao_por_mes,
    historico_custos_por_mes,
    pragas_mais_recorrentes,
    ranking_talhoes,
)


def _colheita(caixas=100, kg=2000.0, receita=1500.0, data=None):
    return SimpleNamespace(
        quantidade_caixas=caixas,
        peso_total=kg,
        receita_total=receita,
        data_colheita=data or date.today(),
    )


def _custo(valor=500.0, categoria='Insumos', data=None):
    return SimpleNamespace(
        valor=valor,
        categoria=categoria,
        data_custo=data or date.today(),
    )


def _ocorrencia(nome='Sigatoka-negra', severidade='Leve', data=None):
    return SimpleNamespace(
        nome=nome,
        severidade=severidade,
        data_ocorrencia=data or date.today(),
    )


def _manejo(data=None):
    return SimpleNamespace(
        data_manejo=data or date.today(),
        tipo='Adubação',
    )


def _talhao(area=10.0, colheitas=None, custos=None, ocorrencias=None, manejos=None, nome='T1'):
    return SimpleNamespace(
        nome=nome,
        area_ha=area,
        colheitas=colheitas or [],
        custos=custos or [],
        ocorrencias=ocorrencias or [],
        manejos=manejos or [],
    )


def _propriedade(talhoes=None):
    return SimpleNamespace(talhoes=talhoes or [])


# ---------- calcular_indicadores_talhao ----------

class TestIndicadoresTalhaoVazio:
    def test_sem_dados_retorna_zeros(self):
        t = _talhao()
        ind = calcular_indicadores_talhao(t)
        assert ind['total_caixas'] == 0
        assert ind['total_kg'] == 0
        assert ind['receita_total'] == 0
        assert ind['custo_total'] == 0
        assert ind['lucro_estimado'] == 0

    def test_sem_dados_produtividade_zero(self):
        ind = calcular_indicadores_talhao(_talhao())
        assert ind['produtividade_caixas_ha'] == 0
        assert ind['produtividade_kg_ha'] == 0

    def test_sem_dados_manejo_none(self):
        ind = calcular_indicadores_talhao(_talhao())
        assert ind['ultimo_manejo'] is None
        assert ind['dias_sem_manejo'] is None

    def test_sem_dados_ocorrencias_zero(self):
        ind = calcular_indicadores_talhao(_talhao())
        assert ind['total_ocorrencias'] == 0
        assert ind['ocorrencias_graves'] == 0


class TestIndicadoresTalhaoComDados:
    def test_colheita_calcula_receita(self):
        t = _talhao(colheitas=[_colheita(caixas=200, receita=3000.0)])
        ind = calcular_indicadores_talhao(t)
        assert ind['total_caixas'] == 200
        assert ind['receita_total'] == 3000.0

    def test_produtividade_por_ha(self):
        t = _talhao(area=10.0, colheitas=[_colheita(caixas=200)])
        ind = calcular_indicadores_talhao(t)
        assert ind['produtividade_caixas_ha'] == 20.0

    def test_custo_total(self):
        t = _talhao(custos=[_custo(500.0), _custo(300.0)])
        ind = calcular_indicadores_talhao(t)
        assert ind['custo_total'] == 800.0

    def test_custo_por_caixa(self):
        t = _talhao(
            colheitas=[_colheita(caixas=100)],
            custos=[_custo(1000.0)],
        )
        ind = calcular_indicadores_talhao(t)
        assert ind['custo_por_caixa'] == 10.0

    def test_custo_por_ha(self):
        t = _talhao(area=10.0, custos=[_custo(1000.0)])
        ind = calcular_indicadores_talhao(t)
        assert ind['custo_por_ha'] == 100.0

    def test_lucro_positivo(self):
        t = _talhao(
            colheitas=[_colheita(receita=3000.0)],
            custos=[_custo(1000.0)],
        )
        ind = calcular_indicadores_talhao(t)
        assert ind['lucro_estimado'] == 2000.0

    def test_lucro_negativo(self):
        t = _talhao(
            colheitas=[_colheita(receita=500.0)],
            custos=[_custo(1000.0)],
        )
        ind = calcular_indicadores_talhao(t)
        assert ind['lucro_estimado'] == -500.0

    def test_ocorrencias_graves_contadas(self):
        t = _talhao(ocorrencias=[
            _ocorrencia(severidade='Grave'),
            _ocorrencia(severidade='Leve'),
            _ocorrencia(severidade='Grave'),
        ])
        ind = calcular_indicadores_talhao(t)
        assert ind['total_ocorrencias'] == 3
        assert ind['ocorrencias_graves'] == 2

    def test_manejo_recente_calcula_dias(self):
        ontem = date.today() - timedelta(days=1)
        t = _talhao(manejos=[_manejo(data=ontem)])
        ind = calcular_indicadores_talhao(t)
        assert ind['dias_sem_manejo'] == 1

    def test_custo_por_categoria(self):
        t = _talhao(custos=[
            _custo(200.0, 'Insumos'),
            _custo(300.0, 'Insumos'),
            _custo(100.0, 'Mão de Obra'),
        ])
        ind = calcular_indicadores_talhao(t)
        assert ind['custo_por_categoria']['Insumos'] == 500.0
        assert ind['custo_por_categoria']['Mão de Obra'] == 100.0

    def test_area_zero_evita_divisao(self):
        t = _talhao(area=0, colheitas=[_colheita(caixas=100)])
        ind = calcular_indicadores_talhao(t)
        assert ind['produtividade_caixas_ha'] == 100.0

    def test_total_manejos(self):
        t = _talhao(manejos=[_manejo(), _manejo(), _manejo()])
        ind = calcular_indicadores_talhao(t)
        assert ind['total_manejos'] == 3


# ---------- historico_producao_por_mes ----------

class TestHistoricoProducao:
    def test_agrupa_por_mes(self):
        jan = date(2025, 1, 10)
        jan2 = date(2025, 1, 20)
        fev = date(2025, 2, 5)
        t = _talhao(colheitas=[
            _colheita(caixas=100, data=jan),
            _colheita(caixas=50, data=jan2),
            _colheita(caixas=200, data=fev),
        ])
        h = historico_producao_por_mes(t)
        assert h['2025-01'] == 150
        assert h['2025-02'] == 200

    def test_retorna_ordenado(self):
        t = _talhao(colheitas=[
            _colheita(data=date(2025, 3, 1)),
            _colheita(data=date(2025, 1, 1)),
        ])
        h = historico_producao_por_mes(t)
        meses = list(h.keys())
        assert meses == sorted(meses)

    def test_sem_colheitas(self):
        assert historico_producao_por_mes(_talhao()) == {}


# ---------- historico_custos_por_mes ----------

class TestHistoricoCustos:
    def test_agrupa_por_mes(self):
        t = _talhao(custos=[
            _custo(300.0, data=date(2025, 1, 5)),
            _custo(200.0, data=date(2025, 1, 15)),
            _custo(500.0, data=date(2025, 2, 1)),
        ])
        h = historico_custos_por_mes(t)
        assert h['2025-01'] == 500.0
        assert h['2025-02'] == 500.0

    def test_sem_custos(self):
        assert historico_custos_por_mes(_talhao()) == {}


# ---------- pragas_mais_recorrentes ----------

class TestPragasMaisRecorrentes:
    def test_ranking_correto(self):
        talhoes = [
            _talhao(ocorrencias=[
                _ocorrencia('Sigatoka-negra'),
                _ocorrencia('Sigatoka-negra'),
                _ocorrencia('Moko'),
            ]),
        ]
        p = _propriedade(talhoes=talhoes)
        resultado = pragas_mais_recorrentes(p)
        assert resultado[0][0] == 'Sigatoka-negra'
        assert resultado[0][1] == 2

    def test_limite_aplicado(self):
        ocs = [_ocorrencia(f'Praga{i}') for i in range(10)]
        p = _propriedade(talhoes=[_talhao(ocorrencias=ocs)])
        assert len(pragas_mais_recorrentes(p, limite=3)) == 3

    def test_sem_ocorrencias(self):
        assert pragas_mais_recorrentes(_propriedade()) == []


# ---------- ranking_talhoes ----------

class TestRankingTalhoes:
    def test_ordena_por_produtividade(self):
        t1 = _talhao(area=10.0, colheitas=[_colheita(caixas=100)], nome='T1')
        t2 = _talhao(area=10.0, colheitas=[_colheita(caixas=200)], nome='T2')
        p = _propriedade(talhoes=[t1, t2])
        ranking = ranking_talhoes(p)
        assert ranking[0]['talhao'].nome == 'T2'

    def test_retorna_todos(self):
        p = _propriedade(talhoes=[_talhao(nome='A'), _talhao(nome='B'), _talhao(nome='C')])
        assert len(ranking_talhoes(p)) == 3


# ---------- calcular_indicadores_propriedade ----------

class TestIndicadoresPropriedade:
    def test_agrega_talhoes(self):
        t1 = _talhao(colheitas=[_colheita(caixas=100, receita=1500.0)], custos=[_custo(500.0)])
        t2 = _talhao(colheitas=[_colheita(caixas=200, receita=3000.0)], custos=[_custo(1000.0)])
        p = _propriedade(talhoes=[t1, t2])
        ind = calcular_indicadores_propriedade(p)
        assert ind['total_caixas'] == 300
        assert ind['total_receita'] == 4500.0
        assert ind['total_custo'] == 1500.0
        assert ind['lucro_total'] == 3000.0

    def test_sem_talhoes(self):
        ind = calcular_indicadores_propriedade(_propriedade())
        assert ind['total_caixas'] == 0
        assert ind['total_talhoes'] == 0
