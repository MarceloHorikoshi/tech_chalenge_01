import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas import models_db as models
from api.schemas.models_db import Producao
from api.dependencies.database import SessionLocal
from api.schemas.models_api import ProducaoBase
from api.services.authentication import get_current_user


router = APIRouter(
    tags=['Producao'],
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


@router.get('/producao/{id_prod}', status_code=status.HTTP_200_OK)
async def producao_id(
        id_prod: int,
        db: db_dependency
):
    """
    Obtém um item da tabela de producao pelo ID.

    Args:
        id_process (int): O ID de producao.
        db: Sessão do banco de dados.

    Returns:
        Exportação: O objeto Exportacao correspondente ao ID,
            ou gera HTTP_404_NOT_FOUND se não encontrado.
    """

    producao = db.query(models.Producao).filter(models.Producao.id == id_prod).first()

    if producao is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    return producao


@router.get('/producao', status_code=status.HTTP_200_OK)
async def total_producao(
        db: db_dependency
):
    """
    Obtém todos os dados da tabela de producao.

    Args:
        db: Sessão do banco de dados.

    Returns:
        list[Producao]: Uma lista de objetos Producao.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao obter os dados.
    """

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
        db: db_dependency
):
    """
    Filtra dados da tabela de producao com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        producao (ProducaoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * id (int, optional): ID único da entrada.
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * valor_producao (float, optional): Valor de producao.
        db: Sessão do banco de dados.

    Returns:
        list[Producao]: Uma lista de objetos Producao que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

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
        db: db_dependency
):
    """
    Insere dados da tabela de producao com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        producao (ProducaoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * valor_producao (float, optional): Valor de producao.
        db: Sessão do banco de dados.

    Returns:
        list[Producao]: Uma lista de objetos Producao que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

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
        db: db_dependency
):
    """
    Altera os dados referentes a um item existente na tabela de producao.

    Args:
        id_producao (int): O ID da producao a ser alterada.
        producao (ProducaoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * valor_producao (float, optional): Valor de producao.
        db: Sessão do banco de dados.

    Returns:
        list[Producao]: lista de objetos Producao que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

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
        db: db_dependency
):
    """
    Deleta um item da tabela de producao pelo ID.

    Args:
        id_producao (int): O ID da producao a ser deletada.
        db: Sessão do banco de dados.

    Returns:
        None: Retorna um status HTTP 204 No Content em caso de sucesso.

    Raises:
        HTTPException: Com status code 404 Not Found se o processamento não for encontrado.
    """

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Producao).filter(Producao.id == id_producao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None
