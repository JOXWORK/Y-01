"""rename token hash column

Revision ID: e30aae3e88d3
Revises: ee661da8760c
Create Date: 2026-07-09 20:27:32.743573

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e30aae3e88d3"
down_revision: Union[str, Sequence[str], None] = "ee661da8760c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("refresh_tokens", sa.Column("fingerprint", sa.String(length=1024), nullable=False))
    op.drop_column("refresh_tokens", "token_hash")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("refresh_tokens", sa.Column("token_hash", sa.String(length=1024), autoincrement=False, nullable=False))
    op.drop_column("refresh_tokens", "fingerprint")
