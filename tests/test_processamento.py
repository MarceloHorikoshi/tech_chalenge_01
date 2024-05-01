import os
import pytest

from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
headers = {"Authorization": f"Bearer {token}"}


def test_processamento_id_sucesso():
    client = TestClient(app)
    response = client.get('/processamento/1', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_processamento_id_sem_token():
    client = TestClient(app)
    response = client.get('/processamento/1')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_processamento_id_item_inexistente():
    client = TestClient(app)
    response = client.get('/processamento/999999', headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_total_processamento_sucesso():
    client = TestClient(app)
    response = client.get('/processamento', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_total_processamento_sem_token():
    client = TestClient(app)
    response = client.get('/processamento')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


@pytest.mark.parametrize("processamento_entrada, expected_json", [
    (
            {"id": 1},
            [
                {
                    "id": 1,
                    "sub_categoria": "TINTAS",
                    "ano": "1970",
                    "categoria": "Viniferas",
                    "nome": "Alicante Bouschet",
                    "valor_producao": 0.0
                }
            ]
    ),
    (
            {
                "sub_categoria": "TINTAS",
                "ano": "2000",
                "nome": "Alicante Bouschet",
                "valor_producao": 160318.0
            },
            [
                {
                    "id": 31,
                    "sub_categoria": "TINTAS",
                    "ano": "2000",
                    "categoria": "Viniferas",
                    "nome": "Alicante Bouschet",
                    "valor_producao": 160318.0
                }
            ]
    ),

])
def test_filtrar_processamento_sucesso(processamento_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/processamento/filtragem', headers=headers, json=processamento_entrada)
    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize('processamento_entrada, expected_json', [
    (
            {"id": 1},
            [
                {
                    "id": 1,
                    "ano": "1970",
                    "valor": 0.0,
                    "quantidade": 0,
                    "categoria": "Vinho_Mesa",
                    "nome": "Afeganistao"
                }
            ]
    ),
])
def test_filtrar_processamento_sem_token(processamento_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/processamento/filtragem', json=processamento_entrada)
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_insere_processamento_sucesso():
    global id_inserted
    processamento_insert = {
        "ano": "1970",
        "valor": 0.0,
        "categoria": "Vinho_Mesa_teste",
        "nome": "Africa do Sul",
        "quantidade": 0
    }
    client = TestClient(app)
    response = client.post('/processamento', headers=headers, json=processamento_insert)

    id_inserted = response.json()['id']

    assert response.status_code == 201
    assert isinstance(id_inserted, int)


def test_insere_processamento_sem_token():
    processamento_insert = {
        "categoria": "VINHO DE MESA_TESTE",
        "litros_comercializacao": 83300735.0,
        "ano": "1970",
        "nome": "Tinto_teste"
    }
    client = TestClient(app)
    response = client.post('/processamento', json=processamento_insert)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_processamento_sucesso():
    processamento_alteracao = {
        "categoria": "Viniferas_teste",
        "nome": "Alicante Bouschet",
        "valor_producao": 0.0,
        "ano": "1970",
        "sub_categoria": "TINTAS_teste"
    }

    client = TestClient(app)
    response = client.put('/processamento/10389', headers=headers, json=processamento_alteracao)

    assert response.status_code == 204


def test_altera_processamento_sem_token():
    processamento_alteracao = {
        "categoria": "Viniferas_teste",
        "nome": "Alicante Bouschet",
        "valor_producao": 0.0,
        "ano": "1970",
        "sub_categoria": "TINTAS_teste"
    }

    client = TestClient(app)
    response = client.put('/processamento/10389', json=processamento_alteracao)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_processamento_item_inexistente():
    processamento_alteracao = {
        "ano": "1970",
        "valor": 0.0,
        "categoria": "Vinho_Mesa_teste",
        "nome": "Africa do Sul UPDATE",
        "quantidade": 0
    }

    client = TestClient(app)
    response = client.put('/processamento/9999999', headers=headers, json=processamento_alteracao)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_deleta_processamento_sucesso():
    global id_inserted
    print(id_inserted)
    client = TestClient(app)
    response = client.delete(f'/processamento/{id_inserted}', headers=headers)

    assert response.status_code == 204


def test_deleta_processamento_sem_token():
    client = TestClient(app)
    response = client.delete(f'/processamento/{id_inserted}')

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_deleta_processamento_item_inexistente():
    client = TestClient(app)
    response = client.delete(f'/processamento/99999999', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}
