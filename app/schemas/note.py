from pydantic import BaseModel


class Note(BaseModel):
    id: int
    author_id: int
    title: str
    content: str


class Note_Create(BaseModel):
    author_id: int
    title: str
    content: str


class Note_Update(BaseModel):
    title: str
    content: str
