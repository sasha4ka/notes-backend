from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.v1.users import router as users_router
from app.api.v1.notes import router as notes_router

app = FastAPI()

bearer_scheme = HTTPBearer(bearerFormat="JWT", description="Enter: Bearer <token>")

app.include_router(users_router)
app.include_router(notes_router)
