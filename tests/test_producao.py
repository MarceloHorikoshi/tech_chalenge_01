import os
import pytest

from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
headers = {"Authorization": f"Bearer {token}"}


def test_producao_id_sucesso():
    client = TestClient(app)
    response = client.get('/producao/1', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_producao_id_sem_token():
    client = TestClient(app)
    response = client.get('/producao/1')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_producao_id_item_inexistente():
    client = TestClient(app)
    response = client.get('/producao/999999', headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_total_producao_sucesso():
    client = TestClient(app)
    response = client.get('/producao', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_total_producao_sem_token():
    client = TestClient(app)
    response = client.get('/producao')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


@pytest.mark.parametrize("producao_entrada, expected_json", [
    (
            {"id": 1},
            [
                {
                    "nome": "Tinto",
                    "valor_producao": 174224052.0,
                    "categoria": "VINHO DE MESA",
                    "ano": "1970",
                    "id": 1
                }
            ]
    ),
    (
            {
                "categoria": "VINHO DE MESA",
                "nome": "Branco",
                "ano": "1971",
                "valor_producao": 1160500.0
            },
            [
                {
                    "nome": "Branco",
                    "valor_producao": 1160500.0,
                    "categoria": "VINHO DE MESA",
                    "ano": "1971",
                    "id": 55
                }
            ]
    ),

])
def test_filtrar_producao_sucesso(producao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/producao/filtragem', headers=headers, json=producao_entrada)
    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize('producao_entrada, expected_json', [
    (
            {"id": 1},
            [
                {
                    "nome": "Tinto",
                    "valor_producao": 174224052.0,
                    "categoria": "VINHO DE MESA",
                    "ano": "1970",
                    "id": 1
                }
            ]
    ),
])
def test_filtrar_producao_sem_token(producao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/producao/filtragem', json=producao_entrada)
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_insere_producao_sucesso():
    global id_inserted
    producao_insert = {
        "nome": "Tinto",
        "valor_producao": 174224052.0,
        "categoria": "VINHO DE MESA_teste",
        "ano": "1970",
    }
    client = TestClient(app)
    response = client.post('/producao', headers=headers, json=producao_insert)

    id_inserted = response.json()['id']

    assert response.status_code == 201
    assert isinstance(id_inserted, int)


def test_insere_producao_sem_token():
    producao_insert = {
        "nome": "Tinto",
        "valor_producao": 174224052.0,
        "categoria": "VINHO DE MESA_teste",
        "ano": "1970",
    }
    client = TestClient(app)
    response = client.post('/producao', json=producao_insert)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_producao_sucesso():
    global id_inserted
    producao_alteracao = {
        "nome": "Tinto",
        "valor_producao": 174224052.0,
        "categoria": "VINHO DE MESA_teste_update",
        "ano": "1970"
    }

    client = TestClient(app)
    response = client.put(f'/producao/{id_inserted}', headers=headers, json=producao_alteracao)

    assert response.status_code == 204


def test_altera_producao_sem_token():
    global id_inserted
    producao_alteracao = {
        "nome": "Tinto",
        "valor_producao": 174224052.0,
        "categoria": "VINHO DE MESA_teste_update",
        "ano": "1970"
    }

    client = TestClient(app)
    response = client.put(f'/producao/{id_inserted}', json=producao_alteracao)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_producao_item_inexistente():
    producao_alteracao = {
        "nome": "Tinto",
        "valor_producao": 174224052.0,
        "categoria": "VINHO DE MESA_teste_update",
        "ano": "1970"
    }

    client = TestClient(app)
    response = client.put('/producao/9999999', headers=headers, json=producao_alteracao)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_deleta_producao_sucesso():
    global id_inserted
    print(id_inserted)
    client = TestClient(app)
    response = client.delete(f'/producao/{id_inserted}', headers=headers)

    assert response.status_code == 204


def test_deleta_producao_sem_token():
    global id_inserted
    client = TestClient(app)
    response = client.delete(f'/producao/{id_inserted}')

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_deleta_producao_item_inexistente():
    client = TestClient(app)
    response = client.delete(f'/producao/99999999', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}
