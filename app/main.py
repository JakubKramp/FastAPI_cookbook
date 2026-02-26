from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app.utils.db import Base
from auth.routes import user_router
from config import settings
from fridge.routes import fridge_router
from recipes.routes import ingredient_router

engine = create_async_engine(settings.DATABASE_URL)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI()


routers = [fridge_router, user_router, ingredient_router]

for router in routers:
    app.include_router(router)
