from datetime import datetime, timedelta

from databases.interfaces import Record
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth import exceptions as auth_exceptions
from src.auth.config import auth_config
from src.auth.schemas import JWTData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/tokens", auto_error=False)


def create_access_token(
    *,
    user: Record,
    expires_delta: timedelta = timedelta(minutes=auth_config.JWT_EXP),
) -> str:
    jwt_data = {
        "sub": str(user["id"]),
        "exp": datetime.utcnow() + expires_delta,
        "is_admin": user["is_admin"],
        "is_active": user["is_active"],
        "is_activated": user["is_activated"],
    }

    return jwt.encode(jwt_data, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        raise auth_exceptions.InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise auth_exceptions.AuthRequired()

    if not token.is_active:
        raise auth_exceptions.AccountSuspended()

    if not token.is_activated:
        raise auth_exceptions.AccountNotActivated()

    return token


async def parse_jwt_admin_data(
    token: JWTData = Depends(parse_jwt_user_data),
) -> JWTData:
    if not token.is_admin:
        raise auth_exceptions.AuthorizationFailed()

    return token


async def validate_admin_access(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> None:
    if token and token.is_admin:
        return

    raise auth_exceptions.AuthorizationFailed()
