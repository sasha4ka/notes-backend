import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_async,
    pool_size=5,
    max_overflow=10
)


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def main():
    async with async_session() as session:
        t = text("SELECT VERSION()")
        res = await session.execute(t)
    print(res.fetchone())

asyncio.run(main())
