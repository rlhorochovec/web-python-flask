import os
import uuid
from flask import Flask, render_template, request, redirect
from models import db, MutanteModel

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///xmen97.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"
db.init_app(app)


@app.before_request
def create_table():
    db.create_all()


@app.route("/xmen/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("novo.html")

    if request.method == "POST":
        mutante_id = request.form["mutante_id"]
        nome = request.form["nome"]
        codinome = request.form["codinome"]
        arquivo = request.files['imagem']
        arquivo_nome = arquivo.filename
        arquivo_extensao = arquivo_nome.rsplit('.', 1)[1].lower()
        arquivo_novo_nome = uuid.uuid4().hex +'.'+arquivo_extensao
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo_novo_nome))
        mutante = MutanteModel(mutante_id=mutante_id, nome=nome, codinome=codinome, imagem=arquivo_novo_nome)
        db.session.add(mutante)
        db.session.commit()
        return redirect("/xmen")


@app.route("/xmen")
def list():
    mutantes = MutanteModel.query.all()
    return render_template("lista.html", mutantes=mutantes)


@app.route("/xmen/<int:id>")
def detail(id):
    mutante = MutanteModel.query.filter_by(mutante_id=id).first()
    if mutante:
        return render_template("info.html", mutante=mutante)
    return f"Mutante com ID = {id} não foi encontrado."


@app.route("/xmen/<int:id>/update", methods=["GET", "POST"])
def update(id):
    mutante = MutanteModel.query.filter_by(mutante_id=id).first()
    if request.method == "POST":
        if mutante:
            db.session.delete(mutante)
            db.session.commit()
            nome = request.form["nome"]
            codinome = request.form["codinome"]
            arquivo = request.files['imagem']
            arquivo_nome = arquivo.filename
            arquivo_extensao = arquivo_nome.rsplit('.', 1)[1].lower()
            arquivo_novo_nome = uuid.uuid4().hex +'.'+arquivo_extensao
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo_novo_nome))
            mutante = MutanteModel(mutante_id=id, nome=nome, codinome=codinome, imagem=arquivo_novo_nome)
            db.session.add(mutante)
            db.session.commit()
            return redirect(f"/xmen/{id}")
        return f"Mutante com ID = {id} não foi encontrado."

    return render_template("edita.html", mutante=mutante)


@app.route("/xmen/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    mutante = MutanteModel.query.filter_by(mutante_id=id).first()
    if request.method == "POST":
        if mutante:
            db.session.delete(mutante)
            db.session.commit()
            return redirect("/xmen")

    return render_template("deleta.html")


app.run(host="localhost", port=5000)