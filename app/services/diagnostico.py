"""
Módulo de diagnóstico por regras.
Classifica cada talhão como normal, atencao ou critico com base
em uma combinação ponderada de indicadores.
"""
from app.services.indicadores import calcular_indicadores_talhao

# Limites de referência agronômica (ajustáveis)
LIMITES = {
    'produtividade_boa_cx_ha': 150,
    'produtividade_critica_cx_ha': 80,
    'custo_por_caixa_bom': 10.0,
    'custo_por_caixa_alto': 20.0,
    'ocorrencias_muitas': 3,
    'dias_sem_manejo_atencao': 30,
    'dias_sem_manejo_critico': 60,
}

SITUACOES = {
    'normal': {'label': 'Normal', 'cor': 'success', 'icone': 'bi-check-circle-fill'},
    'atencao': {'label': 'Atenção', 'cor': 'warning', 'icone': 'bi-exclamation-circle-fill'},
    'critico': {'label': 'Crítico', 'cor': 'danger', 'icone': 'bi-x-circle-fill'},
}


def classificar_talhao(talhao):
    """
    Retorna dict com:
    - situacao: 'normal' | 'atencao' | 'critico'
    - label, cor, icone: para renderização no template
    - motivos: lista de (tipo, texto) para justificar o diagnóstico
    - indicadores: dict completo de indicadores
    """
    ind = calcular_indicadores_talhao(talhao)
    pontos = 0
    motivos = []

    # Avalia produtividade
    if ind['total_caixas'] > 0:
        prod = ind['produtividade_caixas_ha']
        if prod >= LIMITES['produtividade_boa_cx_ha']:
            motivos.append(('positivo', f"Produtividade boa: {prod} cx/ha"))
        elif prod < LIMITES['produtividade_critica_cx_ha']:
            pontos += 2
            motivos.append(('negativo', f"Produtividade baixa: {prod} cx/ha (abaixo de {LIMITES['produtividade_critica_cx_ha']} cx/ha)"))
        else:
            pontos += 1
            motivos.append(('atencao', f"Produtividade intermediária: {prod} cx/ha"))

    # Avalia custo por caixa
    if ind['custo_por_caixa'] > 0:
        cpc = ind['custo_por_caixa']
        if cpc > LIMITES['custo_por_caixa_alto']:
            pontos += 2
            motivos.append(('negativo', f"Custo por caixa muito alto: R$ {cpc:.2f}"))
        elif cpc > LIMITES['custo_por_caixa_bom']:
            pontos += 1
            motivos.append(('atencao', f"Custo por caixa elevado: R$ {cpc:.2f}"))
        else:
            motivos.append(('positivo', f"Custo por caixa adequado: R$ {cpc:.2f}"))

    # Avalia ocorrências de pragas/doenças
    if ind['total_ocorrencias'] >= LIMITES['ocorrencias_muitas']:
        pontos += 1
        motivos.append(('atencao', f"{ind['total_ocorrencias']} ocorrências de pragas/doenças registradas"))
    if ind['ocorrencias_graves'] > 0:
        pontos += 2
        motivos.append(('negativo', f"{ind['ocorrencias_graves']} ocorrência(s) grave(s) registrada(s)"))

    # Avalia frequência de manejo
    if ind['dias_sem_manejo'] is not None:
        dsm = ind['dias_sem_manejo']
        if dsm > LIMITES['dias_sem_manejo_critico']:
            pontos += 2
            motivos.append(('negativo', f"Sem manejo há {dsm} dias (crítico)"))
        elif dsm > LIMITES['dias_sem_manejo_atencao']:
            pontos += 1
            motivos.append(('atencao', f"Sem manejo há {dsm} dias"))
        else:
            motivos.append(('positivo', f"Manejo recente: há {dsm} dias"))
    elif not talhao.manejos:
        pontos += 1
        motivos.append(('atencao', "Nenhum manejo registrado"))

    # Avalia resultado econômico
    if ind['custo_total'] > 0:
        if ind['lucro_estimado'] < 0:
            pontos += 2
            motivos.append(('negativo', f"Prejuízo estimado: R$ {abs(ind['lucro_estimado']):.2f}"))
        elif ind['lucro_estimado'] == 0:
            motivos.append(('atencao', "Resultado econômico nulo"))
        else:
            motivos.append(('positivo', f"Lucro estimado: R$ {ind['lucro_estimado']:.2f}"))

    # Classificação final
    if pontos >= 4:
        situacao = 'critico'
    elif pontos >= 2:
        situacao = 'atencao'
    else:
        situacao = 'normal'

    if not motivos:
        motivos.append(('atencao', 'Dados insuficientes para diagnóstico completo. Registre manejos, colheitas e custos.'))

    return {
        'situacao': situacao,
        'label': SITUACOES[situacao]['label'],
        'cor': SITUACOES[situacao]['cor'],
        'icone': SITUACOES[situacao]['icone'],
        'pontuacao': pontos,
        'motivos': motivos,
        'indicadores': ind,
    }


