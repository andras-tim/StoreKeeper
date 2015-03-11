from app.modules.example_data import ExampleVendors as Vendors
from test.views import CommonApiTest


class TestVendorWithBrandNewDb(CommonApiTest):
    def test_new_db(self):
        self.assertRequest("get", "/vendors", expected_data=[])
        self.assertRequest("get", "/vendors/1", expected_status_codes=404)

    def test_adding_new_vendors(self):
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR1.set(), expected_data=Vendors.VENDOR1.get())
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR2.set(), expected_data=Vendors.VENDOR2.get())

    def test_can_not_add_vendor_with_same_name(self):
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR1.set())
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR2.set(change={"name": Vendors.VENDOR1["name"]}),
                           expected_data={'message': {'name': ['Already exists.']}},
                           expected_status_codes=422)

    def test_can_not_add_vendor_with_missing_name(self):
        self.assertRequest("post", "/vendors", data={},
                           expected_data={"message": {"name": ["This field is required."]}},
                           expected_status_codes=422)
        self.assertRequest("post", "/vendors", data={"name": ""},
                           expected_data={"message": {"name": ["This field is required."]}},
                           expected_status_codes=422)


class TestUserWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR1.set())
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR2.set())

    def test_list_vendors(self):
        self.assertRequest("get", "/vendors", expected_data=[Vendors.VENDOR1.get(),
                                                             Vendors.VENDOR2.get()])

    def test_get_vendor(self):
        self.assertRequest("get", "/vendors/2", expected_data=Vendors.VENDOR2.get())
        self.assertRequest("get", "/vendors/1", expected_data=Vendors.VENDOR1.get())

    def test_remove_vendor(self):
        self.assertRequest("delete", "/vendors/1")
        self.assertRequest("get", "/vendors", expected_data=[Vendors.VENDOR2.get()])

    def test_can_not_remove_non_existed_vendor(self):
        self.assertRequest("delete", "/vendors/3", expected_status_codes=404)
        self.assertRequest("get", "/vendors", expected_data=[Vendors.VENDOR1.get(),
                                                             Vendors.VENDOR2.get()])

    def test_update_vendor(self):
        request = Vendors.VENDOR2.set(change={"name": "foo2"})
        response = Vendors.VENDOR2.get(change={"name": "foo2"})

        self.assertRequest("put", "/vendors/%d" % Vendors.VENDOR2["id"], data=request, expected_data=response)
        self.assertRequest("get", "/vendors", expected_data=[Vendors.VENDOR1.get(), response])

    def test_update_name_to_name_of_another_vendor(self):
        request = Vendors.VENDOR2.set(change={"name": Vendors.VENDOR1["name"]})

        self.assertRequest("put", "/vendors/%d" % Vendors.VENDOR2["id"], data=request, expected_status_codes=422)
