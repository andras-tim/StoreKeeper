from app.modules.example_data import ExampleBarcodes as Barcodes, ExampleItems as Items, ExampleVendors as Vendors, \
    ExampleUnits as Units
from test.views.base_api_test import CommonApiTest


class TestBarcodeWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/barcodes'
    INIT_PUSH = [
        ('/vendors', [Vendors.VENDOR1, Vendors.VENDOR2]),
        ('/units', [Units.UNIT1, Units.UNIT2]),
        ('/items', [Items.ITEM1, Items.ITEM2]),
        ('/items/1/barcodes', [Barcodes.BARCODE1, Barcodes.BARCODE2]),
        ('/items/2/barcodes', [Barcodes.BARCODE3]),
    ]

    def test_list_barcodes(self):
        self.assertApiGet(expected_data=[Barcodes.BARCODE1,
                                         Barcodes.BARCODE3,
                                         Barcodes.BARCODE2])
