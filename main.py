from typing import Annotated
from fastapi import FastAPI, status, Depends

import db.models_db as models
from db.database import engine, SessionLocal

from sqlalchemy.orm import Session

from endpoints import comercializacao
from endpoints import importacao
from endpoints import inicializacao_banco
from endpoints import processamento
from endpoints import producao
from endpoints import users


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


app.include_router(comercializacao.router)
app.include_router(importacao.router)
app.include_router(inicializacao_banco.router)
app.include_router(processamento.router)
app.include_router(producao.router)
app.include_router(users.router)


@app.get('/', status_code=status.HTTP_200_OK)
async def user():
    return {'message': 'Hello World'}


