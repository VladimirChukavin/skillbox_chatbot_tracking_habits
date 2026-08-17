import datetime
from typing import Any

import bcrypt
from jose import jwt

from app.config import get_settings

settings = get_settings()


def hash_password(raw_password: str) -> str:
    return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_token(telegram_id: int, user_id: int, token_type: str = "access") -> str:
    now = datetime.datetime.now(datetime.timezone.utc)

    if token_type == "access":
        expire = now + datetime.timedelta(minutes=settings.access_token_expire_minutes)
    else:
        expire = now + datetime.timedelta(days=settings.refresh_token_expire_days)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "telegram_id": telegram_id,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def extract_token_from_header(authorization_header: str) -> str:
    parts = authorization_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Некорректный заголовок авторизации")

    return parts[1]
