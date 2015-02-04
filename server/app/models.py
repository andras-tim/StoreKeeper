from datetime import datetime
from wtforms.validators import Email

from app.server import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, info={'validators': Email()})
    disabled = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email

    def __repr__(self)-> str:
        return '<User %r>' % self.username


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    article_number = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    barcodes = db.relationship('Barcode', backref='item', lazy='dynamic')

    def __init__(self, name: str, vendor_id: int, quantity: int, unit_id: int):
        self.name = name
        self.vendor_id = vendor_id
        self.quantity = quantity
        self.unit_id = unit_id

    def __repr__(self)-> str:
        return '<Item %r>' % self.name


class Barcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(15), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, barcode: str, quantity: int, item_id: int):
        self.barcode = barcode
        self.quantity = quantity
        self.item_id = item_id

    def __repr__(self)-> str:
        return '<Barcode %r>' % self.barcode


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self)-> str:
        return '<Vendor %r>' % self.name


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(20), nullable=False)

    def __init__(self, unit: str):
        self.unit = unit

    def __repr__(self)-> str:
        return '<Unit %r>' % self.unit


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    comment = db.Column(db.Text)
    outbound_close_timestamp = db.Column(db.DateTime)
    outbound_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    return_close_timestamp = db.Column(db.DateTime)
    return_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    work_items = db.relationship('WorkItem', backref='work', lazy='dynamic')

    def __init__(self, creator_user_id: int, customer_id: int, comment: str):
        self.creator_user_id = creator_user_id
        self.customer_id = customer_id
        self.comment = comment

    def __repr__(self)-> str:
        return '<Work %r>' % self.id


class WorkItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    outbound_quantity = db.Column(db.Integer, nullable=False)
    return_quantity = db.Column(db.Integer)

    def __init__(self, work_id: int, item_id: int, outbound_quantity: int):
        self.work_id = work_id
        self.item_id = item_id
        self.outbound_quantity = outbound_quantity

    def __repr__(self)-> str:
        return '<WorkItem %r>' % self.id


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self)-> str:
        return '<Customer %r>' % self.name


class Acquisition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.Text)
    items = db.relationship('AcquisitionItem', backref='acquisition', lazy='dynamic')

    def __init__(self, comment: str):
        self.date = datetime.utcnow()
        self.comment = comment

    def __repr__(self)-> str:
        return '<Acquisition %r>' % self.id


class AcquisitionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acquisition_id = db.Column(db.Integer, db.ForeignKey('acquisition.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, acquisition_id: int, item_id: int, quantity: int):
        self.acquisition_id = acquisition_id
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self)-> str:
        return '<AcquisitionItem %r>' % self.id


class Stocktaking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.Text)
    items = db.relationship('StocktakingItem', backref='stocktaking', lazy='dynamic')

    def __init__(self, comment: str):
        self.date = datetime.utcnow()
        self.comment = comment

    def __repr__(self)-> str:
        return '<StockTaking %r>' % self.id


class StocktakingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stocktaking_id = db.Column(db.Integer, db.ForeignKey('stocktaking.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, stocktaking_id: int, item_id: int, quantity: int):
        self.stocktaking_id = stocktaking_id
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self)-> str:
        return '<StocktakingItem %r>' % self.id
