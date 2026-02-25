import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.security import get_password_hash
from auth.models import User

@pytest_asyncio.fixture(name="user")
async def create_user_fixture(engine) -> User:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        user = User(username="testuser", password=get_password_hash("test_password"), email="testemail@test.com")
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user  # session closed, user attributes already loaded