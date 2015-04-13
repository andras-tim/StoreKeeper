from app.modules.example_data import ExampleAcquisitionItems as AcquisitionItems, ExampleAcquisitions as Acquisitions, \
    ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='acquisition_item', base_item=AcquisitionItems.ITEM1,
                              mandatory_fields=['acquisition', 'item', 'quantity'])
class TestAcquisitionItemWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/acquisition-items'
    INIT_PUSH = [
        ('/acquisitions', [Acquisitions.ACQUISITION1, Acquisitions.ACQUISITION2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_acquisition_items(self):
        self.assertApiPost(data=AcquisitionItems.ITEM1, expected_data=AcquisitionItems.ITEM1)
        self.assertApiPost(data=AcquisitionItems.ITEM2, expected_data=AcquisitionItems.ITEM2)

    def test_can_not_add_acquisition_item_with_lower_than_one_quantity(self):
        self.assertApiPost(data=AcquisitionItems.ITEM1.set(change={'quantity': 0}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)
        self.assertApiPost(data=AcquisitionItems.ITEM1.set(change={'quantity': -1}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)

    def test_can_not_add_more_than_once_an_item_to_an_acquisition(self):
        self.assertApiPost(data=AcquisitionItems.ITEM1)
        self.assertApiPost(data=AcquisitionItems.ITEM2.set(change={'acquisition': AcquisitionItems.ITEM1['acquisition'],
                                                                   'item': AcquisitionItems.ITEM1['item']}),
                           expected_data={
                               'message': {'acquisition_id, item_id': ['Already exists.']}},
                           expected_status_codes=422)


class TestAcquisitionItemWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/acquisition-items'
    INIT_PUSH = [
        ('/acquisitions', [Acquisitions.ACQUISITION1, Acquisitions.ACQUISITION2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [AcquisitionItems.ITEM1, AcquisitionItems.ITEM2]),
    ]

    def test_list_acquisition_items(self):
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM1,
                                         AcquisitionItems.ITEM2])

    def test_get_acquisition_item(self):
        self.assertApiGet(2, expected_data=AcquisitionItems.ITEM2)
        self.assertApiGet(1, expected_data=AcquisitionItems.ITEM1)

    def test_remove_acquisition_item(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM2])

    def test_can_not_remove_non_existed_acquisition_item(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM1,
                                         AcquisitionItems.ITEM2])

    def test_update_acquisition_item(self):
        request = AcquisitionItems.ITEM2.set(change={'acquisition': Acquisitions.ACQUISITION2.get(),
                                                     'item': Items.ITEM2.get(), 'quantity': 1})
        response = AcquisitionItems.ITEM2.get(change={'acquisition': request['acquisition'], 'item': request['item'],
                                                      'quantity': request['quantity']})

        self.assertApiPut(AcquisitionItems.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM1, response])
