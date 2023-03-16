from typing import Optional

import requests
from sqlalchemy import UniqueConstraint
from sqlalchemy.event import listens_for
from sqlmodel import Field, SQLModel, Session

from users.routes import get_session
from config import settings


class Ingredient(SQLModel, table=True):
    """
    Nutritional values by default refer to 100g serving.
    """

    __table_args__ = (UniqueConstraint("name"),)
    id: int | None = Field(default=None, primary_key=True)
    name: str
    calories: Optional[float]
    fat_total: Optional[float]
    fat_saturated: Optional[float]
    protein: Optional[float]
    sodium: Optional[float]
    potassium: Optional[float]
    cholesterol: Optional[float]
    carbohydrates_total: Optional[float]
    fiber: Optional[float]
    sugar: Optional[float]


class CreateIngredient(SQLModel):
    name: str


class ListIngredient(CreateIngredient):
    calories: Optional[float]
    fat_total: Optional[float]
    protein: Optional[float]
    carbohydrates_total: Optional[float]


class UpdateIngredient(ListIngredient):
    fat_saturated: Optional[float]
    sodium: Optional[float]
    potassium: Optional[float]
    cholesterol: Optional[float]
    fiber: Optional[float]
    sugar: Optional[float]


@listens_for(Ingredient, "before_insert")
def set_nutritional_values(mapper, connection, target):
    response = requests.get(
        settings.NUTRITION_API_URL,
        params={"query": target.name},
        headers={"X-Api-Key": settings.NUTRITION_APIKEY},)
    nutrition_data = response.json()[0]
    nutrition_data.pop("name")
    nutrition_data.pop("serving_size_g")
    for key, value in nutrition_data.items():
        if key.find("_") >= 0:
            key = "_".join(key.split("_")[:-1])
        target.__setattr__(key, value)
