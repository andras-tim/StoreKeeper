from app.modules.example_data import ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units, \
    ExampleItemBarcodes as ItemBarcodes, ExampleBarcodes as Barcodes
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


# I do not want to check the output of printing, therefore this feature is tested only by rights

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
        request = Items.ITEM2.set(change={'name': 'Spray222', 'vendor': Vendors.VENDOR1.get(), 'article_number': 'B222',
                                          'quantity': 222.0, 'unit': Units.UNIT2.get()})
        response = Items.ITEM2.get(change={'name': request['name'], 'vendor': request['vendor'],
                                           'article_number': request['article_number'], 'quantity': request['quantity'],
                                           'unit': request['unit']})

        self.assertApiPut(Items.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Items.ITEM1, response])

    def test_update_name_to_name_of_another_item(self):
        request = Items.ITEM2.set(change={'name': Items.ITEM1['name']})

        self.assertApiPut(Items.ITEM2['id'], data=request, expected_status_codes=422)


@append_mandatory_field_tests(item_name='barcode', base_item=ItemBarcodes.BARCODE1,
                              mandatory_fields=['barcode'])
class TestItemBarcodeWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/items/1/barcodes'
    BAD_ENDPOINT = '/items/3/barcodes'
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_adding_new_item_barcodes(self):
        self.assertApiPost(data=ItemBarcodes.BARCODE1, expected_data=ItemBarcodes.BARCODE1)
        self.assertApiPost(data=ItemBarcodes.BARCODE2, expected_data=ItemBarcodes.BARCODE2)

    def test_can_not_adding_new_barcode_to_a_non_existed_item(self):
        self.assertApiPost(data=ItemBarcodes.BARCODE1, endpoint=self.BAD_ENDPOINT,
                           expected_status_codes=404)

    def test_can_not_add_item_barcode_with_lower_than_one_quantity(self):
        self.assertApiPost(data=ItemBarcodes.BARCODE1.set(change={'quantity': 0}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)
        self.assertApiPost(data=ItemBarcodes.BARCODE1.set(change={'quantity': -1}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)

    def test_can_not_add_more_than_once_an_barcode_to_a_item(self):
        self.assertApiPost(data=ItemBarcodes.BARCODE1)
        self.assertApiPost(data=ItemBarcodes.BARCODE2.set(change={'barcode': ItemBarcodes.BARCODE1['barcode']}),
                           expected_data={'message': {'barcode_id, item_id': ['Already exists.']}},
                           expected_status_codes=422)

    def test_can_not_add_more_than_one_main_barcode(self):
        self.assertApiPost(data=ItemBarcodes.BARCODE1)
        self.assertApiPost(data=ItemBarcodes.BARCODE2.set(change={'main': True}),
                           expected_data={'message': {'main': ['Can not set more than one main barcode to an item.']}},
                           expected_status_codes=422)


class TestItemBarcodeWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/items/1/barcodes'
    BAD_ENDPOINT = '/items/3/barcodes'
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [ItemBarcodes.BARCODE1, ItemBarcodes.BARCODE2]),
    ]

    def test_list_item_barcodes(self):
        self.assertApiGet(expected_data=[ItemBarcodes.BARCODE1,
                                         ItemBarcodes.BARCODE2])

    def test_can_not_list_item_barcodes_of_a_non_existed_item(self):
        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_get_item_barcode(self):
        self.assertApiGet(2, expected_data=ItemBarcodes.BARCODE2)
        self.assertApiGet(1, expected_data=ItemBarcodes.BARCODE1)

    def test_can_not_get_item_barcode_of_a_non_existed_item(self):
        self.assertApiGet(1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_remove_item_barcode(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[ItemBarcodes.BARCODE2])

    def test_can_not_remove_item_barcode_of_a_non_existed_item(self):
        self.assertApiDelete(1, endpoint=self.BAD_ENDPOINT,
                             expected_status_codes=404)

    def test_can_not_remove_non_existed_item_barcode(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[ItemBarcodes.BARCODE1,
                                         ItemBarcodes.BARCODE2])

    def test_update_item_barcode(self):
        request = ItemBarcodes.BARCODE2.set(change={'barcode': 'XX{:s}XX'.format(ItemBarcodes.BARCODE2['barcode']),
                                                    'quantity': ItemBarcodes.BARCODE2['quantity'] + 1})
        response = ItemBarcodes.BARCODE2.get(change={'barcode': request['barcode'], 'quantity': request['quantity'],
                                                     'main': request['main']})

        self.assertApiPut(ItemBarcodes.BARCODE2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[ItemBarcodes.BARCODE1, response])

    def test_can_not_update_item_barcode_of_a_non_existed_item(self):
        self.assertApiPut(ItemBarcodes.BARCODE1['id'], data=ItemBarcodes.BARCODE1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)
