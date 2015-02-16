import os
from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

from app import basedir, test_mode
from app.modules.config import Config


def __get_config():
    config_reader = Config(os.path.join(basedir, "config.yml"), config_variables={"BASEDIR": basedir})
    if test_mode:
        return config_reader.read(used_config="TestingConfig")
    return config_reader.read()


config = __get_config()

app = Flask(__name__)
app.config.update(config["Flask"])

# flask-sqlalchemy
db = SQLAlchemy(app)

# flask-restful
api = restful.Api(app)

# flask-bcrypt
bcrypt = Bcrypt(app)


# Init models and views (must be the last)
from app import views
