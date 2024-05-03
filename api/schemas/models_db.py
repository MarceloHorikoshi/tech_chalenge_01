from sqlalchemy import Column, Integer, String, Float
from api.dependencies.database import Base


class Comercializacao(Base):
    """
    Modelo de dados para a tabela 'comercializacao', representando dados de comercialização de produtos.

    Attributes:
        id (int): ID único da entrada.
        categoria (str): Categoria do produto.
        nome (str): Nome do produto.
        ano (str): Ano dos dados.
        litros_comercializacao (float): Quantidade de litros comercializados.
    """

    __tablename__ = 'comercializacao'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    litros_comercializacao = Column(Float(50, 2))


class Exportacao(Base):
    """
    Modelo de dados para a tabela 'exportacao', representando dados de exportação de produtos.

    Atributos:
        id (int): ID único da entrada.
        categoria (str): Categoria do produto.
        nome (str): Nome do produto.
        ano (str): Ano dos dados.
        quantidade (int): Quantidade exportada.
        valor (float): Valor da exportação.
    """

    __tablename__ = 'exportacao'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    quantidade = Column(Integer)
    valor = Column(Float(50, 2))


class Importacao(Base):
    """
    Modelo de dados para a tabela 'importacao', representando dados de exportação de produtos.

    Atributos:
        id (int): ID único da entrada.
        categoria (str): Categoria do produto.
        nome (str): Nome do produto.
        ano (str): Ano dos dados.
        quantidade (int): Quantidade exportada.
        valor (float): Valor da exportação.
    """

    __tablename__ = 'importacao'
    id: int = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    quantidade = Column(Integer)
    valor = Column(Float(50, 2))


class Processamento(Base):
    """
    Modelo de dados para a tabela 'processamento', representando dados de exportação de produtos.

    Atributos:
        id (int): ID único da entrada.
        categoria (str): Categoria do produto.
        sub_categoria (str): Sub_categoria do produto.
        nome (str): Nome do produto.
        ano (str): Ano dos dados.
        valor_producao (float): Valor do processamento.
    """

    __tablename__ = 'processamento'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    sub_categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    valor_processamento = Column(Float(50, 2))


class Producao(Base):
    """
    Modelo de dados para a tabela 'producao', representando dados de exportação de produtos.

    Atributos:
        id (int): ID único da entrada.
        categoria (str): Categoria do produto.
        nome (str): Nome do produto.
        ano (str): Ano dos dados.
        valor_producao (float): Valor da produção.
    """

    __tablename__ = 'producao'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    valor_producao = Column(Float(50, 2))


class User(Base):
    """
    Modelo de dados para a tabela 'comercializacao', representando dados de comercialização de produtos.

    Attributes:
        id (int): ID único da entrada.
        categoria (str): Categoria do produto.
        nome (str): Nome do produto.
        ano (str): Ano dos dados.
        litros_comercializacao (float): Quantidade de litros comercializados.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    username = Column(String(50), unique=True)
    hashed_password = Column(String(100))
