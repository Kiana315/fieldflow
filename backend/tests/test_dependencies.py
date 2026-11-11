
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.models.user import User, UserRole
from app.security import create_access_token


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
        hashed_password="unused-in-these-tests",
        role=UserRole.TECHNICIAN,
        is_active=True,
        is_available=True,
    )


def test_get_me_success(auth_client, active_user):
    client, fake_db = auth_client
    fake_db.get.return_value = active_user

    token = create_access_token(active_user.id)

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == active_user.email
    assert response.json()["role"] == "technician"
    assert "hashed_password" not in response.json()


def test_get_me_without_token(auth_client):
    client, fake_db = auth_client

    response = client.get("/auth/me")

    assert response.status_code == 401
    fake_db.get.assert_not_called()


def test_get_me_invalid_token(auth_client):
    client, fake_db = auth_client

    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    fake_db.get.assert_not_called()


def test_get_me_inactive_user(auth_client, active_user):
    client, fake_db = auth_client
    active_user.is_active = False
    fake_db.get.return_value = active_user

    token = create_access_token(active_user.id)

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_get_me_unknown_user(auth_client):
    client, fake_db = auth_client
    fake_db.get.return_value = None

    token = create_access_token(999)

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


from typing import Annotated

from fastapi import Depends

from app.dependencies import require_roles


def test_rbac_allows_dispatcher(auth_client, active_user):
    client, fake_db = auth_client

    active_user.role = UserRole.DISPATCHER
    fake_db.get.return_value = active_user

    def dispatcher_only(
        user: Annotated[
            User,
            Depends(require_roles(UserRole.DISPATCHER)),
        ],
    ):
        return {"message": "Access granted"}

    app.add_api_route(
        "/test/dispatcher-only",
        dispatcher_only,
        methods=["GET"],
    )

    token = create_access_token(active_user.id)

    response = client.get(
        "/test/dispatcher-only",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_rbac_denies_technician(auth_client, active_user):
    client, fake_db = auth_client

    fake_db.get.return_value = active_user

    def dispatcher_only(
        user: Annotated[
            User,
            Depends(require_roles(UserRole.DISPATCHER)),
        ],
    ):
        return {"message": "Access granted"}

    app.add_api_route(
        "/test/dispatcher-only-denied",
        dispatcher_only,
        methods=["GET"],
    )

    token = create_access_token(active_user.id)

    response = client.get(
        "/test/dispatcher-only-denied",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"
