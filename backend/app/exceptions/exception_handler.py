from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from app.services import AuthError


async def auth_error(request: Request, exc: AuthError):
    return JSONResponse(status_code=401, content=exc.details)


async def signature_expired(request: Request, exc: ExpiredSignatureError):
    return JSONResponse(status_code=401, content="ExpiredSignatureError")


async def signature_invalid(request: Request, exc: InvalidSignatureError):
    return JSONResponse(status_code=401, content="InvalidSignatureError")


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AuthError, auth_error)
    app.add_exception_handler(ExpiredSignatureError, signature_expired)
    app.add_exception_handler(InvalidSignatureError, signature_invalid)
