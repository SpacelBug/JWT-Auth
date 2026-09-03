from fastapi import APIRouter, Depends, Request, Response

from typing import List

from app.db.session import get_db

from app.schemas import (
    UserLogin,
    UserBase,
    DeviceResponse,
    RefreshTokenResponse,
)
from app.services import AuthService
from app.dependencies import get_current_user

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/login")
def login(request: Request, response: Response, user: UserLogin, db=Depends(get_db)):
    device_uuid = request.cookies.get("device_uuid")
    user_agent = request.headers.get("User-Agent")
    last_ip = request.client.host

    access_token, refresh_token, device_uuid = AuthService.login(
        user, device_uuid, user_agent, last_ip, db
    )

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    response.set_cookie("device_uuid", device_uuid, httponly=True)

    return {"Message": "Successful login"}


@auth.post("/refresh")
def refresh(request: Request, response: Response, db=Depends(get_db)):
    device_uuid = request.cookies.get("device_uuid")
    refresh_token = request.cookies.get("refresh_token")

    access_token, refresh_token = AuthService.refresh(refresh_token, device_uuid, db)

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)


@auth.post("/logout")
def logout(request: Request, response: Response, db=Depends(get_db)):
    AuthService.logout(request.cookies.get("device_uuid"), db)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"Message": "Successful logout"}


@auth.post("/logout/all")
def logout_all(
    response: Response, user: UserBase = Depends(get_current_user), db=Depends(get_db)
):
    AuthService.logout_all(user.id, db)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("device_uuid")

    return {"Message": "Successful logout"}


@auth.post("/logout/{device_id}")
def logout_device(
    response: Response,
    device_id,
    _: UserBase = Depends(get_current_user),
    db=Depends(get_db),
):
    AuthService.logout_device(device_id, db)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("device_uuid")

    return {"Message": "Successful logout"}


@auth.post("/revoke/{token_id}")
def revoke_token(
    token_id: int, user: UserBase = Depends(get_current_user), db=Depends(get_db)
):
    pass


@auth.post("/hasher")
def hasher(data: str, user: UserBase = Depends(get_current_user)):
    from app.services import pwd_context

    return pwd_context.hash(data)


@auth.post("/registration")
def registration():
    pass


@auth.get("/user", response_model=UserBase)
def user(user: UserBase = Depends(get_current_user)):
    return user


@auth.get("/devices", response_model=List[DeviceResponse])
def devices(
    request: Request, user: UserBase = Depends(get_current_user), db=Depends(get_db)
):
    return AuthService.get_devices(request.cookies.get("device_uuid"), user.id, db)


@auth.get("/tokens", response_model=List[RefreshTokenResponse])
def tokens(request: Request, _=Depends(get_current_user), db=Depends(get_db)):
    return AuthService.get_tokens(db)
