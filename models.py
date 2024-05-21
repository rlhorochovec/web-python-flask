from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class MutanteModel(db.Model):
    __tablename__ = "mutante"
 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    codinome = db.Column(db.String())
 
    def __init__(self, id,nome,codinome):
        self.id = id
        self.nome = nome
        self.codinome = codinome
 
    def __repr__(self):
        return f"{self.nome}:{self.id}"