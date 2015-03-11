import json
import unittest
from flask import Response

import app
app.test_mode = True

from app.server import config, app, db, lm
from app.models import User
from app.modules.example_data import ExampleUsers as Users


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
        db.session.add(User(Users.ADMIN["username"], Users.ADMIN["password"], email=Users.ADMIN["email"], admin=True))
        db.session.commit()
        self.client = app.test_client()

    def assertRequest(self, command: str, url: str, data: (dict, None)=None,
                      expected_data: (str, list, dict, None)=None, expected_status_codes: (int, list)=200):

        response = getattr(self.client, command)("/%s/api%s" % (config.App.NAME, url), data=data)

        if expected_data is not None:
            self.assertResponseData(expected_data, response)
        if type(expected_status_codes) != list:
            expected_status_codes = [expected_status_codes]
        self.assertIn(response.status_code, expected_status_codes,
                      msg="request=%r, response=%r" % (data, response.data.decode("utf-8")))

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
            super().assertRequest("post", "/sessions", data=Users.ADMIN.login(),
                                  expected_data=Users.ADMIN.get(),
                                  expected_status_codes=201)
            self.admin_is_authenticated = True
        super().assertRequest(*args, **kwargs)


class CommonRightsTest(CommonSessionTest):
    INIT_PUSH = {}
    OBJECTS = {}
    RIGHTS = ()

    class AnnotatedRight(dict):
        pass

    @classmethod
    def __annotate_right(cls, right: dict):
        name_template = "%(actor)s_calls_%(command)s"
        if "data" in right.keys():
            name_template += "_%(data)s"

        r = cls.AnnotatedRight(right)
        setattr(r, "__name__", name_template % right)
        return r

    @classmethod
    def __iterate_rights(cls, rights: dict):
        for actor, per_command_rights in rights.items():
            for command, expected in per_command_rights.items():
                yield from cls.__parse_expected(actor, command, expected)

    @classmethod
    def __parse_expected(cls, actor: str, command: str, expected: (tuple, list, bool)):
        if type(expected) == list:
            for exp in expected:
                yield from cls.__parse_expected(actor, command, exp)

        elif type(expected) == bool:
            yield {"actor": actor, "command": command, "expected": expected}

        elif type(expected) == tuple:
            data, exp = expected
            yield {"actor": actor, "command": command, "data": data, "expected": exp}

    @classmethod
    def iterate_rights(cls, rights: dict) -> tuple:
        return tuple(cls.__annotate_right(right) for right in cls.__iterate_rights(rights))

    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        for endpoint, push_objects in self.INIT_PUSH.items():
            for push_object in push_objects:
                self.assertRequestAsAdmin("post", endpoint, data=push_object.set())

    def _test_right(self, endpoint: str, actor: str, command: str, expected: bool, data=None):
        url = endpoint
        if data is not None and command != "post":
            url += "/%d" % self.OBJECTS[data].get()["id"]

        if data is not None:
            data = self.OBJECTS[data].set()

        if actor != "anonymous":
            if actor == "admin":
                actor = Users.ADMIN
            elif actor == "user1":
                actor = Users.USER1

            self.assertRequest("post", "/sessions", data=actor.login(),
                               expected_data=actor.get(),
                               expected_status_codes=201)

        expected_status_codes = [200, 201]
        if not expected:
            expected_status_codes = [401, 403]
        self.assertRequest(command, url, data=data, expected_status_codes=expected_status_codes)
