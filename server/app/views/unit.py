from app.models import Unit
from app.views.base_views import BaseListView, BaseView
from app.modules.example_data import ExampleUnits
from app.serializers import UnitSerializer, UnitDeserializer
from app.views.common import api_func


class UnitListView(BaseListView):
    _model = Unit
    _serializer = UnitSerializer()
    _deserializer = UnitDeserializer()

    @api_func('List units', url_tail='/units',
              response=[ExampleUnits.UNIT1.get(), ExampleUnits.UNIT2.get()])
    def get(self):
        return self._get()

    @api_func('Create unit', url_tail='/units',
              request=ExampleUnits.UNIT1.set(),
              response=ExampleUnits.UNIT1.get(),
              status_codes={422: '{{ original }} / unit is already exist'})
    def post(self):
        return self._post()


class UnitView(BaseView):
    _model = Unit
    _serializer = UnitSerializer()
    _deserializer = UnitDeserializer()

    @api_func('Get unit', item_name='unit', url_tail='/units/1',
              response=ExampleUnits.UNIT1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update unit', item_name='unit', url_tail='/units/1',
              request=ExampleUnits.UNIT1.set(change={'unit': 'dl'}),
              response=ExampleUnits.UNIT1.get(change={'unit': 'dl'}),
              status_codes={422: '{{ original }} / unit is already exist'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete unit', item_name='unit', url_tail='/units/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)
