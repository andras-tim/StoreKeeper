from collections import OrderedDict
from flask import g
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

        app.logger.error('client-side error: user: {!r}\n{}'.format(g.user, self._format_data(data)))

    def _format_data(self, data: dict) -> str:
        detailed_error = OrderedDict((
            ('name', None),
            ('message', None),
            ('stack', None),
            ('cause', None),
        ))
        detailed_error.update(data)

        return '\n'.join(['### {!s} ###\n{!s}\n'.format(key, value)
                          for (key, value) in detailed_error.items() if value is not None])
