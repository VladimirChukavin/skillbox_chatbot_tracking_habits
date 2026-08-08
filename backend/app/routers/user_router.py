from fastapi import APIRouter, Depends

from backend.app.core.deps import get_current_user
from backend.app.models.user_model import User
from backend.app.schemas.user_schema import UserRead

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)
