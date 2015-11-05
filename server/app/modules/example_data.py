import json
from copy import deepcopy
from datetime import datetime

from app.modules.common import filter_dict, recursive_dict_update
from app.modules.types import BarcodeType


class FilterableDict:
    def __init__(self, commons: (dict, None)=None, getters: (dict, None)=None, setters: (dict, None)=None):
        self.__commons = commons or {}
        self.__getters = getters or {}
        self.__setters = setters or {}

    def __getitem__(self, item: str):
        result = dict(self.__commons)
        result.update(self.__getters)
        result.update(self.__setters)
        return result[item]

    def get(self, fields_in_result: (list, set, None)=None, change: (dict, None)=None) -> dict:
        return self.__get_results(self.__getters, fields_in_result, change)

    def set(self, fields_in_result: (list, set, None)=None, change: (dict, None)=None) -> dict:
        return self.__get_results(self.__setters, fields_in_result, change)

    def get_changed(self, commons: (dict, None)=None, getters: (dict, None)=None,
                    setters: (dict, None)=None) -> 'FilterableDict':
        new_commons = dict(self.__commons)
        new_commons.update(commons or {})

        new_getters = dict(self.__getters)
        new_getters.update(getters or {})

        new_setters = dict(self.__setters)
        new_setters.update(setters or {})

        return FilterableDict(commons=new_commons, getters=new_getters, setters=new_setters)

    def __get_results(self, call_specific_data: dict, fields_in_result: (list, set, None),
                      changed_fields: (dict, None)) -> dict:
        result = dict(self.__commons)
        result.update(call_specific_data)

        if changed_fields:
            result = deepcopy(result)
            recursive_dict_update(result, changed_fields)

        if fields_in_result is not None:
            result = filter_dict(result, fields_in_result)

        return result


class ExampleUser(FilterableDict):
    def login(self, username: (str, None)=None, password: (str, None)=None, remember: bool=False):
        return {
            'username': username or self['username'],
            'password': password or self['password'],
            'remember': remember
        }


class ExampleTimestamp:
    REST_API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f+00:00'

    @classmethod
    def utcnow(cls) -> str:
        return datetime.utcnow().strftime(cls.REST_API_DATE_FORMAT)


class ExampleBarcode:
    BARCODE_PREFIX = 'SK-TEST-'
    BARCODE_NUMBERS = 7

    @classmethod
    def generate_main(cls) -> str:
        return BarcodeType.generate(cls.BARCODE_PREFIX, cls.BARCODE_NUMBERS)


class ExampleUsers:
    ADMIN = ExampleUser(commons={'username': 'admin', 'email': 'admin@test.com'},
                        setters={'password': 'secret'},
                        getters={'admin': True, 'id': 1, 'disabled': False})

    USER1 = ExampleUser(commons={'username': 'foo', 'email': 'foo@bar.com'},
                        setters={'password': 'bar'},
                        getters={'admin': False, 'id': 2, 'disabled': False})

    USER2 = ExampleUser(commons={'username': '1f-o_o.2', 'email': 'foo2@bar.com'},
                        setters={'password': 'bar2'},
                        getters={'admin': False, 'id': 3, 'disabled': False})

    USER3 = ExampleUser(commons={'username': 'user3', 'email': 'user3@bar.com'},
                        setters={'password': 'pw3'},
                        getters={'admin': False, 'id': 4, 'disabled': False})

    NONE_USER = ExampleUser(getters={'id': None, 'username': None, 'email': None, 'admin': None, 'disabled': None})


class ExampleVendors:
    VENDOR1 = FilterableDict(commons={'name': 'Heavy Duty Ltd.'},
                             getters={'id': 1})
    VENDOR2 = FilterableDict(commons={'name': 'Star Shop Ltd.'},
                             getters={'id': 2})


class ExampleUnits:
    UNIT1 = FilterableDict(commons={'unit': 'm'},
                           getters={'id': 1})
    UNIT2 = FilterableDict(commons={'unit': 'pcs'},
                           getters={'id': 2})


