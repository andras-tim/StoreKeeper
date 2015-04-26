from app.modules.config import ConfigObject
from app.res.restfulApi import RestfulApiWithoutSimpleAuth

from app.views import common, acquisition, acquisition_item, barcode, config, customer, item, session, stocktaking, \
    stocktaking_item, unit, user, vendor, work, work_item


def initialize_endpoints(app_config: ConfigObject, api: RestfulApiWithoutSimpleAuth):
    views = {
        'acquisitions': (acquisition.AcquisitionListView, '/acquisitions'),
        'acquisition': (acquisition.AcquisitionView, '/acquisitions/<int:id>'),

        'acquisition_items': (acquisition_item.AcquisitionItemListView, '/acquisition-items'),
        'acquisition_item': (acquisition_item.AcquisitionItemView, '/acquisition-items/<int:id>'),

        'barcodes': (barcode.BarcodeListView, '/barcodes'),
        'barcode': (barcode.BarcodeView, '/barcodes/<int:id>'),

        'configs': (config.ConfigView, '/configs'),

        'customers': (customer.CustomerListView, '/customers'),
        'customer': (customer.CustomerView, '/customers/<int:id>'),

        'items': (item.ItemListView, '/items'),
        'item': (item.ItemView, '/items/<int:id>'),

        'sessions': (session.SessionView, '/sessions'),

        'stocktakings': (stocktaking.StocktakingListView, '/stocktakings'),
        'stocktaking': (stocktaking.StocktakingView, '/stocktakings/<int:id>'),

        'stocktaking_items': (stocktaking_item.StocktakingItemListView, '/stocktaking-items'),
        'stocktaking_item': (stocktaking_item.StocktakingItemView, '/stocktaking-items/<int:id>'),

        'units': (unit.UnitListView, '/units'),
        'unit': (unit.UnitView, '/units/<int:id>'),

        'users': (user.UserListView, '/users'),
        'user': (user.UserView, '/users/<int:id>'),

        'vendors': (vendor.VendorListView, '/vendors'),
        'vendor': (vendor.VendorView, '/vendors/<int:id>'),

        'works': (work.WorkListView, '/works'),
        'work': (work.WorkView, '/works/<int:id>'),
        'work_close_outbound': (work.WorkCloseOutboundView, '/works/<int:id>/close-outbound'),
        'work_close_returned': (work.WorkCloseReturnedView, '/works/<int:id>/close-returned'),

        'work_items': (work_item.WorkItemListView, '/work-items'),
        'work_item': (work_item.WorkItemView, '/work-items/<int:id>'),
    }

    for (endpoint, view_url) in views.items():
        view, url = view_url
        api.add_resource(view, '/{}/api{}'.format(app_config.App.NAME, url), endpoint=endpoint)
