"""create refresh tokens table

Revision ID: 47fcb8c40796
Revises: e6b688cceaba
Create Date: 2026-06-05 15:06:19.985950

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "47fcb8c40796"
down_revision: Union[str, Sequence[str], None] = "e6b688cceaba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "refresh_tokens",
        sa.Column("token_hash", sa.String(length=1024), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["user_sessions.id"],
            name=op.f("fk_refresh_tokens__session_id__user_sessions__id"),
            ondelete="cascade",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_refresh_tokens__user_id__users__id"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_tokens__id")),
    )
    op.create_index(op.f("ix_refresh_tokens__created_at"), "refresh_tokens", ["created_at"], unique=False)
    op.create_index(op.f("ix_refresh_tokens__revoked_at"), "refresh_tokens", ["revoked_at"], unique=False)
    op.create_index(op.f("ix_refresh_tokens__used_at"), "refresh_tokens", ["used_at"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_refresh_tokens__used_at"), table_name="refresh_tokens")
    op.drop_index(op.f("ix_refresh_tokens__revoked_at"), table_name="refresh_tokens")
    op.drop_index(op.f("ix_refresh_tokens__created_at"), table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
