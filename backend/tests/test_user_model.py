
from sqlalchemy import Boolean, Enum as SQLEnum

from app.models.user import User, UserRole


def test_user_table_name():
    assert User.__tablename__ == "users"


def test_user_columns():
    columns = set(User.__table__.columns.keys())

    assert columns == {
        "id",
        "email",
        "full_name",
        "hashed_password",
        "role",
        "is_active",
        "is_available",
        "created_at",
    }


def test_email_is_unique():
    email = User.__table__.columns["email"]

    assert email.unique is True
    assert email.nullable is False


def test_role_enum_values():
    role = User.__table__.columns["role"]

    assert isinstance(role.type, SQLEnum)
    assert role.type.enums == [
        "admin",
        "dispatcher",
        "technician",
    ]


def test_boolean_defaults():
    active = User.__table__.columns["is_active"]
    available = User.__table__.columns["is_available"]

    assert isinstance(active.type, Boolean)
    assert isinstance(available.type, Boolean)

    assert active.default.arg is True
    assert available.default.arg is False

    assert active.server_default is not None
    assert available.server_default is not None


def test_user_roles():
    assert UserRole.ADMIN.value == "admin"
    assert UserRole.DISPATCHER.value == "dispatcher"
    assert UserRole.TECHNICIAN.value == "technician"
