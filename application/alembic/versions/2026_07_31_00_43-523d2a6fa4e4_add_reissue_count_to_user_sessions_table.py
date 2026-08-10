"""add reissue count to user_sessions table

Revision ID: 523d2a6fa4e4
Revises: e30aae3e88d3
Create Date: 2026-07-31 00:43:30.721393

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "523d2a6fa4e4"
down_revision: Union[str, Sequence[str], None] = "e30aae3e88d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user_sessions", sa.Column("reissue_count", sa.Integer(), server_default="0", nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user_sessions", "reissue_count")
