from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.propriedade import Propriedade

bp = Blueprint('propriedades', __name__, url_prefix='/propriedades')


@bp.route('/')
@login_required
def index():
    propriedades = Propriedade.query.filter_by(usuario_id=current_user.id).order_by(Propriedade.nome).all()
    return render_template('propriedades/index.html', propriedades=propriedades)


@bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        produtor_nome = request.form.get('produtor_nome', '').strip()
        if not nome or not produtor_nome:
            flash('Nome da propriedade e nome do produtor são obrigatórios.', 'danger')
            return render_template('propriedades/form.html', propriedade=None)

        propriedade = Propriedade(
            usuario_id=current_user.id,
            nome=nome,
            produtor_nome=produtor_nome,
            localizacao=request.form.get('localizacao', '').strip(),
            area_total_ha=_float_or_none(request.form.get('area_total_ha')),
        )
        db.session.add(propriedade)
        db.session.commit()
        flash(f'Propriedade "{propriedade.nome}" cadastrada com sucesso!', 'success')
        return redirect(url_for('propriedades.detalhe', id=propriedade.id))

    return render_template('propriedades/form.html', propriedade=None)


@bp.route('/<int:id>')
@login_required
def detalhe(id):
    propriedade = Propriedade.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    return render_template('propriedades/detalhe.html', propriedade=propriedade)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    propriedade = Propriedade.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        produtor_nome = request.form.get('produtor_nome', '').strip()
        if not nome or not produtor_nome:
            flash('Nome da propriedade e nome do produtor são obrigatórios.', 'danger')
            return render_template('propriedades/form.html', propriedade=propriedade)

        propriedade.nome = nome
        propriedade.produtor_nome = produtor_nome
        propriedade.localizacao = request.form.get('localizacao', '').strip()
        propriedade.area_total_ha = _float_or_none(request.form.get('area_total_ha'))
        db.session.commit()
        flash('Propriedade atualizada com sucesso!', 'success')
        return redirect(url_for('propriedades.detalhe', id=propriedade.id))

    return render_template('propriedades/form.html', propriedade=propriedade)


@bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    propriedade = Propriedade.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    nome = propriedade.nome
    db.session.delete(propriedade)
    db.session.commit()
    flash(f'Propriedade "{nome}" excluída.', 'success')
    return redirect(url_for('propriedades.index'))


def _float_or_none(value):
    try:
        return float(value.replace(',', '.')) if value else None
    except (ValueError, AttributeError):
        return None
