from typing import List, Optional

from pydantic import BaseModel

from recipes.tests.test_data import example_ingredient


class NutritionalValues(BaseModel):
    calories: float = 0.0
    fat_total: float = 0.0
    protein: float = 0.0
    sodium: float = 0.0
    potassium: float = 0.0
    fiber: float = 0.0
    carbohydrates_total: float = 0.0
    sugar: float = 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "calories": 34,
                "fat_total": 0.2,
                "protein": 0.8,
                "sodium": 57,
                "potassium": 30,
                "fiber": 3,
                "carbohydrates_total": 8.3,
                "sugar": 3.4,
            }
        }


class CreateIngredient(BaseModel):
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "carrot",
            }
        }


class ListIngredient(CreateIngredient, NutritionalValues):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "carrot",
                "calories": 34,
                "fat_total": 0.2,
                "protein": 0.8,
                "sodium": 57,
                "potassium": 30,
                "fiber": 3,
                "carbohydrates_total": 8.3,
                "sugar": 3.4,
            }
        }


class UpdateIngredient(CreateIngredient):
    calories: Optional[float] | None = None
    fat_total: Optional[float] | None = None
    protein: Optional[float] | None = None
    carbohydrates_total: Optional[float] | None = None
    fat_saturated: Optional[float] | None = None
    sodium: Optional[float] | None = None
    potassium: Optional[float] | None = None
    cholesterol: Optional[float] | None = None
    fiber: Optional[float] | None = None
    sugar: Optional[float] | None = None

    class Config:
        json_schema_extra = {"example": example_ingredient}


class CreateIngredientItem(BaseModel):
    name: str
    amount: int


class CreateDish(BaseModel):
    name: str
    recipe: Optional[str]
    ingredients: List[CreateIngredientItem]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 72,
                "name": "Mashed potatoes",
                "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
                "ingredients": [
                    {
                        "amount": 700,
                        "name": "potato",
                    },
                    {
                        "amount": 300,
                        "name": "butter",
                    },
                ],
            }
        }


class ListIngredientItem(BaseModel):
    amount: int
    ingredient: CreateIngredient


class ListDish(BaseModel):
    id: int
    name: str
    recipe: Optional[str]
    ingredients: List[ListIngredientItem]

    class Config:
        json_schema_extra = {
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
    nutritional_values: NutritionalValues | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mashed potatoes",
                "recipe": "Mash the potatoes along with the butter. Eat the mashed potatoes",
                "ingredients": [{"amount": 700, "name": "potato"}, {"amount": 300, "name": "butter"}],
                "nutritional_values": {
                    "calories": 3339,
                    "fat_total": 315.04,
                    "protein": 27.23,
                    "sodium": 1533,
                    "potassium": 1533,
                    "fiber": 10.5,
                    "carbohydrates_total": 94.43,
                    "sugar": 10.36,
                },
            }
        }
