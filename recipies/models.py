from typing import Optional

import requests
from sqlalchemy import UniqueConstraint
from sqlalchemy.event import listens_for
from sqlmodel import Field, SQLModel
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


@listens_for(Ingredient, 'after_insert')
def set_nutritional_values(mapper, connection, target):
    response = requests.get(settings.NUTRITION_API_URL, params={'query': target.name}, headers={'A-Api-Key'})
    print(response)
    response.json()[0].pop('name')
    response.json()[0].pop('serving_size_g')
    for key, value in response.json()[0].items():
        target.__setattr__(key.strip('_mg'), value)
