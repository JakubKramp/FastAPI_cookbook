import pytest
import requests

from app.utils.tests import MockResponse
from recipies.tests.test_data import (
    example_ingredient,
    example_ingredient_api_response,
    example_create_dish,
)


@pytest.fixture(name="ingredient")
def ingredient_fixture():
    return example_ingredient


def get_example_ingredient(*args, **kwargs):
    r = MockResponse(json_data=example_ingredient_api_response.copy(), status_code=200)
    return r


@pytest.fixture(scope="function", autouse=True)
def mock_nutrition_api(monkeypatch):
    monkeypatch.setattr(requests, "get", get_example_ingredient)


@pytest.fixture(name="create_dish")
def create_dish_fixture():
    return example_create_dish
