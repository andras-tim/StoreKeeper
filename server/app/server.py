import os
from flask import Flask
from flask.ext import restful
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

from app import basedir, test_mode, doc_mode
from app.modules.config import Config, ConfigObject


def __get_config() -> ConfigObject:
    config_reader = Config(os.path.join(basedir, 'config.yml'), config_variables={'BASEDIR': basedir})
    if test_mode:
        return config_reader.read(used_config='TestingConfig')
    return config_reader.read()


config = __get_config()
flask_args = {}

# static sharing
if config.App.SHARE_STATIC:
    from app import static
    flask_args.update(static.get_flask_parameters(config))

app = Flask(__name__, **flask_args)
app.config.update(config['Flask'])

# flask-sqlalchemy
db = SQLAlchemy(app)

# flask-login
lm = LoginManager()
lm.init_app(app)

# flask-restful
api = restful.Api(app)

# flask-bcrypt
bcrypt = Bcrypt(app)

# Init views (must be after common resources)
from app.views import *

# static sharing
if config.App.SHARE_STATIC:
    static.make_static_routes(app, config)

# flask-admin
if config.App.ADMIN_PAGE and not (test_mode or doc_mode):
    from app import admin
    admin.initialize(app, db, config)
