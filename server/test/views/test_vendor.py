from app.modules.example_data import ExampleVendors as Vendors
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name="vendor", base_item=Vendors.VENDOR1,
                              mandatory_fields=["name"])
class TestVendorWithBrandNewDb(CommonApiTest):
    ENDPOINT = "/vendors"

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_vendors(self):
        self.assertApiPost(data=Vendors.VENDOR1, expected_data=Vendors.VENDOR1)
        self.assertApiPost(data=Vendors.VENDOR2, expected_data=Vendors.VENDOR2)

    def test_can_not_add_vendor_with_same_name(self):
        self.assertApiPost(data=Vendors.VENDOR1)
        self.assertApiPost(data=Vendors.VENDOR2.set(change={"name": Vendors.VENDOR1["name"]}),
                           expected_data={'message': {'name': ['Already exists.']}},
                           expected_status_codes=422)


class TestUserWithPreFilledDb(CommonApiTest):
    ENDPOINT = "/vendors"
    INIT_PUSH = [
        (ENDPOINT, [Vendors.VENDOR1, Vendors.VENDOR2]),
    ]

    def test_list_vendors(self):
        self.assertApiGet(expected_data=[Vendors.VENDOR1,
                                         Vendors.VENDOR2])

    def test_get_vendor(self):
        self.assertApiGet(2, expected_data=Vendors.VENDOR2)
        self.assertApiGet(1, expected_data=Vendors.VENDOR1)

    def test_remove_vendor(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Vendors.VENDOR2])

    def test_can_not_remove_non_existed_vendor(self):
        self.assertApiDelete(3, expected_status_codes=404)
        self.assertApiGet(expected_data=[Vendors.VENDOR1,
                                         Vendors.VENDOR2])

    def test_update_vendor(self):
        request = Vendors.VENDOR2.set(change={"name": "foo2"})
        response = Vendors.VENDOR2.get(change={"name": request["name"]})

        self.assertApiPut(Vendors.VENDOR2["id"], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Vendors.VENDOR1,
                                         response])

    def test_update_name_to_name_of_another_vendor(self):
        request = Vendors.VENDOR2.set(change={"name": Vendors.VENDOR1["name"]})

        self.assertApiPut(Vendors.VENDOR2["id"], data=request, expected_status_codes=422)
