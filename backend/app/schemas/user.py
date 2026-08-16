from pydantic import BaseModel


class UserLogin(BaseModel):
    login: str
    password: str


class UserBase(BaseModel):
    id: int
    email: str
    login: str
