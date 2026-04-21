from pydantic import BaseModel
from typing import Optional


class Note_Read(BaseModel):
    id: int
    author_id: int
    title: str
    content: str


class Note_Create(BaseModel):
    author_id: int
    title: str
    content: str


class Note_Update(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
