
from pwdlib import PasswordHash

from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from app.config import get_settings


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(user_id: int) -> str:
    settings = get_settings()

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=["HS256"],
            options={"require": ["sub", "exp"]},
        )

        user_id = payload["sub"]

        if (
            not isinstance(user_id, str)
            or not user_id.isdecimal()
            or int(user_id) <= 0
        ):
            raise InvalidTokenError("Invalid user ID")

        return int(user_id)

    except InvalidTokenError:
        raise
