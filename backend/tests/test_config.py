from app.config import Settings


def test_connection_url_preserves_special_characters_in_password():
    settings = Settings(_env_file=None, postgres_password="local@pass:/#?")
    assert settings.database_url.password == "local@pass:/#?"
    assert settings.database_url.drivername == "postgresql+psycopg"
