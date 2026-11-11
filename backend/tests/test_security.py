
from app.security import hash_password, verify_password


def test_hash_password_is_not_plaintext():
    password = "TestPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$argon2")


def test_verify_correct_password():
    password = "TestPassword123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_wrong_password():
    hashed = hash_password("CorrectPassword123!")

    assert verify_password(
        "WrongPassword123!",
        hashed,
    ) is False


def test_same_password_produces_different_hashes():
    password = "TestPassword123!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
    assert verify_password(password, first_hash)
    assert verify_password(password, second_hash)
