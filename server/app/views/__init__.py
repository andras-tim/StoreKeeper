from app.modules.config import ConfigObject
from app.res.restfulApi import RestfulApiWithoutSimpleAuth

from app.views import common, acquisition, barcode, config, customer, item, session, stocktaking, unit, user, vendor, \
    work


def initialize_endpoints(app_config: ConfigObject, api: RestfulApiWithoutSimpleAuth):
    views = {
        'acquisition_list': (acquisition.AcquisitionListView, '/acquisitions'),
        'acquisition': (acquisition.AcquisitionView, '/acquisitions/<int:id>'),
        'acquisition_item_list': (acquisition.AcquisitionItemListView, '/acquisitions/<int:id>/items'),
        'acquisition_item': (acquisition.AcquisitionItemView, '/acquisitions/<int:id>/items/<int:item_id>'),

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
        'stocktaking_item_list': (stocktaking.StocktakingItemListView, '/stocktakings/<int:id>/items'),
        'stocktaking_item': (stocktaking.StocktakingItemView,
                             '/stocktakings/<int:id>/items/<int:item_id>'),

        'unit_list': (unit.UnitListView, '/units'),
        'unit': (unit.UnitView, '/units/<int:id>'),

        'user_list': (user.UserListView, '/users'),
        'user': (user.UserView, '/users/<int:id>'),
        'user_config_list': (user.UserConfigListView, '/users/<int:id>/config'),
        'user_config': (user.UserConfigView, '/users/<int:id>/config/<string:name>'),

        'vendor_list': (vendor.VendorListView, '/vendors'),
        'vendor': (vendor.VendorView, '/vendors/<int:id>'),

        'work_list': (work.WorkListView, '/works'),
        'work': (work.WorkView, '/works/<int:id>'),
        'work_item_list': (work.WorkItemListView, '/works/<int:id>/items'),
        'work_item': (work.WorkItemView, '/works/<int:id>/items/<int:item_id>'),
        'work_close_outbound': (work.WorkCloseOutboundView, '/works/<int:id>/close-outbound'),
        'work_close_returned': (work.WorkCloseReturnedView, '/works/<int:id>/close-returned'),

    }

    for (endpoint, view_url) in views.items():
        view, url = view_url
        api.add_resource(view, '/{}/api{}'.format(app_config.App.NAME, url), endpoint=endpoint)
