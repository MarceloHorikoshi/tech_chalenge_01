import db.models_db as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.database import SessionLocal
from api_interface.models import ProducaoBase

from utils.funcionaliades_banco import insercao_dados, limpa_tabela
from utils.tratamento_dados_tabela import transformar_em_formato, dataframe_para_json
from utils.importacao_dados import download_tabela, leitura_bytes


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/producao/filtragem')
async def filtrar_producao(producao: ProducaoBase, db: db_dependency):

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
        resultados = query.all()
        return resultados

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.get('/producao/{id_prod}', status_code=status.HTTP_200_OK)
async def producao_id(id_prod: int, db: db_dependency):

    producao = db.query(models.Producao).filter(models.Producao.id == id_prod).first()

    if producao is None:
        HTTPException(status_code=404, detail='id nao encontrado')

    return producao


@router.get('/producao', status_code=status.HTTP_200_OK)
async def total_producao(db: db_dependency):

    try:
        # retorna todas as linhas da tabela
        producoes = db.query(models.Producao).all()
        return producoes
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")