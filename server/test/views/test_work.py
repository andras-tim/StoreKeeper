from app.modules.example_data import ExampleWorks as Works, ExampleCustomers as Customers, ExampleUsers as Users
from test.views.base_api_test import CommonApiTest
from test.views.base_session_test import CommonSessionTest


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


class TesCloseOutboundOftWork(CommonSessionTest):
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


class TesCloseReturnedOftWork(CommonSessionTest):
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
