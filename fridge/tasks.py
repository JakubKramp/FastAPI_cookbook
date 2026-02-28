import asyncio
from datetime import date

from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.celery_app import celery_app
from app.utils.db import engine
from auth.models import Profile, User  # noqa
from config import settings
from fridge.models import Fridge  # noqa
from recipes.models import Ingredient, Product  # noqa

async_session = async_sessionmaker(engine, expire_on_commit=False)


@celery_app.task
def mark_expired_products():
    async def _run():
        print("XDDD")
        engine = create_async_engine(settings.DATABASE_URL)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with async_session() as session:
            await session.execute(
                update(Product).where(Product.expires_on < date.today()).values(marked_for_delete=True)
            )
            await session.commit()

        await engine.dispose()

    asyncio.run(_run())
