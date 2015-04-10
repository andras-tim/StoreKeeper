from operator import attrgetter
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import _BoundDeclarativeMeta as ModelType

from app import models
from app.modules.config import ConfigObject


def initialize(app: Flask, db: SQLAlchemy, config: ConfigObject):
    admin = Admin(app, name=config.App.TITLE)
    __import_models(db, admin)
    app.logger.info('Admin page available: %s' % admin.url)


def __import_models(db: SQLAlchemy, admin: Admin):
    db_models = [obj for name, obj in models.__dict__.items() if type(obj) == ModelType]
    db_models.sort(key=attrgetter('__name__'))

    for db_model in db_models:
        admin.add_view(ModelView(db_model, db.session))
