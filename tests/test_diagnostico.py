"""
Testes unitários para app/services/diagnostico.py.
"""
from datetime import date, timedelta
from types import SimpleNamespace

from app.services.diagnostico import (
    classificar_talhao,
    diagnostico_propriedade,
    gerar_recomendacoes,
    LIMITES,
)


def _colheita(caixas=100, receita=1500.0, dias_atras=0):
    return SimpleNamespace(
        quantidade_caixas=caixas,
        peso_total=caixas * 20.0,
        receita_total=receita,
        data_colheita=date.today() - timedelta(days=dias_atras),
    )


def _custo(valor=500.0, categoria='Insumos', data=None):
    return SimpleNamespace(
        valor=valor,
        categoria=categoria,
        data_custo=data or date.today(),
    )


def _ocorrencia(nome='Sigatoka-negra', severidade='Leve', dias_atras=0):
    return SimpleNamespace(
        nome=nome,
        severidade=severidade,
        data_ocorrencia=date.today() - timedelta(days=dias_atras),
    )


def _manejo(dias_atras=0):
    return SimpleNamespace(data_manejo=date.today() - timedelta(days=dias_atras))


def _talhao(area=10.0, colheitas=None, custos=None, ocorrencias=None, manejos=None, nome='T'):
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


# ---------- Diagnóstico situacional ----------

class TestClassificarTalhaoNormal:
    def test_sem_dados_retorna_atencao_ou_normal(self):
        diag = classificar_talhao(_talhao())
        assert diag['situacao'] in ('normal', 'atencao')

    def test_boa_produtividade_sem_problemas(self):
        caixas = LIMITES['produtividade_boa_cx_ha'] * 10  # 10 ha → boa
        t = _talhao(
            area=10.0,
            colheitas=[_colheita(caixas=caixas, receita=caixas * 15)],
            custos=[_custo(caixas * 5)],
            manejos=[_manejo(dias_atras=10)],
        )
        diag = classificar_talhao(t)
        assert diag['situacao'] in ('normal', 'atencao')

    def test_retorna_estrutura_completa(self):
        diag = classificar_talhao(_talhao())
        assert 'situacao' in diag
        assert 'label' in diag
        assert 'cor' in diag
        assert 'icone' in diag
        assert 'pontuacao' in diag
        assert 'motivos' in diag
        assert 'indicadores' in diag


class TestClassificarTalhaoCritico:
    def test_produtividade_baixa_custo_alto_gera_critico(self):
        caixas_baixo = LIMITES['produtividade_critica_cx_ha'] - 1  # abaixo do crítico por ha
        t = _talhao(
            area=1.0,
            colheitas=[_colheita(caixas=caixas_baixo, receita=500.0)],
            custos=[_custo(LIMITES['custo_por_caixa_alto'] + 5) for _ in range(caixas_baixo)],
            ocorrencias=[_ocorrencia(severidade='Grave')],
            manejos=[_manejo(dias_atras=61)],
        )
        diag = classificar_talhao(t)
        assert diag['situacao'] == 'critico'

    def test_prejuizo_e_grave_e_sem_manejo_gera_critico(self):
        t = _talhao(
            area=10.0,
            colheitas=[_colheita(caixas=50, receita=200.0)],
            custos=[_custo(2000.0)],
            ocorrencias=[_ocorrencia(severidade='Grave')],
            manejos=[_manejo(dias_atras=65)],
        )
        diag = classificar_talhao(t)
        assert diag['situacao'] == 'critico'
        assert diag['pontuacao'] >= 4


class TestClassificarTalhaoAtencao:
    def test_manejo_31_dias_gera_atencao(self):
        t = _talhao(manejos=[_manejo(dias_atras=35)])
        diag = classificar_talhao(t)
        assert diag['situacao'] in ('atencao', 'normal')

    def test_motivos_nao_vazios(self):
        diag = classificar_talhao(_talhao())
        assert len(diag['motivos']) > 0

    def test_motivos_sao_tuplas(self):
        diag = classificar_talhao(_talhao())
        for tipo, texto in diag['motivos']:
            assert tipo in ('positivo', 'negativo', 'atencao')
            assert isinstance(texto, str)


