import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_config import Base, Mutante

app=Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

engine = create_engine('sqlite:///database/xmen97.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Function to list
@app.route('/')
@app.route('/xmen')
def list():
   mutantes = session.query(Mutante).all()
   return render_template("lista.html", mutantes=mutantes)

#Function to add
@app.route('/xmen/add',methods=['GET','POST'])
def add():
   if request.method == 'POST':
       imagem = uuid.uuid4().hex +'.'+ request.files['imagem'].filename.rsplit('.', 1)[1].lower()
       request.files['imagem'].save(os.path.join(app.config['UPLOAD_FOLDER'], imagem))
       novo_mutante = Mutante(nome = request.form['nome'], codinome = request.form['codinome'], imagem = imagem)
       session.add(novo_mutante)
       session.commit()
       return redirect(url_for('list'))
   else:
       return render_template('novo.html')

#Function to edit
@app.route("/xmen/<int:mutante_id>/edit", methods = ['GET', 'POST'])
def update(mutante_id):
   edita_mutante = session.query(Mutante).filter_by(id=mutante_id).one()
   if request.method == 'POST':
       if edita_mutante:
           edita_mutante.nome = request.form['nome']
           edita_mutante.codinome = request.form['codinome']
           imagem = uuid.uuid4().hex +'.'+ request.files['imagem'].filename.rsplit('.', 1)[1].lower()
           request.files['imagem'].save(os.path.join(app.config['UPLOAD_FOLDER'], imagem))
           edita_mutante.imagem = request.form['imagem']
           return redirect(url_for('list'))
   else:
       return render_template('edita.html', mutante = edita_mutante)
   
#Function to detail   
@app.route("/xmen/<int:mutante_id>")
def detail(mutante_id):
    info_mutante = session.query(Mutante).filter_by(id=mutante_id).one()
    if info_mutante:
        return render_template("detalhe.html", mutante=info_mutante)
    else:
        return redirect(url_for('list'))

#Function to delete
@app.route('/xmen/<int:mutante_id>/delete', methods = ['GET','POST'])
def delete(mutante_id):
   deleta_mutante = session.query(Mutante).filter_by(id=mutante_id).one()
   if request.method == 'POST':
       session.delete(deleta_mutante)
       session.commit()
       return redirect(url_for('list', mutante_id=mutante_id))
   else:
       return render_template('deleta.html',mutante = deleta_mutante)

if __name__ == '__main__':
   app.run()