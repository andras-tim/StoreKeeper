"""StoreKeeper v0.3.0

Revision ID: 58d249b8b61
Revises: 305c2b0084f
Create Date: 2015-12-15 21:40:26.652582

"""

revision = '58d249b8b61'
down_revision = '305c2b0084f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('acquisition_item_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('acquisition_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('item_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.Float(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('acquisition_item_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_acquisition_item_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_acquisition_item_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_acquisition_item_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('acquisition_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('comment', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('acquisition_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_acquisition_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_acquisition_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_acquisition_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('barcode_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('barcode', sa.String(length=15), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.Float(), autoincrement=False, nullable=True),
    sa.Column('item_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('master', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('main', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('barcode_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_barcode_version_barcode'), ['barcode'], unique=False)
        batch_op.create_index(batch_op.f('ix_barcode_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_barcode_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_barcode_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('customer_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=60), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('customer_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_customer_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_customer_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_customer_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('item_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=60), autoincrement=False, nullable=True),
    sa.Column('vendor_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('article_number', sa.String(length=20), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.Float(), autoincrement=False, nullable=True),
    sa.Column('warning_quantity', sa.Float(), autoincrement=False, nullable=True),
    sa.Column('purchase_price', sa.Float(), server_default='0', autoincrement=False, nullable=True),
    sa.Column('unit_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('item_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_item_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_item_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_item_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('stocktaking_item_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('stocktaking_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('item_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.Float(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('stocktaking_item_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_stocktaking_item_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_stocktaking_item_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_stocktaking_item_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('stocktaking_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('comment', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('close_timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('close_user_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('stocktaking_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_stocktaking_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_stocktaking_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_stocktaking_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('unit_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('unit', sa.String(length=20), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('unit_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_unit_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_unit_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_unit_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('user_config_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('name', sa.String(length=40), autoincrement=False, nullable=True),
    sa.Column('value', sa.String(length=200), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('user_config_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_config_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_config_version_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_config_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_config_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('user_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('username', sa.String(length=30), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.String(length=80), autoincrement=False, nullable=True),
    sa.Column('email', sa.String(length=50), autoincrement=False, nullable=True),
    sa.Column('admin', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('disabled', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('user_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_version_transaction_id'), ['transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_version_username'), ['username'], unique=False)

    op.create_table('vendor_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=60), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('vendor_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_vendor_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_vendor_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_vendor_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('work_item_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('work_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('item_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('outbound_quantity', sa.Float(), autoincrement=False, nullable=True),
    sa.Column('returned_quantity', sa.Float(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('work_item_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_work_item_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_work_item_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_work_item_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('work_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('customer_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('comment', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('outbound_close_timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('outbound_close_user_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('returned_close_timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('returned_close_user_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    with op.batch_alter_table('work_version', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_work_version_end_transaction_id'), ['end_transaction_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_work_version_operation_type'), ['operation_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_work_version_transaction_id'), ['transaction_id'], unique=False)

    op.create_table('transaction',
    sa.Column('issued_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('remote_addr', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_transaction_user_id'), ['user_id'], unique=False)


def downgrade():
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_transaction_user_id'))

    op.drop_table('transaction')
    with op.batch_alter_table('work_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_work_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_work_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_work_version_end_transaction_id'))

    op.drop_table('work_version')
    with op.batch_alter_table('work_item_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_work_item_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_work_item_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_work_item_version_end_transaction_id'))

    op.drop_table('work_item_version')
    with op.batch_alter_table('vendor_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_vendor_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_vendor_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_vendor_version_end_transaction_id'))

    op.drop_table('vendor_version')
    with op.batch_alter_table('user_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_version_username'))
        batch_op.drop_index(batch_op.f('ix_user_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_user_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_user_version_end_transaction_id'))

    op.drop_table('user_version')
    with op.batch_alter_table('user_config_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_config_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_user_config_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_user_config_version_name'))
        batch_op.drop_index(batch_op.f('ix_user_config_version_end_transaction_id'))

    op.drop_table('user_config_version')
    with op.batch_alter_table('unit_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_unit_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_unit_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_unit_version_end_transaction_id'))

    op.drop_table('unit_version')
    with op.batch_alter_table('stocktaking_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_stocktaking_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_stocktaking_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_stocktaking_version_end_transaction_id'))

    op.drop_table('stocktaking_version')
    with op.batch_alter_table('stocktaking_item_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_stocktaking_item_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_stocktaking_item_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_stocktaking_item_version_end_transaction_id'))

    op.drop_table('stocktaking_item_version')
    with op.batch_alter_table('item_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_item_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_item_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_item_version_end_transaction_id'))

    op.drop_table('item_version')
    with op.batch_alter_table('customer_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_customer_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_customer_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_customer_version_end_transaction_id'))

    op.drop_table('customer_version')
    with op.batch_alter_table('barcode_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_barcode_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_barcode_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_barcode_version_end_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_barcode_version_barcode'))

    op.drop_table('barcode_version')
    with op.batch_alter_table('acquisition_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_acquisition_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_acquisition_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_acquisition_version_end_transaction_id'))

    op.drop_table('acquisition_version')
    with op.batch_alter_table('acquisition_item_version', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_acquisition_item_version_transaction_id'))
        batch_op.drop_index(batch_op.f('ix_acquisition_item_version_operation_type'))
        batch_op.drop_index(batch_op.f('ix_acquisition_item_version_end_transaction_id'))

    op.drop_table('acquisition_item_version')
