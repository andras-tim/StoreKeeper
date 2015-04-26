from app.models import Acquisition
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleAcquisitions
from app.serializers import AcquisitionSerializer, AcquisitionDeserializer
from app.views.common import api_func


class AcquisitionListView(BaseModelListView):
    _model = Acquisition
    _serializer = AcquisitionSerializer
    _deserializer = AcquisitionDeserializer

    @api_func('List acquisitions', url_tail='acquisitions',
              response=[ExampleAcquisitions.ACQUISITION1.get(), ExampleAcquisitions.ACQUISITION2.get()])
    def get(self):
        return self._get()

    @api_func('Create acquisition', url_tail='acquisitions',
              request=ExampleAcquisitions.ACQUISITION1.set(),
              response=ExampleAcquisitions.ACQUISITION1.get())
    def post(self):
        return self._post()


class AcquisitionView(BaseView):
    _model = Acquisition
    _serializer = AcquisitionSerializer
    _deserializer = AcquisitionDeserializer

    @api_func('Get acquisition', item_name='acquisition', url_tail='acquisitions/1',
              response=ExampleAcquisitions.ACQUISITION1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update acquisition', item_name='acquisition', url_tail='acquisitions/1',
              request=ExampleAcquisitions.ACQUISITION1.set(change={'comment': 'A box has been damaged'}),
              response=ExampleAcquisitions.ACQUISITION1.get(change={'comment': 'A box has been damaged'}))
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete acquisition', item_name='acquisition', url_tail='acquisitions/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)
