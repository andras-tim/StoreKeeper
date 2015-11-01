from app.modules.example_data import ExampleAcquisitionItems as AcquisitionItems, ExampleAcquisitions as Acquisitions, \
    ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units
from test.e2e.base_api_test import CommonApiTest, append_mandatory_field_tests


class TestAcquisitionWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/acquisitions'

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_acquisitions(self):
        self.assertApiPost(data=Acquisitions.ACQUISITION1,
                           expected_data=Acquisitions.ACQUISITION1)
        self.assertApiPost(data=Acquisitions.ACQUISITION2,
                           expected_data=Acquisitions.ACQUISITION2)

    def test_can_add_acquisition_with_same_comment(self):
        self.assertApiPost(data=Acquisitions.ACQUISITION1)
        self.assertApiPost(data=Acquisitions.ACQUISITION2.set(
            change={'comment': Acquisitions.ACQUISITION1['comment']}))


class TestUserWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/acquisitions'
    INIT_PUSH = [
        (ENDPOINT, [Acquisitions.ACQUISITION1, Acquisitions.ACQUISITION2]),
    ]

    def test_list_acquisitions(self):
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION1,
                                         Acquisitions.ACQUISITION2])

    def test_get_acquisition(self):
        self.assertApiGet(2, expected_data=Acquisitions.ACQUISITION2)
        self.assertApiGet(1, expected_data=Acquisitions.ACQUISITION1)

    def test_remove_acquisition(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION2])

    def test_can_not_remove_non_existed_acquisition(self):
        self.assertApiDelete(3, expected_status_codes=404)
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION1,
                                         Acquisitions.ACQUISITION2])

    def test_update_acquisition(self):
        request = Acquisitions.ACQUISITION2.set(change={'comment': 'A box has been damaged'})
        response = Acquisitions.ACQUISITION2.get(change={'comment': request['comment']})

        self.assertApiPut(Acquisitions.ACQUISITION2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION1,
                                         response])

    def test_update_name_to_name_of_another_acquisition(self):
        request = Acquisitions.ACQUISITION2.set(change={'comment': Acquisitions.ACQUISITION1['comment']})

        self.assertApiPut(Acquisitions.ACQUISITION2['id'], data=request)


@append_mandatory_field_tests(item_name='acquisition_item', base_item=AcquisitionItems.ITEM1,
                              mandatory_fields=['item', 'quantity'])
class TestAcquisitionItemWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/acquisitions/1/items'
    BAD_ENDPOINT = '/acquisitions/2/items'
    INIT_PUSH = [
        ('/acquisitions', [Acquisitions.ACQUISITION1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_adding_new_acquisition_items(self):
        self.assertApiPost(data=AcquisitionItems.ITEM1, expected_data=AcquisitionItems.ITEM1)
        self.assertApiPost(data=AcquisitionItems.ITEM2, expected_data=AcquisitionItems.ITEM2)

    def test_can_not_adding_new_item_to_a_non_existed_acquisition(self):
        self.assertApiPost(data=AcquisitionItems.ITEM1, endpoint=self.BAD_ENDPOINT,
                           expected_status_codes=404)

    def test_can_not_add_acquisition_item_with_lower_than_one_quantity(self):
        self.assertApiPost(data=AcquisitionItems.ITEM1.set(change={'quantity': 0}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)
        self.assertApiPost(data=AcquisitionItems.ITEM1.set(change={'quantity': -1}),
                           expected_data={'message': {'quantity': ['Must be greater than 0.']}},
                           expected_status_codes=422)

    def test_can_not_add_more_than_once_an_item_to_an_acquisition(self):
        self.assertApiPost(data=AcquisitionItems.ITEM1)
        self.assertApiPost(data=AcquisitionItems.ITEM2.set(change={'item': AcquisitionItems.ITEM1['item']}),
                           expected_data={'message': {'acquisition_id, item_id': ['Already exists.']}},
                           expected_status_codes=422)


class TestAcquisitionItemWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/acquisitions/1/items'
    BAD_ENDPOINT = '/acquisitions/2/items'
    INIT_PUSH = [
        ('/acquisitions', [Acquisitions.ACQUISITION1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2, Items.ITEM3]),
        (ENDPOINT, [AcquisitionItems.ITEM1, AcquisitionItems.ITEM2]),
    ]

    def test_list_acquisition_items(self):
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM1,
                                         AcquisitionItems.ITEM2])

    def test_can_not_list_acquisition_items_of_a_non_existed_acquisition(self):
        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_get_acquisition_item(self):
        self.assertApiGet(2, expected_data=AcquisitionItems.ITEM2)
        self.assertApiGet(1, expected_data=AcquisitionItems.ITEM1)

    def test_can_not_get_acquisition_item_of_a_non_existed_acquisition(self):
        self.assertApiGet(1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_remove_acquisition_item(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM2])

    def test_can_not_remove_acquisition_item_of_a_non_existed_acquisition(self):
        self.assertApiDelete(1, endpoint=self.BAD_ENDPOINT,
                             expected_status_codes=404)

    def test_can_not_remove_non_existed_acquisition_item(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM1,
                                         AcquisitionItems.ITEM2])

    def test_update_acquisition_item(self):
        request = AcquisitionItems.ITEM2.set(change={'item': Items.ITEM3.get(), 'quantity': 1})
        response = AcquisitionItems.ITEM2.get(change={'item': request['item'], 'quantity': request['quantity']})

        self.assertApiPut(AcquisitionItems.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[AcquisitionItems.ITEM1, response])

    def test_can_not_update_acquisition_item_of_a_non_existed_acquisition(self):
        self.assertApiPut(AcquisitionItems.ITEM1['id'], data=AcquisitionItems.ITEM1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)
