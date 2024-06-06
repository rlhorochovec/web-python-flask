import sqlite3

connection = sqlite3.connect("database/xmen97.db")


with open("database/schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO mutantes (nome, codinome, imagem) VALUES (?, ?, ?)",
    ("Logan", "Wolverine", "85385b35-ba18-4806-950d-4f3d9e7b4a5e.jpg"),
)

cur.execute(
    "INSERT INTO mutantes (nome, codinome, imagem) VALUES (?, ?, ?)",
    ("Scott", "Ciclope", "1d45841c-6a05-449e-bede-d8b15fe3e926.jpg"),
)

connection.commit()
connection.close()
