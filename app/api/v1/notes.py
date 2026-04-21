from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.note import create_note, get_note, get_notes, get_notes_by_author, update_note, delete_note
from app.schemas.note import Note_Create, Note_Read, Note_Update


router = APIRouter(prefix="/v1/notes")


@router.get("/", response_model=list[Note_Read])
async def read_notes_endpoint(db: AsyncSession = Depends(get_db)):
    return await get_notes(db)


@router.get("/by_author/{author_id}", response_model=list[Note_Read])
async def read_notes_by_author_endpoint(author_id: int, db: AsyncSession = Depends(get_db)):
    return await get_notes_by_author(db, author_id)


@router.get("/{note_id}", response_model=Note_Read)
async def read_note_endpoint(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}")
async def put_note_endpoint(note_id: int, note_update: Note_Update, db: AsyncSession = Depends(get_db)):
    note = await update_note(db, note_id, note_update)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}")
async def delete_note_endpoint(note_id: int, db: AsyncSession = Depends(get_db)):
    if not delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Note not found")


@router.post("/", response_model=Note_Read)
async def post_note_endpoint(note_create: Note_Create, db: AsyncSession = Depends(get_db)):
    return await create_note(db, note_create)
