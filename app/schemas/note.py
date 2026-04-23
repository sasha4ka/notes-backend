from pydantic import BaseModel, Field
from typing import Optional


class Note_Read(BaseModel):
    id: int
    author_id: int
    title: str
    content: str


class Note_Create(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=8000)


class Note_Update(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = Field(None, max_length=8000)
