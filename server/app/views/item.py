import re
from flask import send_file, request
from flask.ext.restful import abort
from sqlalchemy import or_, and_
from app.modules.view_helper_for_models import get_validated_request
from app.modules.view_helper_for_models import RequestProcessingError

from app.server import config, db
from app.models import Item, Barcode
from app.views.base_views import BaseListView, BaseView, BaseNestedListView, BaseNestedView
from app.modules.example_data import ExampleItems, ExampleItemBarcodes, ExampleItemBarcodePrints, \
    ExampleItemSearchResults
from app.modules.label_printer import LabelPrinter
from app.modules.printer import MissingCups
from app.modules.persistent_storage import PersistentStorage
from app.serializers import ItemSerializer, ItemDeserializer, ItemBarcodeDeserializer, ItemBarcodeSerializer, \
    ItemBarcodePrintDeserializer, ItemSearchSerializer
from app.views.common import api_func

__MAIN_BARCODE_FORMAT = re.compile(r'^' + re.escape(config.App.BARCODE_PREFIX) +
                                   '[0-9]{%d}' % config.App.BARCODE_NUMBERS + '$')


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


class ItemSearchListView(BaseListView):
    _serializer = ItemSearchSerializer()

    @api_func('Search in items and barcodes', url_tail='/items/search?expression=sk&limit=6',
              response=[ExampleItemSearchResults.RESULT1.get(), ExampleItemSearchResults.RESULT2.get()])
    def get(self):
        if 'expression' not in request.args.keys():
            return abort(422, message='Missing mandatory \'expression\' argument')
        data = {
            'expression': request.args['expression'],
            'limit': 6,
        }
        if 'limit' in request.args.keys():
            data['limit'] = int(request.args['limit'])

        results = []

        barcodes = Barcode.query.filter(
            Barcode.barcode.contains(data['expression'])
        ).limit(data['limit']).all()
        results.extend([_CreateObject(type='barcode', item_id=row.item_id, barcode=row.barcode, quantity=row.quantity,
                                      name=row.item.name, unit=row.item.unit.unit) for row in barcodes])

        if len(results) < data['limit']:
            items = db.session.query(Item, Barcode).join(Barcode).filter(
                and_(
                    or_(Item.name.contains(data['expression']), Item.article_number.contains(data['expression'])),
                    Barcode.master
                )
            ).limit(data['limit'] - len(results)).all()
            results.extend([_CreateObject(type='item', item_id=row.Item.id, name=row.Item.name,
                                          article_number=row.Item.article_number, vendor=row.Item.vendor.name,
                                          unit=row.Item.unit.unit,
                                          master_barcode=row.Barcode.barcode) for row in items])

        return self._serializer.dump(results, many=True).data


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

    @api_func('Create barcode (if missing ``barcode`` then server will generate one)', url_tail='/items/1/barcodes',
              request=ExampleItemBarcodes.BARCODE1.set(),
              response=ExampleItemBarcodes.BARCODE1.get(),
              status_codes={422: '{{ original }} / can not add one barcode twice / '
                                 'can not generate unique new barcode / '
                                 'can not set non-main barcode as master barcode / '
                                 'can not set more than one master barcode to an item'},
              queries={'id': 'ID of item'})
    def post(self, id: int):
        item = self._initialize_parent_item(id)
        barcode = self._post_populate(item_id=id)

        if barcode.main is None and barcode.barcode and _is_main_barcode(barcode.barcode):
            barcode.main = True
        if barcode.master is None and barcode.main and item.barcodes.count() == 0:
            barcode.master = True

        _can_be_master_barcode(barcode)

        if barcode.barcode is None:
            return self._post_retryable_commit(_get_barcode_generator(barcode_prefix=config.App.BARCODE_PREFIX,
                                                                      count_of_numbers=int(config.App.BARCODE_NUMBERS),
                                                                      base_barcode=barcode))
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
              status_codes={422: '{{ original }} / can not add one barcode twice / '
                                 'can not set non-main barcode as master barcode / '
                                 'can not set more than one master barcode to an item'},
              queries={'item_id': 'ID of item',
                       'id': 'ID of selected barcode for put'})
    def put(self, item_id: int, id: int):
        self._initialize_parent_item(item_id)
        barcode = self._put_populate(item_id=item_id, id=id)
        _can_be_master_barcode(barcode)
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
    _deserializer = ItemBarcodePrintDeserializer()

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
              request=ExampleItemBarcodePrints.PRINT1.set(),
              response=None,
              status_codes={400: 'missing pycups python3 module'},
              queries={'item_id': 'ID of item',
                       'id': 'ID of selected barcode for get'})
    def put(self, item_id: int, id: int):
        self._initialize_parent_item(item_id)
        try:
            data = get_validated_request(self._deserializer)
        except RequestProcessingError as e:
            return abort(422, message=e.message)

        barcode = self._get_item_by_filter(item_id=item_id, id=id)

        copies = 1
        if 'copies' in data.keys():
            copies = data['copies']

        try:
            label_printer = _get_label_printer(barcode)
        except MissingCups as e:
            return abort(400, message=str(e))
        label_printer.print(copies=copies)


_persistent_storage = PersistentStorage('item')


def _get_barcode_generator(barcode_prefix: str, count_of_numbers: int, base_barcode: Barcode) -> callable:
    def generator():
        barcode_number = _persistent_storage.get('last_barcode_number', 0) + 1
        barcode = '{prefix}{numbers}'.format(
            prefix=barcode_prefix,
            numbers=str(barcode_number).zfill(count_of_numbers)
        )
        _persistent_storage.set('last_barcode_number', barcode_number)

        return Barcode(barcode=barcode, quantity=base_barcode.quantity, item_id=base_barcode.item_id,
                       master=base_barcode.master, main=True)

    return generator


def _is_main_barcode(barcode: str) -> bool:
    return __MAIN_BARCODE_FORMAT.match(barcode)


def _can_be_master_barcode(barcode: Barcode):
    if not barcode.master:
        return
    if barcode.master and barcode.barcode and not barcode.main:
        abort(422, message={'master': ['Can not set non-main barcode as master barcode.']})
    if Barcode.query.filter(Barcode.id != barcode.id,
                            Barcode.item_id == barcode.item_id,
                            Barcode.master).count() > 0:
        abort(422, message={'master': ['Can not set more than one master barcode to an item.']})


def _get_label_printer(barcode: Barcode) -> LabelPrinter:
    title = barcode.item.name
    if barcode.quantity > 1:
        title = '{title} ({quantity!s}{unit})'.format(
            title=title,
            quantity=str(barcode.quantity).rstrip('0').rstrip('.'),
            unit=barcode.item.unit.unit
        )

    return LabelPrinter(title=title, data=barcode.barcode)


class _CreateObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)
