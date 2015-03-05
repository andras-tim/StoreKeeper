import unittest

import app
app.test_mode = True

from app.server import config
from app.modules.doc_helper import ApiDoc, api_doc


class ApiDocTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def assertApiDoc(self, results: str, expected: str):
        expected = self.__fixup_indentation(expected).rstrip(" ")
        self.assertEqual(expected % {"app_name": config.App.NAME}, results)

    def __fixup_indentation(self, text_block: str, indentation_level=1) -> str:
        return "\n".join([line[(indentation_level * 4):] for line in text_block.splitlines()])


class TestApiDoc(ApiDocTestCase):
    def test_minimal_case(self):
        results = ApiDoc.get_doc(title="Test command", command="delete", url_tail="foo")
        self.assertApiDoc(results, """
        Test command

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

    def test_full_case_with_auto_filled_status_code(self):
        results = ApiDoc.get_doc(title="Test command", command="push", url_tail="foobar/2",
                                 request=[{"apple": 1, "banana": {"small": 2, "big": 3}}, {"tree": 1}],
                                 response=[{"orange": 4}, 5], response_status=201,
                                 queries={"foobar_id": "Foobar selector"},
                                 status_codes={201: "", 404: "something is missing"})
        self.assertApiDoc(results, """
        Test command

        :query foobar_id: Foobar selector

        :statuscode 201: no error
        :statuscode 404: something is missing

        **Example request**:

        .. sourcecode:: http

            PUSH /%(app_name)s/api/foobar/2 HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

            [
              {
                "apple": 1,
                "banana": {
                  "big": 3,
                  "small": 2
                }
              },
              {
                "tree": 1
              }
            ]

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 201 CREATED
            Content-Type: application/json

            [
              {
                "orange": 4
              },
              5
            ]
        """)


class TestApiDocDecorator(ApiDocTestCase):
    def test_minimal_get(self):
        @api_doc("Test command", url_tail="foo")
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 200: no error

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
        @api_doc("Test command", url_tail="foo")
        def post():
            pass

        self.assertApiDoc(post.__doc__, """
        Test command

        :statuscode 201: no error
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
        @api_doc("Test command", url_tail="foo")
        def put():
            pass

        self.assertApiDoc(put.__doc__, """
        Test command

        :statuscode 200: no error

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
        @api_doc("Test command", url_tail="foo")
        def delete():
            pass

        self.assertApiDoc(delete.__doc__, """
        Test command

        :statuscode 200: no error

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
        @api_doc("Test command", url_tail="foo", response_status=403)
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

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
        @api_doc("Test command", url_tail="foo", status_codes={600: "foo bar"})
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 200: no error
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
        @api_doc("Test command", url_tail="foo", status_codes={200: "foo bar"})
        def get():
            pass

        self.assertApiDoc(get.__doc__, """
        Test command

        :statuscode 200: foo bar

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
        @api_doc("Test command", url_tail="foo", login_required=True)
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
        @api_doc("Test command", url_tail="foo", admin_required=True)
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
