import os
import pytest

from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
headers = {"Authorization": f"Bearer {token}"}


def test_importacao_id_sucesso():
    client = TestClient(app)
    response = client.get('/importacao/1', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_importacao_id_sem_token():
    client = TestClient(app)
    response = client.get('/importacao/1')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_importacao_id_item_inexistente():
    client = TestClient(app)
    response = client.get('/importacao/99999', headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_total_importacao_sucesso():
    client = TestClient(app)
    response = client.get('/importacao', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_total_importacao_sem_token():
    client = TestClient(app)
    response = client.get('/importacao')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


@pytest.mark.parametrize("importacao_entrada, expected_json", [
    (
            {"id": 1},
            [
                {
                    "ano": "1970",
                    "id": 1,
                    "valor": 0.0,
                    "categoria": "Vinho_Mesa",
                    "nome": "Africa do Sul",
                    "quantidade": 0
                }
            ]
    ),
    (
            {"categoria": "Vinho_Mesa", "nome": "Africa do Sul", "valor": 0.0, "quantidade": 0, "ano": "1970"},
            [
                {
                    "ano": "1970",
                    "id": 1,
                    "valor": 0.0,
                    "categoria": "Vinho_Mesa",
                    "nome": "Africa do Sul",
                    "quantidade": 0
                }
            ]
    ),

])
def test_filtrar_importacao_sucesso(importacao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/importacao/filtragem', headers=headers, json=importacao_entrada)
    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize('importacao_entrada, expected_json', [
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
def test_filtrar_importacao_sem_token(importacao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/importacao/filtragem', json=importacao_entrada)
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_insere_importacao_sucesso():
    global id_inserted
    importacao_insert = {
        "ano": "1970",
        "valor": 0.0,
        "categoria": "Vinho_Mesa_teste",
        "nome": "Africa do Sul",
        "quantidade": 0
    }
    client = TestClient(app)
    response = client.post('/importacao', headers=headers, json=importacao_insert)

    id_inserted = response.json()['id']

    assert response.status_code == 201
    assert isinstance(id_inserted, int)


def test_insere_importacao_sem_token():
    importacao_insert = {
        "categoria": "VINHO DE MESA_TESTE",
        "litros_comercializacao": 83300735.0,
        "ano": "1970",
        "nome": "Tinto_teste"
    }
    client = TestClient(app)
    response = client.post('/importacao', json=importacao_insert)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_importacao_sucesso():
    importacao_alteracao = {
        "ano": "1970",
        "valor": 0.0,
        "quantidade": 0,
        "categoria": "Vinho_Mesa TESTE_update",
        "nome": "Afeganistao"
    }

    client = TestClient(app)
    response = client.put('/importacao/10254', headers=headers, json=importacao_alteracao)

    assert response.status_code == 204


def test_altera_importacao_sem_token():
    importacao_alteracao = {
        "ano": "1970",
        "valor": 0.0,
        "categoria": "Vinho_Mesa_teste",
        "nome": "Africa do Sul UPDATE",
        "quantidade": 0
    }

    client = TestClient(app)
    response = client.put('/importacao/10254', json=importacao_alteracao)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_importacao_item_inexistente():
    importacao_alteracao = {
        "ano": "1970",
        "valor": 0.0,
        "categoria": "Vinho_Mesa_teste",
        "nome": "Africa do Sul UPDATE",
        "quantidade": 0
    }

    client = TestClient(app)
    response = client.put('/importacao/9999999', headers=headers, json=importacao_alteracao)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_deleta_importacao_sucesso():
    global id_inserted
    print(id_inserted)
    client = TestClient(app)
    response = client.delete(f'/importacao/{id_inserted}', headers=headers)

    assert response.status_code == 204


def test_deleta_importacao_sem_token():
    client = TestClient(app)
    response = client.delete(f'/importacao/{id_inserted}')

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_deleta_importacao_item_inexistente():
    client = TestClient(app)
    response = client.delete(f'/importacao/99999999', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}
