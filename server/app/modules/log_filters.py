import logging
import flask
from octoconf import ConfigObject

from app.version import Version


class LogValuesInjectorFilter(logging.Filter):
    __request_values = {
        'request_host': 'host',
        'request_path': 'path',
        'request_url': 'url',
        'request_method': 'method',
        'request_referrer': 'referrer',
        'client_address': 'remote_addr',
        'client_user_agent': 'user_agent',
        'client_accept_languages': 'accept_languages',
    }

    def __init__(self, config: ConfigObject, version_info: Version):
        super().__init__(name=self.__class__.__name__)

        self.__constants = {
            'app_name': config.App.NAME,
            'app_title': config.App.TITLE,
            'app_version': version_info.version,
            'app_release': version_info.release,
        }

    def filter(self, record: logging.LogRecord) -> bool:
        for name, value in self.__constants.items():
            setattr(record, name, value)

        if flask.has_request_context():
            record.user = repr(flask.g.user)

            request = flask.request
            for name, attribute in self.__request_values.items():
                setattr(record, name, getattr(request, attribute))

        else:
            record.user = None

            for name, attribute in self.__request_values.items():
                setattr(record, name, None)

        return True
