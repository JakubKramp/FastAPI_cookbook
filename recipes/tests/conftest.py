import pytest

from recipes.tests.test_data import (
    example_ingredient,
    example_ingredient_api_response,
    example_create_dish,
)


@pytest.fixture(name="ingredient")
def ingredient_fixture():
    return example_ingredient


def get_example_ingredient(*args, **kwargs):
    return example_ingredient_api_response.copy()[0]


@pytest.fixture(scope="function", autouse=True)
def mock_nutrition_api(mocker):
    mocker.patch("recipes.routes.get_nutritional_values", return_value=get_example_ingredient())


@pytest.fixture(name="create_dish")
def create_dish_fixture():
    return example_create_dish
