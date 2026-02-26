from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from recipes.tests.test_data.recipes import nutritional_values, example_ingredient, example_create_ingredient_item, \
    example_create_dish, example_list_dish, example_dish_detail


class NutritionalValues(BaseModel):
    """
    Schema for nutritional values retrieved from the API.
    """
    calories: float = 0.0
    fat_total: float = 0.0
    protein: float = 0.0
    sodium: float = 0.0
    potassium: float = 0.0
    fiber: float = 0.0
    carbohydrates_total: float = 0.0
    sugar: float = 0.0

    model_config = ConfigDict(json_schema_extra={"example": nutritional_values})


class CreateIngredient(BaseModel):
    name: str

    model_config = ConfigDict(json_schema_extra={"example": {"name": "carrot"}})


class ListIngredient(CreateIngredient, NutritionalValues):
    id: int

    model_config = ConfigDict(json_schema_extra={"example": example_ingredient})


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

    model_config = ConfigDict(json_schema_extra={"example": example_ingredient})


class CreateIngredientItem(BaseModel):
    name: str
    amount: int

    model_config = ConfigDict(json_schema_extra={"example": example_create_ingredient_item})


class CreateDish(BaseModel):
    name: str
    recipe: Optional[str]
    ingredients: List[CreateIngredientItem]

    model_config = ConfigDict(json_schema_extra={"example": example_create_dish})


class ListIngredientItem(BaseModel):
    amount: int
    ingredient: CreateIngredient


class ListDish(BaseModel):
    id: int
    name: str
    recipe: Optional[str]
    ingredients: List[ListIngredientItem]

    model_config = ConfigDict(json_schema_extra={"example": example_list_dish})


class DishDetail(ListDish):
    nutritional_values: NutritionalValues | None = None

    model_config = ConfigDict(json_schema_extra={"example": example_dish_detail})