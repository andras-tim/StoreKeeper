import logging

from app.modules.email import Email


class Utf8SMTPHandler(logging.Handler):
    def __init__(self, *args, mail: Email, toaddrs: (tuple, list), subject_format_string: str, **kwargs):
        super().__init__(*args, **kwargs)

        self._mail = mail
        self._toaddrs = toaddrs
        self._subject_format_string = subject_format_string

    def emit(self, record: logging.LogRecord):
        try:
            self._mail.send_email(
                subject=self._subject_format_string % record.__dict__,
                recipients=self._toaddrs,
                text_body=self.format(record),
            )
        except Exception:
            self.handleError(record)
