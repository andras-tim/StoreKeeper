from flask.ext import restful
from flask.ext.restful import abort

from app.forms import VendorCreateForm, VendorUpdateForm
from app.models import Vendor
from app.modules.example_data import ExampleVendors
from app.serializers import VendorSerializer
from app.server import db, config, api
from app.views.common import api_func


class VendorListView(restful.Resource):
    @api_func("List vendors", url_tail="vendors",
              response=[ExampleVendors.VENDOR1.get(), ExampleVendors.VENDOR2.get()])
    def get(self):
        vendors = Vendor.query.all()
        return VendorSerializer(vendors, many=True).data

    @api_func("Create vendor", url_tail="vendors",
              request=ExampleVendors.VENDOR1.set(),
              response=ExampleVendors.VENDOR1.get(),
              status_codes={422: "there is missing field, or vendor is already exist"})
    def post(self):
        form = VendorCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        vendor = Vendor(form.name.data)
        db.session.add(vendor)
        db.session.commit()
        return VendorSerializer(vendor).data


class VendorView(restful.Resource):
    @api_func("Get vendor", url_tail="vendors/1",
              response=ExampleVendors.VENDOR1.get(),
              queries={"id": "ID of selected vendor for change"},
              status_codes={404: "there is no vendor"})
    def get(self, id: int):
        vendor = Vendor.query.filter_by(id=id).first()
        if not vendor:
            abort(404)

        return VendorSerializer(vendor).data
    
    @api_func("Update vendor", url_tail="vendors/1",
              request=ExampleVendors.VENDOR1.set(change={"name": "new_foo"}),
              response=ExampleVendors.VENDOR1.get(change={"name": "new_foo"}),
              queries={"id": "ID of selected vendor for change"})
    def put(self, id: int):
        vendor = Vendor.query.filter_by(id=id).first()
        if not vendor:
            abort(404)
    
        form = VendorUpdateForm(obj=vendor)
        if not form.validate_on_submit():
            abort(422, message=form.errors)
    
        form.populate_obj(vendor)
        db.session.add(vendor)
        db.session.commit()
        return VendorSerializer(vendor).data

    @api_func("Delete vendor", url_tail="vendors/1",
              response=None,
              queries={"id": "ID of selected vendor for change"},
              status_codes={404: "there is no vendor"})
    def delete(self, id: int):
        vendor = Vendor.query.filter_by(id=id).first()
        if not vendor:
            abort(404)

        db.session.delete(vendor)
        db.session.commit()
        return


api.add_resource(VendorListView, '/%s/api/vendors' % config.App.NAME, endpoint='vendors')
api.add_resource(VendorView, '/%s/api/vendors/<int:id>' % config.App.NAME, endpoint='vendor')
