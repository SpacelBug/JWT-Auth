from fastapi import FastAPI
from app.modules.auth.routes import auth

app = FastAPI()
app.include_router(auth)
