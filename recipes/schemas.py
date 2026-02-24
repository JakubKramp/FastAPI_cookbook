from typing import Optional, List

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
        schema_extra = {
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
        schema_extra = {"example": example_ingredient}

class CreateIngredientItem(BaseModel):
    ingredient: CreateIngredient
    amount: int

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


class CreateDish(BaseModel):
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

class CreateIngredientItem(BaseModel):
    ingredient: CreateIngredient
    amount: int


class ListIngredientItem(BaseModel):
    amount: int
    ingredient: CreateIngredient


class ListDish(BaseModel):
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
