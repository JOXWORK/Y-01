"""add uniq constraint to user_id

Revision ID: 7afa97fac4db
Revises: 7e7a2eccb299
Create Date: 2026-08-29 11:47:52.099891

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7afa97fac4db"
down_revision: Union[str, Sequence[str], None] = "7e7a2eccb299"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(op.f("uq_moderation_rules__user_id"), "moderation_rules", ["user_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_moderation_rules__user_id"), "moderation_rules", type_="unique")
