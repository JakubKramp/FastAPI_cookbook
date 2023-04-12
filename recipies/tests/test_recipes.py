from fastapi.testclient import TestClient
from requests import Session
from sqlalchemy import func

from recipies.models import Ingredient, CreateIngredient, Dish, IngredientItem


def test_create_ingredient(
    client: TestClient,
    ingredient: Ingredient,
):
    response = client.post("/ingredients/", json={"name": "carrot"})
    data = response.json()
    data.pop("id")
    assert response.status_code == 201
    assert data == ingredient


def test_get_ingredient(session: Session, client: TestClient, ingredient: Ingredient):
    db_ingredient = Ingredient.from_orm(CreateIngredient(name="carrot"))
    session.add(db_ingredient)
    session.commit()
    response = client.get("/ingredients/1")
    data = response.json()
    data.pop("id")
    assert response.status_code == 200
    assert data == ingredient


def test_get_ingredient_does_not_exist(client: TestClient):
    response = client.get("/ingredients/1")
    data = response.json()
    assert data["detail"] == "Ingredient not found"
    assert response.status_code == 404


def test_list_ingredients(session: Session, client: TestClient, ingredient: Ingredient):
    db_ingredient = Ingredient.from_orm(CreateIngredient(name="carrot"))
    db_ingredient1 = Ingredient.from_orm(CreateIngredient(name="broccoli"))
    session.add(db_ingredient)
    session.add(db_ingredient1)
    session.commit()
    response = client.get("/ingredients/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2


def test_delete_ingredient(session: Session, client: TestClient):
    db_ingredient = Ingredient.from_orm(CreateIngredient(name="carrot"))
    session.add(db_ingredient)
    session.commit()
    response = client.delete("/ingredients/1")
    assert response.status_code == 204


def test_delete_ingredient_does_not_exist(client: TestClient):
    response = client.delete("/ingredients/1")
    assert response.status_code == 404


def test_create_dish(session: Session, client: TestClient, create_dish):
    response = client.post("/ingredients/dish/", json=create_dish)
    assert session.query(func.count(Dish.id)).scalar() == 1
    assert session.query(func.count(IngredientItem.id)).scalar() == 2
    assert response.status_code == 201


def test_list_dishes(session: Session, client: TestClient, create_dish):
    client.post("/ingredients/dish/", json=create_dish)
    response = client.get("/ingredients/dish/")
    assert len(response.json()) == 1
    assert response.status_code == 200


def test_delete_dish(session: Session, client: TestClient, create_dish):
    client.post("/ingredients/dish/", json=create_dish)
    response = client.delete("/ingredients/dish/1")
    assert response.status_code == 204
    assert response.json() == {"message": "Dish 1 deleted"}


def test_delete_dish_does_not_exist(session: Session, client: TestClient, create_dish):
    response = client.delete("/ingredients/dish/1")
    assert response.status_code == 404


def test_dish_detail(session: Session, client: TestClient, create_dish):
    client.post("/ingredients/dish/", json=create_dish)
    response = client.get("/ingredients/dish/1")
    assert response.status_code == 200


def test_dish_detail_does_not_exist(session: Session, client: TestClient, create_dish):
    response = client.get("/ingredients/dish/1")
    assert response.status_code == 404
