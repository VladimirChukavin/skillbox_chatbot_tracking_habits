"""
Роутер для регистрации новых пользователей.

Обеспечивает endpoint для создания учётной записи пользователя
и немедленной выдачи пары JWT-токенов (access и refresh).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token_schema import TokenBundle
from app.schemas.user_schema import UserCreate
from app.database import get_db_session
from app.services.auth_services.issue_token_bundle_service import issue_token_bundle
from app.services.user_services.create_user_service import create_user

router = APIRouter()


@router.post(
    "/register", response_model=TokenBundle, status_code=status.HTTP_201_CREATED
)
async def user_register(
    payload: UserCreate, session: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Зарегистрировать нового пользователя.

    Принимает данные пользователя (Telegram ID, имя, пароль, username)
    в формате JSON. Пароль хешируется перед сохранением в БД. При успехе
    возвращает созданному пользователю пару access/refresh токенов.

    :param payload: Данные для создания пользователя
    :type payload: UserCreate
    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :raises HTTPException: 409 — если пользователь с указанным
        telegram_id уже существует
    :return: Словарь с access и refresh токенами
    :rtype: dict
    """

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
