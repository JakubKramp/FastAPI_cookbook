import pytest

from app.security import get_password_hash
from auth.models import User


@pytest.fixture(name="user")
def create_user_fixture(session):
    password = "test_password"
    hashed_password = get_password_hash(password)
    user = User(
        username="testuser", password=hashed_password, email="testemail@test.com"
    )
    session.add(user)
    session.commit()
    return user
