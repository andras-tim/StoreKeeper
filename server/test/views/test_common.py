from test.modules import ApiDocTestCase
from app.views.common import api_func


class TestApiDocDecorator(ApiDocTestCase):
    def test_minimal_get(self):
        @api_func("Test command", url_tail="foo")
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 200: no error
        :statuscode 401: user was not logged in

        **Example request**:

        .. sourcecode:: http

            GET /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null
        """)

    def test_minimal_post(self):
        @api_func("Test command", url_tail="foo")
        def post():
            pass

        self.assertApiDoc(post.__doc__, """
        Test command

        :statuscode 201: no error
        :statuscode 401: user was not logged in
        :statuscode 422: there is missing field

        **Example request**:

        .. sourcecode:: http

            POST /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 201 CREATED
            Content-Type: application/json

            null
        """)

    def test_minimal_put(self):
        @api_func("Test command", url_tail="foo")
        def put():
            pass

        self.assertApiDoc(put.__doc__, """
        Test command

        :statuscode 200: no error
        :statuscode 401: user was not logged in

        **Example request**:

        .. sourcecode:: http

            PUT /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null
        """)

    def test_minimal_delete(self):
        @api_func("Test command", url_tail="foo")
        def delete():
            pass

        self.assertApiDoc(delete.__doc__, """
        Test command

        :statuscode 200: no error
        :statuscode 401: user was not logged in

        **Example request**:

        .. sourcecode:: http

            DELETE /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null
        """)

    def test_override_default_response_status(self):
        @api_func("Test command", url_tail="foo", response_status=403)
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 401: user was not logged in
        :statuscode 403: user has not enough rights

        **Example request**:

        .. sourcecode:: http

            GET /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 403 FORBIDDEN
            Content-Type: application/json

            null
        """)

    def test_extend_status_codes(self):
        @api_func("Test command", url_tail="foo", status_codes={600: "foo bar"})
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 200: no error
        :statuscode 401: user was not logged in
        :statuscode 600: foo bar

        **Example request**:

        .. sourcecode:: http

            GET /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null
        """)

    def test_override_default_status(self):
        @api_func("Test command", url_tail="foo", status_codes={200: "foo bar"})
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 200: foo bar
        :statuscode 401: user was not logged in

        **Example request**:

        .. sourcecode:: http

            GET /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null
        """)

    def test_login_required(self):
        @api_func("Test command", url_tail="foo", login_required=True)
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 200: no error
        :statuscode 401: user was not logged in

        **Example request**:

        .. sourcecode:: http

            GET /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null
        """)

    def test_admin_required(self):
        @api_func("Test command", url_tail="foo", admin_required=True)
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command *(for administrators only)*

        :statuscode 200: no error
        :statuscode 401: user was not logged in
        :statuscode 403: user has not enough rights

        **Example request**:

        .. sourcecode:: http

            GET /%(app_name)s/api/foo HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null
        """)
