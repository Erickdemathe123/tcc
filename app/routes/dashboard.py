from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.propriedade import Propriedade
from app.services.indicadores import calcular_indicadores_propriedade, pragas_mais_recorrentes, ranking_talhoes
from app.services.alertas import gerar_todos_alertas
from app.services.diagnostico import diagnostico_propriedade, gerar_recomendacoes

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    propriedade = Propriedade.query.filter_by(usuario_id=current_user.id).first()
    if not propriedade:
        return render_template('dashboard/vazio.html')
    return redirect(url_for('dashboard.painel', propriedade_id=propriedade.id))


@bp.route('/dashboard/<int:propriedade_id>')
@login_required
def painel(propriedade_id):
    propriedade = Propriedade.query.filter_by(id=propriedade_id, usuario_id=current_user.id).first_or_404()
    todas_propriedades = Propriedade.query.filter_by(usuario_id=current_user.id).order_by(Propriedade.nome).all()

    indicadores = calcular_indicadores_propriedade(propriedade)
    alertas = gerar_todos_alertas(propriedade)
    diagnosticos = diagnostico_propriedade(propriedade)
    pragas = pragas_mais_recorrentes(propriedade)
    ranking = ranking_talhoes(propriedade)
    recomendacoes = gerar_recomendacoes(propriedade)

    situacoes_count = {
        'Normal': len(diagnosticos['normal']),
        'Atenção': len(diagnosticos['atencao']),
        'Crítico': len(diagnosticos['critico']),
    }

    # Situação geral da propriedade: pior situação entre os talhões
    if diagnosticos['critico']:
        situacao_geral = 'critico'
    elif diagnosticos['atencao']:
        situacao_geral = 'atencao'
    elif diagnosticos['normal']:
        situacao_geral = 'normal'
    else:
        situacao_geral = 'sem_dados'

    return render_template(
        'dashboard/index.html',
        propriedade=propriedade,
        todas_propriedades=todas_propriedades,
        indicadores=indicadores,
        alertas=alertas,
        diagnosticos=diagnosticos,
        pragas=pragas,
        ranking=ranking,
        recomendacoes=recomendacoes,
        situacoes_count=situacoes_count,
        situacao_geral=situacao_geral,
    )
