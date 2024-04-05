import logging
import json
import pandas
import pandas as pd
import requests

from fastapi import FastAPI
from unidecode import unidecode

app = FastAPI()

separador = ';'

def corrigir_caracteres(valor):
    if isinstance(valor, str):  # Verifica se o valor é uma string
        valor.replace("Ã¢", "â").replace("Ã§Ã£", "ç").replace("Ãª", "ê").replace("Ã£", "ã")
        valor = unidecode(valor)
        return valor

    else:
        return valor

def dataframe_para_json(dataframe: pandas.DataFrame) -> dict:
    # Converte o DataFrame para JSON
    json_resultado = dataframe.to_json(orient='records')

    json_resultado = json.loads(json_resultado)
    return json_resultado

def download_arquivo(url: str, nome_arquivo: str) -> str:
    diretorio_download = './embrapa_tables/'
    arquivo_baixado = diretorio_download+nome_arquivo
    # requisicao get para obter arquivo
    resposta = requests.get(url)

    if resposta.status_code == 200:
        with open(arquivo_baixado, 'wb') as arquivo:
            arquivo.write(resposta.content)
        logging.info('Download concluido com sucesso')

    else:
        logging.info('Falha download')

        raise ConnectionError(f'Erro download {resposta.status_code}')

    return arquivo_baixado

def leitura_csv(caminho_arquivo: str, separador: str) -> pandas.DataFrame:
    # Lê o arquivo CSV e carrega-o como um DataFrame do Pandas
    dataframe = pd.read_csv(caminho_arquivo, sep=separador)

    dataframe_corrigido = dataframe.applymap(corrigir_caracteres)

    return dataframe_corrigido

def transformar_em_formato(json_dados: list[dict]) -> dict:
    # Dicionário temporário para armazenar os produtos por categoria
    result_json_formatado = []
    categoria_atual = None

    for item in json_dados:
        if str(item['produto']).isupper():
            # Se o produto está em maiúsculo, é uma nova categoria
            if categoria_atual:
                # Se já havia uma categoria, adicionamos ela ao resultado
                result_json_formatado.append(categoria_atual)

            # Inicializamos uma nova categoria
            categoria_atual = item.copy()
            categoria_atual['lista_produtos'] = []
        else:
            # Adicionamos o produto à lista de produtos da categoria atual
            categoria_atual['lista_produtos'].append(item)

        # Adicionamos a última categoria ao resultado
    if categoria_atual:
        result_json_formatado.append(categoria_atual)

    return result_json_formatado


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/producao')
async def producao():
    url_producao = 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv'
    nome_arquivo = 'producao.csv'

    df = leitura_csv(
        download_arquivo(
            url=url_producao,
            nome_arquivo=nome_arquivo
        ),
        separador=separador
    )

    dict_final = transformar_em_formato(
        json_dados=dataframe_para_json(dataframe=df)
    )

    return dict_final

