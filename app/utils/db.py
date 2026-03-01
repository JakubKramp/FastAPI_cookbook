from types import AsyncGeneratorType

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.main import engine


async def get_session() -> AsyncGeneratorType:
    async with AsyncSession(engine) as session:
        yield session


class Base(DeclarativeBase):
    pass
