import os

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from api.routes.users import db_dependency
from main import app  # Importe a instância FastAPI do seu aplicativo

from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
headers = {"Authorization": f"Bearer {token}"}

# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Sobrescreva a dependência do banco de dados para usar o banco de dados de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[db_dependency] = override_get_db

# Inicialize o cliente de teste
client = TestClient(app)


# Exemplo de caso de teste para a rota GET /auth/users
def test_get_users():
    # Faça uma solicitação GET para /auth/users
    response = client.get('/auth/users', headers=headers)
    assert response.status_code == 200  # Verifique se a resposta é bem-sucedida


# Exemplo de caso de teste para a rota POST /auth/users/
def test_create_user():
    global id_inserted

    # Dados para criar um novo usuário
    new_user_data = {'username': 'testuser', 'password': 'testpassword'}

    # Faça uma solicitação POST para /auth/users/ para criar um novo usuário
    response = client.post('/auth/users/', json=new_user_data)
    id_inserted = response.json()['id']

    # Verifique se a resposta é bem-sucedida e o código de status HTTP é 201 (Created)
    assert response.status_code == 201


# Exemplo de caso de teste para a rota PUT /auth/users/{user_id}
def test_update_user_password():
    global id_inserted
    # Dados para atualizar a senha do usuário
    update_data = {
        "username": "new_user_name",
        "password": "newpassword"
    }

    response = client.put(f'/auth/users/{id_inserted}', json=update_data, headers=headers)

    assert response.status_code == 204


def test_delete_user():
    global id_inserted
    response = client.delete(f'/auth/users/{id_inserted}', headers=headers)

    # Verifique se a resposta é bem-sucedida e o código de status HTTP é 204 (No Content)
    assert response.status_code == 204
