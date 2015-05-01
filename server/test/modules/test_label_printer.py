import os
import unittest

import app
app.test_mode = True
import app.server

from app.modules.label_printer import LabelPrinter
from test.mock.printer_mock import PrinterMock


class TestLabelPrinter(unittest.TestCase):
    title = 'Xxx'
    barcode = 'SK122334'
    __removable_files = []

    def setUp(self):
        self.printer = PrinterMock()

    def tearDown(self):
        for path in self.__removable_files:
            if os.path.isfile(path):
                os.remove(path)

    def test_can_create_label_printer(self):
        LabelPrinter(self.title, self.barcode)

    def test_can_print_to_pdf(self):
        lp = LabelPrinter(self.title, self.barcode)

        path = lp.print_to_pdf()
        self.__removable_files.append(path)

        assert os.path.isfile(path)

    def test_print_to_pdf_generated_pdf_only_once_with_same_metadata(self):
        lp1 = LabelPrinter(self.title, self.barcode)
        lp2 = LabelPrinter(self.title, self.barcode)

        path1 = lp1.print_to_pdf()
        self.__removable_files.append(path1)
        stat1 = os.stat(path1)

        path2 = lp2.print_to_pdf()
        self.__removable_files.append(path2)
        stat2 = os.stat(path2)

        assert path1 == path2
        assert stat1 is not stat2
        assert stat1 == stat2

    def test_can_print(self):
        printer = PrinterMock()
        lp = LabelPrinter(self.title, self.barcode)

        lp.print(printer)
        assert printer.last_printed_pdf is not None
