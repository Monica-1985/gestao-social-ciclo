
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def conectar_banco():
    return sqlite3.connect("gestao_social.db")


def criar_banco():
    conexao = conectar_banco()
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS adesoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultora TEXT NOT NULL,
            iniciativa TEXT NOT NULL,
            ciclo TEXT NOT NULL,
            data TEXT NOT NULL,
            situacao TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/adesoes")
def listar_adesoes():
    conexao = conectar_banco()

    registros = conexao.execute("""
        SELECT id, consultora, iniciativa, ciclo, data, situacao
        FROM adesoes
        ORDER BY id DESC
    """).fetchall()

    conexao.close()

    return render_template("adesoes.html", adesoes=registros)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    mensagem = ""

    if request.method == "POST":
        consultora = request.form.get("consultora", "").strip()
        iniciativa = request.form.get("iniciativa", "")
        ciclo = request.form.get("ciclo", "").strip()
        data = request.form.get("data", "")
        situacao = request.form.get("situacao", "")

        if all([consultora, iniciativa, ciclo, data, situacao]):
            conexao = conectar_banco()
            conexao.execute("""
                INSERT INTO adesoes
                (consultora, iniciativa, ciclo, data, situacao)
                VALUES (?, ?, ?, ?, ?)
            """, (consultora, iniciativa, ciclo, data, situacao))
            conexao.commit()
            conexao.close()

            mensagem = "Adesão cadastrada com sucesso!"
        else:
            mensagem = "Preencha todos os campos obrigatórios."

    return render_template("cadastro.html", mensagem=mensagem)


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
