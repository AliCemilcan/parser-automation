"""add_last_few_column

Revision ID: c35c80062bfa
Revises: 836eb8483f71
Create Date: 2022-10-30 15:00:39.018587

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c35c80062bfa"
down_revision = "836eb8483f71"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
