from api import schemas as models

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session

from api.schemas.database import SessionLocal
from api.schemas.models_db import User

from api.schemas.models_api import CreateUserRequest, Token
from utils.authentication import authenticate_user
from utils.authentication import create_access_token
from utils.authentication import get_current_user

from utils.authentication import bcrypt_context

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
async def user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Falha autentificacao')
    return {'User': user}


@router.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
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


@router.post('/token', response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Usuario nao validado.')
    token = create_access_token(user.username, user.id, timedelta(days=10))

    return {'access_token': token, 'token_type': 'bearer'}
