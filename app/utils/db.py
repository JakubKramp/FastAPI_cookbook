from types import AsyncGeneratorType

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)


async def get_session() -> AsyncGeneratorType:
    async with AsyncSession(engine) as session:
        yield session

class Base(DeclarativeBase):
    pass