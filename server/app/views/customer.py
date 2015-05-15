from app.models import Customer
from app.views.base_views import BaseListView, BaseView
from app.modules.example_data import ExampleCustomers
from app.serializers import CustomerSerializer, CustomerDeserializer
from app.views.common import api_func


class CustomerListView(BaseListView):
    _model = Customer
    _serializer = CustomerSerializer()
    _deserializer = CustomerDeserializer()

    @api_func('List customers', url_tail='/customers',
              response=[ExampleCustomers.CUSTOMER1.get(), ExampleCustomers.CUSTOMER2.get()])
    def get(self):
        return self._get()

    @api_func('Create customer', url_tail='/customers',
              request=ExampleCustomers.CUSTOMER1.set(),
              response=ExampleCustomers.CUSTOMER1.get(),
              status_codes={422: '{{ original }} / customer is already exist'})
    def post(self):
        return self._post()


class CustomerView(BaseView):
    _model = Customer
    _serializer = CustomerSerializer()
    _deserializer = CustomerDeserializer()

    @api_func('Get customer', item_name='customer', url_tail='/customers/1',
              response=ExampleCustomers.CUSTOMER1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update customer', item_name='customer', url_tail='/customers/1',
              request=ExampleCustomers.CUSTOMER1.set(change={'name': 'new_foo'}),
              response=ExampleCustomers.CUSTOMER1.get(change={'name': 'new_foo'}),
              status_codes={422: '{{ original }} / customer is already exist'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete customer', item_name='customer', url_tail='/customers/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)
