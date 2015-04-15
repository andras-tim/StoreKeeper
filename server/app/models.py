from datetime import datetime

from app.server import db, bcrypt
from app.modules.view_helper import nested_fields


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    disabled = db.Column(db.Boolean, nullable=False, default=False)

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


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

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
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self)-> str:
        return '{!s}'.format(self.name)


@nested_fields(vendor=Vendor, unit=Unit)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    article_number = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)

    vendor = db.relationship('Vendor')
    unit = db.relationship('Unit')
    barcodes = db.relationship('Barcode', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s}'.format(self.name)


@nested_fields(item=Item)
class Barcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(15), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    main = db.Column(db.Boolean, default=False)

    item = db.relationship('Item')

    def __repr__(self)-> str:
        return '{!s} [quantity={!r}]'.format(self.barcode, self.quantity)


@nested_fields(customer=Customer, outbound_close_user=User, return_close_user=User)
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    comment = db.Column(db.Text)
    outbound_close_timestamp = db.Column(db.DateTime)
    outbound_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    returned_close_timestamp = db.Column(db.DateTime)
    returned_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship('Customer')
    outbound_close_user = db.relationship('User', foreign_keys=[outbound_close_user_id])
    returned_close_user = db.relationship('User', foreign_keys=[returned_close_user_id])
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
    outbound_quantity = db.Column(db.Integer, nullable=False)
    returned_quantity = db.Column(db.Integer)

    work = db.relationship('Work')
    item = db.relationship('Item')

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
    quantity = db.Column(db.Integer, nullable=False)

    acquisition = db.relationship('Acquisition')
    item = db.relationship('Item')

    __table_args__ = (
        db.Index('acquisition_item__can_not_add_one_item_twice', 'acquisition_id', 'item_id', unique=True),
    )

    def __repr__(self)-> str:
        return '{!s} [{!r}]'.format(self.id, self.item)


class Stocktaking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text)

    items = db.relationship('StocktakingItem', lazy='dynamic')

    def __repr__(self)-> str:
        return '{!s} [{!s}]'.format(self.id, self.timestamp)


@nested_fields(stocktaking=Stocktaking, item=Item)
class StocktakingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stocktaking_id = db.Column(db.Integer, db.ForeignKey('stocktaking.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    stocktaking = db.relationship('Stocktaking')
    item = db.relationship('Item')

    __table_args__ = (
        db.Index('stocktaking_item__can_not_add_one_item_twice', 'stocktaking_id', 'item_id', unique=True),
    )

    def __repr__(self)-> str:
        return '{!s} [{!r}]'.format(self.id, self.item)
