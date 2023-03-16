from sqlalchemy import String, Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str


class UserDetail(SQLModel):
    email: str
    password: str
