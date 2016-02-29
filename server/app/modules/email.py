from threading import Thread
from flask import Flask
from flask_mail import Mail, Message

from app.modules.common import async


class Email:
    def __init__(self, app: Flask):
        self.__app = app
        self.__mail = Mail(app)

    def send_email(self, subject: str, recipients: (tuple, list), text_body=None, html_body=None, assync=False):
        with self.__app.app_context():
            msg = Message(subject, recipients=recipients)
            if text_body:
                msg.body = text_body
            if html_body:
                msg.html = html_body

            if not assync:
                self.__mail.send(msg)
                return

            thread = Thread(target=self.__async_send_email, args=(self.__app, self.__mail, msg))
            thread.start()

    @async
    def __async_send_email(self, app: Flask, mail: Mail, msg: Message):
        with app.app_context():
            mail.send(msg)
