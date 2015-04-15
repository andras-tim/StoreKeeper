from app.modules.example_data import ExampleWorkItems as WorkItems, ExampleWorks as Works, \
    ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units, ExampleCustomers as Customers, \
    ExampleUsers as Users
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests
from test.views.base_session_test import CommonSessionTest


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


class TesCloseOutboundOftWork(CommonSessionTest):
    ENDPOINT = '/work-items'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1, Works.WORK2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [WorkItems.ITEM1]),
    ]

    def setUp(self):
        super().setUp()
        self.assertApiLogin(Users.USER1)
        self.assertApiPut(Works.WORK1['id'], endpoint='/works', url_suffix='/close-outbound')

    def test_can_not_add_new_work_item_after_outbound_items_are_closed(self):
        self.assertApiPost(data=WorkItems.ITEM2.set(change={'work': Works.WORK1.get()}),
                           expected_data={'message': 'Can not add new item.'}, expected_status_codes=403)

    def test_can_not_change_work_of_work_item(self):
        request = WorkItems.ITEM1.set(change={'work': Works.WORK2.get()})
        self.assertApiPut(1, data=request,
                          expected_data={'message': 'Can not change work.'}, expected_status_codes=403)

    def test_can_not_change_outbound_work_item_after_outbound_items_are_closed(self):
        request = WorkItems.ITEM1.set(change={'item': Items.ITEM1.get()})
        self.assertApiPut(1, data=request,
                          expected_data={'message': 'Work item was closed.'}, expected_status_codes=403)

        request = WorkItems.ITEM1.set(change={'outbound_quantity': WorkItems.ITEM1['outbound_quantity'] + 1})
        self.assertApiPut(1, data=request,
                          expected_data={'message': 'Work item was closed.'}, expected_status_codes=403)
