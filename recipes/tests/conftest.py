from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from recipes.models import Ingredient
from recipes.nutritional_data import NutritionalAPIClient
from recipes.tests.test_data.example_data import (
    example_create_dish,
    example_ingredient,
)


@pytest.fixture(name="ingredient")
def ingredient_fixture():
    return example_ingredient.copy()


@pytest_asyncio.fixture(name="db_ingredient")
async def database_ingredient_fixture(session: AsyncSession) -> Ingredient:
    db_ingredient = Ingredient(**example_ingredient)
    session.add(db_ingredient)
    await session.commit()
    await session.refresh(db_ingredient)
    return db_ingredient


@pytest.fixture(autouse=True)
def mock_nutri_client():
    with patch.object(NutritionalAPIClient, "fill_nutritional_values", new_callable=AsyncMock) as mock:
        mock.return_value = None
        yield mock


@pytest.fixture(name="create_dish")
def create_dish_fixture():
    return example_create_dish
