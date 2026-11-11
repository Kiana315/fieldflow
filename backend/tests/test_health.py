from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import app


def test_liveness_and_docs_without_database():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        assert client.get("/docs").status_code == 200
        assert "/health/db" in client.get("/openapi.json").json()["paths"]


def test_database_probe_success_response():
    # Contract test only; this does not replace a live PostgreSQL check.
    with patch("app.main.check_database") as check, TestClient(app) as client:
        response = client.get("/health/db")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "database": "ok"}
        check.assert_called_once()


def test_database_failure_is_503_and_does_not_expose_credentials():
    error = OperationalError("SELECT 1", {}, Exception("private connection details"))
    with patch("app.main.check_database", side_effect=error), TestClient(app) as client:
        response = client.get("/health/db")
        assert response.status_code == 503
        assert response.json() == {"detail": "Database unavailable"}
        assert client.get("/health").status_code == 200
