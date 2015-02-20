import json
import unittest
from flask import Response

from app.server import config, app, db


class CommonTestWithDatabaseSupport(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        CommonTestWithDatabaseSupport.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()


class CommonApiTest(CommonTestWithDatabaseSupport):
    def setUp(self):
        super().setUp()
        self.client = app.test_client()

    def assertRequest(self, command: str, url: str, data: (dict, None)=None,
                      expected_data: (str, list, dict, None)=None, expected_status_code: int=200):

        response = getattr(self.client, command)("/%s/api%s" % (config.App.NAME, url), data=data)

        if expected_data is not None:
            self.assertResponseData(expected_data, response)
        self.assertEqual(expected_status_code, response.status_code)

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
