from sqlmodel import Session, create_engine

from config.settings import Settings


engine = create_engine(Settings().DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
