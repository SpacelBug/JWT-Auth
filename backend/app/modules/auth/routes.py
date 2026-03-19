from fastapi import APIRouter, Depends, Request, Response

from typing import List

from app.db.session import get_db

from app.modules.auth.schemas import UserLogin, UserBase, DeviceResponse
from app.modules.auth.services import AuthService
from app.modules.auth.dependencies import get_current_user

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/login")
async def login(
    request: Request, response: Response, user: UserLogin, db=Depends(get_db)
):
    device_uuid = request.cookies.get("device_uuid")
    user_agent = request.headers.get("User-Agent")
    last_ip = request.client.host

    access_token, refresh_token, device_uuid = AuthService.login(
        user, device_uuid, user_agent, last_ip, db
    )

    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", refresh_token)
    response.set_cookie("device_uuid", device_uuid)

    return {"Message": "Successful login"}


@auth.post("/refresh")
async def refresh(request: Request, response: Response, db=Depends(get_db)):
    device_uuid = request.cookies.get("device_uuid")
    refresh_token = request.cookies.get("refresh_token")

    access_token, refresh_token = AuthService.refresh(refresh_token, device_uuid, db)

    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", refresh_token)


@auth.post("/logout")
async def logout(request: Request, response: Response, db=Depends(get_db)):
    AuthService.logout(request.cookies.get("device_uuid"), db)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"Message": "Successful logout"}


@auth.post("/logout/all")
async def logout_all(response: Response, user: UserBase = Depends(get_current_user), db=Depends(get_db)):
    AuthService.logout_all(user.id, db)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"Message": "Successful logout"}


@auth.post("/hasher")
async def hasher(data: str, user: UserBase = Depends(get_current_user)):
    from app.modules.auth.services import pwd_context

    return pwd_context.hash(data)


@auth.post("/registration")
async def registration():
    pass


@auth.get("/user", response_model=UserBase)
async def user(user: UserBase = Depends(get_current_user)):
    return user


@auth.get("/devices", response_model=List[DeviceResponse])
async def devices(user: UserBase = Depends(get_current_user), db=Depends(get_db)):
    return AuthService.get_devices(user.id, db)
