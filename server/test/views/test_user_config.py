from app.modules.example_data import ExampleUsers as Users, ExampleUserConfigs as UserConfigs
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='user_config', base_item=UserConfigs.CONFIG1,
                              mandatory_fields=['name', 'value'])
class TestUserConfigWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/users/2/config'
    BAD_ENDPOINT = '/users/3/config'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_adding_new_user_config(self):
        self.assertApiPost(data=UserConfigs.CONFIG1, expected_data=UserConfigs.CONFIG1)
        self.assertApiPost(data=UserConfigs.CONFIG2, expected_data=UserConfigs.CONFIG2)

    def test_can_not_adding_new_config_to_a_non_existed_user(self):
        self.assertApiPost(data=UserConfigs.CONFIG1, endpoint=self.BAD_ENDPOINT,
                           expected_status_codes=404)

    def test_can_add_user_config_with_negative_and_zero_quantity(self):
        self.assertApiPost(data=UserConfigs.CONFIG1.set(change={'quantity': -1}))
        self.assertApiPost(data=UserConfigs.CONFIG2.set(change={'quantity': 0}))

    def test_can_not_add_more_than_once_a_name_to_a_user(self):
        self.assertApiPost(data=UserConfigs.CONFIG1)
        self.assertApiPost(data=UserConfigs.CONFIG2.set(change={'name': UserConfigs.CONFIG1['name']}),
                           expected_data={'message': {'name, user_id': ['Already exists.']}},
                           expected_status_codes=422)


class TestUserConfigWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/users/2/config'
    BAD_ENDPOINT = '/users/3/config'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
        (ENDPOINT, [UserConfigs.CONFIG1, UserConfigs.CONFIG2]),
    ]

    def test_list_user_config(self):
        self.assertApiGet(expected_data=[UserConfigs.CONFIG1,
                                         UserConfigs.CONFIG2])

    def test_can_not_list_user_config_of_a_non_existed_user(self):
        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_get_user_config(self):
        self.assertApiGet(UserConfigs.CONFIG2['name'], expected_data=UserConfigs.CONFIG2)
        self.assertApiGet(UserConfigs.CONFIG1['name'], expected_data=UserConfigs.CONFIG1)

    def test_can_not_get_user_config_of_a_non_existed_user(self):
        self.assertApiGet(UserConfigs.CONFIG1['name'], endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_remove_user_config(self):
        self.assertApiDelete(UserConfigs.CONFIG1['name'])
        self.assertApiGet(expected_data=[UserConfigs.CONFIG2])

    def test_can_not_remove_user_config_of_a_non_existed_user(self):
        self.assertApiDelete(UserConfigs.CONFIG1['name'], endpoint=self.BAD_ENDPOINT,
                             expected_status_codes=404)

    def test_can_not_remove_non_existed_user_config(self):
        self.assertApiDelete('not-existed-name', expected_status_codes=404)
        self.assertApiGet(expected_data=[UserConfigs.CONFIG1,
                                         UserConfigs.CONFIG2])

    def test_update_user_config(self):
        request = UserConfigs.CONFIG2.set(change={'value': '{}_new'.format(UserConfigs.CONFIG2['value'])})
        response = UserConfigs.CONFIG2.get(change={'value': request['value']})

        self.assertApiPut(UserConfigs.CONFIG2['name'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[UserConfigs.CONFIG1, response])

    def test_can_not_update_user_config_of_a_non_existed_user(self):
        self.assertApiPut(UserConfigs.CONFIG1['name'], data=UserConfigs.CONFIG1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)
