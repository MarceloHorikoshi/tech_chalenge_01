import os

from api.schemas import models_db as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas.models_db import Importacao
from api.dependencies.database import SessionLocal
from api.schemas.models_api import ImportacaoBase
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


@router.get('/importacao/{id_importacao}', status_code=status.HTTP_200_OK)
async def importacao_id(
        id_importacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

    importacao = db.query(models.Importacao).filter(models.Importacao.id == id_importacao).first()

    if importacao is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    return importacao


@router.get('/importacao', status_code=status.HTTP_200_OK)
async def total_importacao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Importacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/importacao/filtragem')
async def filtrar_importacao(
        importacao: ImportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

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


@router.post('/importacao', status_code=status.HTTP_201_CREATED)
async def insere_importacao(
        comercializacao: ImportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=401, detail=erro_401)

    create_importacao_model = Importacao(
        categoria=comercializacao.categoria,
        nome=comercializacao.nome,
        ano=comercializacao.ano,
        quantidade=comercializacao.quantidade,
        valor=comercializacao.valor
    )

    db.add(create_importacao_model)
    db.commit()

    db.refresh(create_importacao_model)

    return {'id': create_importacao_model.id}


@router.put('/importacao/{id_importacao}', status_code=status.HTTP_204_NO_CONTENT)
async def altera_importacao(
        id_importacao: int,
        importacao: ImportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    importacao_model = db.query(Importacao).filter(Importacao.id == id_importacao).first()
    if importacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    # Atualiza os campos do objeto com os novos valores
    importacao_model.categoria = importacao.categoria
    importacao_model.nome = importacao.nome
    importacao_model.ano = importacao.ano
    importacao_model.quantidade = importacao.quantidade
    importacao_model.valor = importacao.valor

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None


@router.delete('/importacao/{id_importacao}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_importacao(
        id_importacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Importacao).filter(Importacao.id == id_importacao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None
