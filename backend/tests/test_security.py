import datetime
from unittest.mock import patch

import pytest
from jose import JWTError

from app.core.security import (
    create_token,
    decode_token,
    hash_password,
    verify_password,
)

MOCK_SETTINGS = {
    "secret_key": "test-secret-key-for-unit-tests-only",
    "algorithm": "HS256",
    "access_token_expire_minutes": 15,
    "refresh_token_expire_days": 7,
}


@pytest.fixture
def mock_settings():
    with patch("app.core.security.settings", MOCK_SETTINGS):
        yield


class TestPasswordHashing:
    def test_hash_password_returns_str(self):
        assert isinstance(hash_password("secret123"), str)

    def test_hash_password_different_each_time(self):
        h1 = hash_password("secret123")
        h2 = hash_password("secret123")
        assert h1 != h2

    def test_verify_password_correct(self):
        hashed = hash_password("mypassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_verify_password_empty(self):
        hashed = hash_password("mypassword")
        assert verify_password("", hashed) is False

    def test_verify_password_matches(self):
        password = "secret123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True


class TestTokenCreation:
    def test_create_access_token_is_str(self):
        token = create_token(telegram_id=123, user_id=1, token_type="access")
        assert isinstance(token, str)

    def test_create_refresh_token_is_str(self):
        token = create_token(telegram_id=123, user_id=1, token_type="refresh")
        assert isinstance(token, str)

    def test_access_token_has_correct_type(self):
        token = create_token(telegram_id=123, user_id=1, token_type="access")
        payload = decode_token(token)
        assert payload["type"] == "access"

    def test_refresh_token_has_correct_type(self):
        token = create_token(telegram_id=123, user_id=1, token_type="refresh")
        payload = decode_token(token)
        assert payload["type"] == "refresh"

    def test_token_contains_telegram_id(self):
        token = create_token(telegram_id=999, user_id=1)
        payload = decode_token(token)
        assert payload["telegram_id"] == 999

    def test_token_contains_user_id_as_sub(self):
        token = create_token(telegram_id=123, user_id=42)
        payload = decode_token(token)
        assert payload["sub"] == "42"
        assert isinstance(payload["sub"], str)

    def test_token_has_expiration(self):
        token = create_token(telegram_id=123, user_id=1)
        payload = decode_token(token)
        assert "exp" in payload
        assert payload["exp"] > int(
            datetime.datetime.now(datetime.timezone.utc).timestamp()
        )

    def test_refresh_token_lives_than_access(self):
        access_token = create_token(telegram_id=123, user_id=1, token_type="access")
        refresh_token = create_token(telegram_id=123, user_id=1, token_type="refresh")

        access_payload = decode_token(access_token)
        refresh_payload = decode_token(refresh_token)

        access_ttl = access_payload["exp"] - access_payload["iat"]
        refresh_ttl = refresh_payload["exp"] - refresh_payload["iat"]

        assert refresh_ttl > access_ttl


class TestTokenValidation:
    def test_decode_invalid_token_raises(self):
        with pytest.raises(JWTError):
            decode_token("invalid.token.here")

    def test_decode_empty_string_raises(self):
        with pytest.raises(JWTError):
            decode_token("")

    def test_decode_tampered_token_raises(self):
        token = create_token(telegram_id=123, user_id=1, token_type="access")

        parts = token.split(".")
        parts[1] = parts[1] + "x"
        tampered = ".".join(parts)

        with pytest.raises(JWTError):
            decode_token(tampered)
