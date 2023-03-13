import uuid
from datetime import datetime, timedelta

from databases.interfaces import Record
from pydantic import UUID4
from sqlalchemy import insert, select

from src import utils
from src.auth.config import auth_config
from src.auth.exceptions import InvalidCredentials
from src.auth.models import refresh_token_table, user
from src.auth.schemas import AuthUser
from src.auth.security import hash_password, verify_password
from src.database import database


async def create_user(user: AuthUser) -> Record | None:
    insert_query = (
        insert(user)
        .values(
            {
                "email": user.email,
                "password": hash_password(user.password),
                "created_at": datetime.utcnow(),
            }
        )
        .returning(user)
    )

    return await database.fetch_one(insert_query)


async def get_user_by_id(user_id: int) -> Record | None:
    select_query = select(user).where(user.c.id == user_id)
    return await database.fetch_one(select_query)


async def get_user_by_email(email: str) -> Record | None:
    select_query = select(user).where(user.c.email == email)
    return await database.fetch_one(select_query)


async def create_refresh_token(
    *, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)

    insert_query = refresh_token_table.insert().values(
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    await database.execute(insert_query)
    return refresh_token


async def get_refresh_token(refresh_token: str) -> Record | None:
    select_query = refresh_token_table.select().where(
        refresh_token_table.c.token == refresh_token
    )
    return await database.fetch_one(select_query)


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    update_query = (
        refresh_token_table.update()
        .values(expires_at=datetime.utcnow() - timedelta(days=1))
        .where(refresh_token_table.c.uuid == refresh_token_uuid)
    )
    await database.execute(update_query)


async def authenticate_user(auth_data: AuthUser) -> Record:
    user = await get_user_by_email(auth_data.email)
    if not user:
        raise InvalidCredentials()

    if not verify_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    return user
