import pytest

import app
app.test_mode = True

from app.modules.example_data import ExampleUsers as Users
from test.views.base_session_test import CommonSessionTest


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
        self.assertApiRequestAsAdmin("post", "/users", data=Users.USER1.set())
        for endpoint, push_objects in self.INIT_PUSH:
            for push_object in push_objects:
                self.assertApiRequestAsAdmin("post", endpoint, data=push_object.set())

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

            self.assertApiRequest("post", "/sessions", data=actor.login(),
                                  expected_data=actor.get(),
                                  expected_status_codes=201)

        expected_status_codes = [200, 201]
        if not expected:
            expected_status_codes = [401, 403]
        self.assertApiRequest(command, url, data=data, expected_status_codes=expected_status_codes)
