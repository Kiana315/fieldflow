
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.security import (
    create_access_token,
    verify_password,
)

from app.dependencies import get_current_user
from app.schemas.auth import UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: DbSession):
    statement = select(User).where(
        User.email == data.email
    )

    user = db.scalar(statement)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)

    return TokenResponse(access_token=token)


CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser):
    return current_user
