from databases.interfaces import Record
from sqlalchemy import insert, select, desc, update, func

from src import utils
from src.auth.constants import AuthMethod
from src.auth.exceptions import InvalidCredentials
from src.movie.models import movie_tb, watch_history_tb, movie_genre_tb, genre_tb
from src.database import database


async def get_movie_by_id(id: int) -> Record | None:
    select_query = select(movie_tb).filter(movie_tb.c.id == id)
    return await database.fetch_one(select_query)


async def get_or_create_watch_history_if_not_exist(
    user_id: int, movie_id: int
) -> Record | None:
    select_query = select(watch_history_tb).filter(
        watch_history_tb.c.user_id == user_id, watch_history_tb.c.movie_id == movie_id
    )
    watch_history = await database.fetch_one(select_query)
    if watch_history:
        return watch_history
    insert_query = (
        insert(watch_history)
        .values({"user_id": user_id, "movie_id": movie_id})
        .returning(watch_history)
    )
    return await database.fetch_one(insert_query)


async def get_top_rated_movies(page: int, size: int) -> list[Record]:
    select_query = (
        select(movie_tb, func.array_agg(genre_tb.c.name).label("genres"))
        .select_from(movie_tb)
        .join(movie_genre_tb)
        .join(genre_tb)
        .group_by(movie_tb.c.id)
        .order_by(desc(movie_tb.c.vote_average))
        .limit(size)
        .offset((page - 1) * size)
    )
    return await database.fetch_all(select_query)


async def get_watched_movies_by_user_id(
    user_id: int, page: int, size: int
) -> list[Record]:
    select_query = (
        select(movie_tb)
        .join_from(
            movie_tb, watch_history_tb, movie_tb.c.id == watch_history_tb.c.movie_id
        )
        .filter(watch_history_tb.c.user_id == user_id)
        .limit(size)
    )
    return await database.fetch_all(select_query)


# async def track_just_watched_movie(user_id: int, movie_id: int) -> list[Record]:
#     watch_history = get_or_create_watch_history_if_not_exist(
#         user_id=user_id, movie_id=movie_id
#     )
#     update_query = update(watch_history)
#     # watch_history
