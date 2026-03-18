from fastapi import FastAPI

from app.exceptions.exception_handler import register_exception_handlers

from app.modules.auth.routes import auth

app = FastAPI()

register_exception_handlers(app)

app.include_router(auth)
