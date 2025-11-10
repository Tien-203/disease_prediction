"""Create users table and update predictions with user_id

Revision ID: 001_create_users_predictions
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_create_users_predictions'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='patient'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("role IN ('patient', 'data_scientist')", name='check_user_role'),
        sa.CheckConstraint('age >= 0 AND age <= 150', name='check_user_age'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes on users table
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'], unique=False)
    
    # Update predictions table: add user_id and alternatives columns
    # Check if predictions table exists (it might from previous setup)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    if 'predictions' in tables:
        # Table exists - add columns as nullable first, then we can update
        op.add_column('predictions', sa.Column('user_id', sa.Integer(), nullable=True))
        op.add_column('predictions', sa.Column('alternatives', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
        
        # If there are existing predictions, you may want to:
        # 1. Create a default user for existing predictions
        # 2. Or delete existing predictions
        # For now, we'll keep user_id nullable for existing data
        
        # Create foreign key constraint
        op.create_foreign_key(
            'fk_predictions_user',
            'predictions', 'users',
            ['user_id'], ['id'],
            ondelete='CASCADE'
        )
        
        # Create index on user_id
        op.create_index(op.f('ix_predictions_user_id'), 'predictions', ['user_id'], unique=False)
        
        # Add check constraint for confidence if it doesn't exist
        try:
            op.create_check_constraint(
                'check_confidence_range',
                'predictions',
                'confidence >= 0.0 AND confidence <= 1.0'
            )
        except Exception:
            # Constraint might already exist
            pass
    else:
        # Table doesn't exist - create it with user_id as NOT NULL
        op.create_table(
            'predictions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('symptoms', postgresql.ARRAY(sa.Text()), nullable=False),
            sa.Column('predicted_disease', sa.String(length=100), nullable=False),
            sa.Column('confidence', sa.Float(), nullable=False),
            sa.Column('alternatives', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
            sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('session_id', sa.String(length=100), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='fk_predictions_user'),
            sa.CheckConstraint('confidence >= 0.0 AND confidence <= 1.0', name='check_confidence_range'),
            sa.PrimaryKeyConstraint('id')
        )
        
        # Create indexes
        op.create_index(op.f('ix_predictions_id'), 'predictions', ['id'], unique=False)
        op.create_index(op.f('ix_predictions_user_id'), 'predictions', ['user_id'], unique=False)
        op.create_index(op.f('ix_predictions_timestamp'), 'predictions', ['timestamp'], unique=False)
        op.create_index(op.f('ix_predictions_session_id'), 'predictions', ['session_id'], unique=False)


def downgrade() -> None:
    # Remove check constraint
    op.drop_constraint('check_confidence_range', 'predictions', type_='check')
    
    # Drop index and foreign key
    op.drop_index(op.f('ix_predictions_user_id'), table_name='predictions')
    op.drop_constraint('fk_predictions_user', 'predictions', type_='foreignkey')
    
    # Remove columns from predictions
    op.drop_column('predictions', 'alternatives')
    op.drop_column('predictions', 'user_id')
    
    # Drop users table indexes
    op.drop_index(op.f('ix_users_is_active'), table_name='users')
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    
    # Drop users table
    op.drop_table('users')

