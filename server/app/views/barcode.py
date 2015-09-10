from app.models import Barcode
from app.views.base_views import BaseListView
from app.modules.example_data import ExampleBarcodes
from app.serializers import BarcodeSerializer, BarcodeDeserializer
from app.views.common import api_func


class BarcodeListView(BaseListView):
    _model = Barcode
    _serializer = BarcodeSerializer()
    _deserializer = BarcodeDeserializer()

    @api_func('List barcodes items', url_tail='/barcodes',
              response=[ExampleBarcodes.BARCODE1.get(), ExampleBarcodes.BARCODE2.get()])
    def get(self):
        return self._get()
