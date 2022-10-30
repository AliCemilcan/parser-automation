"""cerate post table

Revision ID: 34091c5bfb89
Revises:
Create Date: 2022-10-30 12:44:46.762631

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "34091c5bfb89"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
