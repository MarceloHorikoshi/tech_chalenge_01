from api.schemas import models_db as models
from sqlalchemy import text


def limpa_tabela(db, tabela):
    # limpa a tabela
    db.execute(text(f"TRUNCATE TABLE {tabela}"))
    db.commit()


def insercao_dados(db, dict_final, coluna, tabela, super_categoria=None):
    try:
        # faz a inserção de todos os dados na tabela
        if tabela == 'exportacao' or tabela == 'importacao':
            for elemento in dict_final:
                elemento_sem_id = elemento.copy()  # Copia o dicionário para evitar modificar o original
                elemento_sem_id.pop('id', None)
                nome_produto = elemento_sem_id.pop(coluna, None)  # Obtém o nome do produto

                anos = []
                quantidades = []
                valores = []

                for chave, valor in elemento_sem_id.items():
                    if '.' in chave:
                        valores.append(float(valor))
                    else:
                        anos.append(chave)
                        quantidades.append(int(valor))

                # Cria o dicionário com as informações coletadas
                if tabela == 'exportacao':
                    for ano, quantidade, valor in zip(anos, quantidades, valores):

                        item = models.Exportacao(
                            categoria=str(super_categoria).strip(),
                            nome=str(nome_produto).strip(),
                            ano=ano,
                            quantidade=quantidade,
                            valor=valor
                        )
                        db.add(item)
                else:
                    for ano, quantidade, valor in zip(anos, quantidades, valores):
                        item = models.Importacao(
                            categoria=str(super_categoria).strip(),
                            nome=str(nome_produto).strip(),
                            ano=ano,
                            quantidade=quantidade,
                            valor=valor
                        )
                        db.add(item)

        else:

            for categorias in dict_final:

                nome_categoria = categorias[coluna]

                for elemento_lista in categorias[f'lista_{coluna}']:
                    elemento_lista.pop('id', None)
                    nome_produto = elemento_lista[f'{coluna}']
                    for ano, valor in elemento_lista.items():
                        if ano != coluna:
                            if tabela == 'producao':
                                item = models.Producao(
                                    categoria=str(nome_categoria).strip(),
                                    nome=str(nome_produto).strip(),
                                    ano=ano,
                                    valor_producao=float(valor)
                                )
                            elif tabela == 'processamento':
                                item = models.Processamento(
                                    categoria=str(super_categoria).strip(),
                                    sub_categoria=str(nome_categoria).strip(),
                                    nome=str(nome_produto).strip(),
                                    ano=ano,
                                    valor_producao=float(valor)
                                )
                            elif tabela == 'comercializacao':
                                item = models.Comercializacao(
                                    categoria=str(nome_categoria).strip(),
                                    nome=str(nome_produto).strip(),
                                    ano=ano,
                                    litros_comercializacao=float(valor)
                                )
                            db.add(item)

        db.commit()

    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()

