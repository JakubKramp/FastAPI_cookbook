import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import Profile, User

@pytest.mark.asyncio
async def test_create_profile(client: AsyncClient, session: AsyncSession, user: User, profile_data: dict, mock_dri_client):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = await client.post("/user/profile", json=profile_data, headers={"Authorization": f"Bearer {token}"})
    count = await session.scalar(select(func.count()).select_from(Profile))
    assert count == 1
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_create_profile_unauthorized(client: AsyncClient, session: AsyncSession, profile_data: dict):
    response = await client.post("/user/profile", json=profile_data)
    count = await session.scalar(select(func.count()).select_from(Profile))
    assert count == 0
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient, session: AsyncSession, user: User, profile_data: dict, mock_dri_client):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    await client.post("/user/profile", json=profile_data, headers={"Authorization": f"Bearer {token}"})
    profile = {
        "sex": "Female",
        "age": 35,
    }
    response = await client.patch("/user/profile", json=profile, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    count = await session.scalar(select(func.count()).select_from(Profile))
    assert count == 1
    assert response.json()["sex"] == "Female"
    assert response.json()["age"] == 35

@pytest.mark.asyncio
async def test_delete_user_and_profile(client: AsyncClient, session: AsyncSession, user: User, profile_data: dict, mock_dri_client):
    login_data = dict(username=user.username, password="test_password")
    response = await client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    await client.post("/user/profile", json=profile_data, headers={"Authorization": f"Bearer {token}"})
    user_count = await session.scalar(select(func.count()).select_from(User))
    assert user_count == 1
    profile_count = await session.scalar(select(func.count()).select_from(Profile))
    assert profile_count == 1
    await client.delete("/user/", headers={"Authorization": f"Bearer {token}"})
    user_count = await session.scalar(select(func.count()).select_from(User))
    assert user_count == 0

