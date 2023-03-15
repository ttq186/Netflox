"""rename_fields

Revision ID: bc3aad78c1b0
Revises: f14e405e52b8
Create Date: 2023-03-15 03:33:49.054715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bc3aad78c1b0"
down_revision = "f14e405e52b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("movie", sa.Column("release_date", sa.DATE(), nullable=False))
    op.add_column(
        "movie",
        sa.Column("vote_average", sa.DECIMAL(precision=2, scale=1), nullable=True),
    )
    op.drop_constraint("unique_constraint", "movie", type_="unique")
    op.drop_column("movie", "imdb_rating")
    op.drop_column("movie", "release_year")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "movie",
        sa.Column("release_year", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "movie",
        sa.Column(
            "imdb_rating",
            sa.NUMERIC(precision=2, scale=1),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_unique_constraint(
        "unique_constraint", "movie", ["title", "original_name"]
    )
    op.drop_column("movie", "vote_average")
    op.drop_column("movie", "release_date")
    # ### end Alembic commands ###