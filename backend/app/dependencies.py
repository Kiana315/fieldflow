
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from app.database import get_db
from app.models.user import User
from app.security import decode_access_token


bearer_scheme = HTTPBearer(auto_error=False)

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    db: DbSession,
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        user_id = decode_access_token(credentials.credentials)
    except InvalidTokenError:
        raise unauthorized from None

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise unauthorized

    return user


from collections.abc import Callable

from app.models.user import UserRole


def require_roles(
    *allowed_roles: UserRole,
) -> Callable:
    def check_role(
        current_user: Annotated[
            User,
            Depends(get_current_user),
        ],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return check_role
