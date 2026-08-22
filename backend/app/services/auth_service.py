from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_token, verify_password
from app.models.user_model import User
from app.services.user_services.get_user_by_telegram_id_service import (
    get_user_by_telegram_id,
)
from app.services.user_services.update_refresh_token_service import update_refresh_token


async def authenticate_user(
    session: AsyncSession, telegram_id: int, password: str
) -> User | None:
    user = await get_user_by_telegram_id(session, telegram_id)

    if user is None or not verify_password(password, user.hashed_password):
        return None

    return user


async def issue_token_bundle(session: AsyncSession, user: User) -> dict[str, str]:
    access_token = create_token(user.telegram_id, user.id, token_type="access")
    refresh_token = create_token(user.telegram_id, user.id, token_type="refresh")

    await update_refresh_token(session, user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
