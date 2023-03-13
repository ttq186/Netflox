from sqlalchemy import Column, ForeignKey, Identity, Integer, String, Table

from src.database import metadata

subscription = Table(
    "subscription",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("price", Integer),
    Column("billing_period", String),
)


payment_history = Table(
    "payment_history",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column(
        "subscription_id",
        ForeignKey("subscription.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("price", Integer),
    Column("billing_period", String),
)
