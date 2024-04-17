import db.models_db as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.database import SessionLocal
from api_interface.models import ExportacaoBase
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


@router.get('/exportacao/filtragem')
async def filtrar_importacao(
        exportacao: ExportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        query = db.query(models.Importacao)

        # Adiciona filtro pelo ID se fornecido
        if exportacao.id is not None:
            query = query.filter(models.Importacao.id == exportacao.id)

        # Adiciona filtro pela categoria se fornecida
        if exportacao.categoria is not None:
            query = query.filter(models.Importacao.categoria == exportacao.categoria)

        # Adiciona filtro pelo nome se fornecido
        if exportacao.nome is not None:
            query = query.filter(models.Importacao.nome == exportacao.nome)

        # Adiciona filtro pelo ano se fornecido
        if exportacao.ano is not None:
            query = query.filter(models.Importacao.ano == exportacao.ano)

        # Adiciona filtro pelo valor de produção se fornecido
        if exportacao.quantidade is not None:
            query = query.filter(models.Importacao.quantidade == exportacao.quantidade)

        # Adiciona filtro pelo valor de produção se fornecido
        if exportacao.valor is not None:
            query = query.filter(models.Importacao.valor == exportacao.valor)

        # Executa a consulta e retorna os resultados
        return query.all()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.get('/exportacao/{id_exportacao}', status_code=status.HTTP_200_OK)
async def importacao_id(
        id_exportacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    exportacao = db.query(models.Exportacao).filter(models.Exportacao.id == id_exportacao).first()

    if exportacao is None:
        HTTPException(status_code=404, detail='id nao encontrado')

    return exportacao

@router.get('/exportacao', status_code=status.HTTP_200_OK)
async def total_importacao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Exportacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")