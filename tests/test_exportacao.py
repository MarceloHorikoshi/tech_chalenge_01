import os
import pytest

from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
headers = {"Authorization": f"Bearer {token}"}


def test_exportacao_id_sucesso():
    client = TestClient(app)
    response = client.get('/exportacao/1', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_exportacao_id_sem_token():
    client = TestClient(app)
    response = client.get('/exportacao/1')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_exportacao_id_item_inexistente():
    client = TestClient(app)
    response = client.get('/exportacao/99999', headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_total_exportacao_sucesso():
    client = TestClient(app)
    response = client.get('/exportacao', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_total_exportacao_sem_token():
    client = TestClient(app)
    response = client.get('/exportacao')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


@pytest.mark.parametrize("exportacao_entrada, expected_json", [
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
    (
            {"categoria": "Vinho_Mesa", "nome": "Afeganistao", "ano": "1970"},
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
    (
            {"categoria": "Vinho_Mesa", "nome": "Afeganistao", "valor": 0.0, "quantidade": 0, "ano": "1970"},
            [
                {
                    "ano": "1970",
                    "id": 1,
                    "valor": 0.0,
                    "categoria": "Vinho_Mesa",
                    "nome": "Afeganistao",
                    "quantidade": 0
                }
            ]
    ),

])
def test_filtrar_exportacao_sucesso(exportacao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/exportacao/filtragem', headers=headers, json=exportacao_entrada)
    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize("exportacao_entrada, expected_json", [
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
def test_filtrar_exportacao_sem_token(exportacao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/exportacao/filtragem', json=exportacao_entrada)
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_insere_exportacao_sucesso():
    global id_inserted
    exportacao_insert = {
        "ano": "1970",
        "valor": 0.0,
        "quantidade": 0,
        "categoria": "Vinho_Mesa TESTE",
        "nome": "Afeganistao"
    }
    client = TestClient(app)
    response = client.post('/exportacao', headers=headers, json=exportacao_insert)

    id_inserted = response.json()['id']

    assert response.status_code == 201
    assert isinstance(id_inserted, int)


def test_insere_exportacao_sem_token():
    exportacao_insert = {
        "ano": "1970",
        "valor": 0.0,
        "quantidade": 0,
        "categoria": "Vinho_Mesa TESTE",
        "nome": "Afeganistao"
    }
    client = TestClient(app)
    response = client.post('/exportacao', json=exportacao_insert)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_exportacao_sucesso():
    exportacao_alteracao = {
        "ano": "1970",
        "valor": 0.0,
        "quantidade": 0,
        "categoria": "Vinho_Mesa TESTE_update",
        "nome": "Afeganistao"
    }

    client = TestClient(app)
    response = client.put('/exportacao/25282', headers=headers, json=exportacao_alteracao)

    assert response.status_code == 204


def test_altera_exportacao_sem_token():
    exportacao_alteracao = {
        "ano": "1970",
        "valor": 0.0,
        "quantidade": 0,
        "categoria": "Vinho_Mesa TESTE_update",
        "nome": "Afeganistao"
    }

    client = TestClient(app)
    response = client.put('/exportacao/25282', json=exportacao_alteracao)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_exportacao_item_inexistente():
    exportacao_alteracao = {
        "ano": "1970",
        "valor": 0.0,
        "quantidade": 0,
        "categoria": "Vinho_Mesa TESTE_update",
        "nome": "Afeganistao"
    }

    client = TestClient(app)
    response = client.put('/exportacao/9999999', headers=headers, json=exportacao_alteracao)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_deleta_exportacao_sucesso():
    global id_inserted
    client = TestClient(app)
    response = client.delete(f'/exportacao/{id_inserted}', headers=headers)

    assert response.status_code == 204


def test_deleta_exportacao_sem_token():
    client = TestClient(app)
    response = client.delete(f'/exportacao/{id_inserted}')

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_deleta_exportacao_item_inexistente():
    client = TestClient(app)
    response = client.delete(f'/exportacao/9999999', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}
