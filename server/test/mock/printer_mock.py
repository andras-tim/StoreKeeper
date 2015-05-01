class PrinterMock:
    def __init__(self, name: str=''):
        self.last_printed_pdf = None

    def print_pdf(self, pdf_path: str, printer_name: (str, None)=None):
        self.last_printed_pdf = pdf_path
