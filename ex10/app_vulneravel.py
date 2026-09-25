# ===== app_vulneravel.py — laboratório apenas =====
# Copia do enunciado do Ex. 10, com TRES mudancas para poder rodar no lab,
# todas marcadas com [LAB]. Nenhuma delas corrige as falhas catalogadas em
# auditoria.md; so tiram o que impediria de executar ou exporia a maquina.
#   1. a conexao usa o MySQL do lab (senha vem do ambiente, nao do codigo);
#   2. escuta em 127.0.0.1 em vez de 0.0.0.0: com debug=True, o console do
#      Werkzeug ficaria acessivel para a rede inteira (Wi-Fi da faculdade);
#   3. a porta vem do ambiente, para o demo.py subir as duas versoes.
# A linha SENHA_MESTRA foi mantida como no original, porque e uma das falhas
# que o exercicio pede para encontrar (credencial fixa no codigo).
import os
import sys
from pathlib import Path

from flask import Flask, request, jsonify
import mysql.connector

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from db import MYSQL_CFG, carregar_env  # noqa: E402  [LAB]

carregar_env()

app = Flask(__name__)
SENHA_MESTRA = "Cyber@2024"  # falha original do enunciado (ver auditoria.md)


def db():
    return mysql.connector.connect(host=MYSQL_CFG["host"],           # [LAB]
                                   port=MYSQL_CFG["port"],
                                   user=MYSQL_CFG["user"],
                                   password=os.environ["MYSQL_PASSWORD"],
                                   database="seguranca")

@app.route("/api/usuarios/buscar")
def buscar():
    nome = request.args.get("nome", "")
    cur = db().cursor(dictionary=True)
    cur.execute(f"SELECT * FROM usuarios WHERE nome LIKE '%{nome}%'")
    return jsonify(cur.fetchall())

@app.route("/perfil")
def perfil():
    return f"<h1>Bem-vindo, {request.args.get('u','')}</h1>"

@app.route("/api/usuarios/<int:uid>", methods=["DELETE"])
def remover(uid):
    con = db(); cur = con.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (uid,))
    con.commit()
    return jsonify({"removido": uid})

@app.route("/api/relatorio")
def relatorio():
    cur = db().cursor()
    cur.execute("SELECT * FROM tabela_inexistente")
    return jsonify(cur.fetchall())

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1",                            # [LAB]
            port=int(os.getenv("PORTA", "5010")))
