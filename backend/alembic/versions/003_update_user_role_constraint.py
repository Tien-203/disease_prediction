"""update_user_role_constraint

Revision ID: 003_update_user_role_constraint
Revises: d40f0d93d9b4
Create Date: 2025-11-24 20:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_update_user_role_constraint'
down_revision: Union[str, None] = 'd40f0d93d9b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the old constraint that only allows 'patient' and 'data_scientist'
    op.drop_constraint('check_user_role', 'users', type_='check')
    
    # Create new constraint that allows all four roles
    op.create_check_constraint(
        'check_user_role',
        'users',
        "role IN ('patient', 'doctor', 'researcher', 'data_scientist')"
    )


def downgrade() -> None:
    # Revert to the old constraint
    op.drop_constraint('check_user_role', 'users', type_='check')
    
    # Restore the old constraint with only 'patient' and 'data_scientist'
    op.create_check_constraint(
        'check_user_role',
        'users',
        "role IN ('patient', 'data_scientist')"
    )

