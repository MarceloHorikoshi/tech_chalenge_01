from typing import Optional, List
from fastapi import FastAPI, Query

from utils.tratamento_dicionarios import query_json, transformar_em_formato, dataframe_para_json
from utils.importacao_dados import download_tabela, leitura_bytes

app = FastAPI()

url_producao = 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv'

separador = ';'


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/producao/filtragem')
async def filtrar_producao(
        categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
        nome_produto: Optional[str] = Query(None, description="Filtrar por nome do produto"),
        ano_producao: Optional[List[int]] = Query([], description="Filtrar por ano de produção")
):
    # carrega dados do site em um dataframe
    df = leitura_bytes(
        download_tabela(url=url_producao),
        separador=separador
    )

    dict_transformado = transformar_em_formato(
        json_dados=dataframe_para_json(dataframe=df)
    )

    # query para buscar a categoria, produto e ano passado
    dict_final = query_json(json_list=dict_transformado,
                            categoria=categoria,
                            sub_categoria=nome_produto,
                            ano_producao=ano_producao
                            )

    return dict_final


@app.get('/producao/{id_prod}')
async def detalhar_producao_id(id_prod: int):
    # carrega dados do site em um dataframe
    df = leitura_bytes(
        download_tabela(url=url_producao),
        separador=separador
    )

    # transforma dataframe para json e faz uma query para buscar o id passado
    dict_final = dataframe_para_json(dataframe=df.query(f'id == {id_prod}'))[0]

    return dict_final


@app.get('/producao')
async def listar_producao_total():
    df = leitura_bytes(
        download_tabela(url=url_producao),
        separador=separador
    )

    dict_final = transformar_em_formato(
        json_dados=dataframe_para_json(dataframe=df)
    )

    return dict_final
