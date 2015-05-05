from app.modules.example_data import ExampleStocktakingItems as StocktakingItems, ExampleStocktakings as Stocktakings, \
    ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


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


@append_mandatory_field_tests(item_name='stocktaking_item', base_item=StocktakingItems.ITEM1,
                              mandatory_fields=['item', 'quantity'])
class TestStocktakingItemWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/stocktakings/1/items'
    BAD_ENDPOINT = '/stocktakings/2/items'
    INIT_PUSH = [
        ('/stocktakings', [Stocktakings.STOCKTAKING1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_adding_new_stocktaking_items(self):
        self.assertApiPost(data=StocktakingItems.ITEM1, expected_data=StocktakingItems.ITEM1)
        self.assertApiPost(data=StocktakingItems.ITEM2, expected_data=StocktakingItems.ITEM2)

    def test_can_not_adding_new_item_to_a_non_existed_stocktaking(self):
        self.assertApiPost(data=StocktakingItems.ITEM1, endpoint=self.BAD_ENDPOINT,
                           expected_status_codes=404)

    def test_can_add_stocktaking_item_with_negative_and_zero_quantity(self):
        self.assertApiPost(data=StocktakingItems.ITEM1.set(change={'quantity': -1}))
        self.assertApiPost(data=StocktakingItems.ITEM2.set(change={'quantity': 0}))

    def test_can_not_add_more_than_once_an_item_to_a_stocktaking(self):
        self.assertApiPost(data=StocktakingItems.ITEM1)
        self.assertApiPost(data=StocktakingItems.ITEM2.set(change={'item': StocktakingItems.ITEM1['item']}),
                           expected_data={'message': {'item_id, stocktaking_id': ['Already exists.']}},
                           expected_status_codes=422)


class TestStocktakingItemWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/stocktakings/1/items'
    BAD_ENDPOINT = '/stocktakings/2/items'
    INIT_PUSH = [
        ('/stocktakings', [Stocktakings.STOCKTAKING1]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2, Items.ITEM3]),
        (ENDPOINT, [StocktakingItems.ITEM1, StocktakingItems.ITEM2]),
    ]

    def test_list_stocktaking_items(self):
        self.assertApiGet(expected_data=[StocktakingItems.ITEM1,
                                         StocktakingItems.ITEM2])

    def test_can_not_list_stocktaking_items_of_a_non_existed_stocktaking(self):
        self.assertApiGet(endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_get_stocktaking_item(self):
        self.assertApiGet(2, expected_data=StocktakingItems.ITEM2)
        self.assertApiGet(1, expected_data=StocktakingItems.ITEM1)

    def test_can_not_get_stocktaking_item_of_a_non_existed_stocktaking(self):
        self.assertApiGet(1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)

    def test_remove_stocktaking_item(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[StocktakingItems.ITEM2])

    def test_can_not_remove_stocktaking_item_of_a_non_existed_stocktaking(self):
        self.assertApiDelete(1, endpoint=self.BAD_ENDPOINT,
                             expected_status_codes=404)

    def test_can_not_remove_non_existed_stocktaking_item(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[StocktakingItems.ITEM1,
                                         StocktakingItems.ITEM2])

    def test_update_stocktaking_item(self):
        request = StocktakingItems.ITEM2.set(change={'item': Items.ITEM3.get(), 'quantity': 1})
        response = StocktakingItems.ITEM2.get(change={'item': request['item'], 'quantity': request['quantity']})

        self.assertApiPut(StocktakingItems.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[StocktakingItems.ITEM1, response])

    def test_can_not_update_stocktaking_item_of_a_non_existed_stocktaking(self):
        self.assertApiPut(StocktakingItems.ITEM1['id'], data=StocktakingItems.ITEM1, endpoint=self.BAD_ENDPOINT,
                          expected_status_codes=404)
