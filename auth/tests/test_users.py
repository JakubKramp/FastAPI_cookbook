from sqlalchemy import func
from sqlmodel import Session
from starlette.testclient import TestClient

from auth.models import User


def test_create_user(client: TestClient, session: Session):
    user = {
        "username": "testuser",
        "password": "test_password",
        "email": "testemail@test.com",
    }
    response = client.post("/user", json=user)
    assert session.query(func.count(User.id)).scalar() == 1
    assert response.status_code == 201


def test_login_user(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"]
    assert response.json()["access_token"]


def test_login_wrong_password(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="wrong_test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json()["detail"]


def test_user_detail(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_update_user(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    user_data = {"username": "newtestuser"}
    response = client.patch(
        "/user", json=user_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newtestuser"


def test_delete_user(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    response = client.delete("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204
