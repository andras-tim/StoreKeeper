import json
from operator import itemgetter
import re
from jinja2 import Template

from app.server import config


class ApiDoc:
    __API_CALL_TEMPLATE = Template("""
    {{ title }}
    {% for query in queries %}
    :query {{ query['name'] }}: {{ query['description'] }}{% endfor %}
    {% for status in statuses %}
    :statuscode {{ status['code'] }}: {{ status['description'] }}{% endfor %}

    **Example request**:

    .. sourcecode:: http

        {{ command }} /{{ app_name }}/api{{ url_tail }} HTTP/1.1
        Host: localhost:8000
        Content-Type: application/json
        {% for request_line in request_lines %}
        {{ request_line }}{% endfor %}

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 {{ response_status }}
        Content-Type: application/json
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
    def get_doc(cls, title: str, command: str, url_tail: str, request: (list, dict, None)=None,
                response: (list, dict, None)=None, response_status: int=200, queries: (dict, None)=None,
                status_codes: (dict, None)=None) -> str:
        doc = cls.__API_CALL_TEMPLATE.render(
            title=title,
            command=command.upper(),
            url_tail=url_tail,
            app_name=config.App.NAME,
            queries=cls.__format_queries(queries),
            statuses=cls.__format_status_codes(status_codes),
            request_lines=cls.__format_request(request),
            response_status=cls.__format_response_status(response_status),
            response_lines=cls.__format_response(response)
        )
        return cls.__remove_double_blank_lines(cls.__rstrip_lines(doc))

    @classmethod
    def __format_queries(cls, queries: (dict, None)) -> list:
        queries = queries or {}
        lines = [{'name': name, 'description': description} for name, description in queries.items()]
        return sorted(lines, key=itemgetter('name'))

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
    def __format_request(cls, request: (list, dict, None)) -> list:
        if request is None:
            return []
        return cls.__json_dump_to_lines(request)

    @classmethod
    def __format_response(cls, response: (list, dict, None)) -> list:
        return cls.__json_dump_to_lines(response)

    @classmethod
    def __format_response_status(cls, response_status: int) -> str:
        return '{:d} {!s}'.format(response_status, cls.__STATUSES[response_status][0])

    @classmethod
    def __json_dump_to_lines(cls, data: (list, dict, None)) -> list:
        return json.dumps(data, sort_keys=True, indent=2).splitlines()

    @classmethod
    def __rstrip_lines(cls, text: str) -> str:
        return '\n'.join([line.rstrip() for line in text.splitlines()])

    @classmethod
    def __remove_double_blank_lines(cls, text: str) -> str:
        return re.sub(r'\n{2,}', r'\n\n', text)
