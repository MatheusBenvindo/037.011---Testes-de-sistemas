from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "dev_secret_for_demo"

# Armazenamento simples em memória para demonstração
users = {"student@example.com": {"password": "password123", "name": "Aluno Exemplo"}}


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Campos vazios", "error")
            return render_template("login.html")

        user = users.get(email)
        if not user:
            flash("Usuário inválido", "error")
            return render_template("login.html")

        if user["password"] != password:
            flash("Senha inválida", "error")
            return render_template("login.html")

        # sucesso
        session["user_email"] = email
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("Campos vazios", "error")
            return render_template("register.html")

        if email in users:
            flash("Email já cadastrado", "error")
            return render_template("register.html")

        users[email] = {"password": password, "name": name}
        flash("Cadastro realizado", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    email = session.get("user_email")
    if not email or email not in users:
        return redirect(url_for("login"))

    user = users[email]
    return render_template("dashboard.html", user=user)


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
