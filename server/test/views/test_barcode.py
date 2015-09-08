from app.modules.example_data import ExampleBarcodes as Barcodes, ExampleItems as Items, ExampleVendors as Vendors, \
    ExampleUnits as Units
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


# I do not want to check the output of printing, therefore this feature is tested only by rights

@append_mandatory_field_tests(item_name='barcode', base_item=Barcodes.BARCODE1,
                              mandatory_fields=['barcode', 'item_id'])
class TestBarcodeWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/barcodes'
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_barcodes(self):
        self.assertApiPost(data=Barcodes.BARCODE1, expected_data=Barcodes.BARCODE1)
        self.assertApiPost(data=Barcodes.BARCODE2, expected_data=Barcodes.BARCODE2)

    def test_can_not_add_barcode_with_lower_than_one_quantity(self):
        self.assertApiPost(data=Barcodes.BARCODE1.set(change={'quantity': 0}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)
        self.assertApiPost(data=Barcodes.BARCODE1.set(change={'quantity': -1}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)

    def test_can_not_add_barcode_with_same_barcode(self):
        self.assertApiPost(data=Barcodes.BARCODE1)
        self.assertApiPost(data=Barcodes.BARCODE2.set(change={'barcode': Barcodes.BARCODE1['barcode']}),
                           expected_data={'message': {'barcode': ['Already exists.']}},
                           expected_status_codes=422)

    def test_can_not_add_more_than_one_main_barcode(self):
        self.assertApiPost(data=Barcodes.BARCODE1)
        self.assertApiPost(data=Barcodes.BARCODE2.set(change={'main': True}),
                           expected_data={'message': {'main': ['Can not set more than one main barcode to an item.']}},
                           expected_status_codes=422)


class TestBarcodeWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/barcodes'
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [Barcodes.BARCODE1, Barcodes.BARCODE2]),
    ]

    def test_list_barcodes(self):
        self.assertApiGet(expected_data=[Barcodes.BARCODE1,
                                         Barcodes.BARCODE2])

    def test_get_barcode(self):
        self.assertApiGet(2, expected_data=Barcodes.BARCODE2)
        self.assertApiGet(1, expected_data=Barcodes.BARCODE1)

    def test_remove_barcode(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Barcodes.BARCODE2])

    def test_can_not_remove_non_existed_barcode(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[Barcodes.BARCODE1,
                                         Barcodes.BARCODE2])

    def test_update_barcode(self):
        request = Barcodes.BARCODE2.set(change={'barcode': 'XX{:s}XX'.format(Barcodes.BARCODE2['barcode']),
                                                'quantity': Barcodes.BARCODE2['quantity'] + 1,
                                                'item_id': Items.ITEM2.get()['id'],
                                                'main': True})
        response = Barcodes.BARCODE2.get(change={'barcode': request['barcode'], 'quantity': request['quantity'],
                                                 'item_id': request['item_id'], 'main': request['main']})

        self.assertApiPut(Barcodes.BARCODE2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Barcodes.BARCODE1, response])

    def test_can_not_set_more_than_one_main_barcode(self):
        self.assertApiPut(Barcodes.BARCODE2['id'], data=Barcodes.BARCODE2.set(change={'main': True}),
                          expected_data={'message': {'main': ['Can not set more than one main barcode to an item.']}},
                          expected_status_codes=422)
