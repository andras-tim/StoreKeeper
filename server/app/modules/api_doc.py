import json
import re
from jinja2 import Template
from operator import itemgetter

from app.server import config


class ApiDoc:
    __API_CALL_TEMPLATE = Template("""
    {{ title }}
    {% for param in params %}
    :param {{ param['name'] }}: {{ param['description'] }}{% endfor %}
    {% for status in statuses %}
    :statuscode {{ status['code'] }}: {{ status['description'] }}{% endfor %}

    **Example request**:

    .. sourcecode:: http

        {{ command }} /{{ app_name }}/api{{ url_tail }} HTTP/1.1
        Host: localhost:8000
        Content-Type: {{ request_content_type }} {% for field in request_header %}
        {{ field['name'] }}: {{ field['value'] }}{% endfor %}
        {% for request_line in request_lines %}
        {{ request_line }}{% endfor %}

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 {{ response_status }}
        Content-Type: {{ response_content_type }} {% for field in response_header %}
        {{ field['name'] }}: {{ field['value'] }}{% endfor %}
        {% for response_line in response_lines %}
        {{ response_line }}{% endfor %}
    """)

    __STATUSES = {
        200: ['OK', 'no error'],
        201: ['CREATED', 'no error'],
        401: ['UNAUTHORIZED', 'user was not logged in'],
        403: ['FORBIDDEN', 'user has not enough rights'],
        404: ['NOT FOUND', ''],
        422: ['UNPROCESSABLE ENTITY', 'there is wrong type / missing field'],
    }

    @classmethod
    def get_doc(cls, title: str, command: str, url_tail: str, request_header: (dict, None)=None,
                request_content_type: str='application/json', request: (list, dict, None)=None,
                response_header: (dict, None)=None, response_content_type: str='application/json',
                response: (list, dict, None)=None, response_status: int=200, params: (dict, None)=None,
                status_codes: (dict, None)=None) -> str:
        doc = cls.__API_CALL_TEMPLATE.render(
            title=title,
            command=command.upper(),
            url_tail=url_tail,
            app_name=config.App.NAME,
            params=cls.__format_parameters(params),
            statuses=cls.__format_status_codes(status_codes),
            request_header=cls.__format_custom_header(request_header),
            request_content_type=request_content_type,
            request_lines=cls.__format_request(request),
            response_header=cls.__format_custom_header(response_header),
            response_content_type=response_content_type,
            response_status=cls.__format_response_status(response_status),
            response_lines=cls.__format_response(response)
        )
        return cls.__remove_double_blank_lines(cls.__rstrip_lines(doc))

    @classmethod
    def __format_parameters(cls, parameters: (dict, None)) -> list:
        if not parameters:
            return []
        return [{'name': name, 'description': parameters[name]} for name in sorted(parameters.keys())]

    @classmethod
    def __format_status_codes(cls, status_codes: (dict, None)) -> list:
        status_codes = status_codes or {}
        lines = []
        for code, description in status_codes.items():
            if not description:
                description = '{{ original }}'
            original = ''
            if code in cls.__STATUSES.keys():
                original = cls.__STATUSES[code][1]
            description = Template(description).render(original=original)
            lines.append({'code': code, 'description': description})
        return sorted(lines, key=itemgetter('code'))

    @classmethod
    def __format_request(cls, request: (str, list, dict, None)) -> list:
        if isinstance(request, str):
            return request.splitlines()
        if request is None:
            return []
        return cls.__json_dump_to_lines(request)

    @classmethod
    def __format_response(cls, response: (str, list, dict, None)) -> list:
        if isinstance(response, str):
            return response.splitlines()
        return cls.__json_dump_to_lines(response)

    @classmethod
    def __format_response_status(cls, response_status: int) -> str:
        return '{:d} {!s}'.format(response_status, cls.__STATUSES[response_status][0])

    @classmethod
    def __format_custom_header(cls, headers: (dict, None)) -> list:
        if not headers:
            return []
        return [{'name': name, 'value': headers[name]} for name in sorted(headers.keys())]

    @classmethod
    def __json_dump_to_lines(cls, data: (list, dict, None)) -> list:
        try:
            return json.dumps(data, sort_keys=True, indent=2).splitlines()
        except TypeError as e:
            raise TypeError('{!s}; data={!r}'.format(e, data))

    @classmethod
    def __rstrip_lines(cls, text: str) -> str:
        return '\n'.join([line.rstrip() for line in text.splitlines()])

    @classmethod
    def __remove_double_blank_lines(cls, text: str) -> str:
        return re.sub(r'\n{2,}', r'\n\n', text)
