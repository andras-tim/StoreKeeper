import json
import unittest
from flask import Response

import app
app.test_mode = True

from app.server import config, app, db, lm


class CommonTestWithDatabaseSupport(unittest.TestCase):
    """
    Super class of database based tests

    Initialize a brand-new database at start, and purge at stop.
    """
    def setUp(self):
        db.create_all()

    def tearDown(self):
        CommonTestWithDatabaseSupport.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()


class CommonApiTest(CommonTestWithDatabaseSupport):
    """
    Super class of API based tests

    Adds some assert function and makes a test client instance into `self.client`.
    """
    def setUp(self):
        super().setUp()
        self.client = app.test_client()

    def assertRequest(self, command: str, url: str, data: (dict, None)=None,
                      expected_data: (str, list, dict, None)=None, expected_status_code: int=200):

        response = getattr(self.client, command)("/%s/api%s" % (config.App.NAME, url), data=data)

        if expected_data is not None:
            self.assertResponseData(expected_data, response)
        self.assertEqual(expected_status_code, response.status_code, msg="response=%r" % response.data.decode("utf-8"))

    def assertResponseData(self, expected_data: (str, list, dict), r: Response):
        data_string = r.data.decode("utf-8")

        if type(expected_data) == str:
            self.assertEqual(expected_data.strip(), data_string.strip())
            return

        data_json = json.loads(data_string)
        if data_json is None:
            return

        if type(expected_data) == list:
            self.assertListEqual(expected_data, data_json)
        elif type(expected_data) == dict:
            self.assertDictEqual(expected_data, data_json)


class CommonSessionTest(CommonApiTest):
    """
    Super class of Session tests

    Have to turn off temporary TESTING mode, because Flask-Login will not authenticate @login_required requests.
    https://flask-login.readthedocs.org/en/latest/#protecting-views
    """
    def setUp(self):
        app.config["TESTING"] = False
        lm.init_app(app)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        app.config["TESTING"] = True
        lm.init_app(app)
