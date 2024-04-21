from pydantic import BaseModel, Field
from typing import Optional


class ComercializacaoBase(BaseModel):

    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    litros_comercializacao: Optional[float] = Field(None, alias="litros_comercializacao")


class ExportacaoBase(BaseModel):
    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    quantidade: Optional[int] = Field(None, alias="quantidade")
    valor: Optional[float] = Field(None, alias="valor")


class ImportacaoBase(BaseModel):
    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    quantidade: Optional[int] = Field(None, alias="quantidade")
    valor: Optional[float] = Field(None, alias="valor")


class ProcessamentoBase(BaseModel):
    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    sub_categoria: Optional[str] = Field(None, alias="sub_categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    valor_producao: Optional[float] = Field(None, alias="valor_producao")


class ProducaoBase(BaseModel):
    id: Optional[int] = None
    categoria: Optional[str] = Field(None, alias="categoria")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    valor_producao: Optional[float] = Field(None, alias="valor_producao")


# Authentication
class UserBase(BaseModel):
    username: str


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

