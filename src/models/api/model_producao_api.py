from typing import Optional
from pydantic import BaseModel, Field


class ProducaoInsert(BaseModel):
    """
    Modelo base para dados para inserção de produção na API.

    Attributes:
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        valor_producao (float, optional): Valor do produção.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    valor_producao: Optional[float] = Field(None, alias="valor_producao")


class ProducaoBase(ProducaoInsert):
    """
    Modelo base para dados base de produção na API.

    Attributes:
        id (int, optional): ID único da entrada.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """
    id: Optional[int] = None
