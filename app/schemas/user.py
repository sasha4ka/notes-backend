from pydantic import BaseModel, field_validator
from typing import Optional


class User_Read(BaseModel):
    id: int
    name: str
    email: str


class User_Registration(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("password")
    def password_rules(cls, v: str) -> str:
        b_len = len(v.encode("utf-8"))
        if b_len > 72:
            raise ValueError("password must be at most 72 bytes (UTF-8)")
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v


class User_Login(BaseModel):
    email: str
    password_hash: str


class User_Update(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
