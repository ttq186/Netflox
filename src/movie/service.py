from databases.interfaces import Record
from sqlalchemy import desc, func, or_, select
from sqlalchemy.sql.selectable import Select

from src.database import database
from src.movie.models import genre_tb, movie_genre_tb, movie_tb, watch_history_tb


async def create_watched_movie(user_id: int, movie_id: int) -> Record:
    insert_query = (
        watch_history_tb.insert()
        .values(user_id=user_id, movie_id=movie_id, view_count=1)
        .returning(watch_history_tb)
    )
    return await database.fetch_one(insert_query)  # type: ignore


async def update_watched_movie(id: int, values: dict) -> None:
    update_query = (
        watch_history_tb.update().values(values).where(watch_history_tb.c.id == id)
    )
    await database.execute(update_query)


def apply_pagination(query: Select, page: int, size: int) -> Select:
    return query.limit(size).offset((page - 1) * size)


def get_base_movie_select_query() -> Select:
    return (
        select(movie_tb, func.array_agg(genre_tb.c.name).label("genres"))
        .select_from(movie_tb)
        .join(movie_genre_tb)
        .join(genre_tb)
        .group_by(movie_tb.c.id)
    )


async def get_movie_by_id(id: int) -> Record | None:
    select_query = select(movie_tb).where(movie_tb.c.id == id)
    return await database.fetch_one(select_query)


async def get_random_movies(
    size: int, exclude_ids: list[int] | None = None
) -> list[Record]:
    select_query = get_base_movie_select_query()
    if exclude_ids:
        select_query = select_query.where(movie_tb.c.id.not_in(exclude_ids))
    select_query = select_query.order_by(func.random() * movie_tb.c.id).limit(size)
    return await database.fetch_all(select_query)


async def get_movies(
    page: int, size: int, search: str | None, genres: list[str] | None
) -> list[Record]:
    if genres:
        select_query = (
            select(movie_tb, func.array_agg(genre_tb.c.name).label("genres"))
            .select_from(movie_tb)
            .join(movie_genre_tb)
            .join(genre_tb)
            .where(genre_tb.c.name.in_(genres))
            .group_by(movie_tb.c.id)
        )
    else:
        select_query = get_base_movie_select_query()

    if search:
        select_query = select_query.where(
            or_(
                movie_tb.c.original_name.ilike(f"%{search}%"),
                movie_tb.c.title.ilike(f"%{search}%"),
            )
        )

    select_query = apply_pagination(query=select_query, page=page, size=size)
    return await database.fetch_all(select_query)


async def get_top_rated_movies(page: int, size: int) -> list[Record]:
    select_query = get_base_movie_select_query().order_by(desc(movie_tb.c.vote_average))
    select_query = apply_pagination(query=select_query, page=page, size=size)
    return await database.fetch_all(select_query)


async def get_watched_movies_by_user_id(
    user_id: int, page: int, size: int
) -> list[Record]:
    select_query = (
        get_base_movie_select_query()
        .join(watch_history_tb)
        .where(watch_history_tb.c.user_id == user_id)
        .order_by(desc(watch_history_tb.c.view_count))
    )
    select_query = apply_pagination(query=select_query, page=page, size=size)
    return await database.fetch_all(select_query)


async def get_recommended_movies_by_user_id(
    user_id: int, page: int, size: int
) -> list[Record]:
    movies = await get_watched_movies_by_user_id(user_id=user_id, page=page, size=size)
    if len(movies) >= size:
        return movies
    movie_ids = [movie["id"] for movie in movies]
    extra_movies = await get_random_movies(
        size=size - len(movies), exclude_ids=movie_ids
    )
    return [*extra_movies, *movies]


async def get_watched_movie_by_user_id_and_movie_id(
    user_id: int, movie_id: int
) -> Record | None:
    select_query = watch_history_tb.select().where(
        watch_history_tb.c.user_id == user_id, watch_history_tb.c.movie_id == movie_id
    )
    return await database.fetch_one(select_query)


async def track_just_watched_movie(user_id: int, movie_id: int) -> Record | dict:
    watch_history = await get_watched_movie_by_user_id_and_movie_id(
        user_id=user_id, movie_id=movie_id
    )
    if not watch_history:
        return await create_watched_movie(user_id=user_id, movie_id=movie_id)

    new_view_count = watch_history["view_count"] + 1
    await update_watched_movie(
        id=watch_history["id"],
        values={"view_count": new_view_count},
    )
    return {**watch_history, "view_count": new_view_count}


async def get_genres() -> list[Record]:
    return await database.fetch_all(genre_tb.select())
