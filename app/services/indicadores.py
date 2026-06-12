"""
Calcula indicadores de desempenho agronômico e econômico por talhão e propriedade.
"""
from datetime import date


def calcular_indicadores_talhao(talhao):
    """Retorna dict completo de indicadores para um talhão."""
    area = talhao.area_ha or 1  # evita divisão por zero

    # Produção acumulada
    total_caixas = sum(c.quantidade_caixas or 0 for c in talhao.colheitas)
    total_kg = sum(c.peso_total for c in talhao.colheitas)
    receita_total = sum(c.receita_total for c in talhao.colheitas)

    # Custos
    custo_total = sum(c.valor for c in talhao.custos)
    custo_por_categoria = {}
    for c in talhao.custos:
        custo_por_categoria[c.categoria] = custo_por_categoria.get(c.categoria, 0) + c.valor

    # Produtividade
    produtividade_caixas_ha = round(total_caixas / area, 2) if total_caixas else 0
    produtividade_kg_ha = round(total_kg / area, 2) if total_kg else 0

    # Custo por unidade
    custo_por_ha = round(custo_total / area, 2) if custo_total else 0
    custo_por_caixa = round(custo_total / total_caixas, 2) if total_caixas else 0

    # Resultado econômico
    lucro_estimado = round(receita_total - custo_total, 2)

    # Pragas e doenças
    total_ocorrencias = len(talhao.ocorrencias)
    ocorrencias_graves = sum(1 for o in talhao.ocorrencias if o.severidade == 'Grave')

    # Último manejo
    ultimo_manejo = None
    dias_sem_manejo = None
    if talhao.manejos:
        ultimo_manejo = max(talhao.manejos, key=lambda m: m.data_manejo)
        dias_sem_manejo = (date.today() - ultimo_manejo.data_manejo).days

    # Última colheita
    ultima_colheita = None
    if talhao.colheitas:
        ultima_colheita = max(talhao.colheitas, key=lambda c: c.data_colheita)

    return {
        'total_caixas': total_caixas,
        'total_kg': round(total_kg, 2),
        'receita_total': round(receita_total, 2),
        'custo_total': round(custo_total, 2),
        'custo_por_categoria': custo_por_categoria,
        'produtividade_caixas_ha': produtividade_caixas_ha,
        'produtividade_kg_ha': produtividade_kg_ha,
        'custo_por_ha': custo_por_ha,
        'custo_por_caixa': custo_por_caixa,
        'lucro_estimado': lucro_estimado,
        'total_ocorrencias': total_ocorrencias,
        'ocorrencias_graves': ocorrencias_graves,
        'ultimo_manejo': ultimo_manejo,
        'ultima_colheita': ultima_colheita,
        'dias_sem_manejo': dias_sem_manejo,
        'total_manejos': len(talhao.manejos),
    }


def calcular_indicadores_propriedade(propriedade):
    """Agrega indicadores de todos os talhões de uma propriedade."""
    indicadores_talhoes = []
    for talhao in propriedade.talhoes:
        ind = calcular_indicadores_talhao(talhao)
        ind['talhao'] = talhao
        indicadores_talhoes.append(ind)

    total_receita = sum(i['receita_total'] for i in indicadores_talhoes)
    total_custo = sum(i['custo_total'] for i in indicadores_talhoes)
    total_caixas = sum(i['total_caixas'] for i in indicadores_talhoes)
    total_area = sum(t.area_ha for t in propriedade.talhoes if t.area_ha) or 1

    return {
        'talhoes': indicadores_talhoes,
        'total_receita': round(total_receita, 2),
        'total_custo': round(total_custo, 2),
        'lucro_total': round(total_receita - total_custo, 2),
        'total_caixas': total_caixas,
        'custo_por_caixa': round(total_custo / total_caixas, 2) if total_caixas else 0,
        'produtividade_media_ha': round(total_caixas / total_area, 2) if total_caixas else 0,
        'total_talhoes': len(propriedade.talhoes),
    }


def historico_producao_por_mes(talhao):
    """Série mensal de caixas produzidas para uso em gráficos."""
    historico = {}
    for c in talhao.colheitas:
        mes = c.data_colheita.strftime('%Y-%m')
        historico[mes] = historico.get(mes, 0) + (c.quantidade_caixas or 0)
    return dict(sorted(historico.items()))


def historico_custos_por_mes(talhao):
    """Série mensal de custos para uso em gráficos."""
    historico = {}
    for c in talhao.custos:
        mes = c.data_custo.strftime('%Y-%m')
        historico[mes] = round(historico.get(mes, 0) + c.valor, 2)
    return dict(sorted(historico.items()))


def pragas_mais_recorrentes(propriedade, limite=5):
    """Ranking das pragas/doenças mais registradas na propriedade."""
    contagem = {}
    for talhao in propriedade.talhoes:
        for o in talhao.ocorrencias:
            contagem[o.nome] = contagem.get(o.nome, 0) + 1
    return sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:limite]


def ranking_talhoes(propriedade):
    """Ordena talhões por produtividade (caixas/ha), do maior para o menor."""
    resultado = []
    for talhao in propriedade.talhoes:
        ind = calcular_indicadores_talhao(talhao)
        resultado.append({'talhao': talhao, 'indicadores': ind})
    return sorted(resultado, key=lambda x: x['indicadores']['produtividade_caixas_ha'], reverse=True)
