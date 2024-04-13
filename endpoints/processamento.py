import db.models_db as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.database import SessionLocal
from api_interface.models import ProcessamentoBase


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/processamento/filtragem')
async def filtrar_processamento(processamento: ProcessamentoBase, db: db_dependency):

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
        resultados = query.all()
        return resultados

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.get('/processamento/{id_process}', status_code=status.HTTP_200_OK)
async def processamento_id(id_process: int, db: db_dependency):

    processamento = db.query(models.Processamento).filter(models.Processamento.id == id_process).first()

    if processamento is None:
        HTTPException(status_code=404, detail='id nao encontrado')

    return processamento

@router.get('/processamento', status_code=status.HTTP_200_OK)
async def total_processamento(db: db_dependency):

    try:
        # retorna todas as linhas da tabela
        processamento = db.query(models.Processamento).all()
        return processamento
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")