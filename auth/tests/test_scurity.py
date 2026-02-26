import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.security import get_password_hash, verify_password, get_user, authenticate_user
from auth.models import User


@pytest.mark.asyncio
async def test_password_verification():
    password = 'Example Password'
    password_hash = get_password_hash(password)
    assert verify_password(password, password_hash)

@pytest.mark.asyncio
async def test_get_user(session: AsyncSession):
    user = User(username="test", password="password", email="example@example.com")
    user1 = User(username="test1", password="password1", email="example1@example.com")
    session.add_all([user, user1])
    await session.flush()
    user2 = await get_user(session, user1.username)
    assert user2 == user1