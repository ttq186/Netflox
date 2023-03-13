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

watchlist = Table(
    "watchlist",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("movie_id", ForeignKey("movie.id", ondelete="CASCADE"), nullable=False),
)


watch_history = Table(
    "watch_history",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("movie_id", ForeignKey("movie.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)


rating = Table(
    "rating",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("movie_id", ForeignKey("movie.id", ondelete="CASCADE"), nullable=False),
    Column("score", DECIMAL(2, 1), nullable=False),
)

review = Table(
    "review",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("movie_id", ForeignKey("movie.id", ondelete="CASCADE"), nullable=False),
    Column("content", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("created_at", DateTime, onupdate=func.now()),
)
