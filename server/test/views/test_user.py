from test.views import CommonApiTest


class TestUserWithBrandNewDb(CommonApiTest):
    def test_new_db(self):
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET])
        self.assertRequest("get", "/users/1", expected_data=self._ADMIN_GET)
        self.assertRequest("get", "/users/2", expected_status_code=404)

    def test_adding_new_users(self):
        self.assertRequest("post", "/users", data=self._USER1_SET, expected_data=self._USER1_GET)
        self.assertRequest("post", "/users", data=self._USER2_SET, expected_data=self._USER2_GET)

    def test_can_not_add_user_with_same_username(self):
        user2 = dict(self._USER2_SET)
        user2["username"] = self._USER1_SET["username"]

        self.assertRequest("post", "/users", data=self._USER1_SET)
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
        user1 = dict(self._USER1_SET)
        user1["email"] = "foo.bar"
        self.assertRequest("post", "/users", data=user1,
                           expected_data={"message": {'email': ['Invalid email address.']}},
                           expected_status_code=422)


class TestUserWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/users", data=self._USER1_SET)
        self.assertRequest("post", "/users", data=self._USER2_SET)

    def test_list_users(self):
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, self._USER1_GET, self._USER2_GET])

    def test_get_user(self):
        self.assertRequest("get", "/users/3", expected_data=self._USER2_GET)
        self.assertRequest("get", "/users/2", expected_data=self._USER1_GET)

    def test_remove_user(self):
        self.assertRequest("delete", "/users/2")
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, self._USER2_GET])

    def test_can_not_remove_non_existed_user(self):
        self.assertRequest("delete", "/users/4", expected_status_code=404)
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, self._USER1_GET, self._USER2_GET])

    def test_update_user(self):
        request = dict(self._USER2_SET)
        request["username"] = "foo2"
        request["email"] = "foo2@bar.com"

        response = dict(self._USER2_GET)
        response["username"] = request["username"]
        response["email"] = request["email"]

        self.assertRequest("put", "/users/%d" % self._USER2_GET["id"], data=request, expected_data=response)
        self.assertRequest("get", "/users", expected_data=[self._ADMIN_GET, self._USER1_GET, response])

    def test_update_username_to_name_of_another_user(self):
        request = dict(self._USER2_SET)
        request["username"] = self._USER1_SET["username"]

        self.assertRequest("put", "/users/%d" % self._USER2_GET["id"], data=request, expected_status_code=422)
