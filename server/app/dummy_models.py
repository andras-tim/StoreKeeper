from .server import db


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    children = db.relationship('Child', backref='parent', lazy='dynamic')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self)-> str:
        return '<Parent %r>' % self.name


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    note = db.Column(db.Text, nullable=False)

    def __init__(self, name: str, note: str):
        self.name = name
        self.note = note

    def __repr__(self)-> str:
        return '<Child %r>' % self.name
