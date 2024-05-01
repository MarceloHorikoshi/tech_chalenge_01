import io
import logging

import pandas as pd
import requests
from unidecode import unidecode


def corrigir_caracteres(valor):
    """
    Corrige caracteres especiais e acentos em um valor de string.

    Args:
        valor: O valor a ser corrigido.

    Returns:
        str: O valor com caracteres corrigidos.
    """
    if isinstance(valor, str):  # Verifica se o valor é uma 'string'
        valor.replace("Ã¢", "â").replace("Ã§Ã£", "ç").replace("Ãª", "ê").replace("Ã£", "ã")
        valor = unidecode(valor)
        return valor

    else:
        return valor


def download_tabela(url: str) -> bytes:
    """
    Faz o download de um arquivo de uma URL e retorna seu conteúdo em bytes.

    Args:
        url (str): A URL do arquivo a ser baixado.

    Returns:
        bytes: O conteúdo do arquivo baixado em bytes.

    Raises:
        ConnectionError: Se houver um erro durante o download (status_code diferente de 200).
    """

    resposta = requests.get(url)

    if resposta.status_code == 200:
        arquivo_baixado = resposta.content

    else:
        logging.info('Falha download')

        raise ConnectionError(f'Erro download {resposta.status_code}')

    return arquivo_baixado


def limpar_titulos(titulo):
    """Limpa um título de coluna removendo acentos e caracteres especiais.

    Args:
        titulo (str): O título da coluna.

    Returns:
        str: O título limpo.
    """
    return unidecode(titulo)


def leitura_bytes(arquivo_bytes: bytes, separador: str, nome_tabela, skiprows=None) -> pd.DataFrame:
    """
    Lê dados de um arquivo em bytes e retorna um DataFrame pandas.

    Args:
        arquivo_bytes (bytes): O conteúdo do arquivo em bytes.
        separador (str): O caractere separador de colunas (ex: ',').
        nome_tabela (str): O nome da tabela (usado para formatação de colunas).
        skiprows (int, optional): Número de linhas a serem puladas no início do arquivo. Defaults to None.

    Returns:
        pd.DataFrame: O DataFrame com os dados do arquivo.
    """

    buffer_bytes = io.BytesIO(arquivo_bytes)

    # Use pd.read_csv com o buffer de bytes
    df = pd.read_csv(buffer_bytes, sep=separador, skiprows=skiprows)

    if nome_tabela == 'exportacao' or nome_tabela == 'importacao':
        df.columns = [limpar_titulos(str(titulo).lower()) for titulo in df.columns]

    df = df.fillna(0)

    dataframe_corrigido = df.map(corrigir_caracteres)

    return dataframe_corrigido
