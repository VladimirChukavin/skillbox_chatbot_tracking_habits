from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.schemas.token_schema import TokenBundle
from app.services.auth_service import authenticate_user, issue_token_bundle

router = APIRouter()


@router.post("/login/oauth", response_model=TokenBundle)
async def login_oauth_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    try:
        telegram_id = int(form_data.username)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="username должен быть числовым Telegram ID",
        ) from error

    user = await authenticate_user(session, telegram_id, form_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный Telegram ID или пароль",
        )

    return await issue_token_bundle(session, user)
