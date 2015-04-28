from flask import Flask
from flask import redirect, url_for

from app.modules.config import ConfigObject
from app import basedir


def get_flask_parameters(config: ConfigObject) -> dict:
    if config.App.SHARE_STATIC:
        return {
            'static_folder': '{!s}/../client/app'.format(basedir),
            'static_url_path': '/{!s}'.format(config.App.NAME),
        }
    return {
        'static_folder': None
    }


def make_static_routes(app: Flask, config):
    @app.route('/{!s}'.format(config.App.NAME), methods=['GET'])
    @app.route('/{!s}/'.format(config.App.NAME), methods=['GET'])
    def index():
        return redirect(url_for('static', filename='index.html'))
