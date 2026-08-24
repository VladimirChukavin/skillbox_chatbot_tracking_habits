"""
Зависимости (Dependencies) для FastAPI.

Содержит функции, используемые в маршрутах для извлечения и проверки
учётных данных, а также получения объекта текущего пользователя из БД.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from .security import decode_token
from app.database import get_db_session
from app.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Получить и проверить текущего авторизованного пользователя.

    Декодирует переданный access-токен, проверяет его тип и извлекает
    telegram_id. Затем ищет пользователя в базе данных. Если токен
    недействителен или пользователь не найден, выбрасывает исключение 401.

    :param token: JWT access-токен из заголовка Authorization
    :type token: str
    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :raises HTTPException: 401 — если токен недействителен, неверного типа
        или пользователь не найден
    :return: Объект модели текущего пользователя
    :rtype: User
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise credentials_exception

        telegram_id = int(payload.get("telegram_id"))
    except (KeyError, ValueError, JWTError):
        raise credentials_exception from None

    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user
