from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token_schema import TokenBundle
from app.schemas.user_schema import UserLogin
from app.database import get_db_session
from app.services.auth_service import issue_token_bundle, authenticate_user

router = APIRouter()


@router.post("/login", response_model=TokenBundle)
async def login_user(
    payload: UserLogin, session: AsyncSession = Depends(get_db_session)
) -> dict:
    user = await authenticate_user(session, payload.telegram_id, payload.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный Telegram ID или пароль",
        )

    return await issue_token_bundle(session, user)
