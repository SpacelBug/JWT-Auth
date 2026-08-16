from fastapi import Depends, Request

from app.db.session import get_db
from backend.app.services import AuthService


def get_current_user(request: Request, db=Depends(get_db)):
    token_payload = AuthService.verify_token(request.cookies.get("access_token"))
    return AuthService.get_user(token_payload["sub"], db)
