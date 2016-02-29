from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from sqlalchemy_continuum import make_versioned, plugins

from app import test_mode, doc_mode, log, static
from app.config import get_config, check_warnings_in_config
from app.modules.email import Email
from app.modules.restful_api import RestfulApiWithoutSimpleAuth
from app.version import Version


version_info = Version()
config = get_config()
flask_args = {}

# static sharing
flask_args.update(static.get_flask_parameters(config))

app = Flask(__name__, **flask_args)
app.config.update(config['Flask'])

# email (wrapped flask-mail)
mail = Email(app)

# logging
if not app.debug and not app.testing and not doc_mode:
    log.initialize(app, config, mail, version_info)

check_warnings_in_config(app, config)

# flask-sqlalchemy
db = SQLAlchemy(app)

# flask-login
lm = LoginManager()
lm.init_app(app)

# flask-restful
api = RestfulApiWithoutSimpleAuth(app)

# flask-bcrypt
bcrypt = Bcrypt(app)

# SQLAlchemy-Continuum
make_versioned(plugins=[plugins.FlaskPlugin()])

# Init views (must be after common resources)
import app.views as views
views.initialize_endpoints(config, api)

# static sharing
if config.App.SHARE_STATIC:
    static.make_static_routes(app, config)

# flask-admin
if config.App.ADMIN_PAGE and not (test_mode or doc_mode):
    from app import admin
    admin.initialize(app, db, config)

app.logger.info('StoreKeeper v{} :: Ready'.format(version_info.release))
