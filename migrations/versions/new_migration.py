"""Add amount property and update isAvailable logic

Revision ID: new_migration
Revises: previous_migration
Create Date: 2024-03-xx

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Rename amount to _amount
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.alter_column('amount', new_column_name='_amount')
    
    # Update isAvailable based on amount
    op.execute('UPDATE item SET isAvailable = CASE WHEN _amount > 0 THEN 1 ELSE 0 END')

def downgrade():
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.alter_column('_amount', new_column_name='amount') 