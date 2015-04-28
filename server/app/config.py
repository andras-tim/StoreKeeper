import os
import shutil

from app import basedir, test_mode
from app.modules.config import Config, ConfigObject


class ConfigurationError(Exception):
    pass


def get_config() -> ConfigObject:
    config = __get_config()
    __check_config(config)
    return config


def __get_config() -> ConfigObject:
    config_reader = __get_config_reader()
    if test_mode:
        return config_reader.read(used_config='TestingConfig')
    return config_reader.read()


def __check_config(config: ConfigObject):
    if config.App.ADMIN_PAGE and not config.App.SHARE_STATIC:
        raise ConfigurationError('Have to enable App.SHARE_STATIC when App.ADMIN_PAGE is enabled')


def __get_config_reader() -> Config:
    config_path = os.path.join(basedir, 'config.yml')
    default_config_path = os.path.join(basedir, 'config_default.yml')

    if not os.path.exists(config_path):
        shutil.copy(default_config_path, config_path)

    return Config(config_path, config_variables={'BASEDIR': basedir})
