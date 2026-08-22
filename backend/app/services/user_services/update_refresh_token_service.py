from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User


async def update_refresh_token(
    session: AsyncSession, user_id: int, refresh_token: str
) -> None:
    user = await session.get(User, user_id)

    if user is not None:
        user.refresh_token = refresh_token
