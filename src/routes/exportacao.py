from src.models import models_db as models
import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from src.models.models_db import Exportacao
from src.dependencies.database import SessionLocal
from src.models.api.model_exportacao_api import ExportacaoBase, ExportacaoInsert
from src.services.authentication import get_current_user


router = APIRouter(
    tags=['Exportacao'],
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


@router.get('/exportacao/{id_exportacao}', status_code=status.HTTP_200_OK)
async def exportacao_id(
        id_exportacao: int,
        db: db_dependency
):
    """
    Obtém um item da tabela de exportacao pelo ID.

    Args:
        id_exportacao (int): O ID da exportacao.
        db: Sessão do banco de dados.

    Returns:
        Exportação: O objeto Exportacao correspondente ao ID,
            ou gera HTTP_404_NOT_FOUND se não encontrado.
    """

    exportacao = db.query(models.Exportacao).filter(models.Exportacao.id == id_exportacao).first()

    if exportacao is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    return exportacao


@router.get('/exportacao', status_code=status.HTTP_200_OK)
async def total_exportacao(
        db: db_dependency
):
    """
    Obtém todos os dados da tabela de exportacao.

    Args:
        db: Sessão do banco de dados.

    Returns:
        list[Exportacao]: Uma lista de objetos Exportacao.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao obter os dados.
    """

    try:
        # retorna todas as linhas da tabela
        return db.query(models.Exportacao).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/exportacao/filtragem')
async def filtrar_exportacao(
        exportacao: ExportacaoBase,
        db: db_dependency
):
    """
    Filtra dados da tabela de exportacao com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        exportacao (ExportacaoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * id (int, optional): ID único da entrada.
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * quantidade (float, optional): Quantidade exportada.
            * valor (float, optional): Valor exportado.
        db: Sessão do banco de dados.

    Returns:
        list[Exportacao]: Uma lista de objetos Exportacao que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

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
        comercializacao: ExportacaoInsert,
        db: db_dependency
):

    """
    Insere dados da tabela de exportacao com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        exportacao (ExportacaoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * quantidade (float, optional): Quantidade exportada.
            * quantidade (float, optional): Valor exportado.
        db: Sessão do banco de dados.

    Returns:
        list[Exportacao]: Uma lista de objetos Exportacao que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """


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
        exportacao: ExportacaoInsert,
        db: db_dependency
):
    """
    Altera os dados referentes a um item existente na tabela de exportacao.

    Args:
        id_exportacao (int): O ID da exportacao a ser alterada.
        exportacao (ExportacaoBase): Objeto com os critérios de filtro.
            Os campos disponíveis para filtro são:
            * categoria (str, optional): Categoria do produto.
            * nome (str, optional): Nome do produto.
            * ano (str, optional): Ano dos dados.
            * quantidade (float, optional): Quantidade exportada.
            * quantidade (float, optional): Valor exportado.
        db: Sessão do banco de dados.

    Returns:
        list[Exportacao]: Uma lista de objetos Exportacao que correspondem aos filtros.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao filtrar os dados.
    """

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
        db: db_dependency
):
    """
    Deleta um item da tabela de exportacao pelo ID.

    Args:
        id_exportacao (int): O ID da exportacao a ser deletada.
        db: Sessão do banco de dados.

    Returns:
        None: Retorna um status HTTP 204 No Content em caso de sucesso.

    Raises:
        HTTPException: Com status code 404 Not Found se a exportacao não for encontrada.
    """

    # Busca o item no banco de dados pelo ID
    comercializacao_model = db.query(Exportacao).filter(Exportacao.id == id_exportacao).first()
    if comercializacao_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(comercializacao_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None
