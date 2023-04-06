from unittest import mock
from unittest.mock import patch

import pytest
from requests.cookies import MockResponse

from sqlalchemy_utils import create_database, drop_database
from sqlmodel import create_engine, SQLModel, Session
from fastapi.testclient import TestClient

from app.main import app
from app.utils import get_session
from config import settings
from recipies.tests.test_data import example_ingredient


@pytest.fixture(name="session", scope="session")
def session_fixture():
    engine = create_engine(settings.TEST_DATABASE_URL)
    create_database(engine.url)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    drop_database(engine.url)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="ingredient")
def ingredient_fixture():
    return example_ingredient


@pytest.fixture
def mock_nutrition_api(monkeypatch):
    def mock_response():
        return example_ingredient

    monkeypatch.setattr("requests.get", lambda url: MockResponse(mock_response()))
