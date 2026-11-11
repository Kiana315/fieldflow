
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.models.user import User, UserRole
from app.security import hash_password, decode_access_token


@pytest.fixture
def auth_client():
    fake_db = Mock()

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client, fake_db
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def active_user():
    return User(
        id=1,
        email="technician@example.com",
        full_name="Test Technician",
        hashed_password=hash_password("TestPassword123!"),
        role=UserRole.TECHNICIAN,
        is_active=True,
        is_available=True,
    )


def test_login_success(auth_client, active_user):
    client, fake_db = auth_client

    fake_db.scalar.return_value = active_user

    response = client.post(
        "/auth/login",
        json={
            "email": "technician@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)

    user_id = decode_access_token(data["access_token"])

    assert user_id == active_user.id


def test_login_email_not_found(auth_client):
    client, fake_db = auth_client

    fake_db.scalar.return_value = None

    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_wrong_password(auth_client, active_user):
    client, fake_db = auth_client

    fake_db.scalar.return_value = active_user

    response = client.post(
        "/auth/login",
        json={
            "email": "technician@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_inactive_user(auth_client, active_user):
    client, fake_db = auth_client

    active_user.is_active = False
    fake_db.scalar.return_value = active_user

    response = client.post(
        "/auth/login",
        json={
            "email": "technician@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_empty_password(auth_client):
    client, fake_db = auth_client

    response = client.post(
        "/auth/login",
        json={
            "email": "technician@example.com",
            "password": "",
        },
    )

    assert response.status_code == 422
    fake_db.scalar.assert_not_called()
