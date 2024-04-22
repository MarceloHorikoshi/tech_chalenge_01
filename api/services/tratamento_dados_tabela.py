import pandas as pd


def montar_json_result(elemento: dict, anos: list[str]) -> dict:
    json_result = {
        'id': elemento['id'],
        'produto': elemento['produto']
    }
    for ano in anos:
        json_result[ano] = elemento.get(ano, None)
    return json_result


def transformar_em_formato(json_dados: list[dict], nome_coluna: str) -> list[dict]:
    # Dicionário temporário para armazenar os produtos por categoria
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
    json_final = dataframe.to_dict(orient='records')
    return json_final


def trata_df_sem_colunas(
        df: pd.DataFrame,
        novas_colunas: list[str],
        coluna_eliminar: str,
        coluna_principal: str
) -> pd.DataFrame:

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
