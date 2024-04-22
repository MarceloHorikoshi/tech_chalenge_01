import os
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas import models_db as models
from api.schemas.models_db import Processamento
from api.dependencies.database import SessionLocal
from api.schemas.models_api import ProcessamentoBase
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


@router.get('/processamento/{id_process}', status_code=status.HTTP_200_OK)
async def processamento_id(
        id_process: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

    processamento = db.query(models.Processamento).filter(models.Processamento.id == id_process).first()

    if processamento is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    return processamento


@router.get('/processamento', status_code=status.HTTP_200_OK)
async def total_processamento(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Processamento).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/processamento/filtragem')
async def filtrar_processamento(
        processamento: ProcessamentoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Falha autentificacao')

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


@router.post('/processamento', status_code=status.HTTP_201_CREATED)
async def insere_processamento(
        processamento: ProcessamentoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=401, detail=erro_401)

    create_processamento_model = Processamento(
        categoria=processamento.categoria,
        sub_categoria=processamento.sub_categoria,
        nome=processamento.nome,
        ano=processamento.ano,
        valor_producao=processamento.valor_producao
    )

    db.add(create_processamento_model)
    db.commit()

    db.refresh(create_processamento_model)

    return {'id': create_processamento_model.id}


@router.put('/processamento/{id_processamento}', status_code=status.HTTP_204_NO_CONTENT)
async def altera_processamento(
        id_processamento: int,
        processamento: ProcessamentoBase,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    processamento_model = db.query(Processamento).filter(Processamento.id == id_processamento).first()
    if processamento_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    # Atualiza os campos do objeto com os novos valores
    processamento_model.categoria = processamento.categoria
    processamento_model.sub_categoria = processamento.sub_categoria
    processamento_model.nome = processamento.nome
    processamento_model.ano = processamento.ano
    processamento_model.valor_producao = processamento.valor_producao

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None


@router.delete('/processamento/{id_processamento}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_processamento(
        id_processamento: int,
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=erro_401)

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Processamento).filter(Processamento.id == id_processamento).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None

