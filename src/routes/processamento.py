import os
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from src.models import models_db as models
from src.models.models_db import Processamento
from src.dependencies.database import SessionLocal
from src.models.api.model_processamento_api import ProcessamentoBase, ProcessamentoInsert
from src.services.authentication import get_current_user


router = APIRouter(
    tags=['Processamento'],
    dependencies=[Depends(get_current_user)],
    responses={401: {'detail': os.environ.get('ERRO_401')}}
)


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
        db: db_dependency
):
    """
    Obtém um item da tabela de processamento pelo ID.

    Args:
        id_process (int): O ID do processamento.
        db: Sessão do banco de dados.

    Returns:
        Exportação: O objeto Exportacao correspondente ao ID,
            ou gera HTTP_404_NOT_FOUND se não encontrado.
    """

    processamento = db.query(models.Processamento).filter(models.Processamento.id == id_process).first()

    if processamento is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    return processamento


@router.get('/processamento', status_code=status.HTTP_200_OK)
async def total_processamento(
        db: db_dependency
):
    """
    Obtém todos os dados da tabela de processamento.

    Args:
        db: Sessão do banco de dados.

    Returns:
        list[Processamento]: Uma lista de objetos Processamento.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao obter os dados.
    """

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Processamento).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/processamento/filtragem')
async def filtrar_processamento(
        processamento: ProcessamentoBase,
        db: db_dependency
):
    """
    Filtra dados da tabela de processamento com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        processamento (ProcessamentoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * id (int, optional): ID único da entrada.
            * categoria (str, optional): Categoria do produto.
            * sub_categoria  (str, optional): Sub_categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * valor_processamento (float, optional): Valor processado.
        db: Sessão do banco de dados.

    Returns:
        list[Processamento]: Uma lista de objetos Processamento que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

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
            query = query.filter(models.Processamento.valor_processamento == processamento.valor_processamento)

        # Executa a consulta e retorna os resultados
        return query.all()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao filtrar os dados de produção")


@router.post('/processamento', status_code=status.HTTP_201_CREATED)
async def insere_processamento(
        processamento: ProcessamentoInsert,
        db: db_dependency
):
    """
    Insere dados da tabela de processamento com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        processamento (ProcessamentoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * categoria (str, optional): Categoria do produto.
            * sub_categoria  (str, optional): Sub_categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * valor_processamento (float, optional): Valor processado.
        db: Sessão do banco de dados.

    Returns:
        list[Processamento]: Uma lista de objetos Processamento que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

    create_processamento_model = Processamento(
        categoria=processamento.categoria,
        sub_categoria=processamento.sub_categoria,
        nome=processamento.nome,
        ano=processamento.ano,
        valor_processamento=processamento.valor_processamento
    )

    db.add(create_processamento_model)
    db.commit()

    db.refresh(create_processamento_model)

    return {'id': create_processamento_model.id}


@router.put('/processamento/{id_processamento}', status_code=status.HTTP_204_NO_CONTENT)
async def altera_processamento(
        id_processamento: int,
        processamento: ProcessamentoInsert,
        db: db_dependency
):
    """
    Altera os dados referentes a um item existente na tabela de processamento.

    Args:
        id_processamento (int): O ID do processamento a ser alterado.
        processamento (ProcessamentoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * categoria (str, optional): Categoria do produto.
            * sub_categoria  (str, optional): Sub_categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * valor_processamento (float, optional): Valor processado.
        db: Sessão do banco de dados.

    Returns:
        list[Processamento]: lista de objetos Processamento que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """


    # Busca o item no banco de dados pelo ID
    processamento_model = db.query(Processamento).filter(Processamento.id == id_processamento).first()
    if processamento_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    # Atualiza os campos do objeto com os novos valores
    processamento_model.categoria = processamento.categoria
    processamento_model.sub_categoria = processamento.sub_categoria
    processamento_model.nome = processamento.nome
    processamento_model.ano = processamento.ano
    processamento_model.valor_processamento = processamento.valor_processamento

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None


@router.delete('/processamento/{id_processamento}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_processamento(
        id_processamento: int,
        db: db_dependency
):

    """
    Deleta um item da tabela de processamento pelo ID.

    Args:
        id_processamento (int): O ID do processamento a ser deletada.
        db: Sessão do banco de dados.

    Returns:
        None: Retorna um status HTTP 204 No Content em caso de sucesso.

    Raises:
        HTTPException: Com status code 404 Not Found se o processamento não for encontrado.
    """

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Processamento).filter(Processamento.id == id_processamento).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None

