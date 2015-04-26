from app.modules.example_data import (
    ExampleAcquisitions as Acquisitions,
    ExampleAcquisitionItems as AcquisitionItems,
    ExampleBarcodes as Barcodes,
    ExampleCustomers as Customers,
    ExampleItems as Items,
    ExampleUnits as Units,
    ExampleStocktakings as Stocktakings,
    ExampleStocktakingItems as StocktakingItems,
    ExampleUsers as Users,
    ExampleVendors as Vendors,
    ExampleWorks as Works,
    ExampleWorkItems as WorkItems,
)
from test.views.base_right_test import CommonRightsTest, use_as_rights_data_provider


def _get_all_rights_for_logged_in_users(existing_element_map_id: str, new_element_map_id: str):
    return {
        'anonymous': {
            'get': [False, (existing_element_map_id, False)],
            'post': [(new_element_map_id, False)],
            'put': [(existing_element_map_id, False)],
            'delete': [(existing_element_map_id, False)],
        },
        'admin': {
            'get': [True, (existing_element_map_id, True)],
            'post': [(new_element_map_id, True)],
            'put': [(existing_element_map_id, True)],
            'delete': [(existing_element_map_id, True)],
        },
        'user1': {
            'get': [True, (existing_element_map_id, True)],
            'post': [(new_element_map_id, True)],
            'put': [(existing_element_map_id, True)],
            'delete': [(existing_element_map_id, True)],
        },
    }


@use_as_rights_data_provider('/acquisitions')
class TestAcquisitionRights(CommonRightsTest):
    INIT_PUSH = [('/acquisitions', [Acquisitions.ACQUISITION1])]
    DATA_MAP = {'acquisition1': Acquisitions.ACQUISITION1, 'acquisition2': Acquisitions.ACQUISITION2}
    RIGHTS = _get_all_rights_for_logged_in_users('acquisition1', 'acquisition2')


@use_as_rights_data_provider('/acquisition-items')
class TestAcquisitionItemRights(CommonRightsTest):
    INIT_PUSH = [
        ('/acquisitions', [Acquisitions.ACQUISITION1, Acquisitions.ACQUISITION2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        ('/acquisition-items', [AcquisitionItems.ITEM1]),
    ]
    DATA_MAP = {'item1': AcquisitionItems.ITEM1, 'item2': AcquisitionItems.ITEM2}
    RIGHTS = _get_all_rights_for_logged_in_users('item1', 'item2')


@use_as_rights_data_provider('/barcodes')
class TestBarcodeRights(CommonRightsTest):
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1]),
        ('/barcodes', [Barcodes.BARCODE1]),
    ]
    DATA_MAP = {'barcode1': Barcodes.BARCODE1, 'barcode2': Barcodes.BARCODE2}
    RIGHTS = _get_all_rights_for_logged_in_users('barcode1', 'barcode2')


@use_as_rights_data_provider('/config')
class TestConfigRights(CommonRightsTest):
    RIGHTS = {
        'anonymous': {
            'get': True,
        },
        'admin': {
            'get': True,
        },
        'user1': {
            'get': True,
        },
    }


@use_as_rights_data_provider('/customers')
class TestCustomerRights(CommonRightsTest):
    INIT_PUSH = [('/customers', [Customers.CUSTOMER1])]
    DATA_MAP = {'customer1': Customers.CUSTOMER1, 'customer2': Customers.CUSTOMER2}
    RIGHTS = _get_all_rights_for_logged_in_users('customer1', 'customer2')


@use_as_rights_data_provider('/items')
class TestItemRights(CommonRightsTest):
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1]),
    ]
    DATA_MAP = {'item1': Items.ITEM1, 'item2': Items.ITEM2}
    RIGHTS = _get_all_rights_for_logged_in_users('item1', 'item2')


