from app.models import Acquisition, AcquisitionItem
from app.views.base_views import BaseView
from app.modules.example_data import ExampleAcquisitions, ExampleAcquisitionItems
from app.serializers import AcquisitionSerializer, AcquisitionDeserializer, AcquisitionItemSerializer, \
    AcquisitionItemDeserializer
from app.views.common import api_func


class AcquisitionListView(BaseView):
    _model = Acquisition
    _serializer = AcquisitionSerializer()
    _deserializer = AcquisitionDeserializer()

    @api_func('List acquisitions', url_tail='/acquisitions',
              response=[ExampleAcquisitions.ACQUISITION1.get(), ExampleAcquisitions.ACQUISITION2.get()])
    def get(self):
        return self._get_list()

    @api_func('Create acquisition', url_tail='/acquisitions',
              request=ExampleAcquisitions.ACQUISITION1.set(),
              response=ExampleAcquisitions.ACQUISITION1.get())
    def post(self):
        return self._post()


class AcquisitionView(BaseView):
    _model = Acquisition
    _serializer = AcquisitionSerializer()
    _deserializer = AcquisitionDeserializer()

    @api_func('Get acquisition', item_name='acquisition', url_tail='/acquisitions/1',
              response=ExampleAcquisitions.ACQUISITION1.get())
    def get(self, id: int):
        return self._get(id=id)

    @api_func('Update acquisition', item_name='acquisition', url_tail='/acquisitions/1',
              request=ExampleAcquisitions.ACQUISITION1.set(change={'comment': 'A box has been damaged'}),
              response=ExampleAcquisitions.ACQUISITION1.get(change={'comment': 'A box has been damaged'}))
    def put(self, id: int):
        return self._put(id=id)

    @api_func('Delete acquisition', item_name='acquisition', url_tail='/acquisitions/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id=id)


class AcquisitionItemListView(BaseView):
    _model = AcquisitionItem
    _parent_model = Acquisition
    _serializer = AcquisitionItemSerializer()
    _deserializer = AcquisitionItemDeserializer()

    @api_func('List acquisition items', url_tail='/acquisitions/1/items',
              response=[ExampleAcquisitionItems.ITEM1.get(), ExampleAcquisitionItems.ITEM2.get()],
              queries={'id': 'ID of acquisition'})
    def get(self, id: int):
        self._initialize_parent_model_object(id)
        return self._get_list(acquisition_id=id)

    @api_func('Create acquisition item', url_tail='/acquisitions/1/items',
              request=ExampleAcquisitionItems.ITEM1.set(),
              response=ExampleAcquisitionItems.ITEM1.get(),
              status_codes={422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of acquisition'})
    def post(self, id: int):
        self._initialize_parent_model_object(id)
        return self._post(acquisition_id=id)


class AcquisitionItemView(BaseView):
    _model = AcquisitionItem
    _parent_model = Acquisition
    _serializer = AcquisitionItemSerializer()
    _deserializer = AcquisitionItemDeserializer()

    @api_func('Get acquisition item', item_name='acquisition item', url_tail='/acquisitions/1/items/1',
              response=ExampleAcquisitionItems.ITEM1.get(),
              queries={'id': 'ID of acquisition',
                       'item_id': 'ID of selected acquisition item for get'})
    def get(self, id: int, item_id: int):
        self._initialize_parent_model_object(id)
        return self._get(acquisition_id=id, id=item_id)

    @api_func('Update acquisition item', item_name='acquisition item', url_tail='/acquisitions/1/items/1',
              request=ExampleAcquisitionItems.ITEM1.set(),
              response=ExampleAcquisitionItems.ITEM1.get(),
              status_codes={422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of acquisition',
                       'item_id': 'ID of selected acquisition item for get'})
    def put(self, id: int, item_id: int):
        self._initialize_parent_model_object(id)
        return self._put(acquisition_id=id, id=item_id)

    @api_func('Delete acquisition item', item_name='acquisition item', url_tail='/acquisitions/1/items/1',
              response=None,
              queries={'id': 'ID of acquisition',
                       'item_id': 'ID of selected acquisition item for get'})
    def delete(self, id: int, item_id: int):
        self._initialize_parent_model_object(id)
        return self._delete(acquisition_id=id, id=item_id)
