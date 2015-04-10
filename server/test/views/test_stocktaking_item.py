from app.modules.example_data import ExampleStocktakingItems as StocktakingItems, ExampleStocktakings as Stocktakings, \
    ExampleItems as Items, ExampleVendors as Vendors, ExampleUnits as Units
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='stocktaking_item', base_item=StocktakingItems.ITEM1,
                              mandatory_fields=['stocktaking', 'item', 'quantity'])
class TestStocktakingItemWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/stocktaking-items'
    INIT_PUSH = [
        ('/stocktakings', [Stocktakings.STOCKTAKING1, Stocktakings.STOCKTAKING2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
    ]

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_items(self):
        self.assertApiPost(data=StocktakingItems.ITEM1, expected_data=StocktakingItems.ITEM1)
        self.assertApiPost(data=StocktakingItems.ITEM2, expected_data=StocktakingItems.ITEM2)


class TestStocktakingItemWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/stocktaking-items'
    INIT_PUSH = [
        ('/stocktakings', [Stocktakings.STOCKTAKING1, Stocktakings.STOCKTAKING2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        (ENDPOINT, [StocktakingItems.ITEM1, StocktakingItems.ITEM2]),
    ]

    def test_list_stocktaking_items(self):
        self.assertApiGet(expected_data=[StocktakingItems.ITEM1,
                                         StocktakingItems.ITEM2])

    def test_get_stocktaking_item(self):
        self.assertApiGet(2, expected_data=StocktakingItems.ITEM2)
        self.assertApiGet(1, expected_data=StocktakingItems.ITEM1)

    def test_remove_stocktaking_item(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[StocktakingItems.ITEM2])

    def test_can_not_remove_non_existed_stocktaking_item(self):
        self.assertApiDelete(4, expected_status_codes=404)
        self.assertApiGet(expected_data=[StocktakingItems.ITEM1,
                                         StocktakingItems.ITEM2])

    def test_update_stocktaking_item(self):
        request = StocktakingItems.ITEM2.set(change={'stocktaking': Stocktakings.STOCKTAKING2.get(),
                                                     'item': Items.ITEM2.get(), 'quantity': 1})
        response = StocktakingItems.ITEM2.get(change={'stocktaking': request['stocktaking'], 'item': request['item'],
                                                      'quantity': request['quantity']})

        self.assertApiPut(StocktakingItems.ITEM2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[StocktakingItems.ITEM1, response])
