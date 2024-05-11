import os
import pytest

from fastapi.testclient import TestClient
from main import app

from api.routes.inicializacao_banco import get_db
from unittest.mock import MagicMock, patch

from dotenv import load_dotenv

load_dotenv()
# test_main.py

token = os.environ.get('TOKEN')
headers = {"Authorization": f"Bearer {token}"}

client = TestClient(app)


def test_get_db():
    # Arrange
    expected_output = "<class 'generator'>"

    # Act
    db = get_db()

    # Assert
    assert str(type(db)) == expected_output


@patch('src.dependencies.database.SessionLocal', MagicMock())
@patch('src.services.funcionalidades_banco.insercao_dados', MagicMock())
def test_total_processamento():
    response = client.get("/inicializacao", headers=headers)
    assert response.status_code == 201
