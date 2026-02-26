from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from app.security import get_password_hash
from auth.models import Profile, User
from auth.schemas import DietaryReferenceIntakes

from auth.tests.test_data import profile, dri_data


@pytest_asyncio.fixture(name="user")
async def create_user_fixture(session) -> User:
    user = User(username="testuser", password=get_password_hash("test_password"), email="testemail@test.com")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@pytest_asyncio.fixture(name="profile_data")
async def profile_data() -> dict[str, str | int| bool]:
    return profile.copy()

@pytest.fixture(autouse=True)
def mock_dri_client():
    with patch("auth.routes.DRIClient") as mock:
        instance = mock.return_value
        instance.fill_profile = AsyncMock()
        yield instance

@pytest_asyncio.fixture(name="profile")
async def create_user__with_profile_fixture(user, session) -> Profile:
    db_profile = Profile(**profile, user_id=user.id)
    session.add(db_profile)
    await session.commit()
    await session.refresh(db_profile)
    return db_profile

@pytest_asyncio.fixture(name="dri_data")
async def create_dri_data(user, session) -> DietaryReferenceIntakes:
    mock_dri_data = DietaryReferenceIntakes(**dri_data)
    return mock_dri_data