@use_as_rights_data_provider('/session')
class TestSessionRights(CommonRightsTest):
    INIT_PUSH = [('/users', [Users.USER2])]
    DATA_MAP = {'admin': Users.ADMIN, 'user1': Users.USER1, 'user2': Users.USER2}
    RIGHTS = {
        'anonymous': {
            'get': False,
            'post': [('admin', True), ('user1', True)],
            'delete': False,
        },
        'admin': {
            'get': True,
            'post': [('admin', True), ('user1', True)],
            'delete': True,
        },
        'user1': {
            'get': True,
            'post': [('admin', True), ('user1', True), ('user2', True)],
            'delete': True,
        },
    }


@use_as_rights_data_provider('/stocktakings')
class TestStocktakingRights(CommonRightsTest):
    INIT_PUSH = [('/stocktakings', [Stocktakings.STOCKTAKING1])]
    DATA_MAP = {'stocktaking1': Stocktakings.STOCKTAKING1, 'stocktaking2': Stocktakings.STOCKTAKING2}
    RIGHTS = _get_all_rights_for_logged_in_users('stocktaking1', 'stocktaking2')


@use_as_rights_data_provider('/stocktaking-items')
class TestStocktakingItemRights(CommonRightsTest):
    INIT_PUSH = [
        ('/stocktakings', [Stocktakings.STOCKTAKING1, Stocktakings.STOCKTAKING2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        ('/stocktaking-items', [StocktakingItems.ITEM1]),
    ]
    DATA_MAP = {'item1': StocktakingItems.ITEM1, 'item2': StocktakingItems.ITEM2}
    RIGHTS = _get_all_rights_for_logged_in_users('item1', 'item2')


@use_as_rights_data_provider('/units')
class TestUnitRights(CommonRightsTest):
    INIT_PUSH = [('/units', [Units.UNIT1])]
    DATA_MAP = {'unit1': Units.UNIT1, 'unit2': Units.UNIT2}
    RIGHTS = _get_all_rights_for_logged_in_users('unit1', 'unit2')


@use_as_rights_data_provider('/users')
class TestUserRights(CommonRightsTest):
    INIT_PUSH = [('/users', [Users.USER2])]
    DATA_MAP = {'admin': Users.ADMIN, 'user1': Users.USER1, 'user2': Users.USER2, 'user3': Users.USER3}
    RIGHTS = {
        'anonymous': {
            'get': [False, ('admin', False), ('user1', False)],
            'post': [('user3', False)],
            'put': [('admin', False), ('user1', False)],
            'delete': [('admin', False), ('user1', False)],
        },
        'admin': {
            'get': [True, ('admin', True), ('user1', True)],
            'post': [('user3', True)],
            'put': [('admin', True), ('user1', True)],
            'delete': [('admin', False), ('user1', True)]
        },
        'user1': {
            'get': [False, ('admin', True), ('user1', True), ('user2', True)],
            'post': [('user3', False)],
            'put': [('admin', False), ('user1', True), ('user2', False)],
            'delete': [('admin', False), ('user1', False), ('user2', False)],
        },
    }


@use_as_rights_data_provider('/vendors')
class TestVendorRights(CommonRightsTest):
    INIT_PUSH = [('/vendors', [Vendors.VENDOR1])]
    DATA_MAP = {'vendor1': Vendors.VENDOR1, 'vendor2': Vendors.VENDOR2}
    RIGHTS = _get_all_rights_for_logged_in_users('vendor1', 'vendor2')


@use_as_rights_data_provider('/works')
class TestWorkRights(CommonRightsTest):
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1]),
    ]
    DATA_MAP = {'work1': Works.WORK1, 'work2': Works.WORK2}
    RIGHTS = _get_all_rights_for_logged_in_users('work1', 'work2')


@use_as_rights_data_provider('/work-items')
class TestWorkItemRights(CommonRightsTest):
    INIT_PUSH = [
        ('/customers', [Customers.CUSTOMER1, Customers.CUSTOMER2]),
        ('/works', [Works.WORK1, Works.WORK2]),
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        ('/work-items', [WorkItems.ITEM1]),
    ]
    DATA_MAP = {'item1': WorkItems.ITEM1, 'item2': WorkItems.ITEM2}
    RIGHTS = _get_all_rights_for_logged_in_users('item1', 'item2')
