"""
Сервис для регистрации (создания) нового пользователя.

Содержит функцию для добавления пользователя в базу данных с предварительной
проверкой уникальности Telegram ID и хешированием пароля.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user_model import User


async def create_user(
    session: AsyncSession,
    telegram_id: int,
    full_name: str,
    password: str,
    username: str | None = None,
) -> User:
    """
    Создать нового пользователя в базе данных.

    Перед созданием проверяет, существует ли уже пользователь с указанным
    telegram_id. Пароль хешируется с помощью bcrypt перед сохранением.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param telegram_id: Уникальный Telegram ID пользователя
    :type telegram_id: int
    :param full_name: Полное имя пользователя
    :type full_name: str
    :param password: Пароль в открытом виде (будет хеширован)
    :type password: str
    :param username: Имя пользователя в Telegram (опционально)
    :type username: str | None
    :raises ValueError: Если пользователь с таким telegram_id уже существует
    :return: Созданный объект пользователя
    :rtype: User
    """

    existing = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )

    if existing.scalar_one_or_none() is not None:
        raise ValueError(f"Пользователь с telegram_id: {telegram_id} уже существует")

    user = User(
        telegram_id=telegram_id,
        full_name=full_name,
        username=username,
        hashed_password=hash_password(password),
    )
    session.add(user)
    await session.flush()

    return user
