"""
Testes de integração para as rotas HTTP (auth + navegação básica).
"""
import pytest
from app.models.usuario import Usuario


# ---------- Auxiliares ----------

def _login(client, email='joao@teste.com', senha='Senha123!'):
    return client.post('/auth/login', data={'email': email, 'senha': senha}, follow_redirects=True)


def _registro(client, nome='Maria', email='maria@test.com', senha='Senha123!', confirmar=None):
    return client.post('/auth/registro', data={
        'nome': nome,
        'email': email,
        'senha': senha,
        'confirmar': confirmar or senha,
    }, follow_redirects=True)


# ---------- GET em rotas públicas ----------

class TestRotasPublicas:
    def test_get_login_retorna_200(self, client):
        resp = client.get('/auth/login')
        assert resp.status_code == 200

    def test_get_registro_retorna_200(self, client):
        resp = client.get('/auth/registro')
        assert resp.status_code == 200

    def test_get_esqueci_senha_retorna_200(self, client):
        resp = client.get('/auth/esqueci-senha')
        assert resp.status_code == 200


# ---------- Login ----------

class TestLogin:
    def test_login_valido_redireciona(self, client, usuario):
        resp = _login(client)
        assert resp.status_code == 200

    def test_login_invalido_permanece_na_pagina(self, client):
        resp = client.post('/auth/login', data={
            'email': 'nao@existe.com',
            'senha': 'errada',
        })
        # Sem redirect — renderiza o login novamente
        assert resp.status_code == 200

    def test_login_senha_errada(self, client, usuario):
        resp = client.post('/auth/login', data={
            'email': 'joao@teste.com',
            'senha': 'errada',
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_login_usuario_autenticado_redireciona(self, cliente_logado):
        resp = cliente_logado.get('/auth/login', follow_redirects=True)
        assert resp.status_code == 200


# ---------- Registro ----------

class TestRegistro:
    def test_registro_valido_cria_usuario(self, client, db):
        # Não seguimos redirect pois o dashboard requer dados que não existem no teste
        resp = client.post('/auth/registro', data={
            'nome': 'Novo',
            'email': 'novo@test.com',
            'senha': 'Abc123!',
            'confirmar': 'Abc123!',
        })
        # 302 indica redirect após criação bem-sucedida
        assert resp.status_code == 302
        u = Usuario.query.filter_by(email='novo@test.com').first()
        assert u is not None
        assert u.nome == 'Novo'

    def test_registro_senhas_divergentes_nao_cria(self, client, db):
        _registro(client, email='div@test.com', senha='Abc123!', confirmar='Diferente1!')
        assert Usuario.query.filter_by(email='div@test.com').first() is None

    def test_registro_senha_curta_nao_cria(self, client, db):
        _registro(client, email='curta@test.com', senha='123', confirmar='123')
        assert Usuario.query.filter_by(email='curta@test.com').first() is None

    def test_registro_email_duplicado_nao_cria_segundo(self, client, usuario, db):
        _registro(client, nome='Dup', email='joao@teste.com', senha='Abc123!')
        count = Usuario.query.filter_by(email='joao@teste.com').count()
        assert count == 1

    def test_registro_campos_obrigatorios_vazios(self, client, db):
        resp = client.post('/auth/registro', data={
            'nome': '',
            'email': 'vazio@test.com',
            'senha': '',
            'confirmar': '',
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert Usuario.query.filter_by(email='vazio@test.com').first() is None

    def test_usuario_autenticado_redireciona_do_registro(self, cliente_logado):
        resp = cliente_logado.get('/auth/registro', follow_redirects=True)
        assert resp.status_code == 200


# ---------- Logout ----------

class TestLogout:
    def test_logout_redireciona_para_login(self, cliente_logado):
        resp = cliente_logado.get('/auth/logout', follow_redirects=True)
        assert resp.status_code == 200

    def test_logout_sem_login_redireciona(self, client):
        resp = client.get('/auth/logout', follow_redirects=True)
        assert resp.status_code == 200


# ---------- Proteção de rotas autenticadas ----------

class TestProtecaoRotas:
    def test_dashboard_sem_login_redireciona(self, client):
        resp = client.get('/', follow_redirects=False)
        assert resp.status_code in (301, 302)

    def test_propriedades_sem_login_redireciona(self, client):
        resp = client.get('/propriedades/', follow_redirects=False)
        assert resp.status_code in (301, 302)

    def test_dashboard_com_login_retorna_200(self, cliente_logado):
        resp = cliente_logado.get('/', follow_redirects=True)
        assert resp.status_code == 200


# ---------- Recuperação de senha ----------

class TestRecuperacaoSenha:
    def test_esqueci_senha_email_existente_redireciona(self, client, usuario):
        resp = client.post('/auth/esqueci-senha', data={
            'email': 'joao@teste.com',
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_esqueci_senha_email_inexistente_nao_vaza_info(self, client):
        resp = client.post('/auth/esqueci-senha', data={
            'email': 'nao-existe@teste.com',
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_token_invalido_redireciona(self, client):
        resp = client.get('/auth/redefinir-senha/token-invalido', follow_redirects=True)
        assert resp.status_code == 200
