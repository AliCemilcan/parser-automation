"""Add User Table

Revision ID: 40589b70935d
Revises: bc58ddb551c1
Create Date: 2022-10-30 14:51:04.037129

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "40589b70935d"
down_revision = "bc58ddb551c1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
