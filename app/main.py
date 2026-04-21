from fastapi import FastAPI
from app.api.v1.users import router as users_router
from app.api.v1.notes import router as notes_router

app = FastAPI()

app.include_router(users_router)
app.include_router(notes_router)