def diagnostico_propriedade(propriedade):
    """Retorna diagnóstico de todos os talhões agrupados por situação."""
    resultado = {'normal': [], 'atencao': [], 'critico': []}
    for talhao in propriedade.talhoes:
        diag = classificar_talhao(talhao)
        diag['talhao'] = talhao
        resultado[diag['situacao']].append(diag)
    return resultado


def gerar_recomendacoes(propriedade):
    """
    Gera recomendações simples e acionáveis para o produtor com base
    no diagnóstico e indicadores de cada talhão.
    Retorna lista de (prioridade, icone, texto, talhao).
    """
    from datetime import date
    recomendacoes = []

    for talhao in propriedade.talhoes:
        diag = classificar_talhao(talhao)
        ind = diag['indicadores']

        if diag['situacao'] == 'critico':
            recomendacoes.append((
                'urgente', 'bi-exclamation-triangle-fill',
                f'Intervenção urgente no talhão "{talhao.nome}" — situação crítica identificada.',
                talhao,
            ))

        if ind['dias_sem_manejo'] is not None and ind['dias_sem_manejo'] > LIMITES['dias_sem_manejo_critico']:
            recomendacoes.append((
                'alta', 'bi-tools',
                f'Realizar manejo imediato no talhão "{talhao.nome}" (há {ind["dias_sem_manejo"]} dias sem registro).',
                talhao,
            ))
        elif ind['dias_sem_manejo'] is not None and ind['dias_sem_manejo'] > LIMITES['dias_sem_manejo_atencao']:
            recomendacoes.append((
                'media', 'bi-tools',
                f'Planejar manejo no talhão "{talhao.nome}" (há {ind["dias_sem_manejo"]} dias sem manejo).',
                talhao,
            ))
        elif not talhao.manejos:
            recomendacoes.append((
                'alta', 'bi-tools',
                f'Registrar o primeiro manejo no talhão "{talhao.nome}".',
                talhao,
            ))

        if ind['ocorrencias_graves'] > 0:
            recomendacoes.append((
                'alta', 'bi-bug-fill',
                f'Intensificar controle fitossanitário no talhão "{talhao.nome}" — ocorrência grave registrada.',
                talhao,
            ))
        elif ind['total_ocorrencias'] >= LIMITES['ocorrencias_muitas']:
            recomendacoes.append((
                'media', 'bi-bug',
                f'Monitorar pragas/doenças no talhão "{talhao.nome}" — {ind["total_ocorrencias"]} ocorrências registradas.',
                talhao,
            ))

        if ind['custo_por_caixa'] > LIMITES['custo_por_caixa_alto']:
            recomendacoes.append((
                'alta', 'bi-cash-stack',
                f'Revisar custos do talhão "{talhao.nome}" — R$ {ind["custo_por_caixa"]:.2f}/cx está acima do ideal.',
                talhao,
            ))

        if ind['total_caixas'] > 0 and ind['produtividade_caixas_ha'] < LIMITES['produtividade_critica_cx_ha']:
            recomendacoes.append((
                'alta', 'bi-graph-down-arrow',
                f'Investigar baixa produtividade no talhão "{talhao.nome}" ({ind["produtividade_caixas_ha"]:.0f} cx/ha).',
                talhao,
            ))

        if ind['custo_total'] > 0 and ind['lucro_estimado'] < 0:
            recomendacoes.append((
                'alta', 'bi-currency-dollar',
                f'Revisar estratégia do talhão "{talhao.nome}" — prejuízo estimado de R$ {abs(ind["lucro_estimado"]):.2f}.',
                talhao,
            ))

        if ind['ultima_colheita']:
            dias_colheita = (date.today() - ind['ultima_colheita'].data_colheita).days
            if dias_colheita >= 270:
                recomendacoes.append((
                    'media', 'bi-basket',
                    f'Verificar ponto de colheita no talhão "{talhao.nome}" ({dias_colheita} dias desde a última).',
                    talhao,
                ))

    if not recomendacoes:
        recomendacoes.append((
            'info', 'bi-check-circle-fill',
            'Todos os talhões apresentam situação satisfatória. Continue monitorando regularmente.',
            None,
        ))

    ordem = {'urgente': 0, 'alta': 1, 'media': 2, 'info': 3}
    return sorted(recomendacoes, key=lambda x: ordem.get(x[0], 4))
