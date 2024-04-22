from api.schemas import models_db as models
import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas.models_db import Exportacao
from api.dependencies.database import SessionLocal
from api.schemas.models_api import ExportacaoBase
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


@router.get('/exportacao/{id_exportacao}', status_code=status.HTTP_200_OK)
async def exportacao_id(
        id_exportacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail=os.environ.get('ERRO_401'))

    exportacao = db.query(models.Exportacao).filter(models.Exportacao.id == id_exportacao).first()

    if exportacao is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    return exportacao


@router.get('/exportacao', status_code=status.HTTP_200_OK)
async def total_exportacao(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail=os.environ.get('ERRO_401'))

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Exportacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/exportacao/filtragem')
async def filtrar_exportacao(
        exportacao: ExportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail=os.environ.get('ERRO_401'))

    try:
        query = db.query(models.Exportacao)

        # Adiciona filtro pelo ID se fornecido
        if exportacao.id is not None:
            query = query.filter(models.Exportacao.id == exportacao.id)

        # Adiciona filtro pela categoria se fornecida
        if exportacao.categoria is not None:
            query = query.filter(models.Exportacao.categoria == exportacao.categoria)

        # Adiciona filtro pelo nome se fornecido
        if exportacao.nome is not None:
            query = query.filter(models.Exportacao.nome == exportacao.nome)

        # Adiciona filtro pelo ano se fornecido
        if exportacao.ano is not None:
            query = query.filter(models.Exportacao.ano == exportacao.ano)

        # Adiciona filtro pelo valor de produção se fornecido
        if exportacao.quantidade is not None:
            query = query.filter(models.Exportacao.quantidade == exportacao.quantidade)

        # Adiciona filtro pelo valor de produção se fornecido
        if exportacao.valor is not None:
            query = query.filter(models.Exportacao.valor == exportacao.valor)

        # Executa a consulta e retorna os resultados
        return query.all()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.post('/exportacao', status_code=status.HTTP_201_CREATED)
async def insere_exportacao(
        comercializacao: ExportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=401, detail=erro_401)

    create_exportacao_model = Exportacao(
        categoria=comercializacao.categoria,
        nome=comercializacao.nome,
        ano=comercializacao.ano,
        quantidade=comercializacao.quantidade,
        valor=comercializacao.valor
    )

    db.add(create_exportacao_model)
    db.commit()

    db.refresh(create_exportacao_model)

    return {'id': create_exportacao_model.id}


@router.put('/exportacao/{id_exportacao}', status_code=status.HTTP_204_NO_CONTENT)
async def altera_exportacao(
        id_exportacao: int,
        exportacao: ExportacaoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    exportacao_model = db.query(Exportacao).filter(Exportacao.id == id_exportacao).first()
    if exportacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    # Atualiza os campos do objeto com os novos valores
    exportacao_model.categoria = exportacao.categoria
    exportacao_model.nome = exportacao.nome
    exportacao_model.ano = exportacao.ano
    exportacao_model.quantidade = exportacao.quantidade
    exportacao_model.valor = exportacao.valor

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None


@router.delete('/exportacao/{id_exportacao}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_exportacao(
        id_exportacao: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Exportacao).filter(Exportacao.id == id_exportacao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None
