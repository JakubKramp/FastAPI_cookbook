from typing import List

from pydantic import BaseModel, ConfigDict

from recipes.schemas import CreateProduct
from recipes.tests.test_data.example_data import example_fridge


class FridgeDetails(BaseModel):
    products: List[CreateProduct]

    model_config = ConfigDict(json_schema_extra={"example": example_fridge})
