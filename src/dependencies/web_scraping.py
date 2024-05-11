import requests
from bs4 import BeautifulSoup


def encontrar_urls_csv(url_base, categorias):
    """
    Encontra URLs de arquivos CSV em diferentes categorias e subcategorias de um site.

    Args:
        url_base: A URL base do site.
        categorias: Um dicionário onde as chaves são os nomes das categorias e os valores são listas de subcategorias (ou None para nenhuma subcategoria).

    Returns:
        Um dicionário onde as chaves são os nomes das categorias e os valores são listas de URLs de arquivos CSV encontrados.
    """

    urls_csv_por_categoria = {}
    url_download = 'http://vitibrasil.cnpuv.embrapa.br/'
    for categoria, subcategorias in categorias.items():
        url_categoria = url_base + f"?opcao=opt_{categoria}"

        if subcategorias is None:
            # Categoria sem subcategorias
            urls_csv_por_categoria[categoria] = encontrar_urls_csv_na_pagina(url_categoria, url_download)
        else:
            # Categoria com subcategorias
            urls_csv_por_categoria[categoria] = {}
            for subcategoria in subcategorias:
                url_subcategoria = url_categoria + f"&subopcao=subopt_{subcategoria}"
                urls_csv_por_categoria[categoria][subcategoria] = encontrar_urls_csv_na_pagina(url_subcategoria,
                                                                                               url_download)

    return urls_csv_por_categoria


def encontrar_urls_csv_na_pagina(url, url_download):
    """
    Encontra URLs de arquivos CSV em uma única página.

    Args:
        url: A URL da página.
        url_download: A URL base do site (para construir URLs relativas se necessário).

    Returns:
        Uma lista de URLs de arquivos CSV encontrados.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        urls_csv = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.csv'):
                if href.startswith('http'):
                    # URL absoluta
                    urls_csv.append(href)
                else:
                    # URL relativa, construir a URL completa
                    urls_csv.append(url_download + href)
        return urls_csv

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return []


def criar_lista_json(urls_encontradas):
    """
    Transforma o dicionário de URLs encontradas no formato JSON desejado.

    Args:
        urls_encontradas: O dicionário com as URLs encontradas, organizado por categoria e subcategoria.

    Returns:
        Uma lista de dicionários no formato especificado.
    """

    lista_json = []
    mapeamento_nomes = {
        "02": "producao",
        "03": ("processamento", "control"),  # Tupla com nome e valor de drop_table
        "04": "comercializacao",
        "05": "importacao",
        "06": "exportacao"
    }
    mapeamento_supercategorias = {
        "03": {
            "01": "Viníferas",
            "02": "Americanas e híbridas",
            "03": "Uvas de mesa",
            "04": "Sem classificação"
        },
        "05": {
            "01": "Vinho_Mesa",
            "02": "Espumante",
            "03": "Uvas_frescas",
            "04": "Uvas_passas",
            "05": "Suco_uva"
        },
        "06": {
            "01": "Vinho_Mesa",
            "02": "Espumantes",
            "03": "Uva",
            "04": "Suco_uva"
        }
    }
    mapeamento_colunas = {
        "02": "produto",
        "03": "cultivar",
        "04": "produto",
        "05": "pais",
        "06": "pais"
    }
    mapeamento_separadores = {
        "02": ";",
        "03": "\t",
        "04": ";",
        "05": ";",
        "06": ";"
    }

    for codigo_categoria, urls_categoria in urls_encontradas.items():
        info_tabela = mapeamento_nomes.get(codigo_categoria, f"categoria_{codigo_categoria}")
        if isinstance(info_tabela, tuple):
            nome_tabela, drop_table = info_tabela  # Desempacotamento se for uma tupla
        else:
            nome_tabela = info_tabela
            drop_table = None  # Valor padrão se não houver drop_table

        nome_coluna = mapeamento_colunas.get(codigo_categoria, "coluna")
        separador = mapeamento_separadores.get(codigo_categoria, ",")

        lista_links = []
        if isinstance(urls_categoria, dict):
            # Categoria com subcategorias
            for subcategoria, url in urls_categoria.items():
                nome_supercategoria = mapeamento_supercategorias.get(codigo_categoria, {}).get(subcategoria,
                                                                                               subcategoria)
                lista_links.append({"super_categoria": nome_supercategoria, "url": url[0]})
        else:
            # Categoria sem subcategorias
            lista_links.append({"super_categoria": None, "url": urls_categoria[0]})

        lista_json.append({
            "nome_tabela": nome_tabela,
            "nome_coluna": nome_coluna,
            "drop_table": drop_table,
            "lista_links": lista_links,
            "separador": separador
        })

    return lista_json

