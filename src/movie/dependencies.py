from src.movie import service
from src.movie.exceptions import MovieNotFound


async def valid_movie_id(movie_id: int) -> int:
    if not await service.get_movie_by_id(id=movie_id):
        raise MovieNotFound(id=movie_id)
    return movie_id
