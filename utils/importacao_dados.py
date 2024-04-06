import io
import logging

import pandas as pd
import requests
from unidecode import unidecode


def corrigir_caracteres(valor):
    if isinstance(valor, str):  # Verifica se o valor é uma string
        valor.replace("Ã¢", "â").replace("Ã§Ã£", "ç").replace("Ãª", "ê").replace("Ã£", "ã")
        valor = unidecode(valor)
        return valor

    else:
        return valor


def download_tabela(url: str) -> bytes:
    # requisicao get para obter arquivo
    resposta = requests.get(url)

    if resposta.status_code == 200:
        arquivo_baixado = resposta.content

    else:
        logging.info('Falha download')

        raise ConnectionError(f'Erro download {resposta.status_code}')

    return arquivo_baixado


def leitura_bytes(arquivo_bytes: bytes, separador: str) -> pd.DataFrame:
    # Crie um buffer de bytes
    buffer_bytes = io.BytesIO(arquivo_bytes)

    # Use pd.read_csv com o buffer de bytes
    df = pd.read_csv(buffer_bytes, sep=separador)

    dataframe_corrigido = df.applymap(corrigir_caracteres)

    return dataframe_corrigido
