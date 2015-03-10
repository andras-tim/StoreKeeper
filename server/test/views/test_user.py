from app.modules.example_data import ExampleUsers as Users
from test.views import CommonApiTest


class TestUserWithBrandNewDb(CommonApiTest):
    def test_new_db(self):
        self.assertRequest("get", "/users", expected_data=[Users.ADMIN.get()])
        self.assertRequest("get", "/users/1", expected_data=Users.ADMIN.get())
        self.assertRequest("get", "/users/2", expected_status_code=404)

    def test_adding_new_users(self):
        self.assertRequest("post", "/users", data=Users.USER1.set(), expected_data=Users.USER1.get())
        self.assertRequest("post", "/users", data=Users.USER2.set(), expected_data=Users.USER2.get())

    def test_can_not_add_user_with_same_username(self):
        self.assertRequest("post", "/users", data=Users.USER1.set())
        self.assertRequest("post", "/users", data=Users.USER2.set(change={"username": Users.USER1["username"]}),
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

        self.assertRequest("post", "/users", data={"username": "", "password": "", "email": ""},
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
        self.assertRequest("post", "/users", data=Users.USER1.set(change={"email": "foo.bar"}),
                           expected_data={"message": {'email': ['Invalid email address.']}},
                           expected_status_code=422)


class TestUserWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/users", data=Users.USER1.set())
        self.assertRequest("post", "/users", data=Users.USER2.set())

    def test_list_users(self):
        self.assertRequest("get", "/users", expected_data=[Users.ADMIN.get(),
                                                           Users.USER1.get(),
                                                           Users.USER2.get()])

    def test_get_user(self):
        self.assertRequest("get", "/users/3", expected_data=Users.USER2.get())
        self.assertRequest("get", "/users/2", expected_data=Users.USER1.get())

    def test_remove_user(self):
        self.assertRequest("delete", "/users/2")
        self.assertRequest("get", "/users", expected_data=[Users.ADMIN.get(),
                                                           Users.USER2.get()])

    def test_can_not_remove_non_existed_user(self):
        self.assertRequest("delete", "/users/4", expected_status_code=404)
        self.assertRequest("get", "/users", expected_data=[Users.ADMIN.get(),
                                                           Users.USER1.get(),
                                                           Users.USER2.get()])

    def test_update_user(self):
        request = Users.USER2.set(change={"username": "foo2", "email": "new_foo2@bar.com"})
        response = Users.USER2.get(change={"username": "foo2", "email": "new_foo2@bar.com"})

        self.assertRequest("put", "/users/%d" % Users.USER2["id"], data=request, expected_data=response)
        self.assertRequest("get", "/users", expected_data=[Users.ADMIN.get(), Users.USER1.get(), response])

    def test_update_username_to_name_of_another_user(self):
        request = Users.USER2.set(change={"username": Users.USER1["username"]})

        self.assertRequest("put", "/users/%d" % Users.USER2["id"], data=request, expected_status_code=422)
