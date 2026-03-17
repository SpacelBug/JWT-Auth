from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{environ.get('DATABASE_LOGIN')}:{environ.get('DATABASE_PASSWORD')}@{environ.get('DATABASE_HOST')}:{environ.get('DATABASE_PORT')}/{environ.get('DATABASE_NAME')}"
)

session_maker = sessionmaker()


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
