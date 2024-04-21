from api import schemas as models
import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.schemas.database import SessionLocal

from utils.authentication import get_current_user
from utils.funcionaliades_banco import insercao_dados, limpa_tabela
from utils.tratamento_dados_tabela import transformar_em_formato, dataframe_para_json
from api.dependencies.importacao_dados import download_tabela, leitura_bytes
from utils.tratamento_dados_tabela import trata_df_sem_colunas

from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


class Inicializacao:

    def __init__(
            self,
            nome_tabela,
            nome_coluna,
            drop_column,
            lista_links,
            separador,
    ):
        self.nome_tabela = nome_tabela
        self.nome_coluna = nome_coluna
        self.drop_column = drop_column
        self.lista_links = lista_links
        self.separador = separador

    def insercoes(self, db):

        limpa_tabela(db, self.nome_tabela)

        for link in self.lista_links:
            df = leitura_bytes(
                download_tabela(url=link['url']),
                separador=self.separador,
                nome_tabela=self.nome_tabela
            )

            if not df.empty:
                if self.drop_column is not None:
                    df.drop(columns=[self.drop_column], inplace=True)

                if self.nome_tabela == 'processamento':
                    df.replace({'nd': 0, '*': 0}, inplace=True)

                if self.nome_tabela == 'comercializacao':
                    novas_colunas = ['id', 'produto_lixo', 'produto']

                    df = trata_df_sem_colunas(
                        df=df,
                        novas_colunas=novas_colunas,
                        coluna_eliminar='produto_lixo',
                        coluna_principal=self.nome_coluna
                    )

                if self.nome_tabela == 'exportacao' or self.nome_tabela == 'importacao':
                    dict_final = dataframe_para_json(dataframe=df)
                else:
                    dict_final = transformar_em_formato(
                        json_dados=dataframe_para_json(dataframe=df),
                        nome_coluna=self.nome_coluna
                    )

                insercao_dados(
                    db=db,
                    dict_final=dict_final,
                    coluna=self.nome_coluna,
                    tabela=self.nome_tabela,
                    super_categoria=link['super_categoria']
                )


@router.get('/inicializacao', status_code=status.HTTP_201_CREATED)
async def total_processamento(
        db: db_dependency,
        user: models.User = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Falha autentificacao')
    try:
        lista_json_insercao = [

            {
                'nome_tabela': 'comercializacao',
                'nome_coluna': 'produto',
                'drop_table': None,
                'lista_links': [
                    {'super_categoria': None, 'url': os.environ.get('URL_COMERCIALIZACAO')},
                ],
                'separador': ';'
            },
            {
                'nome_tabela': 'exportacao',
                'nome_coluna': 'pais',
                'drop_table': None,
                'lista_links': [
                    {'super_categoria': 'Vinho_Mesa', 'url': os.environ.get('URL_EXPORTACAO_VINHOS_MESA')},
                    {'super_categoria': 'Espumante', 'url': os.environ.get('URL_EXPORTACAO_ESPUMANTE')},
                    {'super_categoria': 'Uvas_frescas', 'url': os.environ.get('URL_EXPORTACAO_UVAS_FRESCAS')},
                    {'super_categoria': 'Suco_uva', 'url': os.environ.get('URL_EXPORTACAO_SUCO_UVA')},
                ],
                'separador': ';'
            },
            {
                'nome_tabela': 'importacao',
                'nome_coluna': 'pais',
                'drop_table': None,
                'lista_links': [
                    {'super_categoria': 'Vinho_Mesa', 'url': os.environ.get('URL_IMPORTACAO_VINHOS_MESA')},
                    {'super_categoria': 'Espumante', 'url': os.environ.get('URL_IMPORTACAO_ESPUMANTE')},
                    {'super_categoria': 'Uvas_frescas', 'url': os.environ.get('URL_IMPORTACAO_UVAS_FRESCAS')},
                    {'super_categoria': 'Uvas_passas', 'url': os.environ.get('URL_IMPORTACAO_UVAS_PASSAS')},
                    {'super_categoria': 'Suco_uva', 'url': os.environ.get('URL_IMPORTACAO_SUCO_UVA')},
                ],
                'separador': ';'
            },
            {
                'nome_tabela': 'processamento',
                'nome_coluna': 'cultivar',
                'drop_table': 'control',
                'lista_links': [
                    {'super_categoria': 'Viniferas', 'url': os.environ.get('URL_PROCESSAMENTO_VINIFERAS')},
                    {'super_categoria': 'Americana', 'url': os.environ.get('URL_PROCESSAMENTO_AMERICANAS')},
                    {'super_categoria': 'Mesa', 'url': os.environ.get('URL_PROCESSAMENTO_MESA')},
                    {'super_categoria': 'Outras', 'url': os.environ.get('URL_PROCESSAMENTO_OUTRAS')},
                ],
                'separador': '\t'
            },
            {
                'nome_tabela': 'producao',
                'nome_coluna': 'produto',
                'drop_table': None,
                'lista_links': [
                    {'super_categoria': None, 'url': os.environ.get('URL_PRODUCAO')},
                ],
                'separador': ';'
            },
        ]

        for element in lista_json_insercao:
            iniciar = Inicializacao(
                nome_tabela=element['nome_tabela'],
                nome_coluna=element['nome_coluna'],
                drop_column=element['drop_table'],
                lista_links=element['lista_links'],
                separador=element['separador'],
            )

            iniciar.insercoes(db=db)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter os dados ou inserir {e}"
        )
