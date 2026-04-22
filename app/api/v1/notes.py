from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.dependencies import get_current_active_user
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.note import create_note, get_note, get_notes, get_notes_by_author, update_note, delete_note
from app.schemas.note import Note_Create, Note_Read, Note_Update
from app.schemas.user import User_Read


router = APIRouter(prefix="/v1/notes", tags=["notes"])


@router.get("/", response_model=list[Note_Read])
async def read_notes_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    return await get_notes(db)


@router.get("/by_author/{author_id}", response_model=list[Note_Read])
async def read_notes_by_author_endpoint(
    author_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    return await get_notes_by_author(db, author_id)


@router.get("/{note_id}", response_model=Note_Read)
async def read_note_endpoint(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    note = await get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}")
async def put_note_endpoint(
    note_id: int,
    note_update: Note_Update,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    note = await get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this note")
    note = await update_note(db, note_id, note_update)
    return note


@router.delete("/{note_id}")
async def delete_note_endpoint(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    note = await get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    if not await delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Note not found")


@router.post("/", response_model=Note_Read)
async def post_note_endpoint(
    note_create: Note_Create,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    return await create_note(db, note_create, current_user.id)
