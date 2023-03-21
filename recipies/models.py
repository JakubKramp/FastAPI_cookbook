from typing import Optional, List

import requests
from sqlalchemy import UniqueConstraint
from sqlalchemy.event import listens_for
from sqlmodel import Field, SQLModel, Relationship
from config import settings


class NutritionalValues(SQLModel):
    calories: Optional[float] = 0.0
    fat_total: Optional[float] = 0.0
    fat_saturated: Optional[float] = 0.0
    protein: Optional[float] = 0.0
    sodium: Optional[float] = 0.0
    potassium: Optional[float] = 0.0
    cholesterol: Optional[float] = 0.0
    carbohydrates_total: Optional[float] = 0.0
    fiber: Optional[float] = 0.0
    sugar: Optional[float] = 0.0

    class Config:
        schema_extra = {
            "example": {
                "calories": 34,
                "fat_total": 0.2,
                "fat_saturated": 0,
                "protein": 0.8,
                "sodium": 57,
                "potassium": 30,
                "cholesterol": 0,
                "carbohydrates_total": 8.3,
                "fiber": 3,
                "sugar": 3.4,
            }
        }


class Ingredient(NutritionalValues, table=True):
    """
    Nutritional values by default refer to 100g serving.
    """

    __table_args__ = (UniqueConstraint("name"),)
    id: int | None = Field(default=None, primary_key=True)
    name: str
    ingredient_items: List["IngredientItem"] = Relationship(back_populates="ingredient")

    class Config:
        schema_extra = {
            "example": {
                "id": 72,
                "name": "carrot",
                "calories": 34,
                "fat_total": 0.2,
                "fat_saturated": 0,
                "protein": 0.8,
                "sodium": 57,
                "potassium": 30,
                "cholesterol": 0,
                "carbohydrates_total": 8.3,
                "fiber": 3,
                "sugar": 3.4,
            }
        }


class CreateIngredient(SQLModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "carrot",
            }
        }


class ListIngredient(CreateIngredient):
    calories: Optional[float]
    fat_total: Optional[float]
    protein: Optional[float]
    carbohydrates_total: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "name": "carrot",
                "calories": 34,
                "fat_total": 0.2,
                "protein": 0.8,
                "carbohydrates_total": 8.3,
            }
        }


class UpdateIngredient(ListIngredient):
    fat_saturated: Optional[float]
    sodium: Optional[float]
    potassium: Optional[float]
    cholesterol: Optional[float]
    fiber: Optional[float]
    sugar: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "name": "carrot",
                "calories": 34,
                "fat_total": 0.2,
                "fat_saturated": 0,
                "protein": 0.8,
                "sodium": 57,
                "potassium": 30,
                "cholesterol": 0,
                "carbohydrates_total": 8.3,
                "fiber": 3,
                "sugar": 3.4,
            }
        }


@listens_for(Ingredient, "before_insert")
def set_nutritional_values(mapper, connection, target):
    response = requests.get(
        settings.NUTRITION_API_URL,
        params={"query": target.name},
        headers={"X-Api-Key": settings.NUTRITION_APIKEY},
    )
    nutrition_data = response.json()[0]
    nutrition_data.pop("name")
    nutrition_data.pop("serving_size_g")
    for key, value in nutrition_data.items():
        if key.find("_") >= 0:
            key = "_".join(key.split("_")[:-1])
        target.__setattr__(key, value)


class Dish(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ingredients: List["IngredientItem"] = Relationship(back_populates="dish")
    name: str
    recipe: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 72,
                "name": "Mashed potatoes",
                "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
                "ingredients": [
                    {
                        "amount": 700,
                        "ingredient": {"name": "potato"},
                    },
                    {
                        "amount": 300,
                        "ingredient": {"name": "butter"},
                    },
                ],
            }
        }


class CreateIngredientItem(SQLModel):
    ingredient: CreateIngredient
    amount: int


class CreateDish(SQLModel):
    name: str
    recipe: Optional[str]
    ingredients: List[CreateIngredientItem]

    class Config:
        schema_extra = {
            "example": {
                "id": 72,
                "name": "Mashed potatoes",
                "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
                "ingredients": [
                    {
                        "amount": 700,
                        "ingredient": {"name": "potato"},
                    },
                    {
                        "amount": 300,
                        "ingredient": {"name": "butter"},
                    },
                ],
            }
        }


class ListIngredientItem(SQLModel):
    amount: int
    ingredient: CreateIngredient


class ListDish(SQLModel):
    id: int
    name: str
    recipe: Optional[str]
    ingredients: List[ListIngredientItem]

    class Config:
        schema_extra = {
            "example": {
                "id": 72,
                "name": "Mashed potatoes",
                "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
                "ingredients": [
                    {
                        "amount": 700,
                        "ingredient": {"name": "potato"},
                    },
                    {
                        "amount": 300,
                        "ingredient": {"name": "butter"},
                    },
                ],
            }
        }


class DishDetail(ListDish):
    nutritional_values: NutritionalValues

    class Config:
        schema_extra = {
            "example": {
                "name": "Mashed potatoes",
                "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
                "ingredients": [
                    {
                        "amount": 700,
                        "ingredient": {"name": "potato"},
                    },
                    {
                        "amount": 300,
                        "ingredient": {"name": "butter"},
                    },
                ],
            }
        }


class IngredientItem(SQLModel, table=True):
    """
    This model is a proxy between Ingredient and Recipe, allowing us to set amount of produce for each dish.
    Amount is in grams.
    """

    id: int | None = Field(default=None, primary_key=True)
    ingredient_id: Optional[int] = Field(default=None, foreign_key="ingredient.id")
    ingredient: Optional["Ingredient"] = Relationship(back_populates="ingredient_items")
    dish_id: Optional[int] = Field(default=None, foreign_key="dish.id")
    dish: Optional[Dish] = Relationship(back_populates="ingredients")
    amount: int
