from fastapi import APIRouter, Depends, Query

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.movie import service
from src.movie.dependencies import valid_movie_id
from src.movie.schemas import MovieOut, WatchHistoryOut

router = APIRouter(prefix="/movies", tags=["Movie"])


@router.get("/top_rated")
async def get_top_rated_movies(
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=20),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> list[MovieOut]:
    movies = await service.get_top_rated_movies(page=page, size=size)
    return movies  # type: ignore


@router.get("/watched")
async def get_watched_movies(
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=20),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> list[MovieOut]:
    movies = await service.get_watched_movies_by_user_id(
        user_id=jwt_data.user_id, page=page, size=size
    )
    return movies  # type: ignore


@router.post("/tracking")
async def track_just_watched_movie(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    movie_id: int = Depends(valid_movie_id),
) -> WatchHistoryOut:
    watch_history = await service.track_just_watched_movie(
        user_id=jwt_data.user_id, movie_id=movie_id
    )
    return watch_history  # type: ignore