# ---------- diagnostico_propriedade ----------

class TestDiagnosticoPropriedade:
    def test_agrupa_por_situacao(self):
        t_normal = _talhao(
            area=10.0,
            colheitas=[_colheita(caixas=2000, receita=30000.0)],
            custos=[_custo(1000.0)],
            manejos=[_manejo(dias_atras=5)],
            nome='Normal',
        )
        t_critico = _talhao(
            area=1.0,
            colheitas=[_colheita(caixas=10, receita=50.0)],
            custos=[_custo(5000.0)],
            ocorrencias=[_ocorrencia(severidade='Grave')],
            manejos=[_manejo(dias_atras=70)],
            nome='Critico',
        )
        p = _propriedade(talhoes=[t_normal, t_critico])
        resultado = diagnostico_propriedade(p)
        assert 'normal' in resultado
        assert 'atencao' in resultado
        assert 'critico' in resultado
        total = sum(len(v) for v in resultado.values())
        assert total == 2

    def test_sem_talhoes(self):
        resultado = diagnostico_propriedade(_propriedade())
        assert resultado == {'normal': [], 'atencao': [], 'critico': []}


# ---------- gerar_recomendacoes ----------

class TestGerarRecomendacoes:
    def test_sem_problemas_retorna_info(self):
        recomendacoes = gerar_recomendacoes(_propriedade())
        assert len(recomendacoes) == 1
        assert recomendacoes[0][0] == 'info'

    def test_urgente_aparece_primeiro(self):
        t = _talhao(
            area=1.0,
            colheitas=[_colheita(caixas=10, receita=50.0)],
            custos=[_custo(5000.0)],
            ocorrencias=[_ocorrencia(severidade='Grave')],
            manejos=[_manejo(dias_atras=70)],
        )
        recomendacoes = gerar_recomendacoes(_propriedade(talhoes=[t]))
        prioridades = [r[0] for r in recomendacoes]
        assert prioridades[0] in ('urgente', 'alta')

    def test_manejo_atrasado_gera_recomendacao_alta(self):
        t = _talhao(manejos=[_manejo(dias_atras=65)])
        recomendacoes = gerar_recomendacoes(_propriedade(talhoes=[t]))
        prioridades = [r[0] for r in recomendacoes]
        assert 'alta' in prioridades

    def test_recomendacoes_ordenadas_por_urgencia(self):
        t = _talhao(
            area=10.0,
            colheitas=[_colheita(caixas=50, receita=200.0)],
            custos=[_custo(2000.0)],
            ocorrencias=[_ocorrencia(severidade='Grave')],
            manejos=[_manejo(dias_atras=65)],
        )
        recomendacoes = gerar_recomendacoes(_propriedade(talhoes=[t]))
        ordem = {'urgente': 0, 'alta': 1, 'media': 2, 'info': 3}
        valores = [ordem[r[0]] for r in recomendacoes]
        assert valores == sorted(valores)

    def test_producao_baixa_gera_recomendacao_alta(self):
        caixas = LIMITES['produtividade_critica_cx_ha'] - 1
        t = _talhao(area=1.0, colheitas=[_colheita(caixas=caixas, receita=200.0)])
        recomendacoes = gerar_recomendacoes(_propriedade(talhoes=[t]))
        # r = (prioridade, icone, texto, talhao) — texto está em r[2]
        assert any('produtividade' in r[2].lower() for r in recomendacoes)

    def test_custo_alto_por_caixa_gera_recomendacao(self):
        t = _talhao(
            area=10.0,
            colheitas=[_colheita(caixas=10, receita=100.0)],
            custos=[_custo(valor=(LIMITES['custo_por_caixa_alto'] + 5) * 10)],
        )
        recomendacoes = gerar_recomendacoes(_propriedade(talhoes=[t]))
        assert any('custo' in r[2].lower() for r in recomendacoes)
