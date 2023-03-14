from sqlalchemy import (
    DECIMAL,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Table,
    func,
)

from src.database import metadata

movie = Table(
    "movie",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("title", String, nullable=False),
    Column("original_name", String, nullable=False),
    Column("description", String),
    Column("release_year", Integer, nullable=False),
    Column("background_url", String, nullable=False),
    Column("trailer_url", String, nullable=False),
    Column("imdb_rating", DECIMAL(2, 1)),
    Column("original_language", String),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

genre = Table(
    "genre",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
)

movie_genre = Table(
    "movie_genre",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("movie_id", ForeignKey("movie.id", ondelete="CASCADE"), nullable=False),
    Column("genre_id", ForeignKey("genre.id", ondelete="CASCADE"), nullable=False),
)


actor = Table(
    "actor",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("gender", String, nullable=False),
    Column("description", String, nullable=False),
    Column("birthdate", String, nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

movie_actor = Table(
    "movie_actor",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("actor_id", ForeignKey("actor.id", ondelete="CASCADE"), nullable=False),
    Column("movie_id", ForeignKey("movie.id", ondelete="CASCADE"), nullable=False),
)
