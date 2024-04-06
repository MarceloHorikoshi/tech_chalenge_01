import json

import pandas as pd


def montar_json_result(elemento: dict, anos: list[str]) -> dict:
    json_result = {
        'id': elemento['id'],
        'produto': elemento['produto']
    }
    for ano in anos:
        json_result[ano] = elemento.get(ano, None)
    return json_result


def query_json(json_list: list[dict],
               categoria: str,
               sub_categoria: str,
               ano_producao: list[int]
               ) -> list[dict]:

    anos_str = [str(ano) for ano in ano_producao]
    json_result_list = []

    if sub_categoria is None and categoria is not None:
        for json_element in json_list:
            if str(categoria).upper() in json_element['produto'].upper():
                json_result_list.append(montar_json_result(json_element, anos_str))

    elif categoria is None and sub_categoria is not None:
        for json_element in json_list:
            for sub_json_element in json_element.get('lista_produtos', []):
                if str(sub_categoria).upper() in sub_json_element['produto'].upper():
                    json_result_list.append(montar_json_result(sub_json_element, anos_str))

    else:
        for json_element in json_list:
            if str(categoria).upper() in json_element['produto'].upper():
                for sub_json_element in json_element.get('lista_produtos', []):
                    if str(sub_categoria).upper() in sub_json_element['produto'].upper():
                        json_result_list.append(montar_json_result(sub_json_element, anos_str))

    return json_result_list

# def query_json(json_list: list[dict],
#                categoria: str,
#                sub_categoria: str,
#                ano_producao: list[int]
#                ) -> list[dict]:
#
#     anos_str = [str(ano) for ano in ano_producao]
#     json_result_list = []
#     if sub_categoria is None and categoria is not None:
#         for json_element in json_list:
#             if str(categoria).upper() in json_element['produto'].upper():
#                 json_result = {
#                     'id': json_element['id'],
#                     'produto': json_element['produto']
#                 }
#                 for ano in anos_str:
#                     json_result[ano] = json_element.get(ano, None)
#
#                 json_result_list.append(json_result)
#
#     elif categoria is None and sub_categoria is not None:
#         for json_element in json_list:
#             for sub_json_element in json_element.get('lista_produtos', []):
#                 if str(sub_categoria).upper() in sub_json_element['produto'].upper():
#                     json_result = {
#                         'id': sub_json_element['id'],
#                         'produto': sub_json_element['produto']
#                     }
#                     for ano in anos_str:
#                         json_result[ano] = sub_json_element.get(ano, None)
#
#                     json_result_list.append(json_result)
#
#     else:
#         for json_element in json_list:
#             if str(categoria).upper() in json_element['produto'].upper():
#                 for sub_json_element in json_element.get('lista_produtos', []):
#                     if str(sub_categoria).upper() in sub_json_element['produto'].upper():
#                         json_result = {
#                             'id': sub_json_element['id'],
#                             'produto': sub_json_element['produto']
#                         }
#                         for ano in anos_str:
#                             json_result[ano] = sub_json_element.get(ano, None)
#                         json_result_list.append(json_result)
#
#     return json_result_list


def transformar_em_formato(json_dados: list[dict]) -> list[dict]:
    # Dicionário temporário para armazenar os produtos por categoria
    result_json_formatado = []
    categoria_atual = None

    for item in json_dados:
        if str(item['produto']).isupper():
            # Se o produto está em maiúsculo, é uma nova categoria
            if categoria_atual:
                # Se já havia uma categoria, adicionamos ela ao resultado
                result_json_formatado.append(categoria_atual)

            # Inicializa uma nova categoria
            categoria_atual = item.copy()
            categoria_atual['lista_produtos'] = []
        else:
            # Adiciona o produto à lista de produtos da categoria atual
            categoria_atual['lista_produtos'].append(item)

        # Adiciona última categoria ao resultado
    if categoria_atual:
        result_json_formatado.append(categoria_atual)

    return result_json_formatado


def dataframe_para_json(dataframe: pd.DataFrame) -> list[dict]:
    # Converte o DataFrame para JSON
    json_resultado = dataframe.to_json(orient='records')

    json_resultado = json.loads(json_resultado)
    return json_resultado
