from typing import Optional

from sqlalchemy import select
from app.db.models.note import Note

from app.schemas.note import Note_Create, Note_Update


async def get_notes(db, skip: int = 0, limit: int = 100) -> list[Note]:
    result = await db.execute(select(Note).offset(skip).limit(limit))
    return result.scalars().all()


async def get_notes_by_author(db, author_id: int) -> list[Note]:
    result = await db.execute(select(Note).where(Note.author_id == author_id))
    return result.scalars().all()


async def get_note(db, note_id: int) -> Note:
    result = await db.execute(select(Note).where(Note.id == note_id))
    return result.scalars().first()


async def create_note(db, note_create: Note_Create) -> Note:
    note = Note(
        author_id=note_create.author_id,
        title=note_create.title,
        content=note_create.content
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def update_note(db, note_id: int, note_upd: Note_Update) -> Optional[Note]:
    q = await db.execute(select(Note).where(Note.id == note_id))
    note = q.scalars().first()
    if not note:
        return None
    if note_upd.title:
        note.title = note_upd.title
    if note_upd.content:
        note.content = note_upd.content
    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db, note_id: int) -> bool:
    q = await db.execute(select(Note).where(Note.id == note_id))
    note = q.scalars().first()
    if not q:
        return False
    await db.delete(note)
    await db.commit()
    return True
