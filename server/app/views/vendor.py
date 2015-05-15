from app.models import Vendor
from app.views.base_views import BaseListView, BaseView
from app.modules.example_data import ExampleVendors
from app.serializers import VendorSerializer, VendorDeserializer
from app.views.common import api_func


class VendorListView(BaseListView):
    _model = Vendor
    _serializer = VendorSerializer()
    _deserializer = VendorDeserializer()

    @api_func('List vendors', url_tail='/vendors',
              response=[ExampleVendors.VENDOR1.get(), ExampleVendors.VENDOR2.get()])
    def get(self):
        return self._get()

    @api_func('Create vendor', url_tail='/vendors',
              request=ExampleVendors.VENDOR1.set(),
              response=ExampleVendors.VENDOR1.get(),
              status_codes={422: '{original} / vendor is already exist'})
    def post(self):
        return self._post()


class VendorView(BaseView):
    _model = Vendor
    _serializer = VendorSerializer()
    _deserializer = VendorDeserializer()

    @api_func('Get vendor', item_name='vendor', url_tail='/vendors/1',
              response=ExampleVendors.VENDOR1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update vendor', item_name='vendor', url_tail='/vendors/1',
              request=ExampleVendors.VENDOR1.set(change={'name': 'new_foo'}),
              response=ExampleVendors.VENDOR1.get(change={'name': 'new_foo'}),
              status_codes={422: '{original} / vendor is already exist'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete vendor', item_name='vendor', url_tail='/vendors/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)
