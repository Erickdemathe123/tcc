from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from flask_login import login_required, current_user
from app.extensions import db
from app.models.ocorrencia import Ocorrencia, TIPOS_OCORRENCIA, NIVEIS_SEVERIDADE, PRAGAS_DOENCAS_COMUNS, RECOMENDACOES
from app.models.talhao import Talhao
from app.models.propriedade import Propriedade

bp = Blueprint('ocorrencias', __name__, url_prefix='/ocorrencias')


@bp.route('/')
@login_required
def index():
    ocorrencias = (Ocorrencia.query.join(Talhao).join(Propriedade)
                   .filter(Propriedade.usuario_id == current_user.id)
                   .order_by(Ocorrencia.data_ocorrencia.desc()).all())
    return render_template('ocorrencias/index.html', ocorrencias=ocorrencias)


@bp.route('/<int:id>')
@login_required
def detalhe(id):
    ocorrencia = Ocorrencia.query.get_or_404(id)
    recomendacao = RECOMENDACOES.get(ocorrencia.nome, RECOMENDACOES['Outros'])
    return render_template('ocorrencias/detalhe.html', ocorrencia=ocorrencia, recomendacao=recomendacao)


@bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())
    talhao_id = request.args.get('talhao_id', type=int)

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        tipo = request.form.get('tipo', '').strip()
        nome = request.form.get('nome', '').strip()
        severidade = request.form.get('severidade', '').strip()
        data_str = request.form.get('data_ocorrencia', '').strip()

        if not tid or not tipo or not nome or not severidade or not data_str:
            flash('Talhão, tipo, nome, severidade e data são obrigatórios.', 'danger')
            return render_template('ocorrencias/form.html', ocorrencia=None, talhoes=talhoes,
                                   tipos=TIPOS_OCORRENCIA, severidades=NIVEIS_SEVERIDADE,
                                   pragas_comuns=PRAGAS_DOENCAS_COMUNS, talhao_id_selecionado=tid)

        ocorrencia = Ocorrencia(
            talhao_id=tid,
            tipo=tipo,
            nome=nome,
            severidade=severidade,
            data_ocorrencia=date.fromisoformat(data_str),
            area_afetada_ha=_float_or_none(request.form.get('area_afetada_ha')),
            tratamento_aplicado=request.form.get('tratamento_aplicado', '').strip() or None,
        )
        db.session.add(ocorrencia)
        db.session.commit()
        flash('Ocorrência registrada com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=tid))

    return render_template('ocorrencias/form.html', ocorrencia=None, talhoes=talhoes,
                           tipos=TIPOS_OCORRENCIA, severidades=NIVEIS_SEVERIDADE,
                           pragas_comuns=PRAGAS_DOENCAS_COMUNS, talhao_id_selecionado=talhao_id,
                           recomendacoes=RECOMENDACOES)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    ocorrencia = Ocorrencia.query.get_or_404(id)
    talhoes = (Talhao.query.join(Propriedade)
               .filter(Propriedade.usuario_id == current_user.id)
               .order_by(Propriedade.nome, Talhao.nome).all())

    if request.method == 'POST':
        tid = request.form.get('talhao_id', type=int)
        tipo = request.form.get('tipo', '').strip()
        nome = request.form.get('nome', '').strip()
        severidade = request.form.get('severidade', '').strip()
        data_str = request.form.get('data_ocorrencia', '').strip()

        if not tid or not tipo or not nome or not severidade or not data_str:
            flash('Talhão, tipo, nome, severidade e data são obrigatórios.', 'danger')
            return render_template('ocorrencias/form.html', ocorrencia=ocorrencia, talhoes=talhoes,
                                   tipos=TIPOS_OCORRENCIA, severidades=NIVEIS_SEVERIDADE,
                                   pragas_comuns=PRAGAS_DOENCAS_COMUNS, talhao_id_selecionado=tid)

        ocorrencia.talhao_id = tid
        ocorrencia.tipo = tipo
        ocorrencia.nome = nome
        ocorrencia.severidade = severidade
        ocorrencia.data_ocorrencia = date.fromisoformat(data_str)
        ocorrencia.area_afetada_ha = _float_or_none(request.form.get('area_afetada_ha'))
        ocorrencia.tratamento_aplicado = request.form.get('tratamento_aplicado', '').strip() or None
        db.session.commit()
        flash('Ocorrência atualizada com sucesso!', 'success')
        return redirect(url_for('talhoes.detalhe', id=ocorrencia.talhao_id))

    return render_template('ocorrencias/form.html', ocorrencia=ocorrencia, talhoes=talhoes,
                           tipos=TIPOS_OCORRENCIA, severidades=NIVEIS_SEVERIDADE,
                           pragas_comuns=PRAGAS_DOENCAS_COMUNS, talhao_id_selecionado=ocorrencia.talhao_id,
                           recomendacoes=RECOMENDACOES)


@bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    ocorrencia = Ocorrencia.query.get_or_404(id)
    talhao_id = ocorrencia.talhao_id
    db.session.delete(ocorrencia)
    db.session.commit()
    flash('Ocorrência excluída.', 'success')
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
