import os
import shutil
import datetime
from flask import Flask

from app import basedir, test_mode
from app.modules.yaml_config import Config, ConfigObject


class ConfigurationError(Exception):
    pass


def get_config() -> ConfigObject:
    config = __translate_primitives(__get_config())
    __check_errors_in_config(config)
    return config


def __get_config() -> ConfigObject:
    config_reader = __get_config_reader()
    if test_mode:
        return config_reader.read(used_config='TestingConfig')
    return config_reader.read()


def __check_errors_in_config(config: ConfigObject):
    """
    Checking config errors what block the starting
    """
    if config.App.ADMIN_PAGE and not config.App.SHARE_STATIC:
        raise ConfigurationError('Have to enable App.SHARE_STATIC when App.ADMIN_PAGE is enabled')


def check_warnings_in_config(app: Flask, config: ConfigObject):
    """
    Checking config warnings what does not block the stating
    """
    if config.Flask.SECRET_KEY == 'PleaseChangeThisImportantSecretString':
        app.logger.warning('config: The Flask.SECRET_KEY was not customized; please change it for CSRF protection')


def __translate_primitives(config: ConfigObject) -> ConfigObject:
    """
    Translate primitive types to appropriate objects
    """
    config.Flask['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(days=config.Flask.REMEMBER_COOKIE_DURATION)
    return config


def __get_config_reader() -> Config:
    config_path = os.path.join(basedir, 'config.yml')
    default_config_path = os.path.join(basedir, 'config.default.yml')

    if not os.path.exists(config_path):
        shutil.copy(default_config_path, config_path)

    return Config(config_path, config_variables={'BASEDIR': basedir})
