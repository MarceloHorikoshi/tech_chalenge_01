from sqlalchemy import Column, Integer, String, Float
from api.schemas.database import Base


class Comercializacao(Base):
    __tablename__ = 'comercializacao'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    litros_comercializacao = Column(Float(50, 2))


class Exportacao(Base):
    __tablename__ = 'exportacao'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    quantidade = Column(Integer)
    valor = Column(Float(50, 2))


class Importacao(Base):
    __tablename__ = 'importacao'
    id: int = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    # id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    quantidade = Column(Integer)
    valor = Column(Float(50, 2))


class Processamento(Base):
    __tablename__ = 'processamento'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    sub_categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    valor_producao = Column(Float(50, 2))


class Producao(Base):
    __tablename__ = 'producao'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    valor_producao = Column(Float(50, 2))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    username = Column(String(50), unique=True)
    hashed_password = Column(String(100))
