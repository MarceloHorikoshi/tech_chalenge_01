import os
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from starlette import status

from passlib.context import CryptContext
from jose import jwt, JWTError

from api.schemas.models_db import User


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def authenticate_user(username: str, password: str, db):
    """Autentica um usuário com base nas credenciais fornecidas.

    Args:
        username (str): O nome de usuário para autenticação.
        password (str): A senha para autenticação.
        db: Objeto de sessão do banco de dados.

    Returns:
        Objeto User se a autenticação for bem-sucedida, caso contrário False.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """Gera um token de acesso JWT para um usuário.

    Args:
        username (str): O nome de usuário do usuário.
        user_id (int): O ID do usuário.
        expires_delta (timedelta): A duração pela qual o token é válido.

    Returns:
        str: O token de acesso JWT codificado.
    """
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Recupera o usuário atualmente autenticado do token JWT.

    Args:
        token (str): O token JWT fornecido na solicitação.

    Returns:
        dict: Um dicionário contendo o nome de usuário e o ID do usuário,
            ou gera uma exceção HTTP_401_UNAUTHORIZED se o token for inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=os.environ.get('ERRO_401'))
        return {'username': username, 'id': user_id}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=os.environ.get('ERRO_401'))