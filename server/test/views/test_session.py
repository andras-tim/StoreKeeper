from test.views import CommonSessionTest, TestUsers


class TestAdminCanLogin(CommonSessionTest):
    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_code=401)

    def test_logging_in_with_admin(self):
        self.assertRequest("post", "/sessions", data=TestUsers.ADMIN.login(),
                           expected_data=TestUsers.ADMIN.get(),
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=TestUsers.ADMIN.get())

    def test_logging_in_with_admin_with_bad_password(self):
        self.assertRequest("post", "/sessions",
                           data=TestUsers.ADMIN.login(password="bad_%s" % TestUsers.ADMIN["password"]),
                           expected_status_code=401)


class TestLoginWithoutActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=TestUsers.USER1.set())
        self.assertRequestAsAdmin("post", "/users", data=TestUsers.USER2.set())

    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_code=401)

    def test_logging_in_with_existed_user(self):
        self.assertRequest("post", "/sessions", data=TestUsers.USER1.login(),
                           expected_data=TestUsers.USER1.get(),
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=TestUsers.USER1.get())

    def test_logging_in_with_non_existed_user(self):
        self.assertRequest("post", "/sessions", data={"username": "not_exist",
                                                      "password": "orange"},
                           expected_status_code=401)

    def test_logging_in_with_existed_user_with_bad_password(self):
        self.assertRequest("post", "/sessions",
                           data=TestUsers.USER1.login(password="bad_%s" % TestUsers.USER1["password"]),
                           expected_status_code=401)

    def test_logging_cant_happen_without_active_session(self):
        self.assertRequest("delete", "/sessions", expected_status_code=401)


class TestLoginWithActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=TestUsers.USER1.set())
        self.assertRequestAsAdmin("post", "/users", data=TestUsers.USER2.set())
        self.assertRequest("post", "/sessions", data=TestUsers.USER1.login(),
                           expected_status_code=201)

    def test_re_login_with_different_user(self):
        self.assertRequest("post", "/sessions", data=TestUsers.USER2.login(),
                           expected_data=TestUsers.USER2.get(),
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=TestUsers.USER2.get())

    def test_logout(self):
        self.assertRequest("delete", "/sessions")
        self.assertRequest("get", "/sessions", expected_status_code=401)


class TestAdminRights(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=TestUsers.USER1.set())

    def test_admin_can_get_list_of_users(self):
        self.assertRequestAsAdmin("get", "/users")

    def test_admin_can_get_itself(self):
        self.assertRequestAsAdmin("get", "/users/%d" % TestUsers.ADMIN["id"])

    def test_admin_can_get_another_user(self):
        self.assertRequestAsAdmin("get", "/users/%d" % TestUsers.USER1["id"])

    def test_admin_can_update_itself(self):
        self.assertRequestAsAdmin("put", "/users/%d" % TestUsers.ADMIN["id"], data=TestUsers.ADMIN.set())

    def test_admin_can_update_another_user(self):
        self.assertRequestAsAdmin("put", "/users/%d" % TestUsers.USER1["id"], data=TestUsers.USER1.set())

    def test_admin_can_not_delete_itself(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % TestUsers.ADMIN["id"], expected_status_code=422)

    def test_admin_can_delete_another_user(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % TestUsers.USER1["id"])

    def test_admin_can_get_current_session(self):
        self.assertRequestAsAdmin("get", "/sessions")


class TestUserRights(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=TestUsers.USER1.set())
        self.assertRequest("post", "/sessions", data=TestUsers.USER1.login(),
                           expected_status_code=201)

    def test_user_can_not_get_list_of_users(self):
        self.assertRequest("get", "/users", expected_status_code=403)

    def test_user_can_not_add_new_user(self):
        self.assertRequest("post", "/users", data=TestUsers.USER2.set(), expected_status_code=403)

    def test_user_can_get_itself(self):
        self.assertRequest("get", "/users/%d" % TestUsers.USER1["id"])

    def test_user_can_get_another_user(self):
        self.assertRequest("get", "/users/%d" % TestUsers.ADMIN["id"])

    def test_user_can_update_itself(self):
        self.assertRequest("put", "/users/%d" % TestUsers.USER1["id"], data=TestUsers.USER1.set())

    def test_user_can_not_update_another_user(self):
        self.assertRequest("put", "/users/%d" % TestUsers.ADMIN["id"], data=TestUsers.ADMIN.set(),
                           expected_status_code=403)

    def test_user_can_not_delete_itself(self):
        self.assertRequest("delete", "/users/%d" % TestUsers.USER1["id"], expected_status_code=403)

    def test_user_can_not_delete_another_user(self):
        self.assertRequest("delete", "/users/%d" % TestUsers.ADMIN["id"], expected_status_code=403)

    def test_user_can_get_current_session(self):
        self.assertRequest("get", "/sessions")
