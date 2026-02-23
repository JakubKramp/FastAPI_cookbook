from typing import Any, Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlmodel import Session

from config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)


def get_session() -> Generator[Session, Any, None]:
    with AsyncSession(engine) as session:
        yield session

class Base(DeclarativeBase):
    pass