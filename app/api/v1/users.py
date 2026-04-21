from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.core.exceptions import UserAlreadyExistsError
from app.db.session import get_db
from app.crud.user import create_user, get_user, get_users, update_user, delete_user, get_user_by_email
from app.schemas.user import User_Login, User_Read, User_Registration, User_Update
from app.schemas.token import Token
from app.core.password import verify_password
from app.core.auth import create_access_token


router = APIRouter(prefix="/v1/users", tags=["users"])


@router.post("/login", response_model=Token)
async def login_user_endpoint(user: User_Login, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User_Read)
async def create_user_endpoint(user_create: User_Registration, db: AsyncSession = Depends(get_db)):
    try:
        return await create_user(db, user_create)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Email already registered")


@router.get("/", response_model=list[User_Read])
async def read_users_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_user)
):
    return await get_users(db, skip, limit)


@router.get("/me", response_model=User_Read)
async def read_current_user_endpoint(current_user: User_Read = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=User_Read)
async def update_user_endpoint(
    user_update: User_Update,
    user: User_Read = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await update_user(db, user.id, user_update)
    return user


@router.delete("/me")
async def delete_user_endpoint(
    user: User_Read = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    success = await delete_user(db, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.get("/{user_id}", response_model=User_Read)
async def read_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_user)
):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
