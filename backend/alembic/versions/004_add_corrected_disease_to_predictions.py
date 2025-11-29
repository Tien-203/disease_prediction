"""add_corrected_disease_to_predictions

Revision ID: 004_add_corrected_disease
Revises: 003_update_user_role_constraint
Create Date: 2025-01-27 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_add_corrected_disease'
down_revision: Union[str, None] = '003_update_user_role_constraint'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add corrected_disease column to predictions table
    op.add_column('predictions', sa.Column('corrected_disease', sa.String(length=100), nullable=True))


def downgrade() -> None:
    # Remove corrected_disease column from predictions table
    op.drop_column('predictions', 'corrected_disease')



