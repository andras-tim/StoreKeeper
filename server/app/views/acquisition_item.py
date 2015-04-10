from app.models import AcquisitionItem
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleAcquisitionItems
from app.serializers import AcquisitionItemSerializer
from app.server import config, api
from app.views.common import api_func


class AcquisitionItemListView(BaseModelListView):
    _model = AcquisitionItem
    _serializer = AcquisitionItemSerializer
    _deserializer = AcquisitionItemSerializer

    @api_func('List acquisition items', url_tail='acquisition-items',
              response=[ExampleAcquisitionItems.ITEM1.get(), ExampleAcquisitionItems.ITEM2.get()])
    def get(self):
        return self._get()

    @api_func('Create acquisition item', url_tail='acquisition-items',
              request=ExampleAcquisitionItems.ITEM1.set(),
              response=ExampleAcquisitionItems.ITEM1.get(),
              status_codes={422: 'there is wrong type / missing field'})
    def post(self):
        return self._post()


class AcquisitionItemView(BaseView):
    _model = AcquisitionItem
    _serializer = AcquisitionItemSerializer
    _deserializer = AcquisitionItemSerializer

    @api_func('Get acquisition item', url_tail='acquisition-items/1',
              response=ExampleAcquisitionItems.ITEM1.get(),
              queries={'id': 'ID of selected acquisition item for change'},
              status_codes={404: 'there is no item'})
    def get(self, id: int):
        return self._get(id)

    @api_func('Update acquisition item', url_tail='acquisition-items/1',
              request=ExampleAcquisitionItems.ITEM1.set(),
              response=ExampleAcquisitionItems.ITEM1.get(),
              queries={'id': 'ID of selected acquisition item for change'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete acquisition item', url_tail='acquisition-items/1',
              response=None,
              queries={'id': 'ID of selected acquisition item for change'},
              status_codes={404: 'there is no item'})
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(AcquisitionItemListView, '/{!s}/api/acquisition-items'.format(config.App.NAME),
                 endpoint='acquisition_items')
api.add_resource(AcquisitionItemView, '/{!s}/api/acquisition-items/<int:id>'.format(config.App.NAME),
                 endpoint='acquisition_item')
