"""StoreKeeper v0.2.0

Revision ID: 305c2b0084f
Revises: 90481802d
Create Date: 2015-11-16 09:06:28.270103

"""

revision = '305c2b0084f'
down_revision = '90481802d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('item', sa.Column('purchase_price', sa.Float(), server_default='0', nullable=False))


def downgrade():
    op.drop_column('item', 'purchase_price')
