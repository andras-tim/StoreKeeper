from app.modules.config import ConfigObject
from app.res.restfulApi import RestfulApiWithoutSimpleAuth

from app.views import common, acquisition, acquisition_item, barcode, config, customer, item, session, stocktaking, \
    stocktaking_item, unit, user, vendor, work, work_item


def initialize_endpoints(app_config: ConfigObject, api: RestfulApiWithoutSimpleAuth):
    views = {
        'acquisition_list': (acquisition.AcquisitionListView, '/acquisitions'),
        'acquisition': (acquisition.AcquisitionView, '/acquisitions/<int:id>'),

        'acquisition_item_list': (acquisition_item.AcquisitionItemListView, '/acquisition-items'),
        'acquisition_item': (acquisition_item.AcquisitionItemView, '/acquisition-items/<int:id>'),

        'barcode_list': (barcode.BarcodeListView, '/barcodes'),
        'barcode': (barcode.BarcodeView, '/barcodes/<int:id>'),
        'barcode_print': (barcode.BarcodePrintView, '/barcodes/<int:id>/print'),

        'config': (config.ConfigView, '/config'),

        'customer_list': (customer.CustomerListView, '/customers'),
        'customer': (customer.CustomerView, '/customers/<int:id>'),

        'item_list': (item.ItemListView, '/items'),
        'item': (item.ItemView, '/items/<int:id>'),

        'session': (session.SessionView, '/session'),

        'stocktaking_list': (stocktaking.StocktakingListView, '/stocktakings'),
        'stocktaking': (stocktaking.StocktakingView, '/stocktakings/<int:id>'),

        'stocktaking_item_list': (stocktaking_item.StocktakingItemListView, '/stocktaking-items'),
        'stocktaking_item': (stocktaking_item.StocktakingItemView, '/stocktaking-items/<int:id>'),

        'unit_list': (unit.UnitListView, '/units'),
        'unit': (unit.UnitView, '/units/<int:id>'),

        'user_list': (user.UserListView, '/users'),
        'user': (user.UserView, '/users/<int:id>'),

        'vendor_list': (vendor.VendorListView, '/vendors'),
        'vendor': (vendor.VendorView, '/vendors/<int:id>'),

        'work_list': (work.WorkListView, '/works'),
        'work': (work.WorkView, '/works/<int:id>'),
        'work_close_outbound': (work.WorkCloseOutboundView, '/works/<int:id>/close-outbound'),
        'work_close_returned': (work.WorkCloseReturnedView, '/works/<int:id>/close-returned'),

        'work_item_list': (work_item.WorkItemListView, '/work-items'),
        'work_item': (work_item.WorkItemView, '/work-items/<int:id>'),
    }

    for (endpoint, view_url) in views.items():
        view, url = view_url
        api.add_resource(view, '/{}/api{}'.format(app_config.App.NAME, url), endpoint=endpoint)
