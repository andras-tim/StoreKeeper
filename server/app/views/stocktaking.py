from app.models import Stocktaking
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleStocktakings
from app.serializers import StocktakingSerializer, StocktakingDeserializer
from app.server import config, api
from app.views.common import api_func


class StocktakingListView(BaseModelListView):
    _model = Stocktaking
    _serializer = StocktakingSerializer
    _deserializer = StocktakingDeserializer

    @api_func('List stocktakings', url_tail='stocktakings',
              response=[ExampleStocktakings.STOCKTAKING1.get(), ExampleStocktakings.STOCKTAKING2.get()])
    def get(self):
        return self._get()

    @api_func('Create stocktaking', url_tail='stocktakings',
              request=ExampleStocktakings.STOCKTAKING1.set(),
              response=ExampleStocktakings.STOCKTAKING1.get())
    def post(self):
        return self._post()


class StocktakingView(BaseView):
    _model = Stocktaking
    _serializer = StocktakingSerializer
    _deserializer = StocktakingDeserializer

    @api_func('Get stocktaking', item_name='stocktaking', url_tail='stocktakings/1',
              response=ExampleStocktakings.STOCKTAKING1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update stocktaking', item_name='stocktaking', url_tail='stocktakings/1',
              request=ExampleStocktakings.STOCKTAKING1.set(change={'comment': 'A box has been damaged'}),
              response=ExampleStocktakings.STOCKTAKING1.get(change={'comment': 'A box has been damaged'}))
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete stocktaking', item_name='stocktaking', url_tail='stocktakings/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(StocktakingListView, '/{!s}/api/stocktakings'.format(config.App.NAME), endpoint='stocktakings')
api.add_resource(StocktakingView, '/{!s}/api/stocktakings/<int:id>'.format(config.App.NAME), endpoint='stocktaking')
