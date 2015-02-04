import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

from app import basedir
from app.modules.config import Config


config = Config(os.path.join(basedir, "config.yml"), config_variables={"BASEDIR": basedir}).read()

app = Flask(__name__)
app.config.update(config["Flask"])

# flask-sqlalchemy
db = SQLAlchemy(app)

# flask-bcrypt
bcrypt = Bcrypt(app)


# Init models and views (must be the last)
