"""create access_token table

Revision ID: 6ef3e69ec319
Revises: c0d245155695
Create Date: 2026-05-30 12:02:15.198073

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy  # Necessary hand import
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6ef3e69ec319"
down_revision: Union[str, Sequence[str], None] = "c0d245155695"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "access_tokens",
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_access_tokens:user_id__users:id"), ondelete="cascade"),
        sa.PrimaryKeyConstraint("token", name=op.f("pk_access_tokens_token")),
        sa.UniqueConstraint("token", name=op.f("uq_access_tokens_token")),
    )
    op.create_index(op.f("ix_access_tokens_created_at"), "access_tokens", ["created_at"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_access_tokens_created_at"), table_name="access_tokens")
    op.drop_table("access_tokens")
