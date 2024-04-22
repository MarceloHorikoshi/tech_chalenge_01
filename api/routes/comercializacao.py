from api.schemas import models_db as models
import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas.models_db import Comercializacao
from api.dependencies.database import SessionLocal
from api.schemas.models_api import ComercializacaoBase
from api.services.authentication import get_current_user


router = APIRouter()

erro_401 = os.environ.get('ERRO_401')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@router.get('/comercializacao/{id_comercializacao}', status_code=status.HTTP_200_OK)
async def comercializacao_id(
        id_comercializacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    comercializacao = db.query(models.Comercializacao).filter(models.Comercializacao.id == id_comercializacao).first()

    if comercializacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    return comercializacao


@router.get('/comercializacao', status_code=status.HTTP_200_OK)
async def total_comercializacao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)
    try:
        # retorna todas as linhas da tabela
        return db.query(models.Comercializacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/comercializacao/filtragem', status_code=status.HTTP_200_OK)
async def filtrar_comercializacao(
        comercializacao: ComercializacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

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


@router.post('/comercializacao', status_code=status.HTTP_201_CREATED)
async def insere_comercializacao(
        comercializacao: ComercializacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=401, detail=erro_401)

    create_comercializacao_model = Comercializacao(
        categoria=comercializacao.categoria,
        nome=comercializacao.nome,
        ano=comercializacao.ano,
        litros_comercializacao=comercializacao.litros_comercializacao
    )

    db.add(create_comercializacao_model)
    db.commit()

    db.refresh(create_comercializacao_model)

    return {'id': create_comercializacao_model.id}


@router.put('/comercializacao/{id_comercializacao}', status_code=status.HTTP_204_NO_CONTENT)
async def altera_comercializacao(
        id_comercializacao: int,
        comercializacao: ComercializacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Comercializacao).filter(Comercializacao.id == id_comercializacao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    # Atualiza os campos do objeto com os novos valores
    comercializacao_model.categoria = comercializacao.categoria
    comercializacao_model.nome = comercializacao.nome
    comercializacao_model.ano = comercializacao.ano
    comercializacao_model.litros_comercializacao = comercializacao.litros_comercializacao

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None


@router.delete('/comercializacao/{id_comercializacao}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_comercializacao(
        id_comercializacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Comercializacao).filter(Comercializacao.id == id_comercializacao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None

