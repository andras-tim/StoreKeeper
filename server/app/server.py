from flask import Flask

from .config import Config


config = Config.read()

app = Flask(__name__)
app.config.update(config["Flask"])
