from fastapi.exceptions import HTTPException


class MovieNotFound(HTTPException):
    def __init__(self, id: int):
        detail = f"Movie with id: {id} not found!"
        super().__init__(status_code=404, detail=detail)
