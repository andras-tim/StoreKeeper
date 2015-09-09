from flask import send_file
from flask.ext.restful import abort

from app.models import Item, Barcode
from app.views.base_views import BaseListView, BaseView, BaseNestedListView, BaseNestedView
from app.modules.example_data import ExampleItems, ExampleItemBarcodes
from app.modules.label_printer import LabelPrinter
from app.modules.printer import MissingCups
from app.serializers import ItemSerializer, ItemDeserializer, ItemBarcodeDeserializer, ItemBarcodeSerializer
from app.views.common import api_func


class ItemListView(BaseListView):
    _model = Item
    _serializer = ItemSerializer()
    _deserializer = ItemDeserializer()

    @api_func('List items', url_tail='/items',
              response=[ExampleItems.ITEM1.get(), ExampleItems.ITEM2.get()])
    def get(self):
        return self._get()

    @api_func('Create item', url_tail='/items',
              request=ExampleItems.ITEM1.set(),
              response=ExampleItems.ITEM1.get())
    def post(self):
        return self._post()


class ItemView(BaseView):
    _model = Item
    _serializer = ItemSerializer()
    _deserializer = ItemDeserializer()

    @api_func('Get item', item_name='item', url_tail='/items/1',
              response=ExampleItems.ITEM1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update item', item_name='item', url_tail='/items/1',
              request=ExampleItems.ITEM1.set(),
              response=ExampleItems.ITEM1.get())
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete item', item_name='item', url_tail='/items/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)


class ItemBarcodeListView(BaseNestedListView):
    _model = Barcode
    _parent_model = Item
    _serializer = ItemBarcodeSerializer()
    _deserializer = ItemBarcodeDeserializer()

    @api_func('List barcodes.', url_tail='/items/1/barcodes',
              response=[ExampleItemBarcodes.BARCODE1.get(), ExampleItemBarcodes.BARCODE2.get()],
              queries={'id': 'ID of item'})
    def get(self, id: int):
        self._initialize_parent_item(id)
        return self._get(item_id=id)

    @api_func('Create barcode', url_tail='/items/1/barcodes',
              request=ExampleItemBarcodes.BARCODE1.set(),
              response=ExampleItemBarcodes.BARCODE1.get(),
              status_codes={422: '{{ original }} / can not add one barcode twice'},
              queries={'id': 'ID of item'})
    def post(self, id: int):
        self._initialize_parent_item(id)
        barcode = self._post_populate(item_id=id)
        _check_only_one_main_barcode_per_item(barcode)
        return self._post_commit(barcode)


class ItemBarcodeView(BaseNestedView):
    _model = Barcode
    _parent_model = Item
    _serializer = ItemBarcodeSerializer()
    _deserializer = ItemBarcodeDeserializer()

    @api_func('Get barcode', item_name='barcode', url_tail='/items/1/barcodes/1',
              response=ExampleItemBarcodes.BARCODE1.get(),
              queries={'item_id': 'ID of item',
                       'id': 'ID of selected barcode for get'})
    def get(self, item_id: int, id: int):
        self._initialize_parent_item(item_id)
        return self._get(item_id=item_id, id=id)

    @api_func('Update barcode', item_name='barcode', url_tail='/items/1/barcodes/1',
              request=ExampleItemBarcodes.BARCODE1.set(),
              response=ExampleItemBarcodes.BARCODE1.get(),
              status_codes={422: '{{ original }} / can not add one barcode twice'},
              queries={'item_id': 'ID of item',
                       'id': 'ID of selected barcode for put'})
    def put(self, item_id: int, id: int):
        self._initialize_parent_item(item_id)
        barcode = self._put_populate(item_id=item_id, id=id)
        _check_only_one_main_barcode_per_item(barcode)
        return self._put_commit(barcode)

    @api_func('Delete barcode', item_name='barcode', url_tail='/items/1/barcodes/1',
              response=None,
              queries={'item_id': 'ID of item',
                       'id': 'ID of selected barcode for delete'})
    def delete(self, item_id: int, id: int):
        self._initialize_parent_item(item_id)
        return self._delete(item_id=item_id, id=id)


class ItemBarcodePrintView(BaseNestedView):
    _model = Barcode
    _parent_model = Item
    _serializer = ItemBarcodeSerializer()
    _deserializer = ItemBarcodeDeserializer()

    @api_func('Generate barcode label to PDF with some details, and starts downloading that.',
              item_name='barcode', url_tail='/items/1/barcodes/1/print',
              response_content_type='application/pdf',
              response_filename='label__SK642031__4f0ff51c73703295643a325e55bc7ed2d94aa03d.pdf',
              queries={'item_id': 'ID of item',
                       'id': 'ID of selected barcode for get'})
    def get(self, item_id: int, id: int):
        self._initialize_parent_item(item_id)
        barcode = self._get_item_by_filter(item_id=item_id, id=id)
        label_printer = _get_label_printer(barcode)

        file_path = label_printer.print_to_pdf()
        return send_file(file_path, as_attachment=True)

    @api_func('Print barcode label with some details', item_name='barcode', url_tail='/items/1/barcodes/1/print',
              response=None,
              status_codes={400: 'missing pycups python3 module'},
              queries={'item_id': 'ID of item',
                       'id': 'ID of selected barcode for get'})
    def put(self, item_id: int, id: int):
        self._initialize_parent_item(item_id)
        barcode = self._get_item_by_filter(item_id=item_id, id=id)

        try:
            label_printer = _get_label_printer(barcode)
        except MissingCups as e:
            return abort(400, message=str(e))
        label_printer.print()


def _check_only_one_main_barcode_per_item(barcode: Barcode):
    if not barcode.main:
        return
    if Barcode.query.filter(Barcode.id != barcode.id,
                            Barcode.item_id == barcode.item_id,
                            Barcode.main).count() > 0:
        abort(422, message={'main': ['Can not set more than one main barcode to an item.']})


def _get_label_printer(barcode: Barcode) -> LabelPrinter:
    title = barcode.item.name
    if barcode.quantity > 1:
        title = '{} ({!s}{})'.format(title, barcode.quantity, barcode.item.unit.unit)

    return LabelPrinter(title=title, data=barcode.barcode)
