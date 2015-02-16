from test.base_classes import CommonApiCommonTest


_USER1_ADD = {"username": "foo", "password": "a", "email": "foo@bar.com"}
_USER1_GET = {"id": 1, "username": "foo", "email": "foo@bar.com", "disabled": False}

_USER2_ADD = {"username": "1f-o_o.2", "password": "a", "email": "foo2@bar.com"}
_USER2_GET = {"id": 2, "username": "1f-o_o.2", "email": "foo2@bar.com", "disabled": False}


class TestUserWithInitiallyEmptyDbCommon(CommonApiCommonTest):
    def test_empty_db(self):
        self.assertRequest("get", "/users", expected_data="[]")
        self.assertRequest("get", "/user/1", expected_status_code=404)

    def test_adding_new_users(self):
        self.assertRequest("post", "/users", data=_USER1_ADD, expected_data=_USER1_GET)
        self.assertRequest("post", "/users", data=_USER2_ADD, expected_data=_USER2_GET)

    def test_can_not_add_user_with_same_username(self):
        user2 = dict(_USER2_ADD)
        user2["username"] = _USER1_ADD["username"]

        self.assertRequest("post", "/users", data=_USER1_ADD)
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
        user1 = dict(_USER1_ADD)
        user1["email"] = "foo.bar"
        self.assertRequest("post", "/users", data=user1,
                           expected_data={"message": {'email': ['Invalid email address.']}},
                           expected_status_code=422)


class TestUserWithPreFilledDbCommon(CommonApiCommonTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/users", data=_USER1_ADD)
        self.assertRequest("post", "/users", data=_USER2_ADD)

    def test_list_users(self):
        self.assertRequest("get", "/users", expected_data=[_USER1_GET, _USER2_GET])

    def test_get_user(self):
        self.assertRequest("get", "/users/2", expected_data=_USER2_GET)
        self.assertRequest("get", "/users/1", expected_data=_USER1_GET)

    def test_remove_user(self):
        self.assertRequest("delete", "/users/1")
        self.assertRequest("get", "/users", expected_data=[_USER2_GET])

    def test_can_not_remove_non_existed_user(self):
        self.assertRequest("delete", "/users/3", expected_status_code=404)
        self.assertRequest("get", "/users", expected_data=[_USER1_GET, _USER2_GET])

    def test_update_user(self):
        user2 = {"id": 2, "username": "foo.two", "email": "foo2@bar.com", "disabled": False}
        self.assertRequest("put", "/users/2", data={"username": "foo.two", "password": "a", "email": "foo2@bar.com"},
                           expected_data=user2)
        self.assertRequest("get", "/users", expected_data=[_USER1_GET, user2])
