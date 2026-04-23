from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.exceptions import UserAlreadyExistsError
from app.core.password import hash_password, verify_password
from app.db.models.user import User
from app.schemas.user import User_Change_Password, User_Read, User_Registration, User_Update


async def create_user(db: AsyncSession, user: User_Registration) -> User:
    q = await db.execute(select(User).where(User.email == user.email))
    existing_user = q.scalar_one_or_none()
    if existing_user:
        raise UserAlreadyExistsError("Email already registered")
    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=1
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int) -> User_Read | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user_update: User_Update) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def increment_user_token_version(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    db_user.token_version += 1
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_token_version(db: AsyncSession, user_id: int) -> int | None:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    return db_user.token_version


async def set_user_admin_status(db: AsyncSession, user_id: int, is_admin: bool) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    db_user.is_admin = is_admin
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def is_user_admin(db: AsyncSession, user_id: int) -> bool | None:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    return db_user.is_admin


async def set_user_active_status(db: AsyncSession, user_id: int, is_active: bool) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    db_user.is_active = is_active
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False


async def change_password(db: AsyncSession, user_id: int, password_change: User_Change_Password) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return False
    if not verify_password(password_change.old_password, db_user.hashed_password):
        return False
    db_user.hashed_password = hash_password(password_change.new_password)
    db_user.token_version = db_user.token_version + 1
    await db.commit()
    await db.refresh(db_user)
    return True
