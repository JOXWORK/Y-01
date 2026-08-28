"""create moderation rules table

Revision ID: 7e7a2eccb299
Revises: 523d2a6fa4e4
Create Date: 2026-08-28 14:24:24.416186

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7e7a2eccb299"
down_revision: Union[str, Sequence[str], None] = "523d2a6fa4e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "moderation_rules",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("rules", sa.JSON(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_moderation_rules__user_id__users__id"), ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_moderation_rules__id")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("moderation_rules")
