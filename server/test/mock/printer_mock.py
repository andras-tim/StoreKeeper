class PrinterMock:
    def __init__(self, name: str=''):
        self.last_printed_pdf = None
        self.last_options = None

    def print_pdf(self, pdf_path: str, printer_name: (str, None)=None, options: (dict, None)=None):
        self.last_printed_pdf = pdf_path
        self.last_options = options
