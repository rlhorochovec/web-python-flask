DROP TABLE IF EXISTS mutantes;

CREATE TABLE mutantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    codinome TEXT NOT NULL,
    imagem TEXT
);