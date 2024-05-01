from api.schemas import models_db as models
import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas.models_db import Comercializacao
from api.dependencies.database import SessionLocal
from api.schemas.models_api import ComercializacaoBase
from api.services.authentication import get_current_user

from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    tags=['Comercializacao'],
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


@router.get('/comercializacao/{id_comercializacao}', status_code=status.HTTP_200_OK)
async def comercializacao_id(
        id_comercializacao: int,
        db: db_dependency
):
    """
    Obtém um item da tabela de comercializacao pelo ID.

    Args:
        id_comercializacao (int): O ID da comercializacao.
        db: Sessão do banco de dados.

    Returns:
        Comercializacao: O objeto Comercializacao correspondente ao ID,
            ou gera HTTP_404_NOT_FOUND se não encontrado.
    """

    comercializacao = db.query(models.Comercializacao).filter(models.Comercializacao.id == id_comercializacao).first()

    if comercializacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    return comercializacao


@router.get('/comercializacao', status_code=status.HTTP_200_OK)
async def total_comercializacao(db: db_dependency):
    """
    Obtém todos os dados da tabela de comercializacao.

    Args:
        db: Sessão do banco de dados.

    Returns:
        list[Comercializacao]: Uma lista de objetos Comercializacao.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao obter os dados.
    """
    try:
        # retorna todas as linhas da tabela
        return db.query(models.Comercializacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/comercializacao/filtragem', status_code=status.HTTP_200_OK)
async def filtrar_comercializacao(
        comercializacao: ComercializacaoBase,
        db: db_dependency
):
    """
    Filtra dados da tabela de comercializacao com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        comercializacao (ComercializacaoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * id (int, optional): ID único da entrada.
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * litros_comercializacao (float, optional): Quantidade de litros comercializados.
        db: Sessão do banco de dados.

    Returns:
        list[Comercializacao]: Uma lista de objetos Comercializacao que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

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
        db: db_dependency
):
    """
    Insere dados de na tabela de comercializacao com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        comercializacao (ComercializacaoBase): Objeto com os critérios de filtro.
            Os campos para inserção são:
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * litros_comercializacao (float, optional): Quantidade de litros comercializados.
        db: Sessão do banco de dados.

    Returns:
        ID[int]: Retorna o ID inserido.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao inserir os dados.
    """

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
        db: db_dependency
):
    """
    Altera os dados referentes a um item existente na tabela de comercializacao.
    Args:
        id_comercializacao (int): O ID da comercializacao a ser alterada.
        comercializacao (ComercializacaoBase): Objeto com os novos dados da comercializacao.
            Os campos que podem ser alterados são:
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * litros_comercializacao (float, optional): Quantidade de litros comercializados.
        db: Sessão do banco de dados.

    Returns:
        None: Retorna um status HTTP 204 No Content em caso de sucesso.

    Raises:
        HTTPException: Com status code 404 Not Found se a comercializacao não for encontrada.
    """
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
        db: db_dependency
):
    """
    Deleta um item da tabela de comercializacao pelo ID.

    Args:
        id_comercializacao (int): O ID da comercializacao a ser deletada.
        db: Sessão do banco de dados.

    Returns:
        None: Retorna um status HTTP 204 No Content em caso de sucesso.

    Raises:
        HTTPException: Com status code 404 Not Found se a comercializacao não for encontrada.
    """

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Comercializacao).filter(Comercializacao.id == id_comercializacao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None

