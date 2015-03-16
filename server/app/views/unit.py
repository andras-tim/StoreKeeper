from flask.ext import restful
from flask.ext.restful import abort

from app.forms import UnitCreateForm, UnitUpdateForm
from app.models import Unit
from app.modules.example_data import ExampleUnits
from app.serializers import UnitSerializer
from app.server import db, config, api
from app.views.common import api_func


class UnitListView(restful.Resource):
    @api_func("List units", url_tail="units",
              response=[ExampleUnits.UNIT1.get(), ExampleUnits.UNIT2.get()])
    def get(self):
        units = Unit.query.all()
        return UnitSerializer(units, many=True).data

    @api_func("Create unit", url_tail="units",
              request=ExampleUnits.UNIT1.set(),
              response=ExampleUnits.UNIT1.get(),
              status_codes={422: "there is wrong type / missing field, or unit is already exist"})
    def post(self):
        form = UnitCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        unit = Unit(unit=form.unit.data)
        db.session.add(unit)
        db.session.commit()
        return UnitSerializer(unit).data


class UnitView(restful.Resource):
    @api_func("Get unit", url_tail="units/1",
              response=ExampleUnits.UNIT1.get(),
              queries={"id": "ID of selected unit for change"},
              status_codes={404: "there is no unit"})
    def get(self, id: int):
        unit = Unit.query.filter_by(id=id).first()
        if not unit:
            abort(404)

        return UnitSerializer(unit).data
    
    @api_func("Update unit", url_tail="units/1",
              request=ExampleUnits.UNIT1.set(change={"unit": "dl"}),
              response=ExampleUnits.UNIT1.get(change={"unit": "dl"}),
              queries={"id": "ID of selected unit for change"})
    def put(self, id: int):
        unit = Unit.query.filter_by(id=id).first()
        if not unit:
            abort(404)
    
        form = UnitUpdateForm(obj=unit)
        if not form.validate_on_submit():
            abort(422, message=form.errors)
    
        form.populate_obj(unit)
        db.session.add(unit)
        db.session.commit()
        return UnitSerializer(unit).data

    @api_func("Delete unit", url_tail="units/1",
              response=None,
              queries={"id": "ID of selected unit for change"},
              status_codes={404: "there is no unit"})
    def delete(self, id: int):
        unit = Unit.query.filter_by(id=id).first()
        if not unit:
            abort(404)

        db.session.delete(unit)
        db.session.commit()
        return


api.add_resource(UnitListView, '/%s/api/units' % config.App.NAME, endpoint='units')
api.add_resource(UnitView, '/%s/api/units/<int:id>' % config.App.NAME, endpoint='unit')
