import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv


load_dotenv()

user_db = os.environ.get('USER_DB')
password_db = os.environ.get('PASSWORD_DB')
url_db = os.environ.get('URL_DB')
port_db = os.environ.get('PORT_DB')
schema_db = os.environ.get('SCHEMA_DB')


URL_DATABASE = f'mysql+pymysql://{user_db}:{password_db}@{url_db}:{port_db}/{schema_db}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
