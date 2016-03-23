import os
import shutil
import datetime
import octoconf
from flask import Flask

from app import basedir, configdir, test_mode


class ConfigurationError(Exception):
    pass


def get_config() -> octoconf.ConfigObject:
    config = __translate_primitives(__get_config())
    __check_errors_in_config(config)
    return config


def __check_errors_in_config(config: octoconf.ConfigObject):
    """
    Checking config errors what block the starting
    """
    if config.App.ADMIN_PAGE and not config.App.SHARE_STATIC:
        raise ConfigurationError('Have to enable App.SHARE_STATIC when App.ADMIN_PAGE is enabled')


def check_warnings_in_config(app: Flask, config: octoconf.ConfigObject):
    """
    Checking config warnings what does not block the stating
    """
    if config.Flask.SECRET_KEY == 'PleaseChangeThisImportantSecretString':
        app.logger.warning('config: The Flask.SECRET_KEY was not customized; please change it for CSRF protection')


def __translate_primitives(config: octoconf.ConfigObject) -> octoconf.ConfigObject:
    """
    Translate primitive types to appropriate objects
    """
    config.Flask['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(days=config.Flask.REMEMBER_COOKIE_DURATION)
    return config


def __get_config() -> octoconf.ConfigObject:
    config_path = os.path.join(configdir, 'config.yml')
    default_config_path = os.path.join(configdir, 'config.default.yml')

    if not os.path.exists(config_path):
        shutil.copy(default_config_path, config_path)

    used_config = 'TestingConfig' if test_mode else None
    return octoconf.read(config_path, variables={'SERVER': basedir}, used_config=used_config)
