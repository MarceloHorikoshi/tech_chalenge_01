import db.models_db as models
import pandas as pd

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.database import SessionLocal
from api_interface.models import ComercializacaoBase


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/comercializacao/filtragem')
async def filtrar_comercializacao(comercializacao: ComercializacaoBase, db: db_dependency):
    try:
        query = db.query(models.Comercializacao)

        # Adiciona filtro pelo ID se fornecido
        if comercializacao.id is not None:
            query = query.filter(models.Comercializacao.id == comercializacao.id)

        # Adiciona filtro pela categoria se fornecida
        if comercializacao.categoria is not None:
            query = query.filter(models.Comercializacao.categoria == comercializacao.categoria)

        # Adiciona filtro pelo nome se fornecido
        if comercializacao.nome is not None:
            query = query.filter(models.Comercializacao.nome == comercializacao.nome)

        # Adiciona filtro pelo ano se fornecido
        if comercializacao.ano is not None:
            query = query.filter(models.Comercializacao.ano == comercializacao.ano)

        # Adiciona filtro pelo valor de produção se fornecido
        if comercializacao.litros_comercializacao is not None:
            query = query.filter(models.Comercializacao.litros_comercializacao == comercializacao.litros_comercializacao)

        # Executa a consulta e retorna os resultados
        resultados = query.all()
        return resultados

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de comercializacao")


@router.get('/comercializacao/{id_comercializacao}', status_code=status.HTTP_200_OK)
async def comercializacao_id(id_comercializacao: int, db: db_dependency):
    comercializacao = db.query(models.Comercializacao).filter(models.Comercializacao.id == id_comercializacao).first()

    if comercializacao is None:
        HTTPException(status_code=404, detail='id nao encontrado')

    return comercializacao


@router.get('/comercializacao', status_code=status.HTTP_200_OK)
async def total_comercializacao(db: db_dependency):
    try:
        # retorna todas as linhas da tabela
        producoes = db.query(models.Comercializacao).all()
        return producoes
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")
