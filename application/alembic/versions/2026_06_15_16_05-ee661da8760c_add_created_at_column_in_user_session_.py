"""add created_at column in user_session table

Revision ID: ee661da8760c
Revises: f0c0653c209b
Create Date: 2026-06-15 16:05:14.868705

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ee661da8760c"
down_revision: Union[str, Sequence[str], None] = "f0c0653c209b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user_sessions", sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index(op.f("ix_user_sessions__expires_at"), "user_sessions", ["expires_at"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_user_sessions__expires_at"), table_name="user_sessions")
    op.drop_column("user_sessions", "expires_at")
