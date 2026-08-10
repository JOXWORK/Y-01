"""change naming convention

Revision ID: 11a99d442942
Revises: 6ef3e69ec319
Create Date: 2026-06-01 14:47:42.150990

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "11a99d442942"
down_revision: Union[str, Sequence[str], None] = "6ef3e69ec319"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    ## Index
    op.execute("ALTER INDEX ix_users_email RENAME TO ix_users__email")
    op.execute("ALTER INDEX ix_access_tokens_created_at RENAME TO ix_access_tokens__created_at")

    # ## Unique Constraint
    # op.execute("ALTER TABLE access_tokens RENAME CONSTRAINT uq_access_tokens_token TO uq_access_tokens__token")

    ## ForeignKey Constraint
    op.execute(
        'ALTER TABLE access_tokens RENAME CONSTRAINT "fk_access_tokens:user_id__users:id" TO fk_access_tokens__user_id__users__id'
    )

    ## PrimaryKey Constraint
    op.execute("ALTER TABLE examples RENAME CONSTRAINT pk_examples_id TO pk_examples__id")
    op.execute("ALTER TABLE users RENAME CONSTRAINT pk_users_id TO pk_users__id")
    op.execute("ALTER TABLE access_tokens RENAME CONSTRAINT pk_access_tokens_token TO pk_access_tokens__token")


def downgrade() -> None:
    """Downgrade schema."""
    ## Index
    op.execute("ALTER INDEX ix_users__email RENAME TO ix_users_email")
    op.execute("ALTER INDEX ix_access_tokens__created_at RENAME TO ix_access_tokens_created_at")

    # ## Unique Constraint
    # op.execute("ALTER TABLE access_tokens RENAME CONSTRAINT uq_access_tokens__token TO uq_access_tokens_token")

    ## ForeignKey Constraint
    op.execute(
        'ALTER TABLE access_tokens RENAME CONSTRAINT fk_access_tokens__user_id__users__id TO "fk_access_tokens:user_id__users:id"'
    )

    ## PrimaryKey Constraint
    op.execute("ALTER TABLE examples RENAME CONSTRAINT pk_examples__id TO pk_examples_id")
    op.execute("ALTER TABLE users RENAME CONSTRAINT pk_users__id TO pk_users_id")
    op.execute("ALTER TABLE access_tokens RENAME CONSTRAINT pk_access_tokens__token TO pk_access_tokens_token")
