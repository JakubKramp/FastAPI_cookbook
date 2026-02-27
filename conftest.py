import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.main import app
from app.utils.db import Base, get_session
from auth.tests.conftest import *
from config import settings


@pytest_asyncio.fixture(name="engine", scope="function")
async def db_engine():
    # connect to default postgres db to create test db
    default_url = settings.TEST_DATABASE_URL.replace("/test_db", "/postgres")
    default_engine = create_async_engine(default_url, isolation_level="AUTOCOMMIT")

    async with default_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1 FROM pg_database WHERE datname='test_db'"))
        if not result.scalar():
            await conn.execute(text("CREATE DATABASE test_db"))

    await default_engine.dispose()

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
