import datetime

import pytest
from jose import JWTError

from app.core.security import (
    create_token,
    decode_token,
    hash_password,
    verify_password,
)


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

    def test_token_has_expiration(self):
        token = create_token(telegram_id=123, user_id=1)
        payload = decode_token(token)
        assert "exp" in payload
        assert payload["exp"] > int(
            datetime.datetime.now(datetime.timezone.utc).timestamp()
        )

    def test_decode_invalid_token_raises(self):
        with pytest.raises(JWTError):
            decode_token("invalid.token.here")
