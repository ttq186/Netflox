from datetime import datetime, date

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
