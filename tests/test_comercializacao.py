import os
import pytest

from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
headers = {"Authorization": f"Bearer {token}"}


def test_comercializacao_id_sucesso():
    client = TestClient(app)
    response = client.get('/comercializacao/1', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_comercializacao_id_sem_token():
    client = TestClient(app)
    response = client.get('/comercializacao/1')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_comercializacao_id_item_inexistente():
    client = TestClient(app)
    response = client.get('/comercializacao/99999', headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_total_comercializacao_sucesso():
    client = TestClient(app)
    response = client.get('/comercializacao', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_total_comercializacao_sem_token():
    client = TestClient(app)
    response = client.get('/comercializacao')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


@pytest.mark.parametrize("comercializacao_entrada, expected_json", [
    (
        {"id": 1},
        [
            {
                "categoria": "VINHO DE MESA",
                "id": 1,
                "ano": "1970",
                "litros_comercializacao": 83300735.0,
                "nome": "Tinto"
            }
        ]
    ),
    (
        {"categoria": "VINHO DE MESA", "ano": "1970"},
        [
            {
                "categoria": "VINHO DE MESA",
                "id": 1,
                "litros_comercializacao": 83300735.0,
                "ano": "1970",
                "nome": "Tinto"
            },
            {
                "categoria": "VINHO DE MESA",
                "id": 54,
                "litros_comercializacao": 107681.0,
                "ano": "1970",
                "nome": "Rosado"
            },
            {
                "categoria": "VINHO DE MESA",
                "id": 107,
                "litros_comercializacao": 14919190.0,
                "ano": "1970",
                "nome": "Branco"
            }
        ]
    ),
    (
            {
                "categoria": "VINHO DE MESA",
                "ano": "1970",
                "litros_comercializacao": 83300735.0,
                "nome": "Tinto"
            },
            [
                {
                    "categoria": "VINHO DE MESA",
                    "id": 1,
                    "ano": "1970",
                    "litros_comercializacao": 83300735.0,
                    "nome": "Tinto"
                }
            ]
    ),

])
def test_filtrar_comercializacao_sucesso(comercializacao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/comercializacao/filtragem', headers=headers, json=comercializacao_entrada)
    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize("comercializacao_entrada, expected_json", [
    (
        {"id": 1},
        [
            {
                "categoria": "VINHO DE MESA",
                "id": 1,
                "ano": "1970",
                "litros_comercializacao": 83300735.0,
                "nome": "Tinto"
            }
        ]
    ),
])
def test_filtrar_comercializacao_sem_token(comercializacao_entrada, expected_json):
    client = TestClient(app)
    response = client.post('/comercializacao/filtragem', json=comercializacao_entrada)
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_insere_comercializacao_sucesso():
    global id_inserted
    comercializacao_insert = {
        "categoria": "VINHO DE MESA_TESTE",
        "litros_comercializacao": 83300735.0,
        "ano": "1970",
        "nome": "Tinto_teste"
    }
    client = TestClient(app)
    response = client.post('/comercializacao', headers=headers, json=comercializacao_insert)

    id_inserted = response.json()['id']

    assert response.status_code == 201
    assert isinstance(id_inserted, int)

def test_insere_comercializacao_sem_token():
    comercializacao_insert = {
        "categoria": "VINHO DE MESA_TESTE",
        "litros_comercializacao": 83300735.0,
        "ano": "1970",
        "nome": "Tinto_teste"
    }
    client = TestClient(app)
    response = client.post('/comercializacao', json=comercializacao_insert)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_comercializacao_sucesso():
    comercializacao_alteracao = {
        "categoria": "VINHO DE MESA_TESTE",
        "litros_comercializacao": 83300735.0,
        "ano": "1970",
        "nome": "Tinto_teste"
    }

    client = TestClient(app)
    response = client.put('/comercializacao/500', headers=headers, json=comercializacao_alteracao)

    assert response.status_code == 204


def test_altera_comercializacao_sem_token():
    comercializacao_alteracao = {
        "categoria": "VINHO DE MESA_TESTE",
        "litros_comercializacao": 83300735.0,
        "ano": "1970",
        "nome": "Tinto_teste"
    }

    client = TestClient(app)
    response = client.put('/comercializacao/2757', json=comercializacao_alteracao)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_comercializacao_item_inexistente():
    comercializacao_alteracao = {
        "categoria": "VINHO DE MESA_TESTE",
        "litros_comercializacao": 83300735.0,
        "ano": "1970",
        "nome": "Tinto_teste"
    }

    client = TestClient(app)
    response = client.put('/comercializacao/9999999', headers=headers, json=comercializacao_alteracao)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_deleta_comercializacao_sucesso():
    global id_inserted
    client = TestClient(app)
    response = client.delete(f'/comercializacao/{id_inserted}', headers=headers)

    assert response.status_code == 204


def test_deleta_comercializacao_sem_token():
    client = TestClient(app)
    response = client.delete(f'/comercializacao/{id_inserted}')

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_deleta_comercializacao_item_inexistente():
    client = TestClient(app)
    response = client.delete(f'/comercializacao/9999999', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}

