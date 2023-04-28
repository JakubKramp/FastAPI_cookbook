from sqlalchemy.orm import sessionmaker, scoped_session
from sqlmodel import Session, create_engine

from config import settings


engine = create_engine(settings.DATABASE_URL)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def get_session():
    return Session
