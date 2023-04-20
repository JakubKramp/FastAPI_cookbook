from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from auth.enums import Sex, ActivityFactor
from auth.models import Profile, User


def test_create_profile(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    profile = {
        "sex": Sex.male,
        "age": 30,
        "height": 180,
        "wieght": 80,
        "activity_factor": ActivityFactor.little,
        "smoking": True,
    }
    response = client.post(
        "/user/profile", json=profile, headers={"Authorization": f"Bearer {token}"}
    )
    assert session.query(func.count(Profile.id)).scalar() == 1
    assert response.status_code == 201


def test_create_profile_unauthorized(client: TestClient, session: Session):
    profile = {
        "sex": Sex.male,
        "age": 30,
        "height": 180,
        "wieght": 80,
        "activity_factor": ActivityFactor.little,
        "smoking": True,
    }
    response = client.post("/user/profile", json=profile)
    assert session.query(func.count(Profile.id)).scalar() == 0
    assert response.status_code == 401


def test_update_profile(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    profile = {
        "sex": Sex.female,
        "age": 35,
    }
    response = client.patch(
        "/user/profile", json=profile, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["sex"] == Sex.female
    assert response.json()["age"] == 35


def test_delete_user_and_profile(client: TestClient, session: Session, user: User):
    login_data = dict(username=user.username, password="test_password")
    response = client.post(
        "/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    profile = {
        "sex": Sex.male,
        "age": 30,
        "height": 180,
        "wieght": 80,
        "activity_factor": ActivityFactor.little,
        "smoking": True,
    }
    client.post(
        "/user/profile", json=profile, headers={"Authorization": f"Bearer {token}"}
    )
    assert session.query(func.count(Profile.id)).scalar() == 1
    client.delete("/user")
    assert session.query(func.count(Profile.id)).scalar() == 0
