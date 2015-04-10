from app.models import Item
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleItems
from app.serializers import ItemSerializer
from app.server import config, api
from app.views.common import api_func


class ItemModelListView(BaseModelListView):
    _model = Item
    _serializer = ItemSerializer
    _deserializer = ItemSerializer

    @api_func('List items', url_tail='items',
              response=[ExampleItems.ITEM1.get(), ExampleItems.ITEM2.get()])
    def get(self):
        return self._get()

    @api_func('Create item', url_tail='items',
              request=ExampleItems.ITEM1.set(),
              response=ExampleItems.ITEM1.get(),
              status_codes={422: 'there is wrong type / missing field'})
    def post(self):
        return self._post()


class ItemView(BaseView):
    _model = Item
    _serializer = ItemSerializer
    _deserializer = ItemSerializer

    @api_func('Get item', url_tail='items/1',
              response=ExampleItems.ITEM1.get(),
              queries={'id': 'ID of selected item for change'},
              status_codes={404: 'there is no item'})
    def get(self, id: int):
        return self._get(id)

    @api_func('Update item', url_tail='items/1',
              request=ExampleItems.ITEM1.set(),
              response=ExampleItems.ITEM1.get(),
              queries={'id': 'ID of selected item for change'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete item', url_tail='items/1',
              response=None,
              queries={'id': 'ID of selected item for change'},
              status_codes={404: 'there is no item'})
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(ItemModelListView, '/{!s}/api/items'.format(config.App.NAME), endpoint='items')
api.add_resource(ItemView, '/{!s}/api/items/<int:id>'.format(config.App.NAME), endpoint='item')
