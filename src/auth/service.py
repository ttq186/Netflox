from datetime import datetime, timedelta

from databases.interfaces import Record
from sqlalchemy import select

from src import utils
from src.auth.config import auth_config
from src.auth.constants import AuthMethod
from src.auth.exceptions import InvalidCredentials
from src.auth.models import refresh_token_tb, user_tb
from src.auth.schemas import AuthUser
from src.auth.security import hash_password, verify_password
from src.database import database


async def create_user(auth_user: AuthUser) -> Record | None:
    insert_query = (
        user_tb.insert()
        .values(
            {
                "email": auth_user.email,
                "password": hash_password(auth_user.password),
                "auth_method": AuthMethod.NORMAL,
                "created_at": datetime.utcnow(),
            }
        )
        .returning(user_tb)
    )
    return await database.fetch_one(insert_query)


async def get_user_by_id(user_id: int) -> Record | None:
    select_query = select(user_tb).where(user_tb.c.id == user_id)
    return await database.fetch_one(select_query)


async def get_user_by_email(email: str) -> Record | None:
    select_query = select(user_tb).where(user_tb.c.email == email)
    return await database.fetch_one(select_query)


async def create_refresh_token(user_id: int, refresh_token: str | None = None) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)

    insert_query = refresh_token_tb.insert().values(
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    await database.execute(insert_query)
    return refresh_token


async def get_refresh_token(refresh_token: str) -> Record | None:
    select_query = refresh_token_tb.select().where(
        refresh_token_tb.c.token == refresh_token
    )
    return await database.fetch_one(select_query)


async def expire_refresh_token(refresh_token_id: int) -> None:
    update_query = (
        refresh_token_tb.update()
        .values(expires_at=datetime.utcnow() - timedelta(days=1))
        .where(refresh_token_tb.c.id == refresh_token_id)
    )
    await database.execute(update_query)


async def authenticate_user(auth_data: AuthUser) -> Record:
    user = await get_user_by_email(auth_data.email)
    if not user or not verify_password(auth_data.password, user["password"]):
        raise InvalidCredentials()
    return user
