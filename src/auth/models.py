from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    LargeBinary,
    String,
    Table,
    func,
)

from src.database import metadata

user = Table(
    "user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("is_active", Boolean, server_default="false", nullable=False),
    Column("auth_method", String, server_default="NORMAL"),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

refresh_token_table = Table(
    "refresh_token",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("token", String, nullable=False),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)
