from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel

from config import settings
from users.routes import user_router
from recipies.routes import ingredient_router

app = FastAPI()

app.include_router(user_router)
app.include_router(ingredient_router)
database_url = settings.DATABASE_URL

engine = create_engine(database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()