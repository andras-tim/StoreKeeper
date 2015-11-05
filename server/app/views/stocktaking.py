from flask.ext.restful import abort

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
              status_codes={403: 'can not add new stocktakings item after items was closed',
                            422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of stocktaking'})
    def post(self, id: int):
        stocktaking = self._initialize_parent_item(id)
        item = self._post_populate(stocktaking_id=id)

        if stocktaking.are_items_frozen():
            abort(403, message='Can not add new item.')

        return self._post_commit(item)


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
              status_codes={403: 'can not change work item after outbound/returned items was closed',
                            422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of stocktaking',
                       'item_id': 'ID of selected stocktaking item for put'})
    def put(self, id: int, item_id: int):
        stocktaking = self._initialize_parent_item(id)
        item = self._put_populate(stocktaking_id=id, id=item_id)

        if stocktaking.are_items_closed():
            abort(403, message='Stocktaking item was closed.')

        return self._put_commit(item)

    @api_func('Delete stocktaking item', item_name='stocktaking item', url_tail='/stocktakings/1/items/1',
              response=None,
              status_codes={403: 'can not delete stocktaking item after items was closed'},
              queries={'id': 'ID of stocktaking',
                       'item_id': 'ID of selected stocktaking item for delete'})
    def delete(self, id: int, item_id: int):
        stocktaking = self._initialize_parent_item(id)

        if stocktaking.are_items_frozen():
            abort(403, message='Can not delete item.')

        return self._delete(stocktaking_id=id, id=item_id)


class StocktakingCloseView(BaseView):
    _model = Stocktaking
    _serializer = StocktakingSerializer()
    _deserializer = StocktakingDeserializer()

    @api_func('Close items on stocktaking', item_name='stocktaking', url_tail='/stocktakings/1/close',
              response=ExampleStocktakings.STOCKTAKING1_CLOSED.get(),
              status_codes={422: '{{ original }} / items have been closed / '
                                 'insufficient quantities for close the stocktaking items'})
    def put(self, id: int):
        stocktaking = self._get_item_by_id(id)

        if stocktaking.are_items_closed():
            abort(422, message='Items have been closed.')

        stocktaking_items = StocktakingItem.query.filter_by(stocktaking_id=stocktaking.id).all()
        self._apply_item_changes(
            model_items=stocktaking_items,
            insufficient_quantity_error_message='insufficient quantities for close the stocktaking items',
            # FIXME: Have to enable when Work started to use and Stocktaking uses for stocktaking only
            # multiplier_for_sign=-1,
        )

        self._close_items(stocktaking.close_items)
        return self._put_commit(stocktaking)
