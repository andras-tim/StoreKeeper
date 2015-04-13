from app.modules.example_data import ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='item', base_item=Items.ITEM1,
                              mandatory_fields=['name', 'vendor', 'quantity', 'unit'])
class TestItemWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/items'
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_items(self):
        self.assertApiPost(data=Items.ITEM1, expected_data=Items.ITEM1)
        self.assertApiPost(data=Items.ITEM2, expected_data=Items.ITEM2)

    def test_can_add_item_with_negative_and_zero_quantity(self):
        self.assertApiPost(data=Items.ITEM1.set(change={'quantity': -1}))
        self.assertApiPost(data=Items.ITEM2.set(change={'quantity': 0}))

    def test_can_not_add_item_with_same_name(self):
        self.assertApiPost(data=Items.ITEM1)
        self.assertApiPost(data=Items.ITEM2.set(change={'name': Items.ITEM1['name']}),
                           expected_data={'message': {'name': ['Already exists.']}},
                           expected_status_codes=422)


class TestItemWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/items'
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        (ENDPOINT, [Items.ITEM1, Items.ITEM2]),
    ]

    def test_list_items(self):
        self.assertApiGet(expected_data=[Items.ITEM1,
                                         Items.ITEM2])

    def test_get_item(self):
        self.assertApiGet(2, expected_data=Items.ITEM2)
        self.assertApiGet(1, expected_data=Items.ITEM1)

    def test_remove_item(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Items.ITEM2])

    def test_can_not_remove_non_existed_item(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[Items.ITEM1,
                                         Items.ITEM2])

    def test_update_item(self):
        request = Items.ITEM2.set(change={'name': 'Spray222', 'vendor': Vendors.VENDOR1.get(), 'article_number': 222,
                                          'quantity': 222, 'unit': Units.UNIT2.get()})
        response = Items.ITEM2.get(change={'name': request['name'], 'vendor': request['vendor'],
                                           'article_number': request['article_number'], 'quantity': request['quantity'],
                                           'unit': request['unit']})

        self.assertApiPut(Items.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Items.ITEM1, response])

    def test_update_name_to_name_of_another_item(self):
        request = Items.ITEM2.set(change={'name': Items.ITEM1['name']})

        self.assertApiPut(Items.ITEM2['id'], data=request, expected_status_codes=422)
