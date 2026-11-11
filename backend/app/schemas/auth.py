
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


from app.models.user import UserRole


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_available: bool

    model_config = {"from_attributes": True}
