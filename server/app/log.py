import logging
import socket
from logging.handlers import RotatingFileHandler, SysLogHandler
from flask import Flask

from app.modules.email import Email
from app.version import Version
from app.modules.yaml_config import ConfigObject
from app.modules.utf8_smtp_handler import Utf8SMTPHandler
from app.modules.log_filters import LogValuesInjectorFilter

LOG_LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}

PROTOCOLS = {
    'UDP': socket.SOCK_DGRAM,
    'TCP': socket.SOCK_STREAM,
}


def initialize(app: Flask, config: ConfigObject, mail: Email, version_info: Version):
    application_log_level = logging.INFO
    log_handler_getters = {
        'ToFile': __get_file_handler,
        'ToEmail': __get_email_handler,
        'ToSyslog': __get_syslog_handler,
    }

    for config_name, log_handler_getter in log_handler_getters.items():
        if config.Log[config_name]['ENABLED']:
            log_handler = log_handler_getter(config=config, mail=mail)
            application_log_level = min(application_log_level, log_handler.level)

            app.logger.addHandler(log_handler)

    app.logger.addFilter(LogValuesInjectorFilter(config, version_info))
    app.logger.setLevel(application_log_level)


def __get_file_handler(config: ConfigObject, **kwargs) -> RotatingFileHandler:
    file_handler = RotatingFileHandler(config.Log.ToFile.PATH,
                                       mode='a',
                                       maxBytes=config.Log.ToFile.MAX_SIXE_IN_MB * (1024 ** 2),
                                       backupCount=config.Log.ToFile.HOLD_COUNT)
    file_handler.setLevel(LOG_LEVELS[config.Log.ToFile.LEVEL])
    file_handler.setFormatter(logging.Formatter(config.Log.ToFile.MESSAGE_FORMAT))

    return file_handler


def __get_email_handler(config: ConfigObject, mail: Email) -> Utf8SMTPHandler:
    mail_handler = Utf8SMTPHandler(mail=mail,
                                   toaddrs=config.Log.ToEmail.RECIPIENTS,
                                   subject_format_string=config.Log.ToEmail.SUBJECT_FORMAT)
    mail_handler.setLevel(LOG_LEVELS[config.Log.ToEmail.LEVEL])
    mail_handler.setFormatter(logging.Formatter(config.Log.ToEmail.MESSAGE_FORMAT))

    return mail_handler


def __get_syslog_handler(config: ConfigObject, **kwargs) -> SysLogHandler:
    syslog_handler = SysLogHandler((config.Log.ToSyslog.ADDRESS, config.Log.ToSyslog.PORT),
                                   socktype=PROTOCOLS[config.Log.ToSyslog.TRANSPORT])
    syslog_handler.setLevel(LOG_LEVELS[config.Log.ToSyslog.LEVEL])
    syslog_handler.setFormatter(logging.Formatter(config.Log.ToSyslog.MESSAGE_FORMAT))

    return syslog_handler
