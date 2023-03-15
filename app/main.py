from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Session

from config import settings
from users.routes import user_router
from recipies.routes import ingredient_router

app = FastAPI()

app.include_router(user_router)
app.include_router(ingredient_router)

engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()