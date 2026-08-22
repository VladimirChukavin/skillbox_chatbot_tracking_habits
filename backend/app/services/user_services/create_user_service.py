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
