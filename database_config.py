from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Mutante(Base):
   __tablename__ = 'mutantes'
   id = Column(Integer, primary_key=True)
   nome = Column(String(250))
   codinome = Column(String(250))
   imagem = Column(String(250))

engine = create_engine('sqlite:///database/xmen97.db')

Base.metadata.create_all(engine)