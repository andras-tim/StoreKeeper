from datetime import datetime

from app.server import db, bcrypt
from app.modules.view_helper_for_models import nested_fields


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    disabled = db.Column(db.Boolean, nullable=False, default=False)

    configs = db.relationship('UserConfig', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s} [admin={!r} disabled={!r}]'.format(self.username, self.admin, self.disabled)

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    # flask-loginmanager
    def is_authenticated(self) -> bool:
        return True

    # flask-loginmanager
    def is_active(self) -> bool:
        return not self.disabled

    # flask-loginmanager
    def is_anonymous(self) -> bool:
        return False

    # flask-loginmanager
    def get_id(self) -> str:
        return str(self.id)


@nested_fields(user=User)
class UserConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(40), index=True, nullable=False)
    value = db.Column(db.String(200), nullable=False)

    configs = db.relationship('User')

    __table_args__ = (
        db.Index('user_config__can_not_add_one_name_twice_to_a_user', 'user_id', 'name', unique=True),
    )

    def __repr__(self)-> str:
        return '{!s} [{!r}]'.format(self.id, self.name)


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)

    items = db.relationship('Item', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s}'.format(self.name)


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self)-> str:
        return '{!s}'.format(self.unit)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)

    def __repr__(self)-> str:
        return '{!s}'.format(self.name)


@nested_fields(vendor=Vendor, unit=Unit)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    article_number = db.Column(db.String(20))
    quantity = db.Column(db.Float, nullable=False, default=0)
    warning_quantity = db.Column(db.Float, nullable=False, default=0)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)

    vendor = db.relationship('Vendor', lazy='joined')
    unit = db.relationship('Unit', lazy='joined')
    barcodes = db.relationship('Barcode', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s}'.format(self.name)


@nested_fields(item=Item)
class Barcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(15), nullable=False, unique=True, index=True)
    quantity = db.Column(db.Float, nullable=False, default=1)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    master = db.Column(db.Boolean, default=False)
    main = db.Column(db.Boolean, default=False)

    item = db.relationship('Item')

    def __repr__(self)-> str:
        return '{!s} [quantity={!r}, main={!s}, master={!s}]'.format(
            self.barcode, self.quantity, self.main, self.master)


@nested_fields(customer=Customer, outbound_close_user=User, returned_close_user=User)
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    comment = db.Column(db.Text)
    outbound_close_timestamp = db.Column(db.DateTime)
    outbound_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    returned_close_timestamp = db.Column(db.DateTime)
    returned_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship('Customer', lazy='joined')
    outbound_close_user = db.relationship('User', foreign_keys=[outbound_close_user_id], lazy='joined')
    returned_close_user = db.relationship('User', foreign_keys=[returned_close_user_id], lazy='joined')
    work_items = db.relationship('WorkItem', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s} [{!r}]'.format(self.id, self.customer)

    def are_items_frozen(self) -> bool:
        return self.are_outbound_items_closed()

    def are_outbound_items_closed(self) -> bool:
        return self.outbound_close_user_id is not None

    def are_returned_items_closed(self) -> bool:
        return self.returned_close_user_id is not None

    def close_outbound_items(self, user: User):
        if self.outbound_close_user_id:
            raise RuntimeError("Outbound items have been closed.")
        self.outbound_close_user_id = user.id
        self.outbound_close_timestamp = datetime.utcnow()

    def close_returned_items(self, user: User):
        if not self.outbound_close_user_id:
            raise RuntimeError("Outbound items have not been closed.")
        if self.returned_close_user_id:
            raise RuntimeError("Returned items have been closed.")
        self.returned_close_user_id = user.id
        self.returned_close_timestamp = datetime.utcnow()


@nested_fields(work=Work, item=Item)
class WorkItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    outbound_quantity = db.Column(db.Float, nullable=False)
    returned_quantity = db.Column(db.Float)

    work = db.relationship('Work', lazy='joined')
    item = db.relationship('Item', lazy='joined')

    __table_args__ = (
        db.Index('work_item__can_not_add_one_item_twice', 'work_id', 'item_id', unique=True),
    )

    def __repr__(self)-> str:
        return '{!s} [-{!s}, +{!s}]'.format(self.item, self.outbound_quantity, self.returned_quantity)


class Acquisition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text)

    items = db.relationship('AcquisitionItem', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s} [{!s}]'.format(self.id, self.timestamp)


@nested_fields(acquisition=Acquisition, item=Item)
class AcquisitionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acquisition_id = db.Column(db.Integer, db.ForeignKey('acquisition.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    acquisition = db.relationship('Acquisition', lazy='joined')
    item = db.relationship('Item', lazy='joined')

    __table_args__ = (
        db.Index('acquisition_item__can_not_add_one_item_twice', 'acquisition_id', 'item_id', unique=True),
    )

    def __repr__(self)-> str:
        return '{!s} [{!r}]'.format(self.id, self.item)


class Stocktaking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text)
    close_timestamp = db.Column(db.DateTime)
    close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    close_user = db.relationship('User', foreign_keys=[close_user_id], lazy='joined')
    items = db.relationship('StocktakingItem', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s} [{!s}]'.format(self.id, self.timestamp)

    def are_items_frozen(self) -> bool:
        return self.are_items_closed()

    def are_items_closed(self) -> bool:
        return self.close_user_id is not None

    def close_items(self, user: User):
        if self.close_user_id:
            raise RuntimeError("Items have been closed.")
        self.close_user_id = user.id
        self.close_timestamp = datetime.utcnow()


@nested_fields(stocktaking=Stocktaking, item=Item)
class StocktakingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stocktaking_id = db.Column(db.Integer, db.ForeignKey('stocktaking.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    stocktaking = db.relationship('Stocktaking', lazy='joined')
    item = db.relationship('Item', lazy='joined')

    __table_args__ = (
        db.Index('stocktaking_item__can_not_add_one_item_twice', 'stocktaking_id', 'item_id', unique=True),
    )

    def __repr__(self)-> str:
        return '{!s} [{!r}]'.format(self.id, self.item)
