"""make_user_id_nullable_in_predictions

Revision ID: d40f0d93d9b4
Revises: 001_create_users_predictions
Create Date: 2025-11-23 14:32:35.884295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd40f0d93d9b4'
down_revision: Union[str, None] = '001_create_users_predictions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make user_id nullable in predictions table
    op.alter_column('predictions', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade() -> None:
    # Revert user_id to NOT NULL in predictions table
    op.alter_column('predictions', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=False)

