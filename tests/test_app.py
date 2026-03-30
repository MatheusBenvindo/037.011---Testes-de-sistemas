import pytest

from app import app, users


def setup_function():
    app.testing = True
    # reset users para estado inicial conhecido
    users.clear()
    users['student@example.com'] = {'password': 'password123', 'name': 'Aluno Exemplo'}


def test_ct01_login_sucesso():
    client = app.test_client()
    resp = client.post('/login', data={'email': 'student@example.com', 'password': 'password123'}, follow_redirects=True)
    assert b'Acesso permitido' in resp.data


def test_ct02_senha_invalida():
    client = app.test_client()
    resp = client.post('/login', data={'email': 'student@example.com', 'password': 'wrongpass'}, follow_redirects=True)
    assert b'Senha inválida' in resp.data


def test_ct03_cadastro_valido():
    client = app.test_client()
    resp = client.post('/register', data={'name': 'Novo Aluno', 'email': 'novo@example.com', 'password': 'xpass'}, follow_redirects=True)
    # Após cadastro, faz login com o novo usuário
    resp2 = client.post('/login', data={'email': 'novo@example.com', 'password': 'xpass'}, follow_redirects=True)
    assert b'Acesso permitido' in resp2.data


def test_ct04_usuario_invalido():
    client = app.test_client()
    resp = client.post('/login', data={'email': 'naoexiste@example.com', 'password': 'abc'}, follow_redirects=True)
    assert b'Usuário inválido' in resp.data


def test_ct05_campos_vazios():
    client = app.test_client()
    resp = client.post('/login', data={'email': '', 'password': ''}, follow_redirects=True)
    assert b'Campos vazios' in resp.data
