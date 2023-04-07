import pytest
import requests

from sqlalchemy_utils import create_database, drop_database
from sqlmodel import create_engine, SQLModel, Session
from starlette.testclient import TestClient

from app.main import app
from app.utils.db import get_session
from app.utils.tests import MockResponse
from config import settings
from recipies.tests.test_data import (
    example_ingredient,
    example_ingredient_api_response,
    example_create_dish,
)


@pytest.fixture(name="engine", scope="session")
def db_engine():
    engine = create_engine(settings.TEST_DATABASE_URL)
    yield engine


@pytest.fixture(name="db", scope="session", autouse=True)
def database_setup(engine):
    create_database(engine.url)
    SQLModel.metadata.create_all(engine)
    yield
    drop_database(engine.url)


@pytest.fixture(name="session", scope="function", autouse=True)
def session_fixture(engine):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


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


def get_example_ingredient(*args, **kwargs):
    r = MockResponse(json_data=example_ingredient_api_response.copy(), status_code=200)
    return r


@pytest.fixture(scope="function", autouse=True)
def mock_nutrition_api(monkeypatch):
    monkeypatch.setattr(requests, "get", get_example_ingredient)


@pytest.fixture(name="create_dish")
def create_dish_fixture():
    return example_create_dish
