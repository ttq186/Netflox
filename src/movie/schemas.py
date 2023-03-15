from datetime import date

from pydantic import condecimal

from src.schemas import ORJSONModel


class MovieOut(ORJSONModel):
    id: int
    title: str
    original_name: str
    description: str | None
    release_date: date
    background_url: str
    trailer_url: str
    vote_average: condecimal(gt=0, le=10, max_digits=2, decimal_places=1)  # type: ignore
    genres: list[str]
    original_language: str | None


class WatchHistoryData(ORJSONModel):
    id: int | None
    user_id: int
    movie_id: int
    view_count: int | None


class WatchHistoryOut(ORJSONModel):
    id: int
    user_id: int
    movie_id: int
    view_count: int
