from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


class User_Registration(BaseModel):
    name: str
    email: str
    password: str


class User_Login(BaseModel):
    email: str
    password_hash: str
