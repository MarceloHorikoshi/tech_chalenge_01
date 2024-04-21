from typing import Annotated
from fastapi import FastAPI, Depends

from api import schemas as models
from api.schemas.database import engine, SessionLocal

from sqlalchemy.orm import Session

from api.routes import comercializacao, importacao, producao, processamento, inicializacao_banco, users, exportacao

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
app.include_router(exportacao.router)
app.include_router(importacao.router)
app.include_router(inicializacao_banco.router)
app.include_router(processamento.router)
app.include_router(producao.router)
app.include_router(users.router)

