from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.user import create_user, get_user, get_users, update_user, delete_user
from app.schemas.user import User_Read, User_Registration, User_Update


router = APIRouter(prefix="/v1/users")


@router.get("/", response_model=list[User_Read])
async def read_users_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_users(db, skip, limit)


@router.get("/{user_id}", response_model=User_Read)
async def read_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User_Read)
async def create_user_endpoint(user_create: User_Registration, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_create)


@router.put("/{user_id}", response_model=User_Read)
async def update_user_endpoint(user_id: int, user_update: User_Update, db: AsyncSession = Depends(get_db)):
    user = await update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
