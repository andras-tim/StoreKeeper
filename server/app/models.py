import sqlalchemy
from wtforms.validators import Email

from .server import db, bcrypt


def yearly_reset_id(commit_function, retry_count=3):
    def get_new_id(self, session):
        return session.query(
            db.func.ifnull(
                db.func.max(self.__class__.id),
                0
            )
        ).filter(
            Work.year == self.year
        ).first()[0] + 1

    def wrapper(self, session):
        if self.id:
            commit_function(self, session)
            return

        error = None
        for i in range(retry_count):
            self.id = get_new_id(self, session)
            try:
                commit_function(self, session)
                return
            except sqlalchemy.exc.IntegrityError as error:
                session.rollback()

        raise Exception("Can not commit %d time(s)! %s" % (retry_count, str(error)))
    return wrapper


def set_yearly_reset_for_autoincrement_counter(table_object: sqlalchemy.sql.schema.Table,
                                               id_column_name: str="id",
                                               year_column_name: str="year"):
    trigger = """
        CREATE TRIGGER yearly_restart_autoincrement_on_%(table)s BEFORE INSERT ON %(table)s
        FOR EACH ROW
        BEGIN
            IF NEW.%(id)s = 0 THEN
                SET NEW.%(id)s = (SELECT IFNULL(MAX(t.%(id)s), 0) + 1
                                  FROM %(table)s AS t
                                  WHERE t.%(year)s = NEW.%(year)s);
            END IF;
        END;
    """ % {
        "table": table_object.name,
        "id": id_column_name,
        "year": year_column_name,
    }
    sqlalchemy.event.listen(table_object, "after_create", db.DDL(trigger))


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

    def __repr__(self):
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

    def __repr__(self):
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

    def __repr__(self):
        return '<Barcode %r>' % self.barcode


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return '<Vendor %r>' % self.name


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(20), nullable=False)

    def __init__(self, unit: str):
        self.unit = unit

    def __repr__(self):
        return '<Unit %r>' % self.unit


class Work(db.Model):
    year = db.Column(db.Integer, primary_key=True, autoincrement=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=False, default=0)
    full_id = db.column_property(year + "-" + id)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, year: int, name: str):
        self.year = year
        self.name = name

    def __repr__(self):
        return '<Work %r>' % self.full_id

    @yearly_reset_id
    def commit(self, session):
        session.add(self)
        session.commit()
