import logging
from logging.handlers import RotatingFileHandler, SMTPHandler, SysLogHandler
import socket
from flask import Flask

from app.modules.yaml_config import ConfigObject

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


def initialize(app: Flask, config: ConfigObject):
    application_log_level = logging.INFO
    log_handler_getters = {
        'ToFile': __get_file_handler,
        'ToEmail': __get_email_handler,
        'ToSyslog': __get_syslog_handler,
    }

    for config_name, log_handler_getter in log_handler_getters.items():
        if config.Log[config_name]['ENABLED']:
            log_handler = log_handler_getter(config)
            application_log_level = min(application_log_level, log_handler.level)

            app.logger.addHandler(log_handler)

    app.logger.setLevel(application_log_level)


def __get_file_handler(config: ConfigObject) -> RotatingFileHandler:
    log_format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'

    file_handler = RotatingFileHandler(config.Log.ToFile.PATH,
                                       mode='a',
                                       maxBytes=config.Log.ToFile.MAX_SIXE_IN_MB * (1024 ** 2),
                                       backupCount=config.Log.ToFile.HOLD_COUNT)
    file_handler.setLevel(LOG_LEVELS[config.Log.ToFile.LEVEL])
    file_handler.setFormatter(logging.Formatter(log_format))

    return file_handler


def __get_email_handler(config: ConfigObject) -> SMTPHandler:
    mail_subject = '{} Failure'.format(config.App.TITLE)
    log_format = '''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''

    mail_handler = SMTPHandler((config.Log.ToEmail.SERVER, config.Log.ToEmail.PORT),
                               fromaddr=config.Log.ToEmail.SENDER,
                               toaddrs=config.Log.ToEmail.RECIPIENTS,
                               subject=mail_subject,
                               credentials=__get_smpt_credentials(config))
    mail_handler.setLevel(LOG_LEVELS[config.Log.ToEmail.LEVEL])
    mail_handler.setFormatter(logging.Formatter(log_format))

    return mail_handler


def __get_smpt_credentials(config: ConfigObject) -> (None, tuple):
    if config.Log.ToEmail.USERNAME or config.Log.ToEmail.PASSWORD:
        return config.Log.ToEmail.USERNAME, config.Log.ToEmail.PASSWORD
    return None


def __get_syslog_handler(config: ConfigObject) -> SysLogHandler:
    syslog_handler = SysLogHandler((config.Log.ToSyslog.ADDRESS, config.Log.ToSyslog.PORT),
                                   socktype=PROTOCOLS[config.Log.ToSyslog.TRANSPORT])
    syslog_handler.setLevel(LOG_LEVELS[config.Log.ToSyslog.LEVEL])
    return syslog_handler
