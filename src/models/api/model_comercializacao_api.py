from typing import Optional
from pydantic import BaseModel, Field


class ComercializacaoInsert(BaseModel):
    """
    Modelo base para dados para inserção de produção na API.

    Attributes:
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        litros_comercializacao (float, optional): Quantidade de litros comercializados.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    litros_comercializacao: Optional[float] = Field(None, alias="litros_comercializacao")


class ComercializacaoBase(ComercializacaoInsert):
    """
    Modelo base para dados de comercialização na API.

    Attributes:
        id (int, optional): ID único da entrada.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
