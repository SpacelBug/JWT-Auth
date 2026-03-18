from datetime import datetime
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    exp: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserBase(BaseModel):
    id: int
    email: str
    login: str


class DeviceResponse(BaseModel):
    device_uuid: str
    name: str | None = None
    user_agent: str | None = None
    last_ip: str | None = None
    created_at: datetime
    last_seen_at: datetime | None = None
