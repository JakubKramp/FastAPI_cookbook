import pytest

from auth.models import User


@pytest.mark.asyncio
async def test_login_wrong_password(user: User):
    assert str(user) == "User(id=1, name='testuser')"