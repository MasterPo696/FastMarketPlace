"""Add is_active column to item table

Revision ID: add_is_active_column
Revises: 50748c94ac18
Create Date: 2025-02-21 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_is_active_column'
down_revision = '50748c94ac18'
branch_labels = None
depends_on = None

def upgrade():
    # Add is_active column with default value True
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'))

def downgrade():
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_column('is_active') 