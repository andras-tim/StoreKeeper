from app.modules.example_data import ExampleStocktakings as Stocktakings
from test.views import CommonApiTest


class TestStocktakingWithBrandNewDb(CommonApiTest):
    def test_new_db(self):
        self.assertRequest("get", "/stocktakings", expected_data=[])
        self.assertRequest("get", "/stocktakings/1", expected_status_codes=404)

    def test_adding_new_stocktakings(self):
        self.assertRequest("post", "/stocktakings", data=Stocktakings.STOCKTAKING1.set(),
                           expected_data=Stocktakings.STOCKTAKING1.get())
        self.assertRequest("post", "/stocktakings", data=Stocktakings.STOCKTAKING2.set(),
                           expected_data=Stocktakings.STOCKTAKING2.get())

    def test_can_add_stocktaking_with_same_comment(self):
        self.assertRequest("post", "/stocktakings", data=Stocktakings.STOCKTAKING1.set())
        self.assertRequest("post", "/stocktakings", data=Stocktakings.STOCKTAKING2.set(
            change={"comment": Stocktakings.STOCKTAKING1["comment"]}))


class TestUserWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/stocktakings", data=Stocktakings.STOCKTAKING1.set())
        self.assertRequest("post", "/stocktakings", data=Stocktakings.STOCKTAKING2.set())

    def test_list_stocktakings(self):
        self.assertRequest("get", "/stocktakings", expected_data=[Stocktakings.STOCKTAKING1.get(),
                                                                  Stocktakings.STOCKTAKING2.get()])

    def test_get_stocktaking(self):
        self.assertRequest("get", "/stocktakings/2", expected_data=Stocktakings.STOCKTAKING2.get())
        self.assertRequest("get", "/stocktakings/1", expected_data=Stocktakings.STOCKTAKING1.get())

    def test_remove_stocktaking(self):
        self.assertRequest("delete", "/stocktakings/1")
        self.assertRequest("get", "/stocktakings", expected_data=[Stocktakings.STOCKTAKING2.get()])

    def test_can_not_remove_non_existed_stocktaking(self):
        self.assertRequest("delete", "/stocktakings/3", expected_status_codes=404)
        self.assertRequest("get", "/stocktakings", expected_data=[Stocktakings.STOCKTAKING1.get(),
                                                                  Stocktakings.STOCKTAKING2.get()])

    def test_update_stocktaking(self):
        request = Stocktakings.STOCKTAKING2.set(change={"comment": "A box has been damaged"})
        response = Stocktakings.STOCKTAKING2.get(change={"comment": request["comment"]})

        self.assertRequest("put", "/stocktakings/%d" % Stocktakings.STOCKTAKING2["id"], data=request,
                           expected_data=response)
        self.assertRequest("get", "/stocktakings", expected_data=[Stocktakings.STOCKTAKING1.get(), response])

    def test_update_name_to_name_of_another_stocktaking(self):
        request = Stocktakings.STOCKTAKING2.set(change={"comment": Stocktakings.STOCKTAKING1["comment"]})

        self.assertRequest("put", "/stocktakings/%d" % Stocktakings.STOCKTAKING2["id"], data=request)
