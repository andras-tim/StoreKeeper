from flask.ext.restful import abort

from app.models import Barcode
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleBarcodes
from app.modules.label_printer import LabelPrinter
from app.serializers import BarcodeSerializer
from app.views.common import api_func


class BarcodeListView(BaseModelListView):
    _model = Barcode
    _serializer = BarcodeSerializer
    _deserializer = BarcodeSerializer

    @api_func('List barcodes items', url_tail='/barcodes',
              response=[ExampleBarcodes.BARCODE1.get(), ExampleBarcodes.BARCODE2.get()])
    def get(self):
        return self._get()

    @api_func('Create barcodes item', url_tail='/barcodes',
              request=ExampleBarcodes.BARCODE1.set(),
              response=ExampleBarcodes.BARCODE1.get(),
              status_codes={422: '{{ original }} / try to set multiple main barcode to an item'})
    def post(self):
        barcode = self._post_populate()
        _check_only_one_main_barcode_per_item(barcode)
        return self._post_commit(barcode)


class BarcodeView(BaseView):
    _model = Barcode
    _serializer = BarcodeSerializer
    _deserializer = BarcodeSerializer

    @api_func('Get barcodes item', url_tail='/barcodes/1',
              response=ExampleBarcodes.BARCODE1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update barcodes item', url_tail='/barcodes/1',
              request=ExampleBarcodes.BARCODE1.set(),
              response=ExampleBarcodes.BARCODE1.get(),
              status_codes={422: '{{ original }} / try to set multiple main barcode to an item'})
    def put(self, id: int):
        barcode = self._put_populate(id)
        _check_only_one_main_barcode_per_item(barcode)
        return self._put_commit(barcode)

    @api_func('Delete barcodes item', url_tail='/barcodes/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)


class BarcodePrintView(BaseView):
    _model = Barcode
    _serializer = BarcodeSerializer
    _deserializer = BarcodeSerializer

    @api_func('Print barcode label with some details', url_tail='/barcodes/1/print',
              response=None)
    def put(self, id: int):
        barcode = self._get_item_by_id(id)

        title = barcode.item.name
        if barcode.quantity > 1:
            title = '{} ({:d} db)'.format(title, barcode.quantity)

        LabelPrinter(title=title, data=barcode.barcode).print()


def _check_only_one_main_barcode_per_item(barcode: Barcode):
    if not barcode.main:
        return
    if Barcode.query.filter(Barcode.id != barcode.id,
                            Barcode.item_id == barcode.item.id,
                            Barcode.main).count() > 0:
        abort(422, message={'main': ['Can not set more than one main barcode to an item.']})
