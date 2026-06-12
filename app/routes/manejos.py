from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from flask_login import login_required, current_user
from app.extensions import db
from app.models.manejo import Manejo, TIPOS_MANEJO
from app.models.talhao import Talhao
from app.models.propriedade import Propriedade

bp = Blueprint('manejos', __name__, url_prefix='/manejos')


@bp.route('/')
@login_required
def index():
    manejos = (Manejo.query.join(Talhao).join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Manejo.data_manejo.desc()).all())
    return render_template('manejos/index.html', manejos=manejos)


@bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())
    talhao_id = request.args.get('talhao_id', type=int)

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        tipo = request.form.get('tipo', '').strip()
        data_str = request.form.get('data_manejo', '').strip()

        if not tid or not tipo or not data_str:
            flash('Talhão, tipo e data são obrigatórios.', 'danger')
            return render_template('manejos/form.html', manejo=None, talhoes=talhoes,
                                   tipos=TIPOS_MANEJO, talhao_id_selecionado=tid)

        manejo = Manejo(
            talhao_id=tid,
            tipo=tipo,
            data_manejo=date.fromisoformat(data_str),
            descricao=request.form.get('descricao', '').strip() or None,
            responsavel=request.form.get('responsavel', '').strip() or None,
        )
        db.session.add(manejo)
        db.session.commit()
        flash('Manejo registrado com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=tid))

    return render_template('manejos/form.html', manejo=None, talhoes=talhoes,
                           tipos=TIPOS_MANEJO, talhao_id_selecionado=talhao_id)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    manejo = Manejo.query.get_or_404(id)
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        tipo = request.form.get('tipo', '').strip()
        data_str = request.form.get('data_manejo', '').strip()

        if not tid or not tipo or not data_str:
            flash('Talhão, tipo e data são obrigatórios.', 'danger')
            return render_template('manejos/form.html', manejo=manejo, talhoes=talhoes,
                                   tipos=TIPOS_MANEJO, talhao_id_selecionado=tid)

        manejo.talhao_id = tid
        manejo.tipo = tipo
        manejo.data_manejo = date.fromisoformat(data_str)
        manejo.descricao = request.form.get('descricao', '').strip() or None
        manejo.responsavel = request.form.get('responsavel', '').strip() or None
        db.session.commit()
        flash('Manejo atualizado com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=manejo.talhao_id))

    return render_template('manejos/form.html', manejo=manejo, talhoes=talhoes,
                           tipos=TIPOS_MANEJO, talhao_id_selecionado=manejo.talhao_id)


@bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    manejo = Manejo.query.get_or_404(id)
    talhao_id = manejo.talhao_id
    db.session.delete(manejo)
    db.session.commit()
    flash('Manejo excluído.', 'success')
    return redirect(url_for('talhoes.detalhe', id=talhao_id))
