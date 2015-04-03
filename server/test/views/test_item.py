from app.modules.example_data import ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units
from test.views import CommonApiTest


class TestItemWithBrandNewDb(CommonApiTest):
    MANDATORY_FIELDS = ["name", "vendor", "quantity", "unit"]

    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR1.set())
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR2.set())
        self.assertRequest("post", "/units", data=Units.UNIT1.set())
        self.assertRequest("post", "/units", data=Units.UNIT2.set())

    def test_new_db(self):
        self.assertRequest("get", "/items", expected_data=[])
        self.assertRequest("get", "/items/1", expected_status_codes=404)

    def test_adding_new_items(self):
        self.assertRequest("post", "/items", data=Items.ITEM1.set(), expected_data=Items.ITEM1.get())
        self.assertRequest("post", "/items", data=Items.ITEM2.set(), expected_data=Items.ITEM2.get())

    def test_can_not_add_item_with_same_name(self):
        self.assertRequest("post", "/items", data=Items.ITEM1.set())
        self.assertRequest("post", "/items", data=Items.ITEM2.set(change={"name": Items.ITEM1["name"]}),
                           expected_data={'message': {'name': ['Already exists.']}},
                           expected_status_codes=422)

    def test_can_not_add_item_with_missing_one_mandatory_field(self):
        for field_name in self.MANDATORY_FIELDS:
            request = Items.ITEM1.set()
            del request[field_name]

            self.assertRequest("post", "/items", data=request,
                               expected_data={"message": {field_name: ["Missing data for required field."]}},
                               expected_status_codes=422)

    def test_can_not_add_item_with_missing_all_mandatory_fields(self):
        request = Items.ITEM1.set()
        for field_name in self.MANDATORY_FIELDS:
            del request[field_name]

        self.assertRequest("post", "/items", data=request,
                           expected_data={"message": dict((field_name, ["Missing data for required field."])
                                                          for field_name in self.MANDATORY_FIELDS)},
                           expected_status_codes=422)


class TestItemWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR1.set())
        self.assertRequest("post", "/vendors", data=Vendors.VENDOR2.set())
        self.assertRequest("post", "/units", data=Units.UNIT1.set())
        self.assertRequest("post", "/units", data=Units.UNIT2.set())
        self.assertRequest("post", "/items", data=Items.ITEM1.set())
        self.assertRequest("post", "/items", data=Items.ITEM2.set())

    def test_list_items(self):
        self.assertRequest("get", "/items", expected_data=[Items.ITEM1.get(),
                                                           Items.ITEM2.get()])

    def test_get_item(self):
        self.assertRequest("get", "/items/2", expected_data=Items.ITEM2.get())
        self.assertRequest("get", "/items/1", expected_data=Items.ITEM1.get())

    def test_remove_item(self):
        self.assertRequest("delete", "/items/1")
        self.assertRequest("get", "/items", expected_data=[Items.ITEM2.get()])

    def test_can_not_remove_non_existed_item(self):
        self.assertRequest("delete", "/items/4", expected_status_codes=404)
        self.assertRequest("get", "/items", expected_data=[Items.ITEM1.get(),
                                                           Items.ITEM2.get()])

    def test_update_item(self):
        request = Items.ITEM2.set(change={"name": "Spray222", "vendor": Vendors.VENDOR1.get(), "article_number": 222,
                                          "quantity": 222, "unit": Units.UNIT2.get()})
        response = Items.ITEM2.get(change={"name": request["name"], "vendor": request["vendor"],
                                           "article_number": request["article_number"], "quantity": request["quantity"],
                                           "unit": request["unit"]})

        self.assertRequest("put", "/items/%d" % Items.ITEM2["id"], data=request, expected_data=response)
        self.assertRequest("get", "/items", expected_data=[Items.ITEM1.get(), response])

    def test_update_name_to_name_of_another_item(self):
        request = Items.ITEM2.set(change={"name": Items.ITEM1["name"]})

        self.assertRequest("put", "/items/%d" % Items.ITEM2["id"], data=request, expected_status_codes=422)
