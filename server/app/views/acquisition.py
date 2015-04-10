from app.models import Acquisition
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleAcquisitions
from app.serializers import AcquisitionSerializer, AcquisitionDeserializer
from app.server import config, api
from app.views.common import api_func


class AcquisitionModelListView(BaseModelListView):
    _model = Acquisition
    _serializer = AcquisitionSerializer
    _deserializer = AcquisitionDeserializer

    @api_func('List acquisitions', url_tail='acquisitions',
              response=[ExampleAcquisitions.ACQUISITION1.get(), ExampleAcquisitions.ACQUISITION2.get()])
    def get(self):
        return self._get()

    @api_func('Create acquisition', url_tail='acquisitions',
              request=ExampleAcquisitions.ACQUISITION1.set(),
              response=ExampleAcquisitions.ACQUISITION1.get(),
              status_codes={422: 'there is wrong type / missing field'})
    def post(self):
        return self._post()


class AcquisitionView(BaseView):
    _model = Acquisition
    _serializer = AcquisitionSerializer
    _deserializer = AcquisitionDeserializer

    @api_func('Get acquisition', url_tail='acquisitions/1',
              response=ExampleAcquisitions.ACQUISITION1.get(),
              queries={'id': 'ID of selected acquisition for change'},
              status_codes={404: 'there is no acquisition'})
    def get(self, id: int):
        return self._get(id)

    @api_func('Update acquisition', url_tail='acquisitions/1',
              request=ExampleAcquisitions.ACQUISITION1.set(change={'comment': 'A box has been damaged'}),
              response=ExampleAcquisitions.ACQUISITION1.get(change={'comment': 'A box has been damaged'}),
              queries={'id': 'ID of selected acquisition for change'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete acquisition', url_tail='acquisitions/1',
              response=None,
              queries={'id': 'ID of selected acquisition for change'},
              status_codes={404: 'there is no acquisition'})
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(AcquisitionModelListView, '/%s/api/acquisitions' % config.App.NAME, endpoint='acquisitions')
api.add_resource(AcquisitionView, '/%s/api/acquisitions/<int:id>' % config.App.NAME, endpoint='acquisition')
