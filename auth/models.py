from sqlalchemy import String, Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    username: str = Field(sa_column=Column("username", String, unique=True))
    password: str


class UserDetail(SQLModel):
    email: str
    password: str
    username: str

    class Config:
        schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }


class UserList(SQLModel):
    id: int
    email: str
    username: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "jeff.spicoli@labeouf.com",
                "username": "jeffS",
            }
        }
