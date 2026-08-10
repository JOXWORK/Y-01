"""add session id column to access token table

Revision ID: f0c0653c209b
Revises: 47fcb8c40796
Create Date: 2026-06-08 10:09:41.097613

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f0c0653c209b"
down_revision: Union[str, Sequence[str], None] = "47fcb8c40796"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("access_tokens", sa.Column("session_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f("fk_access_tokens__session_id__user_sessions__id"),
        "access_tokens",
        "user_sessions",
        ["session_id"],
        ["id"],
        ondelete="cascade",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("fk_access_tokens__session_id__user_sessions__id"), "access_tokens", type_="foreignkey")
    op.drop_column("access_tokens", "session_id")
