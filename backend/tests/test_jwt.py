
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from jwt.exceptions import InvalidTokenError

from app.config import get_settings
from app.security import create_access_token, decode_access_token


def test_create_and_decode_access_token():
    token = create_access_token(user_id=123)

    assert isinstance(token, str)
    assert decode_access_token(token) == 123


def test_expired_token_is_rejected():
    settings = get_settings()

    expired_payload = {
        "sub": "123",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }

    token = jwt.encode(
        expired_payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_token_with_wrong_signature_is_rejected():
    token = jwt.encode(
        {
            "sub": "123",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        "different-secret-key-for-testing-only-123456",
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_token_without_expiration_is_rejected():
    settings = get_settings()

    token = jwt.encode(
        {"sub": "123"},
        settings.jwt_secret_key.get_secret_value(),
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_token_with_invalid_user_id_is_rejected():
    settings = get_settings()

    token = jwt.encode(
        {
            "sub": "not-a-user-id",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        settings.jwt_secret_key.get_secret_value(),
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)
