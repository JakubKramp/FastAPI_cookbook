import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.main import app
from app.utils.db import get_session, Base
from config import settings



@pytest_asyncio.fixture(name="session", scope="function", autouse=True)
async def session_fixture(engine):
    async with AsyncSession(engine) as session:
        yield session
        # truncate all tables after each test
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

@pytest_asyncio.fixture(name="engine", scope="function")
async def db_engine():
    engine = create_async_engine(settings.TEST_DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(name="db", scope="function", autouse=True)
async def database_setup(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



from httpx import AsyncClient, ASGITransport

@pytest_asyncio.fixture(name="client")
async def client_fixture(engine):
    async with AsyncSession(engine) as session:
        async def get_session_override():
            yield session

        app.dependency_overrides[get_session] = get_session_override

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client

        await session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

    app.dependency_overrides.clear()

@pytest_asyncio.fixture(name="session")
async def session_fixture(engine):
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()