class ExampleCustomers:
    CUSTOMER1 = FilterableDict(commons={'name': 'Big Customer Ltd.'},
                               getters={'id': 1})
    CUSTOMER2 = FilterableDict(commons={'name': 'Buy Everything Co.'},
                               getters={'id': 2})


class ExampleAcquisitions:
    ACQUISITION1 = FilterableDict(commons={'comment': 'Maybe missing some items'},
                                  getters={'id': 1, 'timestamp': ExampleTimestamp.utcnow()})
    ACQUISITION2 = FilterableDict(getters={'id': 2, 'comment': None, 'timestamp': ExampleTimestamp.utcnow()})


class ExampleStocktakings:
    STOCKTAKING1 = FilterableDict(commons={'comment': 'Maybe missing some items'},
                                  getters={'id': 1, 'timestamp': ExampleTimestamp.utcnow(),
                                           'close_timestamp': None,
                                           'close_user': ExampleUsers.NONE_USER.get()})
    STOCKTAKING2 = FilterableDict(getters={'id': 2, 'comment': None, 'timestamp': ExampleTimestamp.utcnow(),
                                           'close_timestamp': None,
                                           'close_user': ExampleUsers.NONE_USER.get()})

    STOCKTAKING1_CLOSED = STOCKTAKING1.get_changed(
        getters={'close_timestamp': ExampleTimestamp.utcnow(),
                 'close_user': ExampleUsers.USER1.get()})


class ExampleItems:
    ITEM1 = FilterableDict(commons={'name': 'Spray', 'vendor': ExampleVendors.VENDOR1.get(),
                                    'warning_quantity': 4.0, 'unit': ExampleUnits.UNIT2.get()},
                           setters={'article_number': 'sk132465'},
                           getters={'id': 1, 'article_number': 'SK132465', 'quantity': 0.0})
    ITEM2 = FilterableDict(commons={'name': 'Pipe', 'vendor': ExampleVendors.VENDOR2.get(),
                                    'article_number': 'FO213546',
                                    'unit': ExampleUnits.UNIT1.get()},
                           getters={'id': 2, 'quantity': 0.0, 'warning_quantity': 0.0})
    ITEM3 = FilterableDict(commons={'name': 'Screw', 'vendor': ExampleVendors.VENDOR2.get(),
                                    'article_number': 'BA45678', 'warning_quantity': 3.14,
                                    'unit': ExampleUnits.UNIT2.get()},
                           getters={'id': 3, 'quantity': 0.0})


class ExampleItemSearchResults:
    RESULT1 = FilterableDict(getters={'type': 'barcode', 'item_id': 326, 'barcode': 'SK586936', 'quantity': 1})
    RESULT2 = FilterableDict(getters={'type': 'item', 'item_id': 309, 'name': 'Skate', 'article_number': 'SE180826',
                                      'vendor': 'Import'})


class ExampleAcquisitionItems:
    ITEM1 = FilterableDict(commons={'item': ExampleItems.ITEM2.get(), 'quantity': 132.4},
                           getters={'id': 1})
    ITEM2 = FilterableDict(commons={'item': ExampleItems.ITEM1.get(), 'quantity': 32.1},
                           getters={'id': 2})


class ExampleStocktakingItems:
    ITEM1 = FilterableDict(commons={'item': ExampleItems.ITEM2.get(), 'quantity': 52.1},
                           getters={'id': 1})
    ITEM2 = FilterableDict(commons={'item': ExampleItems.ITEM1.get(), 'quantity': 26.8},
                           getters={'id': 2})
    ITEM1_MINUS = FilterableDict(commons={'item': ExampleItems.ITEM2.get(), 'quantity': -52.1},
                                 getters={'id': 1})
    ITEM2_MINUS = FilterableDict(commons={'item': ExampleItems.ITEM1.get(), 'quantity': -26.8},
                                 getters={'id': 2})


