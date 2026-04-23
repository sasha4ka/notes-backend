from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_active_user
from app.core.exceptions import UserAlreadyExistsError
from app.db.session import get_db
from app.crud.user import change_password, create_user, get_user, get_users, update_user, delete_user, get_user_by_email
from app.schemas.user import User_Change_Password, User_Login, User_Read, User_Registration, User_Update
from app.schemas.token import Token
from app.core.password import verify_password
from app.core.auth import create_access_token


router = APIRouter(prefix="/v1/users", tags=["users"])


@router.post("/login", response_model=Token)
async def login_user_endpoint(user: User_Login, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    token_version = db_user.token_version if db_user.token_version is not None else 0
    access_token = create_access_token(data={"sub": db_user.email}, token_version=token_version)
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
    current_user: User_Read = Depends(get_current_active_user)
):
    return await get_users(db, skip, limit)


@router.get("/me", response_model=User_Read)
async def read_current_user_endpoint(current_user: User_Read = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=User_Read)
async def update_user_endpoint(
    user_update: User_Update,
    user: User_Read = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if user_update.is_active is not None and not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can change active status")
    user = await update_user(db, user.id, user_update)
    return user


@router.delete("/me")
async def delete_user_endpoint(
    user: User_Read = Depends(get_current_active_user),
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
    current_user: User_Read = Depends(get_current_active_user)
):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User_Read)
async def update_user_by_id_endpoint(
    user_id: int,
    user_update: User_Update,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    if user_update.is_active is not None and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can change active status")
    user = await update_user(db, user_id, user_update)
    return user


@router.delete("/{user_id}")
async def delete_user_by_id_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.post("/me/change-password")
async def change_password_endpoint(
    password_change: User_Change_Password,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    return await change_password(db, current_user.id, password_change)


@router.post("/{user_id}/change-password")
async def change_password_by_id_endpoint(
    user_id: int,
    password_change: User_Change_Password,
    db: AsyncSession = Depends(get_db),
    current_user: User_Read = Depends(get_current_active_user)
):
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to change this user's password")
    return await change_password(db, user_id, password_change)
