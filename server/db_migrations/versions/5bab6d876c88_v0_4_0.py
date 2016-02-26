"""StoreKeeper v0.4.0

Revision ID: 5bab6d876c88
Revises: 58d249b8b61
Create Date: 2016-02-26 21:11:00.993867

"""

revision = '5bab6d876c88'
down_revision = '58d249b8b61'

from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=15), nullable=True))

    with op.batch_alter_table('item_version', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=15), autoincrement=False, nullable=True))

    with op.batch_alter_table('user_version', schema=None) as batch_op:
        batch_op.drop_column('password_hash')


def downgrade():
    with op.batch_alter_table('user_version', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(length=80), autoincrement=False, nullable=True))

    with op.batch_alter_table('item_version', schema=None) as batch_op:
        batch_op.drop_column('location')

    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_column('location')
