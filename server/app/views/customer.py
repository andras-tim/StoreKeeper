from flask.ext import restful
from flask.ext.restful import abort

from app.forms import CustomerCreateForm, CustomerUpdateForm
from app.models import Customer
from app.modules.example_data import ExampleCustomers
from app.serializers import CustomerSerializer
from app.server import db, config, api
from app.views.common import api_func


class CustomerListView(restful.Resource):
    @api_func("List customers", url_tail="customers",
              response=[ExampleCustomers.CUSTOMER1.get(), ExampleCustomers.CUSTOMER2.get()])
    def get(self):
        customers = Customer.query.all()
        return CustomerSerializer(customers, many=True).data

    @api_func("Create customer", url_tail="customers",
              request=ExampleCustomers.CUSTOMER1.set(),
              response=ExampleCustomers.CUSTOMER1.get(),
              status_codes={422: "there is wrong type / missing field, or customer is already exist"})
    def post(self):
        form = CustomerCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        customer = Customer()
        form.populate_obj(customer)

        db.session.add(customer)
        db.session.commit()
        return CustomerSerializer(customer).data


class CustomerView(restful.Resource):
    @api_func("Get customer", url_tail="customers/1",
              response=ExampleCustomers.CUSTOMER1.get(),
              queries={"id": "ID of selected customer for change"},
              status_codes={404: "there is no customer"})
    def get(self, id: int):
        customer = Customer.query.filter_by(id=id).first()
        if not customer:
            abort(404)

        return CustomerSerializer(customer).data

    @api_func("Update customer", url_tail="customers/1",
              request=ExampleCustomers.CUSTOMER1.set(change={"name": "new_foo"}),
              response=ExampleCustomers.CUSTOMER1.get(change={"name": "new_foo"}),
              queries={"id": "ID of selected customer for change"})
    def put(self, id: int):
        customer = Customer.query.filter_by(id=id).first()
        if not customer:
            abort(404)

        form = CustomerUpdateForm(obj=customer)
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        form.populate_obj(customer)

        db.session.add(customer)
        db.session.commit()
        return CustomerSerializer(customer).data

    @api_func("Delete customer", url_tail="customers/1",
              response=None,
              queries={"id": "ID of selected customer for change"},
              status_codes={404: "there is no customer"})
    def delete(self, id: int):
        customer = Customer.query.filter_by(id=id).first()
        if not customer:
            abort(404)

        db.session.delete(customer)
        db.session.commit()
        return


api.add_resource(CustomerListView, '/%s/api/customers' % config.App.NAME, endpoint='customers')
api.add_resource(CustomerView, '/%s/api/customers/<int:id>' % config.App.NAME, endpoint='customer')
