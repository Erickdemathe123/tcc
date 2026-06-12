from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from flask_login import login_required, current_user
from app.extensions import db
from app.models.talhao import Talhao, VARIEDADES
from app.models.propriedade import Propriedade
from app.services.indicadores import calcular_indicadores_talhao, historico_producao_por_mes, historico_custos_por_mes
from app.services.alertas import gerar_alertas_talhao
from app.services.diagnostico import classificar_talhao

bp = Blueprint('talhoes', __name__, url_prefix='/talhoes')


@bp.route('/')
@login_required
def index():
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())
    return render_template('talhoes/index.html', talhoes=talhoes)


@bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    propriedades = Propriedade.query.filter_by(usuario_id=current_user.id).order_by(Propriedade.nome).all()
    propriedade_id = request.args.get('propriedade_id', type=int)

    if request.method == 'POST':
        prop_id = request.form.get('propriedade_id', type=int)
        nome = request.form.get('nome', '').strip()
        area_ha = _float_or_none(request.form.get('area_ha'))

        if not prop_id or not nome or not area_ha:
            flash('Propriedade, nome do talhão e área são obrigatórios.', 'danger')
            return render_template('talhoes/form.html', talhao=None, propriedades=propriedades,
                                   variedades=VARIEDADES, propriedade_id_selecionado=prop_id)

        data_plantio = _date_or_none(request.form.get('data_plantio'))
        talhao = Talhao(
            propriedade_id=prop_id,
            nome=nome,
            area_ha=area_ha,
            variedade=request.form.get('variedade', '').strip() or None,
            data_plantio=data_plantio,
        )
        db.session.add(talhao)
        db.session.commit()
        flash(f'Talhão "{talhao.nome}" cadastrado com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=talhao.id))

    return render_template('talhoes/form.html', talhao=None, propriedades=propriedades,
                           variedades=VARIEDADES, propriedade_id_selecionado=propriedade_id)


@bp.route('/<int:id>')
@login_required
def detalhe(id):
    talhao = Talhao.query.get_or_404(id)
    indicadores = calcular_indicadores_talhao(talhao)
    diagnostico = classificar_talhao(talhao)
    alertas = gerar_alertas_talhao(talhao)
    hist_producao = historico_producao_por_mes(talhao)
    hist_custos = historico_custos_por_mes(talhao)
    return render_template(
        'talhoes/detalhe.html',
        talhao=talhao,
        indicadores=indicadores,
        diagnostico=diagnostico,
        alertas=alertas,
        hist_producao=hist_producao,
        hist_custos=hist_custos,
    )


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    talhao = Talhao.query.get_or_404(id)
    propriedades = Propriedade.query.filter_by(usuario_id=current_user.id).order_by(Propriedade.nome).all()

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        area_ha = _float_or_none(request.form.get('area_ha'))
        if not nome or not area_ha:
            flash('Nome e área são obrigatórios.', 'danger')
            return render_template('talhoes/form.html', talhao=talhao, propriedades=propriedades,
                                   variedades=VARIEDADES, propriedade_id_selecionado=talhao.propriedade_id)

        talhao.nome = nome
        talhao.area_ha = area_ha
        talhao.variedade = request.form.get('variedade', '').strip() or None
        talhao.data_plantio = _date_or_none(request.form.get('data_plantio'))
        talhao.propriedade_id = request.form.get('propriedade_id', type=int) or talhao.propriedade_id
        db.session.commit()
        flash('Talhão atualizado com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=talhao.id))

    return render_template('talhoes/form.html', talhao=talhao, propriedades=propriedades,
                           variedades=VARIEDADES, propriedade_id_selecionado=talhao.propriedade_id)


@bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    talhao = Talhao.query.get_or_404(id)
    propriedade_id = talhao.propriedade_id
    nome = talhao.nome
    db.session.delete(talhao)
    db.session.commit()
    flash(f'Talhão "{nome}" excluído.', 'success')
    return redirect(url_for('propriedades.detalhe', id=propriedade_id))


def _float_or_none(value):
    try:
        return float(str(value).replace(',', '.')) if value else None
    except ValueError:
        return None


def _date_or_none(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None
