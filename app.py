from datetime import datetime
import os
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e450cd13-c929-4667-9d63-7403e143d129'
app.config["UPLOAD_FOLDER"] = "static/uploads"


def get_db_connection():
    conn = sqlite3.connect("database/xmen97.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
@app.route("/xmen")
def index():
    conn = get_db_connection()
    mutantes = conn.execute("SELECT * FROM mutantes").fetchall()
    conn.close()
    return render_template("lista.html", mutantes=mutantes)


@app.route("/xmen/add", methods=("GET", "POST"))
def add():
    if request.method == "POST":
        nome = request.form["nome"]
        codinome = request.form["codinome"]
        
        arquivo = request.files['imagem']
        arquivo_nome = arquivo.filename
        arquivo_extensao = arquivo_nome.rsplit('.', 1)[1].lower()
        imagem = str(uuid.uuid4()) +'.'+ arquivo_extensao
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem))

        if not nome:
            flash("Nome é obrigatório!")
        elif not codinome:
            flash("Codinome é obrigatório!")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO mutantes (nome, codinome, imagem) VALUES (?, ?, ?)",
                (nome, codinome, imagem),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("novo.html")

def get_mutante(mutante_id):
    conn = get_db_connection()
    mutante = conn.execute('SELECT * FROM mutantes WHERE id = ?',
                        (mutante_id,)).fetchone()
    conn.close()
    if mutante is None:
        abort(404)
    return mutante

@app.route('/xmen/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    mutante_edit = get_mutante(id)
    if request.method=="POST":
        nome = request.form["nome"]
        codinome = request.form["codinome"]
        
        arquivo = request.files['imagem']
        arquivo_nome = arquivo.filename
        arquivo_extensao = arquivo_nome.rsplit('.', 1)[1].lower()
        imagem = str(uuid.uuid4()) +'.'+ arquivo_extensao
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem))

        if not nome:
            flash("Nome é obrigatório!")
        elif not codinome:
            flash("Codinome é obrigatório!")
        else:
            conn = get_db_connection()
            conn.execute('UPDATE mutantes SET nome = ?, codinome = ?, imagem = ?'
                            ' WHERE id = ?',
                            (nome, codinome, imagem, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edita.html', mutante=mutante_edit)

@app.route('/xmen/<int:id>/', methods=('GET', 'POST'))
def detail(id):
    mutante_view = get_mutante(id)
    return render_template('detalhe.html', mutante=mutante_view)

@app.route('/xmen/<int:id>/delete/', methods=('POST',))
def delete(id):
    mutante = get_mutante(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM mutantes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" excluído com sucesso!'.format(mutante['codinome']))
    return redirect(url_for('index'))