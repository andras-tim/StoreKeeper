from app.modules.example_data import ExampleStocktakings as Stocktakings
from test.views.base_api_test import CommonApiTest


class TestStocktakingWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/stocktakings'

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_stocktakings(self):
        self.assertApiPost(data=Stocktakings.STOCKTAKING1, expected_data=Stocktakings.STOCKTAKING1)
        self.assertApiPost(data=Stocktakings.STOCKTAKING2, expected_data=Stocktakings.STOCKTAKING2)

    def test_can_add_stocktaking_with_same_comment(self):
        self.assertApiPost(data=Stocktakings.STOCKTAKING1)
        self.assertApiPost(data=Stocktakings.STOCKTAKING2.set(
            change={'comment': Stocktakings.STOCKTAKING1['comment']}))


class TestUserWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/stocktakings'
    INIT_PUSH = [
        (ENDPOINT, [Stocktakings.STOCKTAKING1, Stocktakings.STOCKTAKING2])
    ]

    def test_list_stocktakings(self):
        self.assertApiGet(expected_data=[Stocktakings.STOCKTAKING1,
                                         Stocktakings.STOCKTAKING2])

    def test_get_stocktaking(self):
        self.assertApiGet(2, expected_data=Stocktakings.STOCKTAKING2)
        self.assertApiGet(1, expected_data=Stocktakings.STOCKTAKING1)

    def test_remove_stocktaking(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Stocktakings.STOCKTAKING2.get()])

    def test_can_not_remove_non_existed_stocktaking(self):
        self.assertApiDelete(3, expected_status_codes=404)
        self.assertApiGet(expected_data=[Stocktakings.STOCKTAKING1,
                                         Stocktakings.STOCKTAKING2])

    def test_update_stocktaking(self):
        request = Stocktakings.STOCKTAKING2.set(change={'comment': 'A box has been damaged'})
        response = Stocktakings.STOCKTAKING2.get(change={'comment': request['comment']})

        self.assertApiPut(Stocktakings.STOCKTAKING2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Stocktakings.STOCKTAKING1,
                                         response])

    def test_update_name_to_name_of_another_stocktaking(self):
        request = Stocktakings.STOCKTAKING2.set(change={'comment': Stocktakings.STOCKTAKING1['comment']})

        self.assertApiPut(Stocktakings.STOCKTAKING2['id'], data=request)
