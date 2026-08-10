"""add timezone to user session table

Revision ID: e6b688cceaba
Revises: 95612225c405
Create Date: 2026-06-05 11:36:48.991666

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e6b688cceaba"
down_revision: Union[str, Sequence[str], None] = "95612225c405"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #! op.create_unique_constraint(op.f("uq_access_tokens__token"), "access_tokens", ["token"])
    op.alter_column(
        "user_sessions",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "user_sessions",
        "revoked_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "user_sessions",
        "revoked_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
    )
    op.alter_column(
        "user_sessions",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    #! op.drop_constraint(op.f("uq_access_tokens__token"), "access_tokens", type_="unique")
