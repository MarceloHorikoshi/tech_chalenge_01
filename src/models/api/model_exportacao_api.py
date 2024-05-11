from typing import Optional
from pydantic import BaseModel, Field


class ExportacaoInsert(BaseModel):
    """
    Modelo base para dados para inserção de produção na API.

    Attributes:
        categoria (str, optional): Categoria do produto.
        nome (str, optional): Nome do produto.
        ano (str, optional): Ano dos dados.
        quantidade (int, optional): Quantidade exportada.
        valor (float, optional): Valor da exportação.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    quantidade: Optional[int] = Field(None, alias="quantidade")
    valor: Optional[float] = Field(None, alias="valor")


class ExportacaoBase(ExportacaoInsert):
    """
    Modelo base para dados de comercialização na API.

    Attributes:
        id (int, optional): ID único da entrada.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
