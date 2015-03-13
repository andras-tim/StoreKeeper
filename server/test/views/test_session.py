from app.modules.example_data import ExampleUsers as Users
from test.views import CommonSessionTest


class TestAdminCanLogin(CommonSessionTest):
    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_codes=401)

    def test_logging_in_with_admin(self):
        self.assertRequest("post", "/sessions", data=Users.ADMIN.login(),
                           expected_data=Users.ADMIN.get(),
                           expected_status_codes=201)

        self.assertRequest("get", "/sessions", expected_data=Users.ADMIN.get())

    def test_logging_in_with_admin_with_bad_password(self):
        self.assertRequest("post", "/sessions",
                           data=Users.ADMIN.login(password="bad_%s" % Users.ADMIN["password"]),
                           expected_status_codes=401)


class TestLoginWithoutActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        self.assertRequestAsAdmin("post", "/users", data=Users.USER2.set())

    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_codes=401)

    def test_logging_in_with_existed_user(self):
        self.assertRequest("post", "/sessions", data=Users.USER1.login(),
                           expected_data=Users.USER1.get(),
                           expected_status_codes=201)

        self.assertRequest("get", "/sessions", expected_data=Users.USER1.get())

    def test_logging_in_with_non_existed_user(self):
        self.assertRequest("post", "/sessions", data={"username": "not_exist",
                                                      "password": "orange"},
                           expected_status_codes=401)

    def test_logging_in_with_existed_user_with_bad_password(self):
        self.assertRequest("post", "/sessions",
                           data=Users.USER1.login(password="bad_%s" % Users.USER1["password"]),
                           expected_status_codes=401)

    def test_logging_cant_happen_without_active_session(self):
        self.assertRequest("delete", "/sessions", expected_status_codes=401)


class TestLoginWithActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        self.assertRequestAsAdmin("post", "/users", data=Users.USER2.set())
        self.assertRequest("post", "/sessions", data=Users.USER1.login(), expected_status_codes=201)

    def test_re_login_with_different_user(self):
        self.assertRequest("post", "/sessions", data=Users.USER2.login(),
                           expected_data=Users.USER2.get(),
                           expected_status_codes=201)

        self.assertRequest("get", "/sessions", expected_data=Users.USER2.get())

    def test_logout(self):
        self.assertRequest("delete", "/sessions")
        self.assertRequest("get", "/sessions", expected_status_codes=401)


class TestDisabledUser(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        self.assertRequestAsAdmin("put", "/users/%d" % Users.USER1["id"],
                                  data=Users.USER1.set(change={"disabled": True}))
        self.assertRequestAsAdmin("post", "/users", data=Users.USER2.set())

    def test_logging_in_with_disabled_user(self):
        self.assertRequest("post", "/sessions", data=Users.USER1.login(),
                           expected_status_codes=401)

    def test_logging_out_recently_disabled_user(self):
        self.assertRequest("post", "/sessions", data=Users.USER2.login(),
                           expected_status_codes=201)
        self.assertRequest("put", "/users/%d" % Users.USER2["id"],
                           data=Users.USER2.set(change={"disabled": True}))
        self.assertRequest("get", "/sessions", expected_status_codes=401)
