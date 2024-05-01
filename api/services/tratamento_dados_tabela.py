import pandas as pd


def montar_json_result(elemento: dict, anos: list[str]) -> dict:
    """
    Monta um dicionário JSON com informações do elemento para cada ano.

    Args:
        elemento (dict): Dicionário contendo informações de um produto ou categoria.
        anos (list[str]): Lista de anos a serem incluídos no JSON.

    Returns:
        dict: Dicionário JSON com o ID, nome do produto e valores para cada ano.
    """
    json_result = {
        'id': elemento['id'],
        'produto': elemento['produto']
    }
    for ano in anos:
        json_result[ano] = elemento.get(ano, None)
    return json_result


def transformar_em_formato(json_dados: list[dict], nome_coluna: str) -> list[dict]:
    """
    Transforma uma lista de dicionários em um formato específico com categorias e subitens.

    Args:
        json_dados (list[dict]): Lista de dicionários contendo dados de produtos ou categorias.
        nome_coluna (str): Nome da coluna que identifica o produto ou categoria.

    Returns:
        list[dict]: Lista de dicionários formatados com categorias e seus respectivos subitens.
    """
    result_json_formatado = []
    categoria_atual = None
    for item in json_dados:
        if str(item[nome_coluna]).isupper() or str(item[nome_coluna]).upper() == 'SEM CLASSIFICACAO':
            # Se o produto está em maiúsculo, é uma nova categoria
            if categoria_atual:
                # Se já havia uma categoria, adicionamos ela ao resultado
                result_json_formatado.append(categoria_atual)

            # Inicializa uma nova categoria
            categoria_atual = item.copy()
            categoria_atual[f'lista_{nome_coluna}'] = []
        else:
            # Adiciona o produto à lista de produtos da categoria atual
            categoria_atual[f'lista_{nome_coluna}'].append(item)

        # Adiciona última categoria ao resultado
    if categoria_atual:
        result_json_formatado.append(categoria_atual)

    return result_json_formatado


def dataframe_para_json(dataframe: pd.DataFrame) -> list[dict]:
    """
    Converte um DataFrame pandas em uma lista de dicionários JSON.

    Args:
        dataframe (pd.DataFrame): O DataFrame a ser convertido.

    Returns:
        list[dict]: Uma lista de dicionários representando as linhas do DataFrame.
    """
    json_final = dataframe.to_dict(orient='records')
    return json_final


def trata_df_sem_colunas(
        df: pd.DataFrame,
        novas_colunas: list[str],
        coluna_eliminar: str,
        coluna_principal: str
) -> pd.DataFrame:
    """
    Processa um DataFrame, adicionando novas colunas com anos e formatando a coluna principal.

    Args:
        df (pd.DataFrame): O DataFrame a ser processado.
        novas_colunas (list[str]): Lista para armazenar os nomes das novas colunas (anos).
        coluna_eliminar (str): Nome da coluna a ser eliminada do DataFrame.
        coluna_principal (str): Nome da coluna principal a ser formatada.

    Returns:
        pd.DataFrame: O DataFrame processado com as novas colunas e formatação.
        """
    acumulador = 1970
    range_colunas = len(df.columns) - 3
    for i in range(range_colunas):
        novas_colunas.append(str(acumulador + i))

    # Criar um DataFrame vazio com as novas colunas
    novo_df = pd.DataFrame(columns=novas_colunas)

    valores_linha_1 = df.columns.tolist()

    novo_df.loc[0] = valores_linha_1

    for i in range(df.shape[0]):
        if i == 0:
            novo_df.loc[1] = df.loc[i].values
        else:
            novo_df.loc[i + 1] = df.loc[i].values

    novo_df = novo_df.drop(columns=[coluna_eliminar])

    novo_df[coluna_principal] = novo_df[coluna_principal].replace('\d+', '', regex=True)
    novo_df[coluna_principal] = novo_df[coluna_principal].replace('\.', '', regex=True)
    return novo_df
