"""add rules_numbered column

Revision ID: 9c5cff3a00f7
Revises: 7afa97fac4db
Create Date: 2026-09-10 20:00:05.459016

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c5cff3a00f7"
down_revision: Union[str, Sequence[str], None] = "7afa97fac4db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("moderation_rules", sa.Column("rules_numbered", sa.JSON(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("moderation_rules", "rules_numbered")
