from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

from app import test_mode, doc_mode
from app.config import get_config
from app.res.restfulApi import RestfulApiWithoutSimpleAuth


config = get_config()
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
api = RestfulApiWithoutSimpleAuth(app)

# flask-bcrypt
bcrypt = Bcrypt(app)

# Init views (must be after common resources)
import app.views as views

# static sharing
if config.App.SHARE_STATIC:
    static.make_static_routes(app, config)

# flask-admin
if config.App.ADMIN_PAGE and not (test_mode or doc_mode):
    from app import admin
    admin.initialize(app, db, config)
