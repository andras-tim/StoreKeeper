import pytest

import app
app.test_mode = True

from app.modules.example_data import ExampleUsers as Users
from test.e2e.base_session_test import CommonSessionTest


def use_as_rights_data_provider(endpoint: str):
    """
    Data provider decorator for rights

    Example:
    >>> @use_as_rights_data_provider('/unit')
    ... class TestAcquisitionRights(CommonRightsTest):
    ...     INIT_PUSH = [...]
    ...     DATA_MAP = {...}
    ...     RIGHTS = {...}
    """
    def decorator(test_class):
        setattr(test_class, 'ENDPOINT', endpoint)
        for right in test_class.iterate_rights(test_class.RIGHTS):
            setattr(test_class, 'test_%(actor)s_access_rights' % right, test_wrapper(test_class, right))
        return test_class

    def test_wrapper(test_class, right: dict) -> callable:
        def test_func(self):
            test_class.check_access_rights(self, **right)
        return test_func
    return decorator


@pytest.mark.rights_test
class CommonRightsTest(CommonSessionTest):
    DATA_MAP = {}
    RIGHTS = ()
    ID_FIELD = 'id'

    @classmethod
    def setUpClass(cls):
        cls.INIT_PUSH = [('/users', [Users.USER1])] + cls.INIT_PUSH
        CommonSessionTest.setUpClass()

    @classmethod
    def iterate_rights(cls, rights: dict):
        for actor, expected_per_command in rights.items():
            yield {'actor': actor, 'expected_per_command': expected_per_command}

    def check_access_rights(self, actor: str, expected_per_command: dict):
        commands_in_order = ('get', 'post', 'put', 'delete')

        for command in commands_in_order:
            if command not in expected_per_command.keys():
                continue
            expected = expected_per_command[command]

            for case in self.__iterate_cases(actor, command, expected):
                try:
                    self.__check_right(**case)
                except Exception:
                    print('check access rights: case={!r}'.format(case))
                    raise

    def __iterate_cases(self, actor: str, command: str, expected: (tuple, list, bool)):
        if type(expected) == list:
            for exp in expected:
                yield from self.__iterate_cases(actor, command, exp)

        elif type(expected) == bool:
            yield {'actor': actor, 'command': command, 'expected': expected}

        elif type(expected) == tuple:
            data, exp = expected
            yield {'actor': actor, 'command': command, 'data': data, 'expected': exp}

        else:
            raise ValueError('Test case error: Unsupported data type used as expected; '
                             'type={}'.format(type(expected).__name__))

    def __check_right(self, actor: str, command: str, expected: bool, data=None):
        url = self.ENDPOINT
        if data is not None and command != 'post':
            url += '/{!s}'.format(self.DATA_MAP[data].get()[self.ID_FIELD])

        if data is not None:
            data = self.DATA_MAP[data].set()

        if actor != 'anonymous':
            if actor == 'admin':
                actor = Users.ADMIN
            elif actor == 'user1':
                actor = Users.USER1

            self.assertApiLogin(credential=actor,
                                expected_data=actor)

        expected_status_codes = [200, 201]
        if not expected:
            expected_status_codes = [401, 403]
        self.assertApiRequest(command, url, data=data,
                              expected_status_codes=expected_status_codes)