class ExampleBarcodes:
    BARCODE1 = FilterableDict(getters={'id': 1, 'barcode': ExampleBarcode.generate_main(), 'quantity': 32.7,
                                       'item_id': 1, 'master': True, 'main': True})
    BARCODE2 = FilterableDict(getters={'id': 2, 'barcode': '9843-184125', 'quantity': 1.5,
                                       'item_id': 1, 'master': False, 'main': False})
    BARCODE3 = FilterableDict(getters={'id': 3, 'barcode': ExampleBarcode.generate_main(), 'quantity': 35.0,
                                       'item_id': 2, 'master': False, 'main': True})


class ExampleItemBarcodes:
    BARCODE1 = FilterableDict(commons={'barcode': ExampleBarcode.generate_main(), 'quantity': 32.7, 'master': True},
                              getters={'id': 1, 'main': True})
    BARCODE2 = FilterableDict(commons={'barcode': '9843-184125', 'quantity': 1.5, 'master': False},
                              getters={'id': 2, 'main': False})
    BARCODE3 = FilterableDict(commons={'quantity': 35.0, 'master': False},
                              getters={'id': 3, 'main': True, 'barcode': ExampleBarcode.generate_main()})


class ExampleItemBarcodePrints:
    PRINT1 = FilterableDict(setters={'copies': 3})


class ExampleWorks:
    WORK1 = FilterableDict(commons={'customer': ExampleCustomers.CUSTOMER1.get(), 'comment': 'First work'},
                           getters={'id': 1, 'outbound_close_timestamp': None,
                                    'outbound_close_user': ExampleUsers.NONE_USER.get(),
                                    'returned_close_timestamp': None,
                                    'returned_close_user': ExampleUsers.NONE_USER.get()})
    WORK2 = FilterableDict(commons={'customer': ExampleCustomers.CUSTOMER2.get()},
                           getters={'id': 2, 'comment': None, 'outbound_close_timestamp': None,
                                    'outbound_close_user': ExampleUsers.NONE_USER.get(),
                                    'returned_close_timestamp': None,
                                    'returned_close_user': ExampleUsers.NONE_USER.get()})

    WORK1_OUTBOUND_CLOSED = WORK1.get_changed(
        getters={'outbound_close_timestamp': ExampleTimestamp.utcnow(),
                 'outbound_close_user': ExampleUsers.USER1.get()})

    WORK1_RETURNED_CLOSED = WORK1_OUTBOUND_CLOSED.get_changed(
        getters={'returned_close_timestamp': ExampleTimestamp.utcnow(),
                 'returned_close_user': ExampleUsers.USER1.get()})


class ExampleWorkItems:
    ITEM1 = FilterableDict(commons={'item': ExampleItems.ITEM2.get(), 'outbound_quantity': 132.8},
                           getters={'id': 1, 'returned_quantity': None})
    ITEM2 = FilterableDict(commons={'item': ExampleItems.ITEM1.get(), 'outbound_quantity': 41.2,
                                    'returned_quantity': 2.1},
                           getters={'id': 2})


class ExampleConfigs:
    CONFIG1 = FilterableDict(getters={'app_name': 'storekeeper', 'app_title': 'StoreKeeper', 'forced_language': None,
                                      'debug': False})


class ExampleUserConfigs:
    CONFIG1 = FilterableDict(commons={'name': 'lang', 'value': 'hu'})
    CONFIG2 = FilterableDict(commons={'name': 'fruits', 'value': json.dumps(['apple', 'orange', 'banana'])})


class ExampleErrors:
    ERROR1 = FilterableDict(setters={'name': 'ReferenceError', 'message': 'foo is not defined',
                                     'stack': 'ReferenceError: foo is not defined\n'
                                              '    at Scope.printLabel (http://.../storekeeper.js:58678:21)\n'
                                              '    at ...'})
