import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src import redis
from src.auth.router import router as auth_router
from src.config import app_configs, settings
from src.database import database
from src.movie.router import router as movie_router

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)
app.add_middleware(GZipMiddleware, minimum_size=5000)


@app.on_event("startup")
async def startup() -> None:
    pool = aioredis.ConnectionPool.from_url(
        settings.REDIS_URL, max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
    await redis.redis_client.close()


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(movie_router)
