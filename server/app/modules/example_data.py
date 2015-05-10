from datetime import datetime
import json


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

    def get(self, fields_in_result: (list, None)=None, change: (dict, None)=None) -> dict:
        return self.__get_results(self.__getters, fields_in_result, change)

    def set(self, fields_in_result: (list, None)=None, change: (dict, None)=None) -> dict:
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

    def __get_results(self, call_specific_data: dict, fields_in_result: (list, None),
                      changed_fields: (dict, None)) -> dict:
        result = dict(self.__commons)
        result.update(call_specific_data)

        if changed_fields:
            result.update(changed_fields)

        if fields_in_result is not None:
            result = dict((k, v) for k, v in result.items() if k in fields_in_result)

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
    ACQUISITION2 = FilterableDict(getters={'id': 2, 'comment': '', 'timestamp': ExampleTimestamp.utcnow()})


class ExampleStocktakings:
    STOCKTAKING1 = FilterableDict(commons={'comment': 'Maybe missing some items'},
                                  getters={'id': 1, 'timestamp': ExampleTimestamp.utcnow()})
    STOCKTAKING2 = FilterableDict(getters={'id': 2, 'comment': '', 'timestamp': ExampleTimestamp.utcnow()})


class ExampleItems:
    ITEM1 = FilterableDict(commons={'name': 'Spray', 'vendor': ExampleVendors.VENDOR1.get(), 'article_number': 132465,
                                    'quantity': 132, 'unit': ExampleUnits.UNIT2.get()},
                           getters={'id': 1})
    ITEM2 = FilterableDict(commons={'name': 'Pipe', 'vendor': ExampleVendors.VENDOR2.get(), 'article_number': 213546,
                                    'quantity': 32, 'unit': ExampleUnits.UNIT1.get()},
                           getters={'id': 2})
    ITEM3 = FilterableDict(commons={'name': 'Screw', 'vendor': ExampleVendors.VENDOR2.get(), 'article_number': 45678,
                                    'quantity': 12, 'unit': ExampleUnits.UNIT2.get()},
                           getters={'id': 3})


class ExampleAcquisitionItems:
    ITEM1 = FilterableDict(commons={'item': ExampleItems.ITEM2.get(), 'quantity': 132},
                           getters={'id': 1})
    ITEM2 = FilterableDict(commons={'item': ExampleItems.ITEM1.get(), 'quantity': 32},
                           getters={'id': 2})


class ExampleStocktakingItems:
    ITEM1 = FilterableDict(commons={'item': ExampleItems.ITEM2.get(), 'quantity': 132},
                           getters={'id': 1})
    ITEM2 = FilterableDict(commons={'item': ExampleItems.ITEM1.get(), 'quantity': 32},
                           getters={'id': 2})


class ExampleBarcodes:
    BARCODE1 = FilterableDict(commons={'barcode': '56456786416', 'quantity': 32, 'item': ExampleItems.ITEM1.get(),
                                       'main': True},
                              getters={'id': 1})
    BARCODE2 = FilterableDict(commons={'barcode': '9843184125', 'quantity': 1, 'item': ExampleItems.ITEM1.get(),
                                       'main': False},
                              getters={'id': 2})


class ExampleWorks:
    WORK1 = FilterableDict(commons={'customer': ExampleCustomers.CUSTOMER1.get(), 'comment': 'First work'},
                           getters={'id': 1, 'outbound_close_timestamp': None,
                                    'outbound_close_user': ExampleUsers.NONE_USER.get(),
                                    'returned_close_timestamp': None,
                                    'returned_close_user': ExampleUsers.NONE_USER.get()})
    WORK2 = FilterableDict(commons={'customer': ExampleCustomers.CUSTOMER2.get()},
                           getters={'id': 2, 'comment': '', 'outbound_close_timestamp': None,
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
    ITEM1 = FilterableDict(commons={'item': ExampleItems.ITEM2.get(), 'outbound_quantity': 132},
                           getters={'id': 1, 'returned_quantity': None})
    ITEM2 = FilterableDict(commons={'item': ExampleItems.ITEM1.get(), 'outbound_quantity': 32, 'returned_quantity': 0},
                           getters={'id': 2})


class ExampleConfigs:
    CONFIG1 = FilterableDict(getters={'app_name': 'storekeeper', 'app_title': 'StoreKeeper', 'forced_language': 'hu',
                                      'debug': False})


class ExampleUserConfigs:
    CONFIG1 = FilterableDict(commons={'name': 'lang', 'value': 'hu'})
    CONFIG2 = FilterableDict(commons={'name': 'fruits', 'value': json.dumps(['apple', 'orange', 'banana'])})
