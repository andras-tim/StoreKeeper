from operator import attrgetter
from flask import Flask
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import _BoundDeclarativeMeta as ModelType

from app import models
from app.modules.config import ConfigObject


def initialize(app: Flask, db: SQLAlchemy, config: ConfigObject):
    url = '/{!s}/admin'.format(config.App.NAME)
    title = 'Admin'

    admin = Admin(app, url=url, name=title, template_mode='bootstrap3')
    __import_models(db, admin)

    if config.App.ADMIN_MANAGE_STATIC:
        __add_file_managers(app, admin)

    app.logger.debug('Admin page available: {!s}'.format(admin.url))


def __import_models(db: SQLAlchemy, admin: Admin):
    db_models = [obj for name, obj in models.__dict__.items() if type(obj) == ModelType]
    db_models.sort(key=attrgetter('__name__'))

    for db_model in db_models:
        admin.add_view(ModelView(db_model, db.session, category='Tables'))


def __add_file_managers(app: Flask, admin: Admin):
    if app.has_static_folder:
        admin.add_view(FileAdmin(app.static_folder, name='Static Files', endpoint='static'))
