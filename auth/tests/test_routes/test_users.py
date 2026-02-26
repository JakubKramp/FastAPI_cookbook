import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User


@pytest.mark.asyncio
async def test_sign_up(client: AsyncClient, session: AsyncSession):
    response = await client.post("/user/", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 201
    count = await session.scalar(select(func.count()).select_from(User))
    assert count == 1
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@test.com"
    assert "password" not in data

@pytest.mark.asyncio
async def test_sign_up_duplicate(client: AsyncClient):
    payload = {"username": "testuser", "email": "test@test.com", "password": "password123"}
    await client.post("/user/", json=payload)
    response = await client.post("/user/", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Username/email already taken"

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"]
    assert response.json()["access_token"]

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, user: User):
    login_data = dict(username=user.username, password="test_wrong_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_me(client: AsyncClient, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = await client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_user_detail(client: AsyncClient, user: User):
    response = await client.get(f"/user/{user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == user.username

@pytest.mark.asyncio
async def test_user_detail_no_user(client: AsyncClient):
    response = await client.get("/user/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient,  user: User):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    user_data = {"username": "newtestuser"}
    response = await client.patch("/user/", json=user_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "newtestuser"

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient,  user: User):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = await client.delete("/user/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204



@pytest.mark.asyncio
async def test_delete_user_unauthorized(client: AsyncClient):
    response = await client.delete("/user/",)
    assert response.status_code == 401
