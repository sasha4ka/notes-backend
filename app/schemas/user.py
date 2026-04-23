from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class User_Read(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    @classmethod
    def from_orm(cls, obj):
        return cls(id=obj.id, name=obj.name, email=obj.email, is_active=obj.is_active, is_admin=obj.is_admin)


class User_Registration(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr = Field(..., max_length=255)
    password: str

    @field_validator("password")
    def password_rules(cls, v: str) -> str:
        b_len = len(v.encode("utf-8"))
        if b_len > 72:
            raise ValueError("password must be at most 72 bytes (UTF-8)")
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        if v.isascii():
            raise ValueError("password must contain at least one non-ASCII character")
        if v == v.lower() or v == v.upper():
            raise ValueError("password must contain both uppercase and lowercase characters")
        return v


class User_Login(BaseModel):
    email: str = Field(..., max_length=255)
    password: str


class User_Update(BaseModel):
    name: Optional[str] = Field(..., max_length=255)
    is_active: Optional[bool] = None


class User_Change_Password(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    def password_rules(cls, v: str) -> str:
        b_len = len(v.encode("utf-8"))
        if b_len > 72:
            raise ValueError("password must be at most 72 bytes (UTF-8)")
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        if v.isascii():
            raise ValueError("password must contain at least one non-ASCII character")
        if v == v.lower() or v == v.upper():
            raise ValueError("password must contain both uppercase and lowercase characters")
        return v
