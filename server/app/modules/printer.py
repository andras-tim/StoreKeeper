import os

from app.server import app, config


try:
    import cups
except ImportError:
    app.logger.warning('Missing \'pycups\' python3 module; printing was deactivated')


class MissingCups(Exception):
    pass


class MissingPrinter(Exception):
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

        self.__cups_connection = cups.Connection()
        self.__printer_name = self.__evaluate_printer_name(name)

    def print_pdf(self, pdf_path: str, options: (dict, None)=None) -> 'Printer':
        job_title = '{} - {}'.format(config.App.TITLE, os.path.basename(pdf_path))

        current_options = self.printer_options.copy()
        if options:
            current_options.update(options)

        app.logger.info('Printing {pdf_name!r} on {printer!r}; {options!s}'.format(
            pdf_name=pdf_path,
            printer=self.__printer_name,
            options=current_options
        ))
        self.__cups_connection.printFile(self.__printer_name, pdf_path, job_title, current_options)

        return self

    def __evaluate_printer_name(self, printer_name: str) -> str:
        if printer_name == self.DEFAULT_PRINTER:
            printer_name = self.__cups_connection.getDefault()

        if printer_name is None:
            raise MissingPrinter('Cups has not default printer when the application config set to use the default.')

        printers = self.__cups_connection.getPrinters()
        if printer_name not in printers.keys():
            raise MissingPrinter('The selected printer is not found; printer_name={!r}'.format(printer_name))

        return printer_name
