from pydantic import BaseModel, Field
from typing import Optional


class ComercializacaoBase(BaseModel):
    """
    Modelo base para dados de comercialização na API.

    Attributes:
        id (int, optional): ID único da entrada.
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        litros_comercializacao (float, optional): Quantidade de litros comercializados.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    litros_comercializacao: Optional[float] = Field(None, alias="litros_comercializacao")


class ExportacaoBase(BaseModel):
    """
    Modelo base para dados de exportação na API.

    Attributes:
        id (int, optional): ID único da entrada.
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        quantidade (int, optional): Quantidade exportada.
        valor (float, optional): Valor da exportação.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    quantidade: Optional[int] = Field(None, alias="quantidade")
    valor: Optional[float] = Field(None, alias="valor")


class ImportacaoBase(BaseModel):
    """
    Modelo base para dados de importação na API.

    Attributes:
        id (int, optional): ID único da entrada.
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        quantidade (int, optional): Quantidade importação.
        valor (float, optional): Valor da importação.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    quantidade: Optional[int] = Field(None, alias="quantidade")
    valor: Optional[float] = Field(None, alias="valor")


class ProcessamentoBase(BaseModel):
    """
    Modelo base para dados de processamento na API.

    Attributes:
        id (int, optional): ID único da entrada.
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        quantidade (int, optional): Quantidade processamento.
        valor_producao (float, optional): Valor do processamento.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    sub_categoria: Optional[str] = Field(None, alias="sub_categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    valor_processamento: Optional[float] = Field(None, alias="valor_processamento")


class ProducaoBase(BaseModel):
    """
    Modelo base para dados de produção na API.

    Attributes:
        id (int, optional): ID único da entrada.
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        quantidade (int, optional): Quantidade produção.
        valor_producao (float, optional): Valor do produção.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    valor_producao: Optional[float] = Field(None, alias="valor_producao")


# Authentication
class CreateUserRequest(BaseModel):
    """
    Modelo para requisições de criação de usuário.

    Attributes:
        username (str): Nome de usuário.
        password (str): Senha do usuário.
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Modelo para representar um token de acesso.

    Attributes:
        access_token (str): O token de acesso.
        token_type (str): O tipo de token (e.g., "bearer").
    """

    access_token: str
    token_type: str

