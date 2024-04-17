import db.models_db as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.database import SessionLocal
from api_interface.models import ImportacaoBase
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


@router.get('/importacao/filtragem')
async def filtrar_importacao(
        importacao: ImportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        query = db.query(models.Importacao)

        # Adiciona filtro pelo ID se fornecido
        if importacao.id is not None:
            query = query.filter(models.Importacao.id == importacao.id)

        # Adiciona filtro pela categoria se fornecida
        if importacao.categoria is not None:
            query = query.filter(models.Importacao.categoria == importacao.categoria)

        # Adiciona filtro pelo nome se fornecido
        if importacao.nome is not None:
            query = query.filter(models.Importacao.nome == importacao.nome)

        # Adiciona filtro pelo ano se fornecido
        if importacao.ano is not None:
            query = query.filter(models.Importacao.ano == importacao.ano)

        # Adiciona filtro pelo valor de produção se fornecido
        if importacao.quantidade is not None:
            query = query.filter(models.Importacao.quantidade == importacao.quantidade)

        # Adiciona filtro pelo valor de produção se fornecido
        if importacao.valor is not None:
            query = query.filter(models.Importacao.valor == importacao.valor)

        # Executa a consulta e retorna os resultados
        return query.all()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.get('/importacao/{id_importacao}', status_code=status.HTTP_200_OK)
async def importacao_id(
        id_importacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    importacao = db.query(models.Importacao).filter(models.Importacao.id == id_importacao).first()

    if importacao is None:
        HTTPException(status_code=404, detail='id nao encontrado')

    return importacao


@router.get('/importacao', status_code=status.HTTP_200_OK)
async def total_importacao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Importacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")