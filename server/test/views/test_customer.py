from app.modules.example_data import ExampleCustomers as Customers
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='customer', base_item=Customers.CUSTOMER1,
                              mandatory_fields=['name'])
class TestCustomerWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/customers'

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_customers(self):
        self.assertApiPost(data=Customers.CUSTOMER1, expected_data=Customers.CUSTOMER1)
        self.assertApiPost(data=Customers.CUSTOMER2, expected_data=Customers.CUSTOMER2)

    def test_can_not_add_customer_with_same_name(self):
        self.assertApiPost(data=Customers.CUSTOMER1)
        self.assertApiPost(data=Customers.CUSTOMER2.set(change={'name': Customers.CUSTOMER1['name']}),
                           expected_data={'message': {'name': ['Already exists.']}},
                           expected_status_codes=422)


class TestUserWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/customers'
    INIT_PUSH = [
        (ENDPOINT, [Customers.CUSTOMER1, Customers.CUSTOMER2]),
    ]

    def test_list_customers(self):
        self.assertApiGet(expected_data=[Customers.CUSTOMER1,
                                         Customers.CUSTOMER2])

    def test_get_customer(self):
        self.assertApiGet(2, expected_data=Customers.CUSTOMER2)
        self.assertApiGet(1, expected_data=Customers.CUSTOMER1)

    def test_remove_customer(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Customers.CUSTOMER2])

    def test_can_not_remove_non_existed_customer(self):
        self.assertApiDelete(3, expected_status_codes=404)
        self.assertApiGet(expected_data=[Customers.CUSTOMER1,
                                         Customers.CUSTOMER2])

    def test_update_customer(self):
        request = Customers.CUSTOMER2.set(change={'name': 'foo2'})
        response = Customers.CUSTOMER2.get(change={'name': request['name']})

        self.assertApiPut(Customers.CUSTOMER2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Customers.CUSTOMER1,
                                         response])

    def test_update_name_to_name_of_another_customer(self):
        request = Customers.CUSTOMER2.set(change={'name': Customers.CUSTOMER1['name']})

        self.assertApiPut(Customers.CUSTOMER2['id'], data=request, expected_status_codes=422)
