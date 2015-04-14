from app.modules.example_data import ExampleWorkItems as WorkItems, ExampleWorks as Works, \
    ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units, ExampleCustomers as Customers
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='work_item', base_item=WorkItems.ITEM1,
                              mandatory_fields=['work', 'item', 'outbound_quantity'])
class TestWorkItemWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/work-items'
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1, Works.WORK2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_work_items(self):
        self.assertApiPost(data=WorkItems.ITEM1, expected_data=WorkItems.ITEM1)
        self.assertApiPost(data=WorkItems.ITEM2, expected_data=WorkItems.ITEM2)

    def test_can_add_work_item_with_minimal_quantities(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'outbound_quantity': 1}))
        self.assertApiPost(data=WorkItems.ITEM2.set(change={'returned_quantity': 0}))

    def test_can_not_add_work_item_with_zero_outbound_quantity(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'outbound_quantity': 0}), expected_status_codes=422)

    def test_can_not_add_work_item_with_zero_returned_quantity(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'returned_quantity': -1}), expected_status_codes=422)

    def test_can_add_work_item_with_more_returned_quantity_than_outbound_quantity(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'outbound_quantity': 1, 'returned_quantity': 3}))

    def test_can_not_add_more_than_once_an_item_to_a_work(self):
        self.assertApiPost(data=WorkItems.ITEM1)
        self.assertApiPost(data=WorkItems.ITEM2.set(change={'work': WorkItems.ITEM1['work'],
                                                            'item': WorkItems.ITEM1['item']}),
                           expected_data={
                               'message': {'item_id, work_id': ['Already exists.']}},
                           expected_status_codes=422)


class TestWorkItemWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/work-items'
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1, Works.WORK2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [WorkItems.ITEM1, WorkItems.ITEM2]),
    ]

    def test_list_work_items(self):
        self.assertApiGet(expected_data=[WorkItems.ITEM1,
                                         WorkItems.ITEM2])

    def test_get_work_item(self):
        self.assertApiGet(2, expected_data=WorkItems.ITEM2)
        self.assertApiGet(1, expected_data=WorkItems.ITEM1)

    def test_remove_work_item(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[WorkItems.ITEM2])

    def test_can_not_remove_non_existed_work_item(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[WorkItems.ITEM1,
                                         WorkItems.ITEM2])

    def test_update_work_item(self):
        request = WorkItems.ITEM2.set(change={'work': Works.WORK2.get(), 'item': Items.ITEM2.get(),
                                              'outbound_quantity': 8, 'returned_quantity': 8})
        response = WorkItems.ITEM2.get(change={'work': request['work'], 'item': request['item'],
                                               'outbound_quantity': request['outbound_quantity'],
                                               'returned_quantity': request['returned_quantity']})

        self.assertApiPut(WorkItems.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[WorkItems.ITEM1, response])
