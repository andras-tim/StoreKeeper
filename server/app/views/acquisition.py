from flask.ext import restful
from flask.ext.restful import abort

from app.forms import AcquisitionCreateForm, AcquisitionUpdateForm
from app.models import Acquisition
from app.modules.example_data import ExampleAcquisitions
from app.serializers import AcquisitionSerializer
from app.server import db, config, api
from app.views.common import api_func


class AcquisitionListView(restful.Resource):
    @api_func("List acquisitions", url_tail="acquisitions",
              response=[ExampleAcquisitions.ACQUISITION1.get(), ExampleAcquisitions.ACQUISITION2.get()])
    def get(self):
        acquisitions = Acquisition.query.all()
        return AcquisitionSerializer(acquisitions, many=True).data

    @api_func("Create acquisition", url_tail="acquisitions",
              request=ExampleAcquisitions.ACQUISITION1.set(),
              response=ExampleAcquisitions.ACQUISITION1.get(),
              status_codes={422: "there is wrong type / missing field"})
    def post(self):
        form = AcquisitionCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        acquisition = Acquisition()
        form.populate_obj(acquisition)

        db.session.add(acquisition)
        db.session.commit()
        return AcquisitionSerializer(acquisition).data


class AcquisitionView(restful.Resource):
    @api_func("Get acquisition", url_tail="acquisitions/1",
              response=ExampleAcquisitions.ACQUISITION1.get(),
              queries={"id": "ID of selected acquisition for change"},
              status_codes={404: "there is no acquisition"})
    def get(self, id: int):
        acquisition = Acquisition.query.filter_by(id=id).first()
        if not acquisition:
            abort(404)

        return AcquisitionSerializer(acquisition).data

    @api_func("Update acquisition", url_tail="acquisitions/1",
              request=ExampleAcquisitions.ACQUISITION1.set(change={"comment": "A box has been damaged"}),
              response=ExampleAcquisitions.ACQUISITION1.get(change={"comment": "A box has been damaged"}),
              queries={"id": "ID of selected acquisition for change"})
    def put(self, id: int):
        acquisition = Acquisition.query.filter_by(id=id).first()
        if not acquisition:
            abort(404)

        form = AcquisitionUpdateForm(obj=acquisition)
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        form.populate_obj(acquisition)

        db.session.add(acquisition)
        db.session.commit()
        return AcquisitionSerializer(acquisition).data

    @api_func("Delete acquisition", url_tail="acquisitions/1",
              response=None,
              queries={"id": "ID of selected acquisition for change"},
              status_codes={404: "there is no acquisition"})
    def delete(self, id: int):
        acquisition = Acquisition.query.filter_by(id=id).first()
        if not acquisition:
            abort(404)

        db.session.delete(acquisition)
        db.session.commit()
        return


api.add_resource(AcquisitionListView, '/%s/api/acquisitions' % config.App.NAME, endpoint='acquisitions')
api.add_resource(AcquisitionView, '/%s/api/acquisitions/<int:id>' % config.App.NAME, endpoint='acquisition')
