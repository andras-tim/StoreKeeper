from app.modules.example_data import ExampleWorkItems as WorkItems, ExampleWorks as Works, \
    ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units, ExampleCustomers as Customers, \
    ExampleUsers as Users
from test.e2e.base_api_test import CommonApiTest, append_mandatory_field_tests
from test.e2e.base_session_test import CommonSessionTest
from test.e2e.base_session_test_w_mutable_item import CommonSessionTestWithItemManipulation


class TestWorkWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/works'
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_works(self):
        self.assertApiPost(data=Works.WORK1, expected_data=Works.WORK1)
        self.assertApiPost(data=Works.WORK2, expected_data=Works.WORK2)

    def test_can_add_work_with_same_comment(self):
        self.assertApiPost(data=Works.WORK1)
        self.assertApiPost(data=Works.WORK2.set(
            change={'comment': Works.WORK1['comment']}))


class TestUserWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/works'
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        (ENDPOINT, [Works.WORK1, Works.WORK2]),
    ]

    def test_list_works(self):
        self.assertApiGet(expected_data=[Works.WORK1,
                                         Works.WORK2])

    def test_get_work(self):
        self.assertApiGet(2, expected_data=Works.WORK2)
        self.assertApiGet(1, expected_data=Works.WORK1)

    def test_remove_work(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Works.WORK2.get()])

    def test_can_not_remove_non_existed_work(self):
        self.assertApiDelete(3, expected_status_codes=404)
        self.assertApiGet(expected_data=[Works.WORK1,
                                         Works.WORK2])

    def test_update_work(self):
        request = Works.WORK2.set(change={'comment': 'Something are not finished'})
        response = Works.WORK2.get(change={'comment': request['comment']})

        self.assertApiPut(Works.WORK2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Works.WORK1,
                                         response])


class TesCloseOutboundOfWorkWithoutWorkItems(CommonSessionTest):
    ENDPOINT = '/works'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
        ('/customers', [Customers.CUSTOMER1]),
    ]

    def setUp(self):
        super().setUp()
        self.assertApiLogin(Users.USER1)

    def test_can_not_close_outbound_of_non_existed_work(self):
        self.assertApiPut(1, url_suffix='/close-outbound',
                          expected_status_codes=404)

    def test_can_close_outbound_once(self):
        self.assertApiPost(data=Works.WORK1, expected_data=Works.WORK1)
        self.assertApiPut(1, url_suffix='/close-outbound',
                          expected_data=Works.WORK1_OUTBOUND_CLOSED)

    def test_can_not_close_outbound_twice(self):
        self.assertApiPost(data=Works.WORK1, expected_data=Works.WORK1)
        self.assertApiPut(1, url_suffix='/close-outbound')
        self.assertApiPut(1, url_suffix='/close-outbound',
                          expected_data={'message': 'Outbound items have been closed.'},
                          expected_status_codes=422)


class TesCloseReturnedOfWorkWithoutWorkItems(CommonSessionTest):
    ENDPOINT = '/works'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
        ('/customers', [Customers.CUSTOMER1]),
    ]

    def setUp(self):
        super().setUp()
        self.assertApiLogin(Users.USER1)

    def test_can_not_close_returned_of_non_existed_work(self):
        self.assertApiPut(1, url_suffix='/close-returned',
                          expected_status_codes=404)

    def test_can_not_close_returned_before_not_closed_outbound_of_work(self):
        self.assertApiPost(data=Works.WORK1, expected_data=Works.WORK1)
        self.assertApiPut(1, url_suffix='/close-returned',
                          expected_data={'message': 'Outbound items have not been closed.'},
                          expected_status_codes=422)

    def test_can_close_returned_once(self):
        self.assertApiPost(data=Works.WORK1, expected_data=Works.WORK1)
        self.assertApiPut(1, url_suffix='/close-outbound')
        self.assertApiPut(1, url_suffix='/close-returned',
                          expected_data=Works.WORK1_RETURNED_CLOSED)

    def test_can_not_close_returned_twice(self):
        self.assertApiPost(data=Works.WORK1, expected_data=Works.WORK1)
        self.assertApiPut(1, url_suffix='/close-outbound')
        self.assertApiPut(1, url_suffix='/close-returned')
        self.assertApiPut(1, url_suffix='/close-returned',
                          expected_data={'message': 'Returned items have been closed.'},
                          expected_status_codes=422)


