import json
import re
from flask import Response

import app
app.test_mode = True

from app.server import config, app, db
from app.models import User
from app.modules.example_data import ExampleUsers as Users
from test.views.base_database_test import CommonTestWithDatabaseSupport


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
            self.__assert_response_data(expected_data, response)
        self.__assert_status_code(expected_status_codes, response)

    def __assert_response_data(self, expected_data: (str, list, dict, None), response: Response):
        response_string = self.__make_testable_data(response.data.decode("utf-8"))
        expected_data = self.__make_testable_data(expected_data)
        try:
            data_json = json.loads(response_string)
        except Exception as e:
            assert False, "Can not parse received data as JSON; data=%r, error=%r" % (response_string, e)
        assert expected_data == data_json

    def __assert_status_code(self, expected_status_codes: (int, list), response: Response):
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
