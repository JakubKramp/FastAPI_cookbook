import pytest
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

@pytest_asyncio.fixture(name="profile_data")
async def profile_data() -> dict[str, str | int| bool]:
    return {
        "sex": "Male",
        "age": 30,
        "height": 180,
        "weight": 80,
        "activity_factor": "Little/no exercise",
        "smoking": True,
    }

from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_dri_client():
    with patch("auth.routes.DRIClient") as mock:
        instance = mock.return_value
        instance.fill_profile = AsyncMock()
        yield instance