from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.users import router as users_router
from app.api.v1.notes import router as notes_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer(bearerFormat="JWT", description="Enter: Bearer <token>")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(notes_router)
