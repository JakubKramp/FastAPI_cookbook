from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import create_engine, SQLModel

from config import settings
from users.routes import user_router
from recipies.routes import ingredient_router

app = FastAPI()

app.include_router(user_router)
app.include_router(ingredient_router)

engine = create_engine(settings.DATABASE_URL, echo=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


create_db_and_tables()


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
