from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, SQLModel

class Ingredient(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("name"),)
    id: int | None = Field(default=None, primary_key=True)
    name: str


class IngredientDetail(SQLModel):
    name: str