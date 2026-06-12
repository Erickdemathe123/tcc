from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.propriedade import Propriedade
from app.models.talhao import Talhao
from app.services.indicadores import (
    calcular_indicadores_talhao, calcular_indicadores_propriedade,
    historico_producao_por_mes, historico_custos_por_mes, ranking_talhoes,
    pragas_mais_recorrentes,
)
from app.services.alertas import gerar_alertas_talhao
from app.services.diagnostico import classificar_talhao, diagnostico_propriedade
from datetime import date

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')


@bp.route('/')
@login_required
def index():
    propriedades = Propriedade.query.filter_by(usuario_id=current_user.id).order_by(Propriedade.nome).all()
    return render_template('relatorios/index.html', propriedades=propriedades)


@bp.route('/talhao/<int:id>')
@login_required
def talhao(id):
    t = Talhao.query.get_or_404(id)
    indicadores = calcular_indicadores_talhao(t)
    diagnostico = classificar_talhao(t)
    alertas = gerar_alertas_talhao(t)
    hist_producao = historico_producao_por_mes(t)
    hist_custos = historico_custos_por_mes(t)

    # Produtividade média da propriedade para comparação
    prop_indicadores = calcular_indicadores_propriedade(t.propriedade)
    media_propriedade = prop_indicadores['produtividade_media_ha']

    return render_template(
        'relatorios/talhao.html',
        talhao=t,
        indicadores=indicadores,
        diagnostico=diagnostico,
        alertas=alertas,
        hist_producao=hist_producao,
        hist_custos=hist_custos,
        media_propriedade=media_propriedade,
        data_geracao=date.today(),
    )


@bp.route('/propriedade/<int:id>')
@login_required
def propriedade(id):
    prop = Propriedade.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    indicadores = calcular_indicadores_propriedade(prop)
    diagnosticos = diagnostico_propriedade(prop)
    ranking = ranking_talhoes(prop)
    pragas = pragas_mais_recorrentes(prop)

    if diagnosticos['critico']:
        situacao_geral = 'critico'
    elif diagnosticos['atencao']:
        situacao_geral = 'atencao'
    elif diagnosticos['normal']:
        situacao_geral = 'normal'
    else:
        situacao_geral = 'sem_dados'

    return render_template(
        'relatorios/propriedade.html',
        propriedade=prop,
        indicadores=indicadores,
        diagnosticos=diagnosticos,
        ranking=ranking,
        pragas=pragas,
        situacao_geral=situacao_geral,
        data_geracao=date.today(),
    )
