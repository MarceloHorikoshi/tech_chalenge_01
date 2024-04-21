from api import schemas as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas.database import SessionLocal
from api.schemas.models_api import ProducaoBase
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


@router.post('/producao/filtragem')
async def filtrar_producao(
        producao: ProducaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        query = db.query(models.Producao)

        # Adiciona filtro pelo ID se fornecido
        if producao.id is not None:
            query = query.filter(models.Producao.id == producao.id)

        # Adiciona filtro pela categoria se fornecida
        if producao.categoria is not None:
            query = query.filter(models.Producao.categoria == producao.categoria)

        # Adiciona filtro pelo nome se fornecido
        if producao.nome is not None:
            query = query.filter(models.Producao.nome == producao.nome)

        # Adiciona filtro pelo ano se fornecido
        if producao.ano is not None:
            query = query.filter(models.Producao.ano == producao.ano)

        # Adiciona filtro pelo valor de produção se fornecido
        if producao.valor_producao is not None:
            query = query.filter(models.Producao.valor_producao == producao.valor_producao)

        # Executa a consulta e retorna os resultados
        return query.all()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.get('/producao/{id_prod}', status_code=status.HTTP_200_OK)
async def producao_id(
        id_prod: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    producao = db.query(models.Producao).filter(models.Producao.id == id_prod).first()

    if producao is None:
        raise HTTPException(status_code=404, detail='id nao encontrado')

    return producao


@router.get('/producao', status_code=status.HTTP_200_OK)
async def total_producao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        # retorna todas as linhas da tabela
        producoes = db.query(models.Producao).all()
        return producoes
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")