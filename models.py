from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MutanteModel(db.Model):
    __tablename__ = "mutantes"

    id = db.Column(db.Integer, primary_key=True)
    mutante_id = db.Column(db.Integer(), unique=True)
    nome = db.Column(db.String())
    codinome = db.Column(db.String())

    def __init__(self, mutante_id, nome, codinome):
        self.mutante_id = mutante_id
        self.nome = nome
        self.codinome = codinome

    def __repr__(self):
        return f"{self.nome} | {self.codinome}"