@append_mandatory_field_tests(item_name='work_item', base_item=WorkItems.ITEM1,
                              mandatory_fields=['item', 'outbound_quantity'])
class TestWorkItemWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/works/1/items'
    BAD_ENDPOINT = '/works/2/items'
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_adding_new_work_items(self):
        self.assertApiPost(data=WorkItems.ITEM1, expected_data=WorkItems.ITEM1)
        self.assertApiPost(data=WorkItems.ITEM2, expected_data=WorkItems.ITEM2)

    def test_can_not_adding_new_item_to_a_non_existed_work(self):
        self.assertApiPost(data=WorkItems.ITEM1, endpoint=self.BAD_ENDPOINT,
                           expected_status_codes=404)

    def test_can_add_work_item_with_minimal_quantities(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'outbound_quantity': 1}))
        self.assertApiPost(data=WorkItems.ITEM2.set(change={'returned_quantity': 0}))

    def test_can_not_add_work_item_with_zero_outbound_quantity(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'outbound_quantity': 0}), expected_status_codes=422)

    def test_can_not_add_work_item_with_lower_than_zero_returned_quantity(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'returned_quantity': -1}), expected_status_codes=422)

    def test_can_add_work_item_with_more_returned_quantity_than_outbound_quantity(self):
        self.assertApiPost(data=WorkItems.ITEM1.set(change={'outbound_quantity': 1, 'returned_quantity': 3}))

    def test_can_not_add_more_than_once_an_item_to_a_work(self):
        self.assertApiPost(data=WorkItems.ITEM1)
        self.assertApiPost(data=WorkItems.ITEM2.set(change={'item': WorkItems.ITEM1['item']}),
                           expected_data={'message': {'item_id, work_id': ['Already exists.']}},
                           expected_status_codes=422)


class TestWorkItemWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/works/1/items'
    BAD_ENDPOINT = '/works/2/items'
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2, Items.ITEM3]),
        (ENDPOINT, [WorkItems.ITEM1, WorkItems.ITEM2]),
    ]

    def test_list_work_items(self):
        self.assertApiGet(expected_data=[WorkItems.ITEM1,
                                         WorkItems.ITEM2])

    def test_can_not_list_work_items_of_a_non_existed_work(self):
        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_get_work_item(self):
        self.assertApiGet(2, expected_data=WorkItems.ITEM2)
        self.assertApiGet(1, expected_data=WorkItems.ITEM1)

    def test_can_not_get_work_item_of_a_non_existed_work(self):
        self.assertApiGet(1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_remove_work_item(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[WorkItems.ITEM2])

    def test_can_not_remove_work_item_of_a_non_existed_work(self):
        self.assertApiDelete(1, endpoint=self.BAD_ENDPOINT,
                             expected_status_codes=404)

    def test_can_not_remove_non_existed_work_item(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[WorkItems.ITEM1,
                                         WorkItems.ITEM2])

    def test_update_work_item(self):
        request = WorkItems.ITEM2.set(change={'item': Items.ITEM3.get(),
                                              'outbound_quantity': 8,
                                              'returned_quantity': 8})
        response = WorkItems.ITEM2.get(change={'item': request['item'],
                                               'outbound_quantity': request['outbound_quantity'],
                                               'returned_quantity': request['returned_quantity']})

        self.assertApiPut(WorkItems.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[WorkItems.ITEM1, response])

    def test_can_not_update_work_item_of_a_non_existed_work(self):
        self.assertApiPut(WorkItems.ITEM1['id'], data=WorkItems.ITEM1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)


class TesCloseOutboundOfWorkWithWorkItems(CommonSessionTestWithItemManipulation):
    ENDPOINT = '/works/1/items'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [WorkItems.ITEM1, WorkItems.ITEM2]),
    ]

    def setUp(self):
        super().setUp()
        self.assertApiLogin(Users.USER1)

    def test_can_not_close_outbound_with_insufficient_item_quantities(self):
        self.assertApiPut(Works.WORK1['id'], endpoint='/works', url_suffix='/close-outbound',
                          expected_data={'message': 'insufficient quantities for close the outbound work items: '
                                                    '\'Spray\': 0.0 - 41.2, \'Pipe\': 0.0 - 132.8'
                                         },
                          expected_status_codes=422)

        self.assertApiGet(Works.WORK1['id'], endpoint='/works', expected_data=Works.WORK1)
        self.assertApiGet(expected_data=[
            WorkItems.ITEM1,
            WorkItems.ITEM2,
        ])

    def test_can_not_close_outbound_with_one_insufficient_item_quantity(self):
        self._set_item_quantity({'item_id': WorkItems.ITEM1['item']['id'], 'quantity': 1000.0})

        self.assertApiPut(Works.WORK1['id'], endpoint='/works', url_suffix='/close-outbound',
                          expected_data={'message': 'insufficient quantities for close the outbound work items: '
                                                    '\'Spray\': 0.0 - 41.2'
                                         },
                          expected_status_codes=422)

        self.assertApiGet(Works.WORK1['id'], endpoint='/works', expected_data=Works.WORK1)
        self.assertApiGet(expected_data=[
            WorkItems.ITEM1.get(change={'item': {'quantity': 1000.0}}),
            WorkItems.ITEM2,
        ])

    def test_can_close_outbound_with_enough_item_quantities(self):
        self._set_item_quantity(
            {'item_id': WorkItems.ITEM1['item']['id'], 'quantity': 1000.0},
            {'item_id': WorkItems.ITEM2['item']['id'], 'quantity': 1000.0},
        )

        self.assertApiPut(Works.WORK1['id'], endpoint='/works', url_suffix='/close-outbound')
        self.assertApiGet(Works.WORK1['id'], endpoint='/works', expected_data=Works.WORK1_OUTBOUND_CLOSED)
        self.assertApiGet(expected_data=[
            WorkItems.ITEM1.get(change={'item': {'quantity': 1000.0 - WorkItems.ITEM1['outbound_quantity']}}),
            WorkItems.ITEM2.get(change={'item': {'quantity': 1000.0 - WorkItems.ITEM2['outbound_quantity']}}),
        ])

    def test_can_close_outbound_with_just_enough_item_quantities(self):
        self._set_item_quantity(
            {'item_id': WorkItems.ITEM1['item']['id'], 'quantity': WorkItems.ITEM1['outbound_quantity']},
            {'item_id': WorkItems.ITEM2['item']['id'], 'quantity': WorkItems.ITEM2['outbound_quantity']},
        )

        self.assertApiPut(Works.WORK1['id'], endpoint='/works', url_suffix='/close-outbound')
        self.assertApiGet(Works.WORK1['id'], endpoint='/works', expected_data=Works.WORK1_OUTBOUND_CLOSED)
        self.assertApiGet(expected_data=[
            WorkItems.ITEM1.get(change={'item': {'quantity': 0.0}}),
            WorkItems.ITEM2.get(change={'item': {'quantity': 0.0}}),
        ])


