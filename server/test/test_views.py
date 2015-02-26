from test import CommonApiTest, CommonSessionTest


_USER1_SET = {"username": "foo", "password": "a", "email": "foo@bar.com"}
_USER1_GET = {"admin": False, "id": 2, "username": "foo", "email": "foo@bar.com", "disabled": False}

_USER2_SET = {"username": "1f-o_o.2", "password": "a", "email": "foo2@bar.com"}
_USER2_GET = {"admin": False, "id": 3, "username": "1f-o_o.2", "email": "foo2@bar.com", "disabled": False}


class TestUserWithBrandNewDb(CommonApiTest):
    def test_new_db(self):
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET])
        self.assertRequest("get", "/users/1", expected_data=self._ADMIN_GET)
        self.assertRequest("get", "/users/2", expected_status_code=404)

    def test_adding_new_users(self):
        self.assertRequest("post", "/users", data=_USER1_SET, expected_data=_USER1_GET)
        self.assertRequest("post", "/users", data=_USER2_SET, expected_data=_USER2_GET)

    def test_can_not_add_user_with_same_username(self):
        user2 = dict(_USER2_SET)
        user2["username"] = _USER1_SET["username"]

        self.assertRequest("post", "/users", data=_USER1_SET)
        self.assertRequest("post", "/users", data=user2,
                           expected_data={'message': {'username': ['Already exists.']}},
                           expected_status_code=422)

    def test_can_not_add_user_with_missing_fields(self):
        self.assertRequest("post", "/users", data={"username": "foo", "password": "a"},
                           expected_data={"message": {"email": ["This field is required."]}},
                           expected_status_code=422)

        self.assertRequest("post", "/users", data={"username": "foo", "email": "foo@bar.com"},
                           expected_data={"message": {"password": ["This field is required."]}},
                           expected_status_code=422)

        self.assertRequest("post", "/users", data={"password": "a", "email": "foo@bar.com"},
                           expected_data={"message": {"username": ["This field is required."]}},
                           expected_status_code=422)

        self.assertRequest("post", "/users", data={"email": "foo@bar.com"},
                           expected_data={"message": {"username": ["This field is required."],
                                                      "password": ["This field is required."]}},
                           expected_status_code=422)

        self.assertRequest("post", "/users", data={},
                           expected_data={"message": {"username": ["This field is required."],
                                                      "password": ["This field is required."],
                                                      "email": ["This field is required."]}},
                           expected_status_code=422)

    def test_can_not_add_user_with_bad_username(self):
        bad_usernames = ["_foo",
                         "foo_",
                         "fo__o",
                         "Foo"]

        for username in bad_usernames:
            self.assertRequest("post", "/users", data={"username": username, "password": "a", "email": "foo@bar.com"},
                               expected_data={"message": {'username': ['Invalid input.']}},
                               expected_status_code=422)

    def test_can_not_add_user_with_bad_email(self):
        user1 = dict(_USER1_SET)
        user1["email"] = "foo.bar"
        self.assertRequest("post", "/users", data=user1,
                           expected_data={"message": {'email': ['Invalid email address.']}},
                           expected_status_code=422)


class TestUserWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/users", data=_USER1_SET)
        self.assertRequest("post", "/users", data=_USER2_SET)

    def test_list_users(self):
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, _USER1_GET, _USER2_GET])

    def test_get_user(self):
        self.assertRequest("get", "/users/3", expected_data=_USER2_GET)
        self.assertRequest("get", "/users/2", expected_data=_USER1_GET)

    def test_remove_user(self):
        self.assertRequest("delete", "/users/2")
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, _USER2_GET])

    def test_can_not_remove_non_existed_user(self):
        self.assertRequest("delete", "/users/4", expected_status_code=404)
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, _USER1_GET, _USER2_GET])

    def test_update_user(self):
        request = dict(_USER2_SET)
        request["username"] = "foo2"
        request["email"] = "foo2@bar.com"

        response = dict(_USER2_GET)
        response["username"] = request["username"]
        response["email"] = request["email"]

        self.assertRequest("put", "/users/%d" % _USER2_GET["id"], data=request, expected_data=response)
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, _USER1_GET, response])


class TestAdminCanLogin(CommonSessionTest):
    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_code=401)

    def test_logging_in_with_admin(self):
        self.assertRequest("post", "/sessions", data={"username": self._ADMIN_SET["username"],
                                                      "password": self._ADMIN_SET["password"]},
                           expected_data=self._ADMIN_GET,
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=self._ADMIN_GET)

    def test_logging_in_with_admin_with_bad_password(self):
        self.assertRequest("post", "/sessions", data={"username": self._ADMIN_SET["username"],
                                                      "password": "bad_%s" % self._ADMIN_SET["password"]},
                           expected_status_code=401)


class TestLoginWithoutActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=_USER1_SET)
        self.assertRequestAsAdmin("post", "/users", data=_USER2_SET)

    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_code=401)

    def test_logging_in_with_existed_user(self):
        self.assertRequest("post", "/sessions", data={"username": _USER1_SET["username"],
                                                      "password": _USER1_SET["password"]},
                           expected_data=_USER1_GET,
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=_USER1_GET)

    def test_logging_in_with_non_existed_user(self):
        self.assertRequest("post", "/sessions", data={"username": "not_exist",
                                                      "password": "orange"},
                           expected_status_code=401)

    def test_logging_in_with_existed_user_with_bad_password(self):
        self.assertRequest("post", "/sessions", data={"username": _USER1_SET["username"],
                                                      "password": "bad_%s" % _USER1_SET["password"]},
                           expected_status_code=401)

    def test_logging_cant_happen_without_active_session(self):
        self.assertRequest("delete", "/sessions", expected_status_code=401)


class TestLoginWithActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=_USER1_SET)
        self.assertRequestAsAdmin("post", "/users", data=_USER2_SET)
        self.assertRequest("post", "/sessions", data={"username": _USER1_SET["username"],
                                                      "password": _USER1_SET["password"]},
                           expected_status_code=201)

    def test_re_login_with_different_user(self):
        self.assertRequest("post", "/sessions", data={"username": _USER2_SET["username"],
                                                      "password": _USER2_SET["password"]},
                           expected_data=_USER2_GET,
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=_USER2_GET)

    def test_logout(self):
        self.assertRequest("delete", "/sessions")
        self.assertRequest("get", "/sessions", expected_status_code=401)


class TestAdminRights(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=_USER1_SET)

    def test_admin_can_get_list_of_users(self):
        self.assertRequestAsAdmin("get", "/users")

    def test_admin_can_get_itself(self):
        self.assertRequestAsAdmin("get", "/users/%d" % self._ADMIN_GET["id"])

    def test_admin_can_get_another_user(self):
        self.assertRequestAsAdmin("get", "/users/%d" % _USER1_GET["id"])

    def test_admin_can_update_itself(self):
        self.assertRequestAsAdmin("put", "/users/%d" % self._ADMIN_GET["id"], data=self._ADMIN_SET)

    def test_admin_can_update_another_user(self):
        self.assertRequestAsAdmin("put", "/users/%d" % _USER1_GET["id"], data=_USER1_SET)

    def test_admin_can_not_delete_itself(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % self._ADMIN_GET["id"], expected_status_code=422)

    def test_admin_can_delete_another_user(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % _USER1_GET["id"])

    def test_admin_can_get_current_session(self):
        self.assertRequestAsAdmin("get", "/sessions")


class TestUserRights(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=_USER1_SET)
        self.assertRequest("post", "/sessions", data={"username": _USER1_SET["username"],
                                                      "password": _USER1_SET["password"]},
                           expected_status_code=201)

    def test_user_can_not_get_list_of_users(self):
        self.assertRequest("get", "/users", expected_status_code=403)

    def test_user_can_not_add_new_user(self):
        self.assertRequest("post", "/users", data=_USER2_SET, expected_status_code=403)

    def test_user_can_get_itself(self):
        self.assertRequest("get", "/users/%d" % _USER1_GET["id"])

    def test_user_can_get_another_user(self):
        self.assertRequest("get", "/users/%d" % self._ADMIN_GET["id"])

    def test_user_can_update_itself(self):
        self.assertRequest("put", "/users/%d" % _USER1_GET["id"], data=_USER1_SET)

    def test_user_can_not_update_another_user(self):
        self.assertRequest("put", "/users/%d" % self._ADMIN_GET["id"], data=self._ADMIN_SET, expected_status_code=403)

    def test_user_can_not_delete_itself(self):
        self.assertRequest("delete", "/users/%d" % _USER1_GET["id"], expected_status_code=403)

    def test_user_can_not_delete_another_user(self):
        self.assertRequest("delete", "/users/%d" % self._ADMIN_GET["id"], expected_status_code=403)

    def test_user_can_get_current_session(self):
        self.assertRequest("get", "/sessions")
