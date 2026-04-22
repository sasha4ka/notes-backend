from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import decode_access_token
from app.crud.user import get_user_by_email
from app.db.session import get_db
from app.schemas.user import User_Read


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User_Read:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    email: str | None = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return User_Read.from_orm(user)


async def get_current_active_user(current_user: User_Read = Depends(get_current_user)) -> User_Read:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user
