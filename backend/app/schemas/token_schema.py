from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    telegram_id: int
    exp: int | None = None
    type: str = "access"


class TokenBundle(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
