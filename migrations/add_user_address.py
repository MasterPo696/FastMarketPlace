from app.config import db
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('user', sa.Column('address', sa.JSON, nullable=True))

def downgrade():
    op.drop_column('user', 'address') 