"""example_table_init

Revision ID: b5f9a9fba4b3
Revises:
Create Date: 2025-09-17 18:38:21.265346

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b5f9a9fba4b3"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "examples",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("example", sa.String(), server_default="example", nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_examples_id")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("examples")
