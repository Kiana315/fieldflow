
from app.config import Settings


def test_connection_url_preserves_special_characters_in_password():
    settings = Settings(
        postgres_password="local@pass:/#?",
        jwt_secret_key="test-only-secret-not-for-production",
    )

    assert settings.database_url.password == "local@pass:/#?"
    assert settings.database_url.drivername == "postgresql+psycopg"
