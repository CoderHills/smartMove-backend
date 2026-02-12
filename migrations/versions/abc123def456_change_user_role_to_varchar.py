"""Change user_role from enum to VARCHAR.

Revision ID: abc123def456
Revises: f7bfc2104dfd
Create Date: 2026-02-11

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123def456'
down_revision = 'f7bfc2104dfd'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the old enum type
    op.execute("DROP TYPE IF EXISTS userrole")
    
    # Change role column to VARCHAR
    op.alter_column('users', 'role', 
        existing_type=sa.Enum('CUSTOMER', 'MOVER', 'ADMIN', name='userrole'),
        type_=sa.String(20),
        existing_nullable=False)

def downgrade():
    # Change back to enum
    op.alter_column('users', 'role',
        existing_type=sa.String(20),
        type_=sa.Enum('CUSTOMER', 'MOVER', 'ADMIN', name='userrole'),
        existing_nullable=False)