class TesCloseReturnedOfWorkWithWorkItems(CommonSessionTestWithItemManipulation):
    ENDPOINT = '/works/1/items'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [WorkItems.ITEM1, WorkItems.ITEM2]),
    ]

    def setUp(self):
        super().setUp()
        # set just enough item quantity for closing outbound
        self._set_item_quantity(
            {'item_id': WorkItems.ITEM1['item']['id'], 'quantity': WorkItems.ITEM1['outbound_quantity']},
            {'item_id': WorkItems.ITEM2['item']['id'], 'quantity': WorkItems.ITEM2['outbound_quantity']},
        )
        self.assertApiLogin(Users.USER1)
        self.assertApiPut(Works.WORK1['id'], endpoint='/works', url_suffix='/close-outbound')

    def test_can_close_returned_item_quantities(self):
        self.assertApiPut(WorkItems.ITEM1['id'], data=WorkItems.ITEM1.set(change={'returned_quantity': 4.4}))
        self.assertApiPut(WorkItems.ITEM2['id'], data=WorkItems.ITEM2.set(change={'returned_quantity': 9.9}))

        self.assertApiPut(Works.WORK1_OUTBOUND_CLOSED['id'], endpoint='/works', url_suffix='/close-returned')

        self.assertApiGet(Works.WORK1_OUTBOUND_CLOSED['id'], endpoint='/works',
                          expected_data=Works.WORK1_RETURNED_CLOSED)
        self.assertApiGet(expected_data=[
            WorkItems.ITEM1.get(change={'item': {'quantity': 4.4}, 'returned_quantity': 4.4}),
            WorkItems.ITEM2.get(change={'item': {'quantity': 9.9}, 'returned_quantity': 9.9}),
        ])

    def test_can_close_returned_with_zero_and_none_item_quantities(self):
        # WorkItems.ITEM1 has returned_quantity=None
        self.assertApiPut(WorkItems.ITEM2['id'], data=WorkItems.ITEM2.set(change={'returned_quantity': 0.0}))

        self.assertApiPut(Works.WORK1_OUTBOUND_CLOSED['id'], endpoint='/works', url_suffix='/close-returned')

        self.assertApiGet(Works.WORK1_OUTBOUND_CLOSED['id'], endpoint='/works',
                          expected_data=Works.WORK1_RETURNED_CLOSED)
        self.assertApiGet(expected_data=[
            WorkItems.ITEM1.get(change={'item': {'quantity': 0.0}, 'returned_quantity': 0.0}),
            WorkItems.ITEM2.get(change={'item': {'quantity': 0.0}, 'returned_quantity': 0.0}),
        ])


class TestWorkItemWithClosedOutbound(CommonSessionTestWithItemManipulation):
    ENDPOINT = '/works/1/items'
    BAD_ENDPOINT = '/works/2/items'
    INIT_PUSH = [
        ('/users', [Users.USER1]),
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [WorkItems.ITEM1]),
    ]

    def setUp(self):
        super().setUp()
        self._set_item_quantity({'item_id': WorkItems.ITEM1.get()['item']['id'], 'quantity': 1000.0})
        self.assertApiLogin(Users.USER1)
        self.assertApiPut(Works.WORK1['id'], endpoint='/works', url_suffix='/close-outbound')

    def test_can_not_add_new_work_item_after_outbound_items_are_closed(self):
        self.assertApiPost(data=WorkItems.ITEM2.set(change={'work': Works.WORK1.get()}),
                           expected_data={'message': 'Can not add new item.'}, expected_status_codes=403)

    def test_can_not_change_outbound_work_item_after_outbound_items_are_closed(self):
        request = WorkItems.ITEM1.set(change={'item': Items.ITEM1.get()})
        self.assertApiPut(1, data=request,
                          expected_data={'message': 'Work item was closed.'}, expected_status_codes=403)

        request = WorkItems.ITEM1.set(change={'outbound_quantity': WorkItems.ITEM1['outbound_quantity'] + 1})
        self.assertApiPut(1, data=request,
                          expected_data={'message': 'Work item was closed.'}, expected_status_codes=403)

    def test_can_not_delete_work_item_after_outbound_items_are_closed(self):
        self.assertApiDelete(1,
                             expected_data={'message': 'Can not delete item.'}, expected_status_codes=403)
