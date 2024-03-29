"""add_models

Revision ID: a7f05d87566c
Revises: b38a1ec6fa49
Create Date: 2023-03-13 17:15:10.513816

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a7f05d87566c"
down_revision = "b38a1ec6fa49"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "actor",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("gender", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("birthdate", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("actor_pkey")),
    )
    op.create_table(
        "genre",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("genre_pkey")),
    )
    op.create_table(
        "movie",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("original_name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("release_yeare", sa.Integer(), nullable=False),
        sa.Column("background_url", sa.String(), nullable=False),
        sa.Column("trailer_url", sa.String(), nullable=False),
        sa.Column("imdb_rating", sa.DECIMAL(precision=2, scale=1), nullable=True),
        sa.Column("original_language", sa.String(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("movie_pkey")),
    )
    op.create_table(
        "subscription",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=True),
        sa.Column("billing_period", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("subscription_pkey")),
    )
    op.create_table(
        "movie_actor",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("actor_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["actor.id"],
            name=op.f("movie_actor_actor_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            name=op.f("movie_actor_movie_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("movie_actor_pkey")),
    )
    op.create_table(
        "movie_genre",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genre.id"],
            name=op.f("movie_genre_genre_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            name=op.f("movie_genre_movie_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("movie_genre_pkey")),
    )
    op.create_table(
        "payment_history",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("subscription_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=True),
        sa.Column("billing_period", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["subscription_id"],
            ["subscription.id"],
            name=op.f("payment_history_subscription_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("payment_history_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("payment_history_pkey")),
    )
    op.create_table(
        "rating",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.DECIMAL(precision=2, scale=1), nullable=False),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            name=op.f("rating_movie_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("rating_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("rating_pkey")),
    )
    op.create_table(
        "review",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            name=op.f("review_movie_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("review_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("review_pkey")),
    )
    op.create_table(
        "watch_history",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            name=op.f("watch_history_movie_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("watch_history_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("watch_history_pkey")),
    )
    op.create_table(
        "watchlist",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            name=op.f("watchlist_movie_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("watchlist_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("watchlist_pkey")),
    )
    op.add_column(
        "refresh_token",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
    )
    op.add_column("refresh_token", sa.Column("token", sa.String(), nullable=False))
    op.drop_column("refresh_token", "refresh_token")
    op.drop_column("refresh_token", "uuid")
    op.add_column(
        "user",
        sa.Column("is_active", sa.Boolean(), server_default="false", nullable=False),
    )
    op.add_column("user", sa.Column("auth_type", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "auth_type")
    op.drop_column("user", "is_active")
    op.add_column(
        "refresh_token",
        sa.Column("uuid", postgresql.UUID(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "refresh_token",
        sa.Column("refresh_token", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("refresh_token", "token")
    op.drop_column("refresh_token", "id")
    op.drop_table("watchlist")
    op.drop_table("watch_history")
    op.drop_table("review")
    op.drop_table("rating")
    op.drop_table("payment_history")
    op.drop_table("movie_genre")
    op.drop_table("movie_actor")
    op.drop_table("subscription")
    op.drop_table("movie")
    op.drop_table("genre")
    op.drop_table("actor")
    # ### end Alembic commands ###
