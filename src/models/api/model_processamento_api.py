from typing import Optional
from pydantic import BaseModel, Field


class ProcessamentoInsert(BaseModel):
    """
    Modelo base para dados para inserção de produção na API.

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

    categoria: Optional[str] = Field(None, alias="categoria")
    sub_categoria: Optional[str] = Field(None, alias="sub_categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    valor_processamento: Optional[float] = Field(None, alias="valor_processamento")


class ProcessamentoBase(ProcessamentoInsert):
    """
    Modelo base para dados de comercialização na API.

    Attributes:
        id (int, optional): ID único da entrada.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
