from app.models import Customer
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleCustomers
from app.serializers import CustomerSerializer, CustomerDeserializer
from app.server import config, api
from app.views.common import api_func


class CustomerModelListView(BaseModelListView):
    _model = Customer
    _serializer = CustomerSerializer
    _deserializer = CustomerDeserializer

    @api_func("List customers", url_tail="customers",
              response=[ExampleCustomers.CUSTOMER1.get(), ExampleCustomers.CUSTOMER2.get()])
    def get(self):
        return self._get()

    @api_func("Create customer", url_tail="customers",
              request=ExampleCustomers.CUSTOMER1.set(),
              response=ExampleCustomers.CUSTOMER1.get(),
              status_codes={422: "there is wrong type / missing field, or customer is already exist"})
    def post(self):
        return self._post()


class CustomerView(BaseView):
    _model = Customer
    _serializer = CustomerSerializer
    _deserializer = CustomerDeserializer

    @api_func("Get customer", url_tail="customers/1",
              response=ExampleCustomers.CUSTOMER1.get(),
              queries={"id": "ID of selected customer for change"},
              status_codes={404: "there is no customer"})
    def get(self, id: int):
        return self._get(id)

    @api_func("Update customer", url_tail="customers/1",
              request=ExampleCustomers.CUSTOMER1.set(change={"name": "new_foo"}),
              response=ExampleCustomers.CUSTOMER1.get(change={"name": "new_foo"}),
              queries={"id": "ID of selected customer for change"})
    def put(self, id: int):
        return self._put(id)

    @api_func("Delete customer", url_tail="customers/1",
              response=None,
              queries={"id": "ID of selected customer for change"},
              status_codes={404: "there is no customer"})
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(CustomerModelListView, '/%s/api/customers' % config.App.NAME, endpoint='customers')
api.add_resource(CustomerView, '/%s/api/customers/<int:id>' % config.App.NAME, endpoint='customer')
