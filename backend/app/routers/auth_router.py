from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.database import get_db_session
from app.models.user_model import User
from app.schemas.token_schema import TokenBundle
from app.schemas.user_schema import UserCreate, UserRead, UserLogin
from app.services.auth_service import authenticate_user, issue_token_bundle
from app.services.user_service import create_user, get_user_by_telegram_id
from app.core.exceptions import ConflictError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=TokenBundle, status_code=status.HTTP_201_CREATED
)
async def user_register(
    payload: UserCreate, session: AsyncSession = Depends(get_db_session)
) -> dict:
    try:
        user = await create_user(
            session=session,
            telegram_id=payload.telegram_id,
            full_name=payload.full_name,
            password=payload.password,
            username=payload.username,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error

    return await issue_token_bundle(session, user)


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


@router.post("/refresh", response_model=TokenBundle)
async def refresh_access_token(
    refresh_token: str, session: AsyncSession = Depends(get_db_session)
) -> dict:
    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный тип токена",
            )

        telegram_id = int(payload.get("telegram_id"))
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh-token",
        ) from error

    user = await get_user_by_telegram_id(session, telegram_id)

    if user is None or user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh-токен не найден или отозван",
        )

    return await issue_token_bundle(session, user)
