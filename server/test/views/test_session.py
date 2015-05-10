from app.modules.example_data import ExampleUsers as Users
from test.views.base_session_test import CommonSessionTest


class TestAdminCanLogin(CommonSessionTest):
    ENDPOINT = '/session'

    def test_no_sessions(self):
        self.assertApiGet(expected_status_codes=401)

    def test_logging_in_with_admin(self):
        self.assertApiLogin(credential=Users.ADMIN,
                            expected_data=Users.ADMIN)
        self.assertApiSession(expected_data=Users.ADMIN)

    def test_logging_in_with_admin_with_bad_password(self):
        self.assertApiLogin(credential=Users.ADMIN.login(password='bad_{!s}'.format(Users.ADMIN['password'])),
                            expected_data={'message': 'login error'}, expected_status_codes=401)


class TestLoginWithoutActiveSession(CommonSessionTest):
    ENDPOINT = '/session'
    INIT_PUSH = [
        ('/users', [Users.USER1, Users.USER2]),
    ]

    def test_no_sessions(self):
        self.assertApiSession(expected_status_codes=401)

    def test_logging_in_with_existed_user(self):
        self.assertApiLogin(credential=Users.USER1,
                            expected_data=Users.USER1, expected_status_codes=201)
        self.assertApiSession(expected_data=Users.USER1)

    def test_logging_in_with_non_existed_user(self):
        self.assertApiLogin(credential={'username': 'not_exist', 'password': 'orange'},
                            expected_status_codes=401)

    def test_logging_in_with_existed_user_with_bad_password(self):
        self.assertApiLogin(credential=Users.USER1.login(password='bad_{!s}'.format(Users.USER1['password'])),
                            expected_status_codes=401)

    def test_logging_cant_happen_without_active_session(self):
        self.assertApiLogout(expected_status_codes=401)

    def test_logging_in_with_remember_me(self):
        self.assertApiLogin(credential=Users.USER1.login(remember=True),
                            expected_data=Users.USER1, expected_status_codes=201)
        self.assertApiSession(expected_data=Users.USER1)


class TestLoginWithActiveSession(CommonSessionTest):
    ENDPOINT = '/session'
    INIT_PUSH = [
        ('/users', [Users.USER1, Users.USER2]),
    ]

    def setUp(self):
        super().setUp()
        self.assertApiLogin(credential=Users.USER1)

    def test_re_login_with_different_user(self):
        self.assertApiLogin(credential=Users.USER2,
                            expected_data=Users.USER2)

        self.assertApiSession(expected_data=Users.USER2)

    def test_logout(self):
        self.assertApiLogout()
        self.assertApiSession(expected_status_codes=401)


class TestDisabledUser(CommonSessionTest):
    ENDPOINT = '/session'
    INIT_PUSH = [
        ('/users', [Users.USER1, Users.USER2]),
    ]

    def setUp(self):
        super().setUp()
        self.assertApiLogin(credential=Users.ADMIN)
        self.assertApiPut(Users.USER1['id'], endpoint='/users', data=Users.USER1.set(change={'disabled': True}))
        self.assertApiLogout()

    def test_logging_in_with_disabled_user(self):
        self.assertApiLogin(credential=Users.USER1,
                            expected_status_codes=401)

    def test_logging_out_recently_disabled_user(self):
        self.assertApiLogin(credential=Users.USER2)
        self.assertApiPut(Users.USER2['id'], endpoint='/users', data=Users.USER2.set(change={'disabled': True}))
        self.assertApiSession(expected_status_codes=401)


class UserCanChangeItsPassword(CommonSessionTest):
    ENDPOINT = '/session'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
    ]

    def setUp(self):
        super().setUp()
        self.assertApiLogin(credential=Users.USER1)

    def test_login_after_update_password(self):
        request = Users.USER1.set(change={'password': 'new_pw'})
        response = Users.USER1.get()

        self.assertApiPut(response['id'], endpoint='/users', data=request, expected_data=response)
        self.assertApiLogin(credential=Users.USER1, expected_status_codes=401)
        self.assertApiLogin(credential=Users.USER1.login(password=request['password']))
