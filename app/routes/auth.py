from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from app.extensions import db, mail
from app.models.usuario import Usuario

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        lembrar = request.form.get('lembrar') == 'on'

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_senha(senha):
            login_user(usuario, remember=lembrar)
            proximo = request.args.get('next')
            return redirect(proximo or url_for('dashboard.index'))

        flash('E-mail ou senha incorretos.', 'danger')

    return render_template('auth/login.html')


@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        confirmar = request.form.get('confirmar', '')

        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('auth/registro.html')

        if senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/registro.html')

        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
            return render_template('auth/registro.html')

        if Usuario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'danger')
            return render_template('auth/registro.html')

        usuario = Usuario(nome=nome, email=email)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()

        login_user(usuario)
        flash(f'Bem-vindo(a), {nome.split()[0]}! Conta criada com sucesso.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/registro.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        usuario = Usuario.query.filter_by(email=email).first()

        # Sempre mostra a mesma mensagem para não revelar se o email existe
        flash('Se este e-mail estiver cadastrado, você receberá um link de redefinição em instantes.', 'info')

        if usuario:
            token = usuario.gerar_token_reset()
            link = url_for('auth.redefinir_senha', token=token, _external=True)
            msg = Message(
                subject='AgroBanana — Redefinição de Senha',
                recipients=[usuario.email],
            )
            msg.html = f"""
            <p>Olá, <strong>{usuario.nome}</strong>!</p>
            <p>Recebemos uma solicitação para redefinir a senha da sua conta no AgroBanana.</p>
            <p>Clique no botão abaixo para criar uma nova senha. Este link é válido por <strong>1 hora</strong>.</p>
            <p style="text-align:center;margin:2rem 0;">
              <a href="{link}" style="background:#2d6a4f;color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:600;">
                Redefinir Senha
              </a>
            </p>
            <p style="font-size:.85rem;color:#666;">Se você não solicitou a redefinição, ignore este e-mail. Sua senha permanece a mesma.</p>
            <p style="font-size:.85rem;color:#666;">Ou copie este link: {link}</p>
            """
            try:
                mail.send(msg)
            except Exception as e:
                current_app.logger.error(f'Erro ao enviar email de reset: {e}')
                if current_app.debug:
                    flash(f'Erro ao enviar e-mail: {e}', 'danger')
                    return render_template('auth/esqueci_senha.html')

        return redirect(url_for('auth.login'))

    return render_template('auth/esqueci_senha.html')


@bp.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    usuario = Usuario.verificar_token_reset(token)
    if usuario is None:
        flash('O link de redefinição é inválido ou já expirou.', 'danger')
        return redirect(url_for('auth.esqueci_senha'))

    if request.method == 'POST':
        nova_senha = request.form.get('senha', '')
        confirmar = request.form.get('confirmar', '')

        if not nova_senha or len(nova_senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
            return render_template('auth/redefinir_senha.html', token=token)

        if nova_senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/redefinir_senha.html', token=token)

        usuario.set_senha(nova_senha)
        db.session.commit()
        flash('Senha redefinida com sucesso! Faça login com a nova senha.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/redefinir_senha.html', token=token)
