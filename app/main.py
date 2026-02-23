from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app.utils.db import Base
from config import settings
from auth.routes import user_router
from recipes.routes import ingredient_router

app = FastAPI()

app.include_router(user_router)
app.include_router(ingredient_router)

engine = create_async_engine(settings.DATABASE_URL)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
