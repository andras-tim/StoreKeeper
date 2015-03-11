from app.modules.example_data import ExampleUsers as Users, ExampleVendors as Vendors
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


class TestAdminRightsOnSessions(CommonSessionTest):
    def test_admin_can_get_current_session(self):
        self.assertRequestAsAdmin("get", "/sessions")


class TestAdminRightsOnUsers(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())

    def test_admin_can_get_list_of_users(self):
        self.assertRequestAsAdmin("get", "/users")

    def test_admin_can_get_itself(self):
        self.assertRequestAsAdmin("get", "/users/%d" % Users.ADMIN["id"])

    def test_admin_can_get_another_user(self):
        self.assertRequestAsAdmin("get", "/users/%d" % Users.USER1["id"])

    def test_admin_can_update_itself(self):
        self.assertRequestAsAdmin("put", "/users/%d" % Users.ADMIN["id"], data=Users.ADMIN.set())

    def test_admin_can_update_another_user(self):
        self.assertRequestAsAdmin("put", "/users/%d" % Users.USER1["id"], data=Users.USER1.set())

    def test_admin_can_not_delete_itself(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % Users.ADMIN["id"], expected_status_codes=422)

    def test_admin_can_delete_another_user(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % Users.USER1["id"])


class TestAdminRightsOnVendors(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/vendors", data=Vendors.VENDOR1.set())

    def test_admin_can_get_list_of_vendors(self):
        self.assertRequestAsAdmin("get", "/vendors")

    def test_admin_can_get_a_vendor(self):
        self.assertRequestAsAdmin("get", "/vendors/%d" % Vendors.VENDOR1["id"])

    def test_admin_can_update_a_vendor(self):
        self.assertRequestAsAdmin("put", "/vendors/%d" % Vendors.VENDOR1["id"], data=Vendors.VENDOR1.set())

    def test_admin_delete_a_vendor(self):
        self.assertRequestAsAdmin("delete", "/vendors/%d" % Vendors.VENDOR1["id"])


class TestUserRightsOnSessions(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        self.assertRequest("post", "/sessions", data=Users.USER1.login(), expected_status_codes=201)

    def test_user_can_get_current_session(self):
        self.assertRequest("get", "/sessions")


class TestUserRightsOnUsers(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        self.assertRequest("post", "/sessions", data=Users.USER1.login(), expected_status_codes=201)

    def test_user_can_not_get_list_of_users(self):
        self.assertRequest("get", "/users", expected_status_codes=403)

    def test_user_can_not_add_new_user(self):
        self.assertRequest("post", "/users", data=Users.USER2.set(), expected_status_codes=403)

    def test_user_can_get_itself(self):
        self.assertRequest("get", "/users/%d" % Users.USER1["id"])

    def test_user_can_get_another_user(self):
        self.assertRequest("get", "/users/%d" % Users.ADMIN["id"])

    def test_user_can_update_itself(self):
        self.assertRequest("put", "/users/%d" % Users.USER1["id"], data=Users.USER1.set())

    def test_user_can_not_update_another_user(self):
        self.assertRequest("put", "/users/%d" % Users.ADMIN["id"], data=Users.ADMIN.set(), expected_status_codes=403)

    def test_user_can_not_delete_itself(self):
        self.assertRequest("delete", "/users/%d" % Users.USER1["id"], expected_status_codes=403)

    def test_user_can_not_delete_another_user(self):
        self.assertRequest("delete", "/users/%d" % Users.ADMIN["id"], expected_status_codes=403)


class TestUserRightsOnVendors(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=Users.USER1.set())
        self.assertRequestAsAdmin("post", "/vendors", data=Vendors.VENDOR1.set())
        self.assertRequest("post", "/sessions", data=Users.USER1.login(), expected_status_codes=201)

    def test_user_can_get_list_of_vendors(self):
        self.assertRequest("get", "/vendors")

    def test_user_can_get_a_vendor(self):
        self.assertRequest("get", "/vendors/%d" % Vendors.VENDOR1["id"])

    def test_user_can_update_a_vendor(self):
        self.assertRequest("put", "/vendors/%d" % Vendors.VENDOR1["id"], data=Vendors.VENDOR1.set())

    def test_user_delete_a_vendor(self):
        self.assertRequest("delete", "/vendors/%d" % Vendors.VENDOR1["id"])
