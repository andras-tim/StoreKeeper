import json
from pprint import pformat

from flask.ext.restful import Resource, abort

from app.modules.example_data import ExampleErrors
from app.modules.view_helper_for_models import get_validated_request, RequestProcessingError
from app.serializers import ErrorDeserializer
from app.views.common import api_func
from app.server import app


class ErrorView(Resource):
    _deserializer = ErrorDeserializer()

    @api_func('Receive client side errors and forward to logfile / email / syslog (what specified in config)',
              url_tail='/error',
              request=ExampleErrors.ERROR1.set(),
              response=None)
    def post(self):
        try:
            data = get_validated_request(self._deserializer)
        except RequestProcessingError as e:
            return abort(422, message=e.message)

        lines = ['Internal Client Error']
        lines += self.__add_chapter(data, 'stack')
        lines += self.__add_chapter(data, 'cause')

        app.logger.error('\n'.join(lines))

    def __add_chapter(self, data: dict, name: str) -> list:
        value = data.get(name)
        if value is None:
            return []

        return [
            '',
            '[{}]'.format(name),
            '{!s}'.format(value)
        ]
