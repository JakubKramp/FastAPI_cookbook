from functools import lru_cache

from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel

from config.settings import Settings
from auth.routes import user_router
from recipes.routes import ingredient_router

app = FastAPI()

app.include_router(user_router)
app.include_router(ingredient_router)

engine = create_engine(Settings().DATABASE_URL)

@lru_cache
def get_settings():
    return Settings()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
