"""add_indexes

Revision ID: 61cc5dc74f01
Revises: b964188bc2b0
Create Date: 2023-03-16 03:06:11.289038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61cc5dc74f01"
down_revision = "b964188bc2b0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("genre_name_idx"), "genre", ["name"], unique=False)
    op.create_index(
        op.f("movie_original_name_idx"), "movie", ["original_name"], unique=False
    )
    op.create_index(op.f("movie_title_idx"), "movie", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("movie_title_idx"), table_name="movie")
    op.drop_index(op.f("movie_original_name_idx"), table_name="movie")
    op.drop_index(op.f("genre_name_idx"), table_name="genre")
    # ### end Alembic commands ###