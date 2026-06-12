import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from flask_login import login_required, current_user
from app.extensions import db
from app.models.colheita import Colheita, ColheitaItem, DESTINOS
from app.models.talhao import Talhao, VARIEDADES
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
    talhao_variedades = _talhao_variedades_json(talhoes)

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        data_str = request.form.get('data_colheita', '').strip()

        if not tid or not data_str:
            flash('Talhão e data são obrigatórios.', 'danger')
            return render_template('colheitas/form.html', colheita=None, talhoes=talhoes,
                                   destinos=DESTINOS, talhao_id_selecionado=tid,
                                   talhao_variedades=talhao_variedades,
                                   variedades_all=VARIEDADES, itens_existentes=[])

        itens = _extrair_itens(request.form)
        if not itens:
            flash('Adicione ao menos um item de colheita com variedade e quantidade.', 'danger')
            return render_template('colheitas/form.html', colheita=None, talhoes=talhoes,
                                   destinos=DESTINOS, talhao_id_selecionado=tid,
                                   talhao_variedades=talhao_variedades,
                                   variedades_all=VARIEDADES, itens_existentes=[])

        colheita = Colheita(
            talhao_id=tid,
            data_colheita=date.fromisoformat(data_str),
            destino=request.form.get('destino', '').strip() or None,
        )
        colheita.itens = itens
        db.session.add(colheita)
        db.session.commit()
        flash('Colheita registrada com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=tid))

    return render_template('colheitas/form.html', colheita=None, talhoes=talhoes,
                           destinos=DESTINOS, talhao_id_selecionado=talhao_id,
                           talhao_variedades=talhao_variedades,
                           variedades_all=VARIEDADES,
                           itens_existentes=[])


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    colheita = Colheita.query.get_or_404(id)
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())
    talhao_variedades = _talhao_variedades_json(talhoes)

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        data_str = request.form.get('data_colheita', '').strip()

        ie = [{'variedade': i.variedade, 'quantidade_caixas': i.quantidade_caixas,
                'peso_por_caixa': i.peso_por_caixa, 'preco_por_caixa': i.preco_por_caixa}
               for i in colheita.itens]
        if not tid or not data_str:
            flash('Talhão e data são obrigatórios.', 'danger')
            return render_template('colheitas/form.html', colheita=colheita, talhoes=talhoes,
                                   destinos=DESTINOS, talhao_id_selecionado=tid,
                                   talhao_variedades=talhao_variedades,
                                   variedades_all=VARIEDADES, itens_existentes=ie)

        itens = _extrair_itens(request.form)
        if not itens:
            flash('Adicione ao menos um item de colheita com variedade e quantidade.', 'danger')
            return render_template('colheitas/form.html', colheita=colheita, talhoes=talhoes,
                                   destinos=DESTINOS, talhao_id_selecionado=tid,
                                   talhao_variedades=talhao_variedades,
                                   variedades_all=VARIEDADES, itens_existentes=ie)

        colheita.talhao_id = tid
        colheita.data_colheita = date.fromisoformat(data_str)
        colheita.destino = request.form.get('destino', '').strip() or None
        colheita.itens = itens
        db.session.commit()
        flash('Colheita atualizada com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=colheita.talhao_id))

    itens_existentes = [
        {'variedade': i.variedade, 'quantidade_caixas': i.quantidade_caixas,
         'peso_por_caixa': i.peso_por_caixa, 'preco_por_caixa': i.preco_por_caixa}
        for i in colheita.itens
    ]
    return render_template('colheitas/form.html', colheita=colheita, talhoes=talhoes,
                           destinos=DESTINOS, talhao_id_selecionado=colheita.talhao_id,
                           talhao_variedades=talhao_variedades,
                           variedades_all=VARIEDADES,
                           itens_existentes=itens_existentes)


@bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    colheita = Colheita.query.get_or_404(id)
    talhao_id = colheita.talhao_id
    db.session.delete(colheita)
    db.session.commit()
    flash('Colheita excluída.', 'success')
    return redirect(url_for('talhoes.detalhe', id=talhao_id))


def _talhao_variedades_json(talhoes):
    """Retorna JSON mapeando talhao_id → lista de variedades."""
    data = {}
    for t in talhoes:
        data[t.id] = [v.variedade for v in t.variedades_list]
    return json.dumps(data)


def _extrair_itens(form):
    """Lê os arrays do form e retorna lista de ColheitaItem válidos."""
    variedades = form.getlist('variedade')
    quantidades = form.getlist('quantidade_caixas')
    pesos = form.getlist('peso_por_caixa')
    precos = form.getlist('preco_por_caixa')

    itens = []
    for v, q, p, pr in zip(variedades, quantidades, pesos, precos):
        qtd = _int_or_none(q)
        if v and v.strip() and qtd:
            itens.append(ColheitaItem(
                variedade=v.strip(),
                quantidade_caixas=qtd,
                peso_por_caixa=_float_or_none(p),
                preco_por_caixa=_float_or_none(pr),
            ))
    return itens


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


def _int_or_none(value):
    try:
        return int(value) if value else None
    except ValueError:
        return None
