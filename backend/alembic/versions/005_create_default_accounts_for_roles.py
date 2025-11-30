"""create_default_accounts_for_roles

Revision ID: 005_create_default_accounts
Revises: 004_add_corrected_disease
Create Date: 2025-01-27 13:00:00.000000

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext

# Password hashing context (same as in app.core.security)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# revision identifiers, used by Alembic.
revision: str = '005_create_default_accounts'
down_revision: Union[str, None] = '004_add_corrected_disease'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Hash the password once for all accounts
    password_hash = pwd_context.hash("123456")
    
    # Define the 4 roles
    roles = ['patient', 'doctor', 'researcher', 'data_scientist']
    
    # Get the users table
    users_table = sa.table(
        'users',
        sa.column('email', sa.String),
        sa.column('password_hash', sa.String),
        sa.column('name', sa.String),
        sa.column('role', sa.String),
        sa.column('is_active', sa.Boolean),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )
    
    # Insert 4 accounts, one for each role
    for role in roles:
        op.execute(
            users_table.insert().values(
                email=f"{role}@gmail.com",
                password_hash=password_hash,
                name=f"{role}_1",
                role=role,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        )


def downgrade() -> None:
    # Delete the 4 default accounts
    roles = ['patient', 'doctor', 'researcher', 'data_scientist']
    
    users_table = sa.table(
        'users',
        sa.column('email', sa.String),
    )
    
    for role in roles:
        op.execute(
            users_table.delete().where(
                users_table.c.email == f"{role}@gmail.com"
            )
        )

