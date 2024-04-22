import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas import models_db as models
from api.schemas.models_db import Producao
from api.dependencies.database import SessionLocal
from api.schemas.models_api import ProducaoBase
from api.services.authentication import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


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
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    return producao


@router.get('/producao', status_code=status.HTTP_200_OK)
async def total_producao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

    try:
        # retorna todas as linhas da tabela
        producoes = db.query(models.Producao).all()
        return producoes
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/producao/filtragem')
async def filtrar_producao(
        producao: ProducaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

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


@router.post('/producao', status_code=status.HTTP_201_CREATED)
async def insere_producao(
        producao: ProducaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=401, detail=erro_401)

    create_producao_model = Producao(
        categoria=producao.categoria,
        nome=producao.nome,
        ano=producao.ano,
        valor_producao=producao.valor_producao
    )

    db.add(create_producao_model)
    db.commit()

    db.refresh(create_producao_model)

    return {'id': create_producao_model.id}


@router.put('/producao/{id_producao}', status_code=status.HTTP_204_NO_CONTENT)
async def altera_producao(
        id_producao: int,
        producao: ProducaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    producao_model = db.query(Producao).filter(Producao.id == id_producao).first()
    if producao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    # Atualiza os campos do objeto com os novos valores
    producao_model.categoria = producao.categoria
    producao_model.nome = producao.nome
    producao_model.ano = producao.ano
    producao_model.valor_producao = producao.valor_producao

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None


@router.delete('/producao/{id_producao}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_producao(
        id_producao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Producao).filter(Producao.id == id_producao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None
