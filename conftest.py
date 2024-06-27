import pytest
from sqlalchemy_utils import create_database, drop_database
from sqlmodel import create_engine, SQLModel, Session
from starlette.testclient import TestClient

from app.main import app
from app.utils.db import get_session
from config.settings import Settings


@pytest.fixture(name="engine", scope="session")
def db_engine():
    engine = create_engine(Settings().TEST_DATABASE_URL)
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
