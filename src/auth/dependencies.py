from datetime import datetime

from databases.interfaces import Record
from fastapi import Cookie, Depends

from src.auth import service
from src.auth.exceptions import EmailNotRegistered, EmailTaken, RefreshTokenNotValid
from src.auth.schemas import AuthUser, User, UserEmail


async def valid_user(user_email: UserEmail) -> User:
    user = await service.get_user_by_email(user_email.email)
    if not user:
        raise EmailNotRegistered()
    return User(**user._mapping)


async def valid_user_create(user: AuthUser) -> AuthUser:
    if await service.get_user_by_email(user.email):
        raise EmailTaken()
    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> Record:
    db_refresh_token = await service.get_refresh_token(refresh_token)
    if not db_refresh_token or not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()
    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: Record = Depends(valid_refresh_token),
) -> Record:
    user = await service.get_user_by_id(refresh_token["user_id"])
    if not user:
        raise RefreshTokenNotValid()
    return user


def _is_valid_refresh_token(db_refresh_token: Record) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
