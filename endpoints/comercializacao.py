import db.models_db as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.database import SessionLocal
from api_interface.models import ComercializacaoBase
from utils.authentication import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@router.get('/comercializacao/filtragem')
async def filtrar_comercializacao(
        comercializacao: ComercializacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

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
        return query.all()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de comercializacao")


@router.get('/comercializacao/{id_comercializacao}', status_code=status.HTTP_200_OK)
async def comercializacao_id(
        id_comercializacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    comercializacao = db.query(models.Comercializacao).filter(models.Comercializacao.id == id_comercializacao).first()

    if comercializacao is None:
        HTTPException(status_code=404, detail='id nao encontrado')

    return comercializacao


@router.get('/comercializacao', status_code=status.HTTP_200_OK)
async def total_comercializacao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')
    try:
        # retorna todas as linhas da tabela
        return db.query(models.Comercializacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")
