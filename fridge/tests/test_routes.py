import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from recipes.models import Product
from recipes.tests.test_data.example_data import example_product


@pytest.mark.asyncio
async def test_get_fridge(user: User, client: AsyncClient, session: AsyncSession):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = await client.get(f"/fridge/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_product_to_fridge(user: User, client: AsyncClient):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    data = example_product
    token = response.json()["access_token"]
    response = await client.post(f"/fridge/products", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_list_expired_products(
    user: User, client: AsyncClient, expired_product: Product, product: Product, session: AsyncSession
):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = await client.get(f"/fridge/expired", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    count = await session.scalar(select(func.count()).select_from(Product))
    assert count == 2
    assert "products" in response.json().keys()
    assert len(response.json()["products"]) == 1


@pytest.mark.asyncio
async def test_delete_expired_products(
    user: User, client: AsyncClient, expired_product: Product, product: Product, session: AsyncSession
):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = await client.delete(f"/fridge/expired", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204
    count = await session.scalar(select(func.count()).select_from(Product))
    assert count == 1
