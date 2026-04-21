from fastapi import FastAPI, HTTPException
from app.schemas.note import Note, Note_Create, Note_Update

app = FastAPI()

notes: list[Note] = []
note_id_counter = 0
users = []
user_id_counter = 0


@app.get("/v1/notes")
def get_notes() -> list[Note]:
    return notes


@app.post("/v1/notes")
def create_note(note: Note_Create) -> Note:
    global note_id_counter
    notes.append(new_note := Note(
        id=note_id_counter,
        author_id=note.author_id,
        title=note.title,
        content=note.content
    ))
    note_id_counter += 1
    return new_note


@app.get("/v1/notes/{note_id}")
def get_note(note_id: int) -> Note:
    for note in notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.put("/v1/notes/{note_id}")
def update_note(note: Note_Update, note_id: int) -> Note:
    for n in notes:
        if n.id == note_id:
            n.title = note.title
            n.content = note.content
            return n
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/v1/notes/{note_id}")
def delete_note(note_id: int):
    for n in notes:
        if n.id == note_id:
            notes.remove(n)
            return
    raise HTTPException(status_code=404, detail="Note not found")
