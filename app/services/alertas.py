"""
Engine de alertas baseada em regras agronômicas.
Cada regra avalia uma condição e retorna um alerta se a condição for verdadeira.
"""
from datetime import date, timedelta

LIMITE_DIAS_SEM_MANEJO = 30
LIMITE_DIAS_SEM_MANEJO_CRITICO = 60
LIMITE_CUSTO_TOTAL = 5000.0
LIMITE_OCORRENCIAS_RECENTES = 3
DIAS_PREVISAO_COLHEITA = 270  # ~9 meses desde a última colheita


def gerar_alertas_talhao(talhao):
    """Aplica todas as regras de alerta para um talhão. Retorna lista de dicts."""
    alertas = []
    hoje = date.today()

    # Regra 1 — Sem manejo recente
    if talhao.manejos:
        ultimo = max(talhao.manejos, key=lambda m: m.data_manejo)
        dias = (hoje - ultimo.data_manejo).days
        if dias > LIMITE_DIAS_SEM_MANEJO_CRITICO:
            alertas.append(_alerta(
                'danger', 'bi-tools',
                'Sem manejo há muito tempo',
                f'Talhão "{talhao.nome}" está há {dias} dias sem registro de manejo.',
                talhao,
            ))
        elif dias > LIMITE_DIAS_SEM_MANEJO:
            alertas.append(_alerta(
                'warning', 'bi-tools',
                'Atenção: manejo atrasado',
                f'Talhão "{talhao.nome}" está há {dias} dias sem manejo.',
                talhao,
            ))
    else:
        alertas.append(_alerta(
            'warning', 'bi-tools',
            'Nenhum manejo registrado',
            f'Talhão "{talhao.nome}" não possui nenhum manejo cadastrado.',
            talhao,
        ))

    # Regra 2 — Alta incidência de pragas nos últimos 30 dias
    periodo = hoje - timedelta(days=30)
    recentes = [o for o in talhao.ocorrencias if o.data_ocorrencia >= periodo]
    if len(recentes) >= LIMITE_OCORRENCIAS_RECENTES:
        alertas.append(_alerta(
            'danger', 'bi-bug-fill',
            'Alta incidência de pragas/doenças',
            f'{len(recentes)} ocorrências registradas nos últimos 30 dias no talhão "{talhao.nome}".',
            talhao,
        ))

    # Regra 3 — Ocorrência grave recente (últimos 60 dias)
    graves = [o for o in talhao.ocorrencias if o.severidade == 'Grave']
    if graves:
        ultima_grave = max(graves, key=lambda o: o.data_ocorrencia)
        dias_grave = (hoje - ultima_grave.data_ocorrencia).days
        if dias_grave <= 60:
            alertas.append(_alerta(
                'danger', 'bi-exclamation-triangle-fill',
                'Ocorrência grave recente',
                f'"{ultima_grave.nome}" (grave) foi registrada há {dias_grave} dias no talhão "{talhao.nome}".',
                talhao,
            ))

    # Regra 4 — Custo total elevado
    custo_total = sum(c.valor for c in talhao.custos)
    if custo_total > LIMITE_CUSTO_TOTAL:
        alertas.append(_alerta(
            'warning', 'bi-cash-stack',
            'Custo total elevado',
            f'Custo acumulado do talhão "{talhao.nome}" é R$ {custo_total:,.2f} (limite: R$ {LIMITE_CUSTO_TOTAL:,.2f}).',
            talhao,
        ))

    # Regra 5 — Reincidência de praga/doença
    nomes = [o.nome for o in talhao.ocorrencias]
    reincidentes = {n for n in nomes if nomes.count(n) > 1}
    for nome in reincidentes:
        alertas.append(_alerta(
            'info', 'bi-arrow-repeat',
            'Reincidência detectada',
            f'"{nome}" ocorreu mais de uma vez no talhão "{talhao.nome}". Revisar o tratamento aplicado.',
            talhao,
        ))

    # Regra 6 — Previsão de colheita próxima
    if talhao.colheitas:
        ultima_colheita = max(talhao.colheitas, key=lambda c: c.data_colheita)
        dias_desde_colheita = (hoje - ultima_colheita.data_colheita).days
        if dias_desde_colheita >= DIAS_PREVISAO_COLHEITA:
            alertas.append(_alerta(
                'info', 'bi-calendar-check',
                'Colheita prevista',
                f'Talhão "{talhao.nome}" está há {dias_desde_colheita} dias desde a última colheita. Verifique o ponto de corte.',
                talhao,
            ))

    # Regra 7 — Prejuízo estimado
    receita = sum(c.receita_total for c in talhao.colheitas)
    if custo_total > 0 and receita < custo_total:
        alertas.append(_alerta(
            'danger', 'bi-graph-down-arrow',
            'Talhão com prejuízo estimado',
            f'Receita (R$ {receita:,.2f}) menor que custo (R$ {custo_total:,.2f}) no talhão "{talhao.nome}".',
            talhao,
        ))

    # Regra 8 — Queda de produtividade em relação à média anterior
    colheitas_ordenadas = sorted(talhao.colheitas, key=lambda c: c.data_colheita)
    if len(colheitas_ordenadas) >= 2:
        ultima = colheitas_ordenadas[-1]
        anteriores = colheitas_ordenadas[:-1]
        media_anterior = sum(c.quantidade_caixas or 0 for c in anteriores) / len(anteriores)
        ultima_qtd = ultima.quantidade_caixas or 0
        if media_anterior > 0 and ultima_qtd < media_anterior * 0.8:
            queda_pct = round((1 - ultima_qtd / media_anterior) * 100, 1)
            alertas.append(_alerta(
                'warning', 'bi-graph-down-arrow',
                'Queda de produtividade',
                f'Última colheita ({ultima_qtd} cx) está {queda_pct}% abaixo da média anterior ({media_anterior:.0f} cx) no talhão "{talhao.nome}".',
                talhao,
            ))

    return alertas


def gerar_todos_alertas(propriedade):
    """Consolida alertas de todos os talhões da propriedade."""
    todos = []
    for talhao in propriedade.talhoes:
        todos.extend(gerar_alertas_talhao(talhao))
    return todos


def _alerta(tipo, icone, titulo, mensagem, talhao):
    return {
        'tipo': tipo,
        'icone': icone,
        'titulo': titulo,
        'mensagem': mensagem,
        'talhao': talhao,
    }
