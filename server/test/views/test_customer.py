from app.modules.example_data import ExampleCustomers as Customers
from test.views import CommonApiTest


class TestCustomerWithBrandNewDb(CommonApiTest):
    def test_new_db(self):
        self.assertRequest("get", "/customers", expected_data=[])
        self.assertRequest("get", "/customers/1", expected_status_codes=404)

    def test_adding_new_customers(self):
        self.assertRequest("post", "/customers", data=Customers.CUSTOMER1.set(),
                           expected_data=Customers.CUSTOMER1.get())
        self.assertRequest("post", "/customers", data=Customers.CUSTOMER2.set(),
                           expected_data=Customers.CUSTOMER2.get())

    def test_can_not_add_customer_with_same_name(self):
        self.assertRequest("post", "/customers", data=Customers.CUSTOMER1.set())
        self.assertRequest("post", "/customers",
                           data=Customers.CUSTOMER2.set(change={"name": Customers.CUSTOMER1["name"]}),
                           expected_data={'message': {'name': ['Already exists.']}},
                           expected_status_codes=422)

    def test_can_not_add_customer_with_missing_name(self):
        self.assertRequest("post", "/customers", data={},
                           expected_data={"message": {"name": ["Missing data for required field."]}},
                           expected_status_codes=422)
        self.assertRequest("post", "/customers", data={"name": ""},
                           expected_data={"message": {"name": ["Missing data for required field."]}},
                           expected_status_codes=422)


class TestUserWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/customers", data=Customers.CUSTOMER1.set())
        self.assertRequest("post", "/customers", data=Customers.CUSTOMER2.set())

    def test_list_customers(self):
        self.assertRequest("get", "/customers", expected_data=[Customers.CUSTOMER1.get(),
                                                               Customers.CUSTOMER2.get()])

    def test_get_customer(self):
        self.assertRequest("get", "/customers/2", expected_data=Customers.CUSTOMER2.get())
        self.assertRequest("get", "/customers/1", expected_data=Customers.CUSTOMER1.get())

    def test_remove_customer(self):
        self.assertRequest("delete", "/customers/1")
        self.assertRequest("get", "/customers", expected_data=[Customers.CUSTOMER2.get()])

    def test_can_not_remove_non_existed_customer(self):
        self.assertRequest("delete", "/customers/3", expected_status_codes=404)
        self.assertRequest("get", "/customers", expected_data=[Customers.CUSTOMER1.get(),
                                                               Customers.CUSTOMER2.get()])

    def test_update_customer(self):
        request = Customers.CUSTOMER2.set(change={"name": "foo2"})
        response = Customers.CUSTOMER2.get(change={"name": request["name"]})

        self.assertRequest("put", "/customers/%d" % Customers.CUSTOMER2["id"], data=request, expected_data=response)
        self.assertRequest("get", "/customers", expected_data=[Customers.CUSTOMER1.get(), response])

    def test_update_name_to_name_of_another_customer(self):
        request = Customers.CUSTOMER2.set(change={"name": Customers.CUSTOMER1["name"]})

        self.assertRequest("put", "/customers/%d" % Customers.CUSTOMER2["id"], data=request, expected_status_codes=422)
