import json
import re
import unittest
from flask import Response
import pytest

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
        db.drop_all()
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

    # Pattern for timestamp; e.g: "2015-03-14T07:38:08.430655+00:00"
    __API_TIMESTAMP = re.compile(r"(?P<quote>['\"])\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}\.\d{6}\+\d{2}:\d{2}['\"]")

    def setUp(self):
        super().setUp()

        admin = User(username=Users.ADMIN["username"], email=Users.ADMIN["email"], admin=True)
        admin.set_password(Users.ADMIN["password"])

        db.session.add(admin)
        db.session.commit()
        self.client = app.test_client()

    def assertRequest(self, command: str, url: str, data: (dict, None)=None,
                      expected_data: (str, list, dict, None)=None, expected_status_codes: (int, list)=200):
        response = self.__call_api(command, json.dumps(data), url)
        if expected_data is not None:
            self.assertResponseData(expected_data, response)
        self.assertStatusCode(expected_status_codes, response)

    def assertResponseData(self, expected_data: (str, list, dict, None), response: Response):
        response_string = self.__make_testable_data(response.data.decode("utf-8"))
        expected_data = self.__make_testable_data(expected_data)
        try:
            data_json = json.loads(response_string)
        except Exception as e:
            assert False, "Can not parse received data as JSON; data=%r, error=%r" % (response_string, e)
        assert expected_data == data_json

    def assertStatusCode(self, expected_status_codes: (int, list), response: Response):
        if type(expected_status_codes) != list:
            expected_status_codes = [expected_status_codes]
        assert response.status_code in expected_status_codes

    def __call_api(self, command: str, data: str, url: str):
        return getattr(self.client, command)("/%s/api%s" % (config.App.NAME, url),
                                             content_type="application/json", data=data)

    def __make_testable_data(self, data: (str, list, dict)) -> (str, list, dict):
        data_type = type(data)
        if not data_type == str:
            data = json.dumps(data, default=str)

        data = self.__API_TIMESTAMP.sub("\g<quote><TS>\g<quote>", data)

        if not data_type == str:
            data = json.loads(data)
        return data


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


def rights_data_provider(endpoint: str):
    def decorator(test_class):
        setattr(test_class, "ENDPOINT", endpoint)
        for right in test_class.iterate_rights(test_class.RIGHTS):
            setattr(test_class, get_name_of_test_func(right), test_wrapper(test_class, right))
        return test_class

    def get_name_of_test_func(right: dict) -> str:
        values = dict(right)

        values["verb"] = "can_call"
        if not right["expected"]:
            values["verb"] = "can_not_call"

        name_template = "test_%(actor)s_%(verb)s_%(command)s"
        if "data" in right.keys():
            name_template += "_%(data)s"

        return name_template % values

    def test_wrapper(test_class, right: dict) -> callable:
        def test_func(self):
            test_class.check_right(self, **right)
        return test_func
    return decorator


@pytest.mark.single_threaded
class CommonRightsTest(CommonSessionTest):
    ENDPOINT = ""  # Use rights_data_provider() decorator
    INIT_PUSH = {}
    DATA_MAP = {}
    RIGHTS = ()

    @classmethod
    def iterate_rights(cls, rights: dict):
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

    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        for endpoint, push_objects in self.INIT_PUSH:
            for push_object in push_objects:
                self.assertRequestAsAdmin("post", endpoint, data=push_object.set())

    def check_right(self, actor: str, command: str, expected: bool, data=None):
        url = self.ENDPOINT
        if data is not None and command != "post":
            url += "/%d" % self.DATA_MAP[data].get()["id"]

        if data is not None:
            data = self.DATA_MAP[data].set()

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
