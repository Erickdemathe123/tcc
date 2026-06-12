from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from flask_login import login_required, current_user
from app.extensions import db
from app.models.colheita import Colheita, DESTINOS
from app.models.talhao import Talhao
from app.models.propriedade import Propriedade

bp = Blueprint('colheitas', __name__, url_prefix='/colheitas')


@bp.route('/')
@login_required
def index():
    colheitas = (Colheita.query.join(Talhao).join(Propriedade)
                 .filter(Propriedade.usuario_id == current_user.id)
                 .order_by(Colheita.data_colheita.desc()).all())
    return render_template('colheitas/index.html', colheitas=colheitas)


@bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())
    talhao_id = request.args.get('talhao_id', type=int)

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        data_str = request.form.get('data_colheita', '').strip()

        if not tid or not data_str:
            flash('Talhão e data são obrigatórios.', 'danger')
            return render_template('colheitas/form.html', colheita=None, talhoes=talhoes,
                                   destinos=DESTINOS, talhao_id_selecionado=tid)

        colheita = Colheita(
            talhao_id=tid,
            data_colheita=date.fromisoformat(data_str),
            quantidade_caixas=_int_or_none(request.form.get('quantidade_caixas')),
            peso_por_caixa=_float_or_none(request.form.get('peso_por_caixa')),
            preco_por_caixa=_float_or_none(request.form.get('preco_por_caixa')),
            destino=request.form.get('destino', '').strip() or None,
        )
        db.session.add(colheita)
        db.session.commit()
        flash('Colheita registrada com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=tid))

    return render_template('colheitas/form.html', colheita=None, talhoes=talhoes,
                           destinos=DESTINOS, talhao_id_selecionado=talhao_id)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    colheita = Colheita.query.get_or_404(id)
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        data_str = request.form.get('data_colheita', '').strip()

        if not tid or not data_str:
            flash('Talhão e data são obrigatórios.', 'danger')
            return render_template('colheitas/form.html', colheita=colheita, talhoes=talhoes,
                                   destinos=DESTINOS, talhao_id_selecionado=tid)

        colheita.talhao_id = tid
        colheita.data_colheita = date.fromisoformat(data_str)
        colheita.quantidade_caixas = _int_or_none(request.form.get('quantidade_caixas'))
        colheita.peso_por_caixa = _float_or_none(request.form.get('peso_por_caixa'))
        colheita.preco_por_caixa = _float_or_none(request.form.get('preco_por_caixa'))
        colheita.destino = request.form.get('destino', '').strip() or None
        db.session.commit()
        flash('Colheita atualizada com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=colheita.talhao_id))

    return render_template('colheitas/form.html', colheita=colheita, talhoes=talhoes,
                           destinos=DESTINOS, talhao_id_selecionado=colheita.talhao_id)


@bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    colheita = Colheita.query.get_or_404(id)
    talhao_id = colheita.talhao_id
    db.session.delete(colheita)
    db.session.commit()
    flash('Colheita excluída.', 'success')
    return redirect(url_for('talhoes.detalhe', id=talhao_id))


def _float_or_none(value):
    try:
        if not value:
            return None
        s = str(value).strip()
        if ',' in s and '.' in s:
            # formato BR completo: "5.000,50" → "5000.50"
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            # só vírgula como decimal: "5000,50" → "5000.50"
            s = s.replace(',', '.')
        elif s.count('.') > 1:
            # múltiplos pontos = separador de milhar: "5.000.000" → "5000000"
            s = s.replace('.', '')
        return float(s)
    except ValueError:
        return None


def _int_or_none(value):
    try:
        return int(value) if value else None
    except ValueError:
        return None
