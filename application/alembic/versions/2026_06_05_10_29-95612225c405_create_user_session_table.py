"""create user session table

Revision ID: 95612225c405
Revises: 11a99d442942
Create Date: 2026-06-05 10:29:53.202295

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "95612225c405"
down_revision: Union[str, Sequence[str], None] = "11a99d442942"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user_sessions",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_user_sessions__user_id__users__id"), ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_sessions__id")),
    )
    op.create_index(op.f("ix_user_sessions__created_at"), "user_sessions", ["created_at"], unique=False)
    op.create_index(op.f("ix_user_sessions__revoked_at"), "user_sessions", ["revoked_at"], unique=False)
    #! op.create_unique_constraint(op.f("uq_access_tokens__token"), "access_tokens", ["token"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_user_sessions__revoked_at"), table_name="user_sessions")
    op.drop_index(op.f("ix_user_sessions__created_at"), table_name="user_sessions")
    op.drop_table("user_sessions")
