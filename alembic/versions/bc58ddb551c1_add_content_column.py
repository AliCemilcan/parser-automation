"""add content column

Revision ID: bc58ddb551c1
Revises: 34091c5bfb89
Create Date: 2022-10-30 14:47:34.165758

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bc58ddb551c1"
down_revision = "34091c5bfb89"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
