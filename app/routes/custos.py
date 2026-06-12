from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from flask_login import login_required, current_user
from app.extensions import db
from app.models.custo import Custo, CATEGORIAS_CUSTO
from app.models.talhao import Talhao
from app.models.propriedade import Propriedade

bp = Blueprint('custos', __name__, url_prefix='/custos')


@bp.route('/')
@login_required
def index():
    custos = (Custo.query.join(Talhao).join(Propriedade)
              .filter(Propriedade.usuario_id == current_user.id)
              .order_by(Custo.data_custo.desc()).all())
    return render_template('custos/index.html', custos=custos)


@bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())
    talhao_id = request.args.get('talhao_id', type=int)

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        categoria = request.form.get('categoria', '').strip()
        data_str = request.form.get('data_custo', '').strip()
        valor = _float_or_none(request.form.get('valor'))

        if not tid or not categoria or not data_str or valor is None:
            flash('Talhão, categoria, data e valor são obrigatórios.', 'danger')
            return render_template('custos/form.html', custo=None, talhoes=talhoes,
                                   categorias=CATEGORIAS_CUSTO, talhao_id_selecionado=tid)

        custo = Custo(
            talhao_id=tid,
            categoria=categoria,
            data_custo=date.fromisoformat(data_str),
            valor=valor,
            descricao=request.form.get('descricao', '').strip() or None,
        )
        db.session.add(custo)
        db.session.commit()
        flash('Custo registrado com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=tid))

    return render_template('custos/form.html', custo=None, talhoes=talhoes,
                           categorias=CATEGORIAS_CUSTO, talhao_id_selecionado=talhao_id)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    custo = Custo.query.get_or_404(id)
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        categoria = request.form.get('categoria', '').strip()
        data_str = request.form.get('data_custo', '').strip()
        valor = _float_or_none(request.form.get('valor'))

        if not tid or not categoria or not data_str or valor is None:
            flash('Talhão, categoria, data e valor são obrigatórios.', 'danger')
            return render_template('custos/form.html', custo=custo, talhoes=talhoes,
                                   categorias=CATEGORIAS_CUSTO, talhao_id_selecionado=tid)

        custo.talhao_id = tid
        custo.categoria = categoria
        custo.data_custo = date.fromisoformat(data_str)
        custo.valor = valor
        custo.descricao = request.form.get('descricao', '').strip() or None
        db.session.commit()
        flash('Custo atualizado com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=custo.talhao_id))

    return render_template('custos/form.html', custo=custo, talhoes=talhoes,
                           categorias=CATEGORIAS_CUSTO, talhao_id_selecionado=custo.talhao_id)


@bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    custo = Custo.query.get_or_404(id)
    talhao_id = custo.talhao_id
    db.session.delete(custo)
    db.session.commit()
    flash('Custo excluído.', 'success')
    return redirect(url_for('talhoes.detalhe', id=talhao_id))


def _float_or_none(value):
    try:
        if not value:
            return None
        s = str(value).strip()
        if ',' in s and '.' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            s = s.replace(',', '.')
        elif s.count('.') > 1:
            s = s.replace('.', '')
        return float(s)
    except ValueError:
        return None
