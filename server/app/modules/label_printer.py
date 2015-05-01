import hashlib
import os
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39
from reportlab.lib.units import mm

from app import basedir, tempdir
from app.server import config
from app.modules.printer import Printer


class LabelPrinter:
    __logo_path = os.path.abspath(os.path.join(basedir, '..', 'client', 'app', 'img', 'label_logo.gif'))
    __print_cache_dir = os.path.join(tempdir, 'print_cache')
    __pdf_name_template = 'label__{data}__{title_hash}.pdf'

    def __init__(self, title: str, data: str):
        self.__title = title
        self.__data = data

        self.__pdf_path = self.__get_pdf_path()

    def print_to_pdf(self) -> str:
        self.__prepare_print_cache_dir()

        if not self.__is_cached():
            self.__generate_pdf()
        return self.__pdf_path

    def print(self, printer: (Printer, None)=None):
        printer = printer or Printer(config.App.LABEL_PRINTER)

        self.print_to_pdf()
        printer.print_pdf(self.__pdf_path)

    def __generate_pdf(self):
        pdf_generator = _LabelPdfGenerator()
        pdf_generator.generate_label(self.__title, self.__data, self.__logo_path, config.App.LABEL_BORDER,
                                     output_path=self.__pdf_path)

    def __prepare_print_cache_dir(self):
        os.makedirs(self.__print_cache_dir, exist_ok=True)

    def __get_pdf_path(self) -> str:
        pdf_name = self.__pdf_name_template.format(data=self.__data,
                                                   title_hash=hashlib.sha1(self.__title.encode()).hexdigest())
        return os.path.join(self.__print_cache_dir, pdf_name)

    def __is_cached(self) -> bool:
        return os.path.isfile(self.__pdf_path)


class _LabelPdfGenerator:
    page_width = 90 * mm
    page_height = 29 * mm

    margin_left = 3 * mm
    margin_top = 2 * mm
    margin_right = 4 * mm
    margin_bottom = 2 * mm

    inner_left = margin_left
    inner_top = page_height - margin_top
    inner_right = page_width - margin_right
    inner_bottom = margin_bottom
    inner_width = inner_right - margin_left
    inner_height = inner_top - margin_bottom

    title_font_name = 'Helvetica'
    title_font_size = 12

    data_font_name = 'Helvetica'
    data_font_size = 10

    def generate_label(self, title: str, data: str, logo_path: str, label_border: bool, output_path: str):
        canv = self._create_new_canvas(pdf_path=output_path)

        canv.setAuthor(config.App.TITLE)
        canv.setTitle(title)
        canv.setSubject(data)

        if label_border:
            self._draw_border(canv)
        self._draw_logo(canv, self.inner_left + 1 * mm, self.inner_top - 8.5 * mm, logo_path)
        self._draw_title(canv, self.inner_left + 30 * mm, self.inner_top - 7 * mm, title)
        self._draw_barcode(canv, self.inner_bottom + 5 * mm, data, bar_height=10 * mm)

        canv.showPage()
        canv.save()

    def _create_new_canvas(self, pdf_path: str) -> canvas:
        return canvas.Canvas(pdf_path, pagesize=(self.page_width, self.page_height))

    def _draw_border(self, canv: canvas):
        canv.roundRect(self.margin_left, self.margin_bottom, self.inner_width, self.inner_height, radius=5, stroke=1,
                       fill=0)

    def _draw_title(self, canv: canvas, x: int, y: int, title: str):
        canv.setFont(self.title_font_name, self.title_font_size)
        canv.drawString(x, y, title)

    def _draw_logo(self, canv: canvas, x: int, y: int, image_path: str):
        canv.drawImage(image_path, x, y, 28 * mm, 7 * mm)

    def _draw_barcode(self, canv: canvas, y: int, data: str, bar_height: int=20 * mm):
        # http://en.wikipedia.org/wiki/Code_39
        barcode = code39.Standard39(data, barWidth=0.55 * mm, barHeight=bar_height, stop=True, checksum=False)
        barcode.drawOn(canv, self.inner_left + (self.inner_width - barcode.width) / 2, y)

        canv.setFont(self.data_font_name, self.data_font_size)
        canv.drawCentredString(self.inner_left + self.inner_width / 2, y - 4 * mm, data)
