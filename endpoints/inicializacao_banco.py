import db.models_db as models

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.database import SessionLocal
from api_interface.models import ProcessamentoBase

from utils.funcionaliades_banco import insercao_dados, limpa_tabela
from utils.tratamento_dados_tabela import transformar_em_formato, dataframe_para_json
from utils.importacao_dados import download_tabela, leitura_bytes
from utils.tratamento_dados_tabela import cria_organiza_colunas, trata_df_sem_colunas

url_comercializacao = 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv'

url_importacao_vinhos_mesa = 'http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv'
url_importacao_espumante = 'http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv'
url_importacao_uvas_frescas = 'http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv'
url_importacao_uvas_passas = 'http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv'
url_importacao_suco_uva = 'http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv'


url_processamento_viniferas = 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv'
url_processamento_americanas = 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv'
url_processamento_mesa = 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv'
url_processamento_outras = 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv'

url_producao = 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv'

separador_t = '\t'

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


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
            print(link)
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

                # if self.nome_tabela == 'importacao':
                #     novas_colunas = ['quantidade', 'valor']
                #     df = cria_organiza_colunas(df)

                if self.nome_tabela == 'importacao':
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
async def total_processamento(db: db_dependency):
    try:
        lista_json_insercao = [

            {
                'nome_tabela': 'comercializacao',
                'nome_coluna': 'produto',
                'drop_table': None,
                'lista_links': [
                    {'super_categoria': None, 'url': url_comercializacao},
                ],
                'separador': ';'
            },
            {
                'nome_tabela': 'importacao',
                'nome_coluna': 'pais',
                'drop_table': None,
                'lista_links': [
                    {'super_categoria': 'Vinho_Mesa', 'url': url_importacao_vinhos_mesa},
                    {'super_categoria': 'Espumante', 'url': url_importacao_espumante},
                    {'super_categoria': 'Uvas_frescas', 'url': url_importacao_uvas_frescas},
                    {'super_categoria': 'Uvas_passas', 'url': url_importacao_uvas_passas},
                    {'super_categoria': 'Suco_uva', 'url': url_importacao_suco_uva},
                ],
                'separador': ';'
            },
            {
                'nome_tabela': 'processamento',
                'nome_coluna': 'cultivar',
                'drop_table': 'control',
                'lista_links': [
                    {'super_categoria': 'Viniferas', 'url': url_processamento_viniferas},
                    {'super_categoria': 'Americana', 'url': url_processamento_americanas},
                    {'super_categoria': 'Mesa', 'url': url_processamento_mesa},
                    {'super_categoria': 'Outras', 'url': url_processamento_outras},
                ],
                'separador': '\t'
            },
            {
                'nome_tabela': 'producao',
                'nome_coluna': 'produto',
                'drop_table': None,
                'lista_links': [
                    {'super_categoria': None, 'url': url_producao},
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
        raise HTTPException(status_code=500, detail=f"Erro ao obter os dados ou inserir {e}")
