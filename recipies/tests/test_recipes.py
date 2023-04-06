import pytest
from fastapi.testclient import TestClient

from recipies.models import Ingredient


def test_create_ingredient(
    client: TestClient, ingredient: Ingredient, mock_nutrition_api
):
    response = client.post("/ingredients/", json={"name": "carrot"})
    data = response.json()
    data.pop("id")
    print("data", data)
    print("ingredient", ingredient)
    assert response.status_code == 201
    assert data == ingredient


def test_get_ingredient():
    pass


def test_get_ingredient_does_not_exist():
    pass


def test_list_ingredients():
    pass


def test_update_ingredient_data():
    pass


def test_update_ingredient_name():
    pass


def test_delete_ingredient():
    pass


def test_delete_ingredient_does_not_exist():
    pass


def test_create_dish():
    pass


def test_create_dish_and_ingredients():
    pass


def test_list_dishes():
    pass


def test_delete_dish():
    pass


def test_delete_dish_does_not_exist():
    pass


def test_dish_detail():
    pass


def test_dish_detail_does_not_exist():
    pass
