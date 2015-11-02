from app.modules.example_data import ExampleUsers as Users
from test.e2e.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='user', base_item=Users.USER1,
                              mandatory_fields=['username', 'password', 'email'])
class TestUserWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/users'

    def test_new_db(self):
        self.assertApiGet(expected_data=[Users.ADMIN])
        self.assertApiGet(1, expected_data=Users.ADMIN)
        self.assertApiGet(2, expected_status_codes=404)

    def test_adding_new_users(self):
        self.assertApiPost(data=Users.USER1, expected_data=Users.USER1)
        self.assertApiPost(data=Users.USER2, expected_data=Users.USER2)

    def test_can_not_add_user_with_same_username(self):
        self.assertApiPost(data=Users.USER1)
        self.assertApiPost(data=Users.USER2.set(change={'username': Users.USER1['username']}),
                           expected_data={'message': {'username': ['Already exists.']}},
                           expected_status_codes=422)

    def test_can_not_add_user_with_bad_username(self):
        bad_usernames = ['_foo',
                         'foo_',
                         'Foo']

        for username in bad_usernames:
            self.assertApiPost(data={'username': username, 'password': 'a', 'email': 'foo@bar.com'},
                               expected_data={'message': {'username': ['String does not match expected pattern.']}},
                               expected_status_codes=422)

    def test_can_not_add_user_with_bad_email(self):
        self.assertApiPost(data=Users.USER1.set(change={'email': 'foo.bar'}),
                           expected_data={'message': {'email': ['"foo.bar" is not a valid email address.']}},
                           expected_status_codes=422)


class TestUserWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/users'
    INIT_PUSH = [
        (ENDPOINT, [Users.USER1, Users.USER2])
    ]

    def test_list_users(self):
        self.assertApiGet(expected_data=[Users.ADMIN,
                                         Users.USER1,
                                         Users.USER2])

    def test_get_user(self):
        self.assertApiGet(3, expected_data=Users.USER2)
        self.assertApiGet(2, expected_data=Users.USER1)

    def test_remove_user(self):
        self.assertApiDelete(2)
        self.assertApiGet(expected_data=[Users.ADMIN,
                                         Users.USER2])

    def test_can_not_remove_non_existed_user(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[Users.ADMIN,
                                         Users.USER1,
                                         Users.USER2])

    def test_update_user(self):
        request = Users.USER2.set(change={'username': 'foo2', 'email': 'new_foo2@bar.com'})
        response = Users.USER2.get(change={'username': request['username'], 'email': request['email']})

        self.assertApiPut(Users.USER2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Users.ADMIN,
                                         Users.USER1,
                                         response])

    def test_update_username_to_name_of_another_user(self):
        request = Users.USER2.set(change={'username': Users.USER1['username']})

        self.assertApiPut(Users.USER2['id'], data=request, expected_status_codes=422)

    def test_update_password(self):
        request = Users.USER1.set(change={'password': 'new_pw'})
        response = Users.USER1

        self.assertApiPut(Users.USER1['id'], data=request, expected_data=response)
