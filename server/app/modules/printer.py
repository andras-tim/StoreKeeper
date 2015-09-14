import os

from app.server import app, config


try:
    import cups
except ImportError:
    app.logger.warning('Missing \'pycups\' python3 module; printing was deactivated')


class MissingCups(Exception):
    pass


class Printer:
    DEFAULT_PRINTER = 'DEFAULT'

    printer_options = {
        # 'BrCutLabel': '1'
        # 'BrCutAtEnd': 'ON'
        # 'BrMirror': 'OFF'
        # 'BrPriority': 'BrSpeed'
        # 'Resolution': 'Normal'
        # 'BrHalftonePattern': 'BrErrorDiffusion'
        # 'BrBrightness': '0'
        # 'BrContrast': '0'
        # 'PageSize': '29x90'
        # 'PageRegion': '29x90'
        # 'BrMargin': '3'
    }

    def __init__(self, name: str=DEFAULT_PRINTER):
        if 'cups' not in globals().keys():
            raise MissingCups('Can not print while \'pycups\' python3 module is not installed.')

        if name == self.DEFAULT_PRINTER:
            self.conn = cups.Connection()
        else:
            self.conn = cups.Connection(name)

    def print_pdf(self, pdf_path: str, printer_name: (str, None)=None, options: (dict, None)=None):
        printer_name = printer_name or self.conn.getDefault()
        job_title = '{} - {}'.format(config.App.TITLE, os.path.basename(pdf_path))

        current_options = self.printer_options.copy()
        if options:
            current_options.update(options)

        self.conn.printFile(printer_name, pdf_path, job_title, current_options)
