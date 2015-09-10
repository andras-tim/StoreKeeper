from app.models import Stocktaking, StocktakingItem
from app.views.base_views import BaseListView, BaseView, BaseNestedListView, BaseNestedView
from app.modules.example_data import ExampleStocktakings, ExampleStocktakingItems
from app.serializers import StocktakingSerializer, StocktakingDeserializer, StocktakingItemSerializer, \
    StocktakingItemDeserializer
from app.views.common import api_func


class StocktakingListView(BaseListView):
    _model = Stocktaking
    _serializer = StocktakingSerializer()
    _deserializer = StocktakingDeserializer()

    @api_func('List stocktakings', url_tail='/stocktakings',
              response=[ExampleStocktakings.STOCKTAKING1.get(), ExampleStocktakings.STOCKTAKING2.get()])
    def get(self):
        return self._get()

    @api_func('Create stocktaking', url_tail='/stocktakings',
              request=ExampleStocktakings.STOCKTAKING1.set(),
              response=ExampleStocktakings.STOCKTAKING1.get())
    def post(self):
        return self._post()


class StocktakingView(BaseView):
    _model = Stocktaking
    _serializer = StocktakingSerializer()
    _deserializer = StocktakingDeserializer()

    @api_func('Get stocktaking', item_name='stocktaking', url_tail='/stocktakings/1',
              response=ExampleStocktakings.STOCKTAKING1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update stocktaking', item_name='stocktaking', url_tail='/stocktakings/1',
              request=ExampleStocktakings.STOCKTAKING1.set(change={'comment': 'A box has been damaged'}),
              response=ExampleStocktakings.STOCKTAKING1.get(change={'comment': 'A box has been damaged'}))
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete stocktaking', item_name='stocktaking', url_tail='/stocktakings/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)


class StocktakingItemListView(BaseNestedListView):
    _model = StocktakingItem
    _parent_model = Stocktaking
    _serializer = StocktakingItemSerializer()
    _deserializer = StocktakingItemDeserializer()

    @api_func('List stocktaking items.', url_tail='/stocktakings/1/items',
              response=[ExampleStocktakingItems.ITEM1.get(), ExampleStocktakingItems.ITEM2.get()],
              queries={'id': 'ID of stocktaking'})
    def get(self, id: int):
        self._initialize_parent_item(id)
        return self._get(stocktaking_id=id)

    @api_func('Create stocktaking item', url_tail='/stocktakings/1/items',
              request=ExampleStocktakingItems.ITEM1.set(),
              response=ExampleStocktakingItems.ITEM1.get(),
              status_codes={422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of stocktaking'})
    def post(self, id: int):
        self._initialize_parent_item(id)
        return self._post(stocktaking_id=id)


class StocktakingItemView(BaseNestedView):
    _model = StocktakingItem
    _parent_model = Stocktaking
    _serializer = StocktakingItemSerializer()
    _deserializer = StocktakingItemDeserializer()

    @api_func('Get stocktaking item', item_name='stocktaking item', url_tail='/stocktakings/1/items/1',
              response=ExampleStocktakingItems.ITEM1.get(),
              queries={'id': 'ID of stocktaking',
                       'item_id': 'ID of selected stocktaking item for get'})
    def get(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        return self._get(stocktaking_id=id, id=item_id)

    @api_func('Update stocktaking item', item_name='stocktaking item', url_tail='/stocktakings/1/items/1',
              request=ExampleStocktakingItems.ITEM1.set(),
              response=ExampleStocktakingItems.ITEM1.get(),
              status_codes={422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of stocktaking',
                       'item_id': 'ID of selected stocktaking item for put'})
    def put(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        return self._put(stocktaking_id=id, id=item_id)

    @api_func('Delete stocktaking item', item_name='stocktaking item', url_tail='/stocktakings/1/items/1',
              response=None,
              queries={'id': 'ID of stocktaking',
                       'item_id': 'ID of selected stocktaking item for delete'})
    def delete(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        return self._delete(stocktaking_id=id, id=item_id)
