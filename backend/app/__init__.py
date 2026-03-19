import os
import signal

from fastapi import FastAPI

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.exceptions.exception_handler import register_exception_handlers

from app.modules.auth.routes import auth

from app.db.session import engine

app = None

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(auth)
except OperationalError:
    print("Have no connection to database\n")

    pid = os.getppid()
    os.kill(pid, signal.SIGINT)
