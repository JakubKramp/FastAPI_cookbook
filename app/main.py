from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.middleware.authentication import AuthenticationMiddleware

from app.middleware import JWTAuthBackend
from app.utils.db import engine
from auth.routes import user_router
from recipies.routes import ingredient_router


app = FastAPI()

app.include_router(user_router)
app.include_router(ingredient_router)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
