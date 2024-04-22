import asyncio
from datetime import timedelta, datetime
from unittest.mock import MagicMock  # Para criar objetos simulados
from jose import jwt, JWTError

# Importe suas funções e classes relevantes
from api.schemas.models_db import User
from api.services.authentication import authenticate_user, create_access_token, get_current_user, bcrypt_context, \
    SECRET_KEY, ALGORITHM


def test_authenticate_user():
    # Simula um banco de dados com um usuário existente
    fake_user = User(username='testuser', hashed_password=bcrypt_context.hash('testpassword'))
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = fake_user

    # Autentica o usuário com credenciais válidas
    authenticated_user = authenticate_user('testuser', 'testpassword', db)
    assert authenticated_user == fake_user

    # Tenta autenticar o usuário com credenciais inválidas
    invalid_user = authenticate_user('testuser', 'wrongpassword', db)
    assert invalid_user == False


# Teste de geração de token de acesso
def test_create_access_token():
    # Gera um token de acesso para um usuário específico
    access_token = create_access_token('testuser', 1, timedelta(days=1))
    assert isinstance(access_token, str)

    # Decodifica o token e verifica se os dados estão corretos
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token['sub'] == 'testuser'
    assert decoded_token['id'] == 1


# Teste de obtenção do usuário atual a partir do token de acesso
def test_get_current_user():
    # Gera um token de acesso válido para um usuário
    access_token = create_access_token('testuser', 1, timedelta(days=1))

    # Obtém o usuário atual a partir do token
    current_user = asyncio.run(get_current_user(access_token))

    # Verifica se os dados do usuário atual estão corretos
    assert current_user['username'] == 'testuser'
    assert current_user['id'] == 1
