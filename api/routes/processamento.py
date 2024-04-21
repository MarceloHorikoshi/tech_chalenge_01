from api import schemas as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas.database import SessionLocal
from api.schemas.models_api import ProcessamentoBase
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


@router.post('/processamento/filtragem')
async def filtrar_processamento(
        processamento: ProcessamentoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        query = db.query(models.Processamento)

        # Adiciona filtro pelo ID se fornecido
        if processamento.id is not None:
            query = query.filter(models.Processamento.id == processamento.id)

        # Adiciona filtro pela categoria se fornecida
        if processamento.categoria is not None:
            query = query.filter(models.Processamento.categoria == processamento.categoria)

        # Adiciona filtro pela sub_categoria se fornecido
        if processamento.sub_categoria is not None:
            query = query.filter(models.Processamento.sub_categoria == processamento.sub_categoria)

        # Adiciona filtro pelo nome se fornecido
        if processamento.nome is not None:
            query = query.filter(models.Processamento.nome == processamento.nome)

        # Adiciona filtro pelo ano se fornecido
        if processamento.ano is not None:
            query = query.filter(models.Processamento.ano == processamento.ano)

        # Adiciona filtro pelo valor de produção se fornecido
        if processamento.valor_producao is not None:
            query = query.filter(models.Processamento.valor_producao == processamento.valor_producao)

        # Executa a consulta e retorna os resultados
        return query.all()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.get('/processamento/{id_process}', status_code=status.HTTP_200_OK)
async def processamento_id(
        id_process: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    processamento = db.query(models.Processamento).filter(models.Processamento.id == id_process).first()

    if processamento is None:
        raise HTTPException(status_code=404, detail='id nao encontrado')

    return processamento


@router.get('/processamento', status_code=status.HTTP_200_OK)
async def total_processamento(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Processamento).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")
