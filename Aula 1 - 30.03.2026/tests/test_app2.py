from app import app, users

def setup_function():
    app.testing = True
    users.clear()
    users["student@example.com"] =  {"password": "password123", "name": "Aluno Exemplo"}

def test_ct01_login_sucesso():
    client = app.test_client()
    resp = client.post(
        "/login",
        data={"email": "student@example.com", "password": "password123"},
        follow_redirects=True,
    )

    result = "Acesso Permitido"
    bytes_result = result.encode("utf-8")
    assert bytes_result in resp.data

