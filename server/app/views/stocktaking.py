from app.models import Stocktaking
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleStocktakings
from app.serializers import StocktakingSerializer, StocktakingDeserializer
from app.server import config, api
from app.views.common import api_func


class StocktakingModelListView(BaseModelListView):
    _model = Stocktaking
    _serializer = StocktakingSerializer
    _deserializer = StocktakingDeserializer

    @api_func('List stocktakings', url_tail='stocktakings',
              response=[ExampleStocktakings.STOCKTAKING1.get(), ExampleStocktakings.STOCKTAKING2.get()])
    def get(self):
        return self._get()

    @api_func('Create stocktaking', url_tail='stocktakings',
              request=ExampleStocktakings.STOCKTAKING1.set(),
              response=ExampleStocktakings.STOCKTAKING1.get(),
              status_codes={422: 'there is wrong type / missing field'})
    def post(self):
        return self._post()


class StocktakingView(BaseView):
    _model = Stocktaking
    _serializer = StocktakingSerializer
    _deserializer = StocktakingDeserializer

    @api_func('Get stocktaking', url_tail='stocktakings/1',
              response=ExampleStocktakings.STOCKTAKING1.get(),
              queries={'id': 'ID of selected stocktaking for change'},
              status_codes={404: 'there is no stocktaking'})
    def get(self, id: int):
        return self._get(id)

    @api_func('Update stocktaking', url_tail='stocktakings/1',
              request=ExampleStocktakings.STOCKTAKING1.set(change={'comment': 'A box has been damaged'}),
              response=ExampleStocktakings.STOCKTAKING1.get(change={'comment': 'A box has been damaged'}),
              queries={'id': 'ID of selected stocktaking for change'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete stocktaking', url_tail='stocktakings/1',
              response=None,
              queries={'id': 'ID of selected stocktaking for change'},
              status_codes={404: 'there is no stocktaking'})
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(StocktakingModelListView, '/%s/api/stocktakings' % config.App.NAME, endpoint='stocktakings')
api.add_resource(StocktakingView, '/%s/api/stocktakings/<int:id>' % config.App.NAME, endpoint='stocktaking')
