import json
import unittest
from flask import Response

import app
app.test_mode = True

from app.server import config, app, db, lm
from app.models import User
from app.modules.example_data import ExampleUsers as TestUsers


class CommonTestWithDatabaseSupport(unittest.TestCase):
    """
    Super class of database based tests

    Initialize a brand-new database at start, and purge at stop.
    """
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

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

    Added default `admin` user, added some assert functions and made a test client instance into `self.client`.
    """
    def setUp(self):
        super().setUp()
        db.session.add(User(TestUsers.ADMIN["username"], TestUsers.ADMIN["password"], email=TestUsers.ADMIN["email"],
                            admin=True))
        db.session.commit()
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

        try:
            data_json = json.loads(data_string)
        except Exception as e:
            self.assertTrue(False, msg="Can not parse received data as JSON; data=%r, error=%r" % (data_string, e))
            return
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
        CommonSessionTest.__set_testing_mode(False)
        super().setUp()
        self.admin_is_authenticated = False

    def tearDown(self):
        super().tearDown()
        CommonSessionTest.__set_testing_mode(True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.__set_testing_mode(True)

    @classmethod
    def __set_testing_mode(cls, enable: bool):
        app.config["TESTING"] = enable
        lm.init_app(app)

    def assertRequest(self, *args, **kwargs):
        if self.admin_is_authenticated:
            super().assertRequest("delete", "/sessions")
            self.admin_is_authenticated = False
        super().assertRequest(*args, **kwargs)

    def assertRequestAsAdmin(self, *args, **kwargs):
        if not self.admin_is_authenticated:
            super().assertRequest("post", "/sessions", data=TestUsers.ADMIN.login(),
                                  expected_data=TestUsers.ADMIN.get(),
                                  expected_status_code=201)
            self.admin_is_authenticated = True
        super().assertRequest(*args, **kwargs)
