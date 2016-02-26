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
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('purchase_price', sa.Float(), server_default='0', nullable=False))


def downgrade():
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_column('purchase_price')
