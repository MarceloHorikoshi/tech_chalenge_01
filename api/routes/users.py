import os

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session

from api.schemas import models_db as models
from api.dependencies.database import SessionLocal

from api.schemas.models_api import CreateUserRequest
from api.schemas.models_api import Token
from api.schemas.models_db import User

from api.services.authentication import authenticate_user
from api.services.authentication import bcrypt_context
from api.services.authentication import create_access_token
from api.services.authentication import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@router.get('/users', status_code=status.HTTP_200_OK)
async def user(user_total: user_dependency,
               user_authentication: models.User = Depends(get_current_user)
               ):
    # if user is None:
    #     raise HTTPException(status_code=401, detail='Falha autentificacao')
    return {'User': user_total}


@router.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user_id: int,
                    db: db_dependency,
                    user_authentication: models.User = Depends(get_current_user)
                    ):
    # if user_authentication is None:
    #     raise HTTPException(status_code=401, detail='Falha autentificacao')
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))
    return user


@router.post('/users/', status_code=status.HTTP_201_CREATED)
async def create_user(
        create_user_request: CreateUserRequest,
        db: db_dependency
):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )

    db.add(create_user_model)
    db.commit()

    db.refresh(create_user_model)

    return {'id': create_user_model.id}


@router.put('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_password_user(user_id: int,
                               update_data: CreateUserRequest,
                               db: db_dependency,
                               user_authentication: models.User = Depends(get_current_user)
                               ):
    # Verifica se o usuário existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    # Atualiza os dados do usuário
    user.hashed_password = bcrypt_context.hash(update_data.password)

    # Commit da atualização no banco de dados
    db.commit()

    return user


@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      db: db_dependency,
                      user_authentication: models.User = Depends(get_current_user)
                      ):
    # Verifica se o usuário existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=os.environ.get('ERRO_404'))

    # Exclui o usuário do banco de dados
    db.delete(user)
    db.commit()

    return None


@router.post('/token', response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=os.environ.get('ERRO_401'))

    token = create_access_token(user.username, user.id, timedelta(days=10))

    return {'access_token': token, 'token_type': 'bearer'}
