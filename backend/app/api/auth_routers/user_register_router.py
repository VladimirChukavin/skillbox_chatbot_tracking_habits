from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token_schema import TokenBundle
from app.schemas.user_schema import UserCreate
from app.database import get_db_session
from app.services.auth_service import issue_token_bundle
from app.services.user_services.create_user_service import create_user

router = APIRouter()


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
