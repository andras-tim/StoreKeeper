from flask.ext import restful
from flask.ext.restful import abort

from app.forms import StocktakingCreateForm, StocktakingUpdateForm
from app.models import Stocktaking
from app.modules.example_data import ExampleStocktakings
from app.serializers import StocktakingSerializer
from app.server import db, config, api
from app.views.common import api_func


class StocktakingListView(restful.Resource):
    @api_func("List stocktakings", url_tail="stocktakings",
              response=[ExampleStocktakings.STOCKTAKING1.get(), ExampleStocktakings.STOCKTAKING2.get()])
    def get(self):
        stocktakings = Stocktaking.query.all()
        return StocktakingSerializer(stocktakings, many=True).data

    @api_func("Create stocktaking", url_tail="stocktakings",
              request=ExampleStocktakings.STOCKTAKING1.set(),
              response=ExampleStocktakings.STOCKTAKING1.get(),
              status_codes={422: "there is wrong type / missing field"})
    def post(self):
        form = StocktakingCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        stocktaking = Stocktaking()
        form.populate_obj(stocktaking)

        db.session.add(stocktaking)
        db.session.commit()
        return StocktakingSerializer(stocktaking).data


class StocktakingView(restful.Resource):
    @api_func("Get stocktaking", url_tail="stocktakings/1",
              response=ExampleStocktakings.STOCKTAKING1.get(),
              queries={"id": "ID of selected stocktaking for change"},
              status_codes={404: "there is no stocktaking"})
    def get(self, id: int):
        stocktaking = Stocktaking.query.filter_by(id=id).first()
        if not stocktaking:
            abort(404)

        return StocktakingSerializer(stocktaking).data

    @api_func("Update stocktaking", url_tail="stocktakings/1",
              request=ExampleStocktakings.STOCKTAKING1.set(change={"comment": "A box has been damaged"}),
              response=ExampleStocktakings.STOCKTAKING1.get(change={"comment": "A box has been damaged"}),
              queries={"id": "ID of selected stocktaking for change"})
    def put(self, id: int):
        stocktaking = Stocktaking.query.filter_by(id=id).first()
        if not stocktaking:
            abort(404)

        form = StocktakingUpdateForm(obj=stocktaking)
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        form.populate_obj(stocktaking)

        db.session.add(stocktaking)
        db.session.commit()
        return StocktakingSerializer(stocktaking).data

    @api_func("Delete stocktaking", url_tail="stocktakings/1",
              response=None,
              queries={"id": "ID of selected stocktaking for change"},
              status_codes={404: "there is no stocktaking"})
    def delete(self, id: int):
        stocktaking = Stocktaking.query.filter_by(id=id).first()
        if not stocktaking:
            abort(404)

        db.session.delete(stocktaking)
        db.session.commit()
        return


api.add_resource(StocktakingListView, '/%s/api/stocktakings' % config.App.NAME, endpoint='stocktakings')
api.add_resource(StocktakingView, '/%s/api/stocktakings/<int:id>' % config.App.NAME, endpoint='stocktaking')
