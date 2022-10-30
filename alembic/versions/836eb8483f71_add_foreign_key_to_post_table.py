"""add foreign key to post table

Revision ID: 836eb8483f71
Revises: 40589b70935d
Create Date: 2022-10-30 14:54:40.862578

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "836eb8483f71"
down_revision = "40589b70935d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_constraint("posts", "owner_id")
    pass
