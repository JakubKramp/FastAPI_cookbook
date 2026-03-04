from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from recipes.models import Dish, Ingredient, IngredientItem


@pytest.mark.asyncio
async def test_get_ingredient(session: AsyncSession, client: AsyncClient, db_ingredient: Ingredient):
    ingredient = await session.scalar(select(Ingredient).limit(1))
    response = await client.get(f"/ingredients/{ingredient.id}")
    assert db_ingredient.id == ingredient.id
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_ingredient_does_not_exist(client: AsyncClient):
    response = await client.get("/ingredients/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_ingredients(
    session: AsyncSession, client: AsyncClient, db_ingredient: Ingredient, mock_nutri_client: AsyncMock
):
    db_ingredient1 = Ingredient(name="broccoli")
    session.add(db_ingredient1)
    await session.commit()
    response = await client.get("/ingredients/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2


@pytest.mark.asyncio
async def test_delete_ingredient(client: AsyncClient, db_ingredient: Ingredient):
    response = await client.delete("/ingredients/1")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_ingredient_does_not_exist(client: AsyncClient):
    response = await client.delete("/ingredients/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_dish(session: AsyncSession, client: AsyncClient, create_dish: dict):
    response = await client.post("/ingredients/dish/", json=create_dish)
    dish_count = await session.scalar(select(func.count(Dish.id)))
    assert dish_count == 1
    ingredient_item_count = await session.scalar(select(func.count(IngredientItem.id)))
    assert ingredient_item_count == 2
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_list_dishes(client: AsyncClient, create_dish):
    await client.post("/ingredients/dish/", json=create_dish)
    response = await client.get("/ingredients/dish/")
    assert len(response.json()) == 1
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_dish(client: AsyncClient, create_dish):
    await client.post("/ingredients/dish/", json=create_dish)
    response = await client.delete("/ingredients/dish/1")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_dish_does_not_exist(client: AsyncClient):
    response = await client.delete("/ingredients/dish/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_dish_detail(client: AsyncClient, create_dish):
    await client.post("/ingredients/dish/", json=create_dish)
    response = await client.get("/ingredients/dish/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dish_detail_does_not_exist(client: AsyncClient):
    response = await client.get("/ingredients/dish/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_dish_add_tag(client: AsyncClient, create_dish: dict, tag: dict):
    await client.post("/ingredients/dish/", json=create_dish)
    response = await client.post("/ingredients/dish/1/tag", json=tag)
    assert response.json()["tags"][0]["name"] == tag["name"]
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dish_add_to_favorites_unauthenticated(
    session: AsyncSession, client: AsyncClient, create_dish: dict
):
    await client.post("/ingredients/dish/", json=create_dish)
    response = await client.post("/ingredients/dish/1/favorite")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_dish_add_to_favorites(client: AsyncClient, create_dish: dict, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    await client.post("/ingredients/dish/", json=create_dish)
    response = await client.post("/ingredients/dish/1/favorite", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["is_favorite"] == True


@pytest.mark.asyncio
async def test_dish_remove_from_favorites(client: AsyncClient, create_dish: dict, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    await client.post("/ingredients/dish/", json=create_dish)
    await client.post("/ingredients/dish/1/favorite", headers={"Authorization": f"Bearer {token}"})
    response = await client.post("/ingredients/dish/1/favorite", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["is_favorite"] == False